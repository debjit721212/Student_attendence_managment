import base64
import os
from fastapi import FastAPI, HTTPException, status, Header, Depends, Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta, date
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import User, Parent, Student, Attendance, Camera, UnknownFace
from fastapi.responses import StreamingResponse
import csv
from io import StringIO
from app.utils.embedding import generate_embedding, insert_embedding_to_milvus

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security settings
SECRET_KEY = "your-very-secret-key"  # Change this to a strong, random value!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_role(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        if role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return role
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas for request/response
class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str

class AddUserRequest(BaseModel):
    username: str
    password: str
    role: str
    name: str = None
    department: str = None

class StudentRegisterRequest(BaseModel):
    name: str
    father_name: str
    mother_name: str
    roll_number: str
    dob: date
    gender: str
    class_grade: str
    photo: str = None  # base64 string
    address: str
    parent_mobile: str
    emergency_contact: str
    parent_id: int = None

class AttendanceMarkRequest(BaseModel):
    student_id: str  # Accept the global student_id string
    status: str
    timestamp: datetime = None

class StudentUpdateRequest(BaseModel):
    name: str = None
    father_name: str = None
    mother_name: str = None
    roll_number: str = None
    dob: date = None
    gender: str = None
    class_grade: str = None
    photo: str = None
    address: str = None
    parent_mobile: str = None
    emergency_contact: str = None

# Admin exists check
@app.get("/admin/exists")
def admin_exists(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == "admin").first() is not None

# Register first admin
@app.post("/auth/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.role == "admin").first() is None:
        user = User(
            username=req.username,
            password_hash=hash_password(req.password),
            role=req.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"msg": "First admin registered successfully"}
    raise HTTPException(status_code=403, detail="Registration is disabled. Please contact admin.")

# Add user (admin only)
@app.post("/admin/add-user")
def add_user(req: AddUserRequest, authorization: str = Header(...), db: Session = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Only admin can add users")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(
        username=req.username,
        password_hash=hash_password(req.password),
        role=req.role,
        name=req.name,
        department=req.department
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User added successfully"}

@app.get("/")
def read_root():
    return {"msg": "Backend is running!"}

# Login
@app.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.role != req.role:
        raise HTTPException(status_code=403, detail="Role mismatch")
    if user.role == "parent":
        raise HTTPException(status_code=403, detail="Parents must use OTP login")
    access_token = create_access_token(
        data={"sub": req.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }

# Student registration
@app.post("/students/register")
def register_student(req: StudentRegisterRequest, db: Session = Depends(get_db)):
    current_year = datetime.now().year
    student_id = f"SCHOOL{current_year}-{str(db.query(Student).count() + 1).zfill(4)}"

    # Save photo if provided
    photo_filename = None
    if req.photo:
        os.makedirs("photos", exist_ok=True)
        photo_filename = f"student_{student_id}.jpg"
        with open(f"photos/{photo_filename}", "wb") as f:
            f.write(base64.b64decode(req.photo.split(",")[1]))

    student = Student(
        student_id=student_id,
        name=req.name,
        father_name=req.father_name,
        mother_name=req.mother_name,
        roll_number=req.roll_number,
        dob=req.dob,
        gender=req.gender,
        class_grade=req.class_grade,
        photo=photo_filename,
        address=req.address,
        parent_mobile=req.parent_mobile,
        emergency_contact=req.emergency_contact,
        parent_id=req.parent_id
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    # Generate and store embedding in Milvus
    try:
        if photo_filename:
            photo_path = f"photos/{photo_filename}"
            embedding = generate_embedding(photo_path)
            insert_embedding_to_milvus(student_id, embedding)
    except Exception as e:
        print(f"[ERROR] Failed to generate/insert embedding for {student_id}: {e}")

    return {"msg": "Student registered successfully", "student_id": student_id}

# Student list with optional filtering
@app.get("/students/list")
def list_students(
    name: str = None,
    class_grade: str = None,
    roll_number: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student)
    if name:
        query = query.filter(Student.name.ilike(f"%{name}%"))
    if class_grade:
        query = query.filter(Student.class_grade == class_grade)
    if roll_number:
        query = query.filter(Student.roll_number == roll_number)
    students = query.all()
    return [
        {
            "student_id": s.student_id,
            "roll_number": s.roll_number,
            "class_grade": s.class_grade,
            "name": s.name,
            "gender": s.gender,
            "dob": s.dob,
            "father_name": s.father_name,
            "mother_name": s.mother_name,
            "address": s.address,
            "parent_mobile": s.parent_mobile,
            "emergency_contact": s.emergency_contact,
            "photo": s.photo,
            "parent_id": s.parent_id
        }
        for s in students
    ]

# Attendance marking
@app.post("/attendance/mark")
def mark_attendance(
    req: AttendanceMarkRequest,
    role: str = Depends(get_current_user_role),
    db: Session = Depends(get_db)
):
    if role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    # Look up the student by global student_id string
    student = db.query(Student).filter(Student.student_id == req.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    # Use today's date
    attendance_date = req.timestamp.date() if req.timestamp else datetime.now().date()
    # Check for duplicate
    existing = db.query(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.date == attendance_date,
        Attendance.status == req.status
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Attendance for {req.status} already marked today.")
    attendance = Attendance(
        student_id=student.id,
        status=req.status,
        date=attendance_date,
        timestamp=req.timestamp or datetime.now()
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    return {"msg": "Attendance marked", "record": {
        "student_id": student.student_id,
        "status": attendance.status,
        "timestamp": attendance.timestamp
    }}

# Attendance list with optional filtering
@app.get("/attendance/list")
def list_attendance(student_id: str = None, db: Session = Depends(get_db)):
    query = db.query(Attendance)
    if student_id:
        # Look up the student by global student_id string
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if student:
            query = query.filter(Attendance.student_id == student.id)
        else:
            return []
    records = query.all()
    # Map DB primary key back to global student_id for display
    student_map = {s.id: s.student_id for s in db.query(Student).all()}
    return [
        {
            "student_id": student_map.get(r.student_id, r.student_id),
            "status": r.status,
            "timestamp": r.timestamp
        }
        for r in records
    ]

# Parent management and my-child endpoint (example)
@app.get("/my-child")
def get_my_child(x_username: str = Header(...), db: Session = Depends(get_db)):
    parent = db.query(Parent).filter(Parent.phone == x_username).first()
    if not parent:
        return []
    return [
        {
            "student_id": s.student_id,
            "name": s.name,
            "father_name": s.father_name,
            "phone": s.phone,
            "address": s.address,
            "dob": s.dob,
            "photo": s.photo
        }
        for s in parent.students
    ]

@app.get("/students/export")
def export_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow([
        "Student ID", "Roll Number", "Class/Grade", "Name", "Gender", "DOB",
        "Father Name", "Mother Name", "Address", "Parent Mobile", "Emergency Contact"
    ])
    for s in students:
        cw.writerow([
            s.student_id, s.roll_number, s.class_grade, s.name, s.gender, s.dob,
            s.father_name, s.mother_name, s.address, s.parent_mobile, s.emergency_contact
        ])
    si.seek(0)
    return StreamingResponse(si, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=students.csv"})

@app.put("/students/{student_id}")
def update_student(
    student_id: str = Path(..., description="The unique student_id"),
    req: StudentUpdateRequest = None,
    db: Session = Depends(get_db),
    role: str = Depends(get_current_user_role)
):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update student info")
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for field, value in req.dict(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student)
    return {"msg": "Student updated successfully", "student": {
        "student_id": student.student_id,
        "name": student.name,
        "father_name": student.father_name,
        "mother_name": student.mother_name,
        "roll_number": student.roll_number,
        "dob": student.dob,
        "gender": student.gender,
        "class_grade": student.class_grade,
        "photo": student.photo,
        "address": student.address,
        "parent_mobile": student.parent_mobile,
        "emergency_contact": student.emergency_contact,
    }}
    
    
class CameraRegisterRequest(BaseModel):
    name: str
    location: str
    rtsp_url: str
    status: str = "active"
    gate: str = None

@app.get("/cameras/")
def get_cameras(db: Session = Depends(get_db)):
    return db.query(Camera).all()

@app.post("/cameras/")
def add_camera(req: CameraRegisterRequest, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add cameras")
    camera = Camera(**req.dict())
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera

@app.put("/cameras/{camera_id}")
def update_camera(camera_id: int, req: CameraRegisterRequest, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can update cameras")
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    for field, value in req.dict(exclude_unset=True).items():
        setattr(camera, field, value)
    db.commit()
    db.refresh(camera)
    return camera

@app.delete("/cameras/{camera_id}")
def delete_camera(camera_id: int, db: Session = Depends(get_db), role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete cameras")
    camera = db.query(Camera).filter(Camera.id == camera_id).first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    db.delete(camera)
    db.commit()
    return {"msg": "Camera deleted"}


# Attendance event confirmation endpoints
@app.get("/attendance/pending")
def get_pending_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.status == "pending").all()

@app.post("/attendance/confirm/{event_id}")
def confirm_attendance(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Attendance).filter(Attendance.id == event_id).first()
    if event:
        event.status = "confirmed"
        db.commit()
    return {"msg": "Attendance confirmed"}

@app.post("/attendance/reject/{event_id}")
def reject_attendance(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Attendance).filter(Attendance.id == event_id).first()
    if event:
        event.status = "rejected"
        db.commit()
    return {"msg": "Attendance rejected"}

# Unknown face review endpoints
class UnknownFaceEvent(BaseModel):
    camera_id: str
    timestamp: str
    face_crop: str  # base64 string

@app.post("/unknown-faces/")
def unknown_face_event(req: UnknownFaceEvent, db: Session = Depends(get_db)):
    os.makedirs("unknown_faces", exist_ok=True)
    filename = f"unknown_faces/{req.camera_id}_{req.timestamp.replace(':', '-')}.jpg"
    with open(filename, "wb") as f:
        f.write(base64.b64decode(req.face_crop))
    event = UnknownFace(
        camera_id=req.camera_id,
        timestamp=datetime.fromisoformat(req.timestamp),
        image_path=filename
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return {"msg": "Unknown face event received", "file": filename, "id": event.id}

@app.get("/unknown-faces/")
def list_unknown_faces(db: Session = Depends(get_db)):
    return db.query(UnknownFace).all()

@app.post("/unknown-faces/label/{event_id}")
def label_unknown_face(event_id: int, label: str, db: Session = Depends(get_db)):
    event = db.query(UnknownFace).filter(UnknownFace.id == event_id).first()
    if event:
        event.label = label
        db.commit()
    return {"msg": "Unknown face labeled"}

@app.delete("/unknown-faces/{event_id}")
def delete_unknown_face(event_id: int, db: Session = Depends(get_db)):
    event = db.query(UnknownFace).filter(UnknownFace.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
    return {"msg": "Unknown face deleted"}

@app.get("/attendance/confirmed")
def get_confirmed_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.status == "confirmed").all()

@app.get("/attendance/rejected")
def get_rejected_attendance(db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.status == "rejected").all()

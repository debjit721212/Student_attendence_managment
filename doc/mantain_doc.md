School Face Recognition Attendance System
A scalable, production-ready system for real-time student attendance using DeepStream, Milvus, FastAPI, and a modern React UI.

Table of Contents
Features
Architecture
Setup
Running the System
API Endpoints
Usage Guide
Troubleshooting
Contributing
License
Features
Student registration with photo, unique ID, and all metadata
Camera management (add/edit/delete, config sync)
DeepStream pipeline for multi-camera face detection and embedding extraction
Milvus vector search for fast face matching
Real-time attendance event sync and admin confirmation
Unknown face review and admin labeling
JWT authentication and role-based access
Modern, responsive UI (Material-UI)
Dockerized for easy deployment
Architecture
text

[React UI] <--> [FastAPI Backend] <--> [PostgreSQL, Milvus]
      ^                ^
      |                |
      v                v
[DeepStream Docker] <--> [Camera Streams]
UI: Student/camera/attendance management, admin review
Backend: API, embedding generation, Milvus integration
Milvus: Vector DB for face embeddings
DeepStream: Real-time face detection, embedding, and event sync
Setup
1. Clone the Repository
Bash

git clone <your-repo-url>
cd <your-repo-folder>
2. Backend Setup
Install Python dependencies:
Bash

pip install -r requirements.txt
Set up PostgreSQL and run Alembic migrations:
Bash

alembic upgrade head
Set up Milvus (see Milvus docs).
3. Frontend Setup
Install Node dependencies:
Bash

cd frontend
npm install
Set API URL in .env:
text

REACT_APP_API_URL=http://localhost:8000
4. DeepStream Setup
Build and run your DeepStream Docker container.
Make sure it can access the backend and Milvus.
Running the System
Start backend:
Bash

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
Start frontend:
Bash

npm start
Start Milvus:
Bash

docker compose up -d
Start DeepStream pipeline:
Bash

python3 pipeline.py
API Endpoints
Authentication
POST /auth/register — Register first admin
POST /auth/login — Login (admin/teacher)
User Management
POST /admin/add-user — Add user (admin only)
GET /admin/list — List admins (testing only)
POST /admin/reset-password — Reset admin password (testing only)
Student Management
POST /students/register — Register student
GET /students/list — List students (with filters)
PUT /students/{student_id} — Update student
GET /students/export — Export students to CSV
Attendance
POST /attendance/mark — Mark attendance (DeepStream event)
GET /attendance/list — List attendance records
GET /attendance/pending — List pending events
POST /attendance/confirm/{event_id} — Confirm event
POST /attendance/reject/{event_id} — Reject event
Unknown Face Review
POST /unknown-faces/ — Add unknown face event
GET /unknown-faces/ — List unknown faces
POST /unknown-faces/label/{event_id} — Label unknown face
DELETE /unknown-faces/{event_id} — Delete unknown face
Camera Management
GET /cameras/ — List cameras
POST /cameras/ — Add camera
PUT /cameras/{camera_id} — Update camera
DELETE /cameras/{camera_id} — Delete camera
Usage Guide
Register First Admin
Go to /register in the UI or use /auth/register in Swagger UI.
Add Cameras
Use the CameraConfig page in the UI to add/edit/delete cameras.
Register Students
Use the student registration page in the UI, upload a photo, and fill in all metadata.
Mark Attendance
DeepStream will automatically send attendance events when a face is matched.
Admin Review
Go to the Attendance Review page to confirm/reject events.
Go to the Unknown Face Review page to label or register unknown faces.
Troubleshooting
Cannot connect to backend:
Make sure backend is running on 0.0.0.0:8000 and accessible from other containers.
Milvus errors:
Make sure collection is created, indexed, and loaded.
Registration/login issues:
Check backend logs for error messages.
DeepStream not sending events:
Check network connectivity and JWT token.
Contributing
Fork the repo, create a branch, and submit a pull request.
Please write tests and update documentation for new features.
License
MIT License


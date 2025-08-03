from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    name = Column(String)
    department = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    students = relationship("Student", back_populates="parent")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date)
    status = Column(String, default="pending")  # "pending", "confirmed", "rejected"
    timestamp = Column(DateTime)
    student = relationship("Student", back_populates="attendance")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True)
    name = Column(String)
    father_name = Column(String)
    mother_name = Column(String)
    roll_number = Column(String)  # Not unique globally
    dob = Column(Date)
    gender = Column(String)
    class_grade = Column(String)
    photo = Column(String)
    address = Column(String)
    parent_mobile = Column(String)
    emergency_contact = Column(String)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    parent = relationship("Parent", back_populates="students")
    attendance = relationship("Attendance", back_populates="student")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    rtsp_url = Column(String, nullable=False)
    status = Column(String, default="active")  # active/inactive
    gate = Column(String)
    last_seen = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UnknownFace(Base):
    __tablename__ = "unknown_faces"
    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(String)
    timestamp = Column(DateTime)
    image_path = Column(String)
    label = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
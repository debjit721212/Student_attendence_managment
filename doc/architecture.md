student-attendance-management/
│
├── backend/                                 # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py              # Auth endpoints (login, register, etc.)
│   │   │   │   │   ├── students.py          # Student endpoints (CRUD, registration, etc.)
│   │   │   │   │   ├── attendance.py        # Attendance endpoints (mark, fetch, etc.)
│   │   │   │   │   ├── notifications.py     # Notification endpoints
│   │   │   │   │   └── __init__.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py                    # App settings, env variables
│   │   │   ├── security.py                  # Security utils (JWT, password hashing)
│   │   │   └── __init__.py
│   │   ├── db/
│   │   │   ├── base.py                      # SQLAlchemy base
│   │   │   ├── models.py                    # All DB models (User, Student, Attendance, etc.)
│   │   │   ├── session.py                   # DB session management
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── user.py                      # Pydantic schemas for User
│   │   │   ├── student.py                   # Pydantic schemas for Student
│   │   │   ├── attendance.py                # Pydantic schemas for Attendance
│   │   │   ├── notification.py              # Pydantic schemas for Notification
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── user_service.py              # User-related business logic
│   │   │   ├── student_service.py           # Student-related business logic
│   │   │   ├── attendance_service.py        # Attendance-related business logic
│   │   │   ├── notification_service.py      # Notification-related business logic
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── jwt.py                       # JWT helper functions
│   │   │   ├── hashing.py                   # Password hashing
│   │   │   └── __init__.py
│   │   ├── main.py                          # FastAPI entry point
│   │   └── __init__.py
│   ├── tests/                               # Backend tests
│   │   └── ...
│   ├── requirements.txt                     # Python dependencies
│   ├── Dockerfile                           # Backend Dockerfile
│   └── README.md
│
├── frontend/                                # React.js frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── assets/                          # Images, logos, styles, etc.
│   │   ├── components/                      # Reusable UI components (Button, Table, Modal, etc.)
│   │   ├── pages/                           # Page-level components (Dashboard, Login, Register, etc.)
│   │   ├── layouts/                         # Layout components (Sidebar, Navbar, etc.)
│   │   ├── routes/                          # Route definitions and guards
│   │   ├── services/                        # API calls (authService.js, studentService.js, etc.)
│   │   ├── hooks/                           # Custom React hooks (useAuth, useFetch, etc.)
│   │   ├── context/                         # React Contexts (AuthContext, ThemeContext, etc.)
│   │   ├── utils/                           # Utility functions (formatDate, validators, etc.)
│   │   ├── constants/                       # App-wide constants (roles, API endpoints, etc.)
│   │   ├── App.js                           # Main app component
│   │   ├── index.js                         # Entry point
│   │   └── theme.js                         # Theme and style overrides (if using MUI, etc.)
│   ├── .env                                 # Environment variables (API base URL, etc.)
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
│
├── face_registration/                       # OpenCV face registration scripts
│   ├── capture_faces.py                     # Main script for capturing faces
│   ├── face_utils.py                        # Helper functions (face detection, alignment, etc.)
│   ├── requirements.txt                     # Python dependencies (opencv-python, requests, etc.)
│   ├── config.py                            # Configurations (API endpoint, image save path, etc.)
│   ├── README.md
│   └── samples/                             # (Optional) Sample captured images
│
├── deepstream_pipeline/                     # DeepStream face recognition pipeline
│   ├── main.py                              # Entry point for DeepStream pipeline
│   ├── pipeline_config/
│   │   ├── config.txt                       # DeepStream pipeline config
│   │   ├── model/                           # Face detection/recognition models
│   │   └── ...
│   ├── face_matcher.py                      # Embedding extraction and matching logic
│   ├── api_client.py                        # Sends recognized faces to backend API
│   ├── requirements.txt                     # Python dependencies (deepstream, requests, etc.)
│   ├── README.md
│   └── logs/                                # (Optional) Pipeline logs
│
├── notifications/                           # Notification service integration
│   ├── sms_service.py                       # Twilio integration for SMS
│   ├── email_service.py                     # SendGrid integration for Email
│   ├── config.py                            # API keys, sender info, etc.
│   ├── templates/
│   │   ├── sms_template.txt                 # SMS message templates
│   │   └── email_template.html              # Email message templates
│   ├── utils.py                             # Helper functions (formatting, error handling)
│   ├── requirements.txt                     # Python dependencies (twilio, sendgrid, etc.)
│   └── README.md
│
├── docs/                                    # Documentation (HLD, LLD, API docs, etc.)
│   ├── architecture.md
│   ├── api_spec.md
│   └── ...
│
├── docker-compose.yml                       # For running all services together
├── README.md                                # Project overview and setup instructions
└── .gitignore
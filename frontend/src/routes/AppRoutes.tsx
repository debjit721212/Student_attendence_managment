import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MainLogin from '../pages/MainLogin';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
import ProtectedRoute from './ProtectedRoute';
import StudentRegister from '../pages/StudentRegister';
import Attendance from '../pages/Attendance';
import StudentList from '../pages/StudentList';
import MyChild from '../pages/MyChild';
import ParentLogin from '../pages/ParentLogin';
import ParentOTPVerify from '../pages/ParentOTPVerify';
import ParentDashboard from '../pages/ParentDashboard';
import AddUser from '../pages/AddUser';
import CameraConfig from '../pages/CameraConfig'; 
import AttendanceReview from '../pages/AttendanceReview';
import UnknownFaceReview from '../pages/UnknownFaceReview';



// ParentProtectedRoute component
const ParentProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const token = localStorage.getItem('parent_token');
    if (!token) return <Navigate to="/parent-login" replace />;
    return <>{children}</>;
};

const AppRoutes: React.FC = () => (
    <Router>
        <Routes>
            <Route path="/" element={<MainLogin />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
                path="/dashboard"
                element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/student-register"
                element={
                    <ProtectedRoute>
                        <StudentRegister />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/attendance"
                element={
                    <ProtectedRoute>
                        <Attendance />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/student-list"
                element={
                    <ProtectedRoute>
                        <StudentList />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/my-child"
                element={
                    <ProtectedRoute>
                        <MyChild />
                    </ProtectedRoute>
                }
            />
            <Route path="/parent-login" element={<ParentLogin />} />
            <Route path="/parent-verify-otp" element={<ParentOTPVerify />} />
            <Route
                path="/parent-dashboard"
                element={
                    <ParentProtectedRoute>
                        <ParentDashboard />
                    </ParentProtectedRoute>
                }
            />
            <Route
                path="/add-user"
                element={
                    <ProtectedRoute>
                        <AddUser />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/cameras"
                element={
                    <ProtectedRoute>
                        <CameraConfig />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/attendance-review"
                element={
                    <ProtectedRoute>
                        <AttendanceReview />
                    </ProtectedRoute>
                }
            />
            <Route
                path="/unknown-faces-review"
                element={
                    <ProtectedRoute>
                        <UnknownFaceReview />
                    </ProtectedRoute>
                }
            />
            <Route path="*" element={<MainLogin />} />
        </Routes>
    </Router>
);

export default AppRoutes;
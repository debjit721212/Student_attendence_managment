// src/services/attendanceService.ts
import axios from 'axios';
const API_URL = process.env.REACT_APP_API_URL;

export const getPendingAttendance = async () => {
    const token = localStorage.getItem('token');
    const res = await axios.get(`${API_URL}/attendance/pending`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
};

export const confirmAttendance = async (event_id: number) => {
    const token = localStorage.getItem('token');
    return axios.post(`${API_URL}/attendance/confirm/${event_id}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
    });
};

export const rejectAttendance = async (event_id: number) => {
    const token = localStorage.getItem('token');
    return axios.post(`${API_URL}/attendance/reject/${event_id}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
    });
};
// src/services/unknownFaceService.ts
import axios from 'axios';
const API_URL = process.env.REACT_APP_API_URL;

export const getUnknownFaces = async () => {
    const token = localStorage.getItem('token');
    const res = await axios.get(`${API_URL}/unknown-faces/`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
};

export const labelUnknownFace = async (event_id: number, label: string) => {
    const token = localStorage.getItem('token');
    return axios.post(`${API_URL}/unknown-faces/label/${event_id}`, { label }, {
        headers: { Authorization: `Bearer ${token}` }
    });
};

export const deleteUnknownFace = async (event_id: number) => {
    const token = localStorage.getItem('token');
    return axios.delete(`${API_URL}/unknown-faces/${event_id}`, {
        headers: { Authorization: `Bearer ${token}` }
    });
};
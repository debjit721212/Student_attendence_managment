import axios from 'axios';
const API_URL = process.env.REACT_APP_API_URL;

export const getCameras = async () => {
    const token = localStorage.getItem('token');
    const res = await axios.get(`${API_URL}/cameras/`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
};

export const addCamera = async (camera: any) => {
    const token = localStorage.getItem('token');
    const res = await axios.post(`${API_URL}/cameras/`, camera, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
};

export const updateCamera = async (id: number, camera: any) => {
    const token = localStorage.getItem('token');
    const res = await axios.put(`${API_URL}/cameras/${id}`, camera, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
};

export const deleteCamera = async (id: number) => {
    const token = localStorage.getItem('token');
    const res = await axios.delete(`${API_URL}/cameras/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    return res.data;
};

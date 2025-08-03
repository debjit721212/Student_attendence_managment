import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

// Debug helper
const logRequest = (endpoint: string, payload: any) => {
    console.log(`[API] POST ${endpoint}`, payload);
};
const logResponse = (endpoint: string, response: any) => {
    console.log(`[API] Response from ${endpoint}:`, response);
};
const logError = (endpoint: string, error: any) => {
    if (error.response) {
        console.error(`[API] Error from ${endpoint}:`, error.response.status, error.response.data);
    } else {
        console.error(`[API] Error from ${endpoint}:`, error.message);
    }
};

// Login for admin/teacher
export const login = async (
    username: string,
    password: string,
    role: string
): Promise<any> => {
    const endpoint = `${API_URL}/auth/login`;
    const payload = { username, password, role };
    logRequest(endpoint, payload);
    try {
        const response = await axios.post(endpoint, payload);
        logResponse(endpoint, response.data);
        localStorage.setItem('token', response.data.access_token);
        localStorage.setItem('username', username);
        localStorage.setItem('role', response.data.role); // Save role
        return response.data;
    } catch (error: any) {
        logError(endpoint, error);
        throw error;
    }
};

// Register (only for first admin)
export const register = async (
    username: string,
    password: string,
    role: string
): Promise<any> => {
    const endpoint = `${API_URL}/auth/register`;
    const payload = { username, password, role };
    logRequest(endpoint, payload);
    try {
        const response = await axios.post(endpoint, payload);
        logResponse(endpoint, response.data);
        return response.data;
    } catch (error: any) {
        logError(endpoint, error);
        throw error;
    }
};

// Add user (admin adds teacher or another admin)
export const addUser = async (
    username: string,
    password: string,
    role: string
): Promise<any> => {
    const token = localStorage.getItem('token');
    const endpoint = `${API_URL}/admin/add-user`;
    const payload = { username, password, role };
    logRequest(endpoint, payload);
    try {
        const response = await axios.post(
            endpoint,
            payload,
            { headers: { Authorization: `Bearer ${token}` } }
        );
        logResponse(endpoint, response.data);
        return response.data;
    } catch (error: any) {
        logError(endpoint, error);
        throw error;
    }
};

// Check if any admin exists (for registration page logic)
export const adminExists = async (): Promise<any> => {
    const endpoint = `${API_URL}/admin/exists`;
    console.log(`[API] GET ${endpoint}`);
    try {
        const response = await axios.get(endpoint);
        logResponse(endpoint, response.data);
        return response.data;
    } catch (error: any) {
        logError(endpoint, error);
        throw error;
    }
};
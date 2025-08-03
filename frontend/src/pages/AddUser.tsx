import React, { useState } from 'react';
import axios from 'axios';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    Snackbar,
    Stack,
    Select,
    MenuItem,
    InputLabel,
    FormControl
} from '@mui/material';
import MyAppBar from '../components/MyAppBar'; // <-- Import here

const API_URL = process.env.REACT_APP_API_URL;

const AddUser: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('teacher');
    const [name, setName] = useState('');
    const [department, setDepartment] = useState('');
    const [success, setSuccess] = useState('');
    const [error, setError] = useState('');
    const [open, setOpen] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSuccess('');
        setError('');
        try {
            const token = localStorage.getItem('token');
            await axios.post(
                `${API_URL}/admin/add-user`,
                { username, password, role, name, department: role === 'teacher' ? department : undefined },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setSuccess('User added successfully!');
            setOpen(true);
            setUsername('');
            setPassword('');
            setName('');
            setDepartment('');
            setRole('teacher');
        } catch (err) {
            setError('Failed to add user.');
            setOpen(true);
        }
    };

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            <MyAppBar /> {/* Add the AppBar here */}
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <Card sx={{ minWidth: 400, p: 3, boxShadow: 3 }}>
                    <CardContent>
                        <Typography variant="h5" align="center" gutterBottom color="primary">
                            Add User (Admin Only)
                        </Typography>
                        <form onSubmit={handleSubmit}>
                            <Stack spacing={2}>
                                <TextField
                                    label="Username"
                                    value={username}
                                    onChange={e => setUsername(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <TextField
                                    label="Password"
                                    type="password"
                                    value={password}
                                    onChange={e => setPassword(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <FormControl fullWidth>
                                    <InputLabel id="role-label">Select Role</InputLabel>
                                    <Select
                                        labelId="role-label"
                                        value={role}
                                        label="Select Role"
                                        onChange={e => setRole(e.target.value)}
                                    >
                                        <MenuItem value="teacher">Teacher</MenuItem>
                                        <MenuItem value="admin">Admin</MenuItem>
                                    </Select>
                                </FormControl>
                                <TextField
                                    label="Name"
                                    value={name}
                                    onChange={e => setName(e.target.value)}
                                    fullWidth
                                    required
                                />
                                {role === 'teacher' && (
                                    <TextField
                                        label="Department"
                                        value={department}
                                        onChange={e => setDepartment(e.target.value)}
                                        fullWidth
                                        required
                                    />
                                )}
                                <Button type="submit" variant="contained" color="primary" fullWidth>
                                    Add User
                                </Button>
                            </Stack>
                        </form>
                        <Snackbar
                            open={open}
                            autoHideDuration={4000}
                            onClose={() => setOpen(false)}
                            message={error || success}
                            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
                        />
                    </CardContent>
                </Card>
            </Box>
        </Box>
    );
};

export default AddUser;
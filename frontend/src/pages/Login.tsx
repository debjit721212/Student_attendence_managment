import React, { useState } from 'react';
import { login } from '../services/authService';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    Select,
    MenuItem,
    InputLabel,
    FormControl,
    Snackbar,
    Stack
} from '@mui/material';

const Login: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('teacher');
    const [error, setError] = useState('');
    const [open, setOpen] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        try {
            await login(username, password, role);
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid credentials');
            setOpen(true);
        }
    };

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f5f5f5">
            <Card sx={{ minWidth: 350, p: 3, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h5" align="center" gutterBottom color="primary">
                        Admin/Teacher Login
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
                            <Button type="submit" variant="contained" color="primary" fullWidth>
                                Login
                            </Button>
                        </Stack>
                    </form>
                    <Typography align="center" mt={3}>
                        Don't have an account?{' '}
                        <Button
                            component={RouterLink}
                            to="/register"
                            color="secondary"
                            size="small"
                            sx={{ textTransform: 'none', p: 0, minWidth: 0 }}
                        >
                            Register here
                        </Button>
                    </Typography>
                    <Snackbar
                        open={open}
                        autoHideDuration={4000}
                        onClose={() => setOpen(false)}
                        message={error}
                        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
                    />
                </CardContent>
            </Card>
        </Box>
    );
};

export default Login;
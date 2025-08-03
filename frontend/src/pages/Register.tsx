import React, { useState } from 'react';
import { register } from '../services/authService';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    Snackbar,
    Stack
} from '@mui/material';

const Register: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [open, setOpen] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        try {
            await register(username, password, 'admin');
            setSuccess('Registration successful! You can now log in.');
            setOpen(true);
            setUsername('');
            setPassword('');
            setTimeout(() => navigate('/login'), 2000); // Redirect after 2s
        } catch (err) {
            setError('Registration failed. Try a different username.');
            setOpen(true);
        }
    };

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f5f5f5">
            <Card sx={{ minWidth: 350, p: 3, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h5" align="center" gutterBottom color="primary">
                        Admin Registration
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
                            <Button type="submit" variant="contained" color="primary" fullWidth>
                                Register as Admin
                            </Button>
                        </Stack>
                    </form>
                    <Typography align="center" mt={3}>
                        Already have an account?{' '}
                        <Button
                            component={RouterLink}
                            to="/login"
                            color="secondary"
                            size="small"
                            sx={{ textTransform: 'none', p: 0, minWidth: 0 }}
                        >
                            Login here
                        </Button>
                    </Typography>
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
    );
};

export default Register;
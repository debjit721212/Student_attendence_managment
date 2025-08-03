import React, { useEffect } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
    Typography,
    Box,
    Card,
    CardContent,
    Button,
    Stack,
    Divider
} from '@mui/material';
import MyAppBar from '../components/MyAppBar';

const Dashboard = () => {
    const navigate = useNavigate();
    const role = localStorage.getItem('role');

    useEffect(() => {
        if (role === 'parent') {
            localStorage.clear();
            navigate('/login');
        }
    }, [role, navigate]);

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            <MyAppBar />
            <Box display="flex" justifyContent="center" alignItems="flex-start" minHeight="80vh" mt={4}>
                <Card sx={{ minWidth: 400, p: 3, boxShadow: 3 }}>
                    <CardContent>
                        <Typography variant="h5" align="center" gutterBottom color="primary">
                            Welcome to the Dashboard!
                        </Typography>
                        <Typography align="center" color="text.secondary" mb={3}>
                            This is a protected page. Only logged-in users can see this.
                        </Typography>
                        <Stack spacing={2}>
                            {(role === 'admin' || role === 'teacher') && (
                                <Button
                                    component={RouterLink}
                                    to="/attendance"
                                    variant="contained"
                                    color="primary"
                                    fullWidth
                                >
                                    Go to Attendance
                                </Button>
                            )}
                            {role === 'admin' && (
                                <>
                                    <Divider sx={{ my: 1 }} />
                                    <Typography variant="subtitle1" color="text.secondary" align="center">
                                        Admin Actions
                                    </Typography>
                                    <Button
                                        component={RouterLink}
                                        to="/student-register"
                                        variant="outlined"
                                        color="primary"
                                        fullWidth
                                    >
                                        Register a Student
                                    </Button>
                                    <Button
                                        component={RouterLink}
                                        to="/add-user"
                                        variant="outlined"
                                        color="secondary"
                                        fullWidth
                                    >
                                        Add User (Teacher/Admin)
                                    </Button>
                                    <Button
                                        component={RouterLink}
                                        to="/cameras"
                                        variant="contained"
                                        color="info"
                                        fullWidth
                                    >
                                        Camera Configuration
                                    </Button>
                                </>
                            )}
                            {(role === 'admin' || role === 'teacher') && (
                                <Button
                                    component={RouterLink}
                                    to="/student-list"
                                    variant="contained"
                                    color="secondary"
                                    fullWidth
                                >
                                    View Student List
                                </Button>
                            )}
                        </Stack>
                    </CardContent>
                </Card>
            </Box>
        </Box>
    );
};

export default Dashboard;
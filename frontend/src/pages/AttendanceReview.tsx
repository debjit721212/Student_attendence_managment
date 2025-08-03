// src/pages/AttendanceReview.tsx
import React, { useEffect, useState } from 'react';
import { getPendingAttendance, confirmAttendance, rejectAttendance } from '../services/attendanceService';
import {
    Box, Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer,
    TableHead, TableRow, Paper, Button, Stack, Snackbar, Alert
} from '@mui/material';
import MyAppBar from '../components/MyAppBar';

const AttendanceReview: React.FC = () => {
    const [events, setEvents] = useState<any[]>([]);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', color: 'success' });

    const fetchEvents = async () => {
        const data = await getPendingAttendance();
        setEvents(data);
    };

    useEffect(() => {
        fetchEvents();
    }, []);

    const handleConfirm = async (id: number) => {
        await confirmAttendance(id);
        setSnackbar({ open: true, message: 'Attendance confirmed!', color: 'success' });
        fetchEvents();
    };

    const handleReject = async (id: number) => {
        await rejectAttendance(id);
        setSnackbar({ open: true, message: 'Attendance rejected!', color: 'error' });
        fetchEvents();
    };

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            <MyAppBar />
            <Box display="flex" justifyContent="center" alignItems="flex-start" minHeight="100vh" pt={6}>
                <Card sx={{ minWidth: 900, p: 4, boxShadow: 4 }}>
                    <CardContent>
                        <Typography variant="h4" align="center" gutterBottom color="primary">
                            Pending Attendance Events
                        </Typography>
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Student ID</TableCell>
                                        <TableCell>Status</TableCell>
                                        <TableCell>Timestamp</TableCell>
                                        <TableCell>Actions</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {events.map((event: any) => (
                                        <TableRow key={event.id}>
                                            <TableCell>{event.student_id}</TableCell>
                                            <TableCell>{event.status}</TableCell>
                                            <TableCell>{event.timestamp}</TableCell>
                                            <TableCell>
                                                <Stack direction="row" spacing={1}>
                                                    <Button variant="contained" color="success" onClick={() => handleConfirm(event.id)}>
                                                        Confirm
                                                    </Button>
                                                    <Button variant="contained" color="error" onClick={() => handleReject(event.id)}>
                                                        Reject
                                                    </Button>
                                                </Stack>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                        <Snackbar
                            open={snackbar.open}
                            autoHideDuration={3000}
                            onClose={() => setSnackbar({ ...snackbar, open: false })}
                        >
                            <Alert onClose={() => setSnackbar({ ...snackbar, open: false })} severity={snackbar.color as any}>
                                {snackbar.message}
                            </Alert>
                        </Snackbar>
                    </CardContent>
                </Card>
            </Box>
        </Box>
    );
};

export default AttendanceReview;
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Button,
    Snackbar,
    Stack,
    Select,
    MenuItem,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
    FormControl,
    InputLabel,
    TextField
} from '@mui/material';
import MyAppBar from '../components/MyAppBar';

const API_URL = process.env.REACT_APP_API_URL;

const classOptions = [
    "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"
];

const Attendance: React.FC = () => {
    const [students, setStudents] = useState<any[]>([]);
    const [filteredStudents, setFilteredStudents] = useState<any[]>([]);
    const [selectedStudent, setSelectedStudent] = useState('');
    const [status, setStatus] = useState('entry');
    const [records, setRecords] = useState<any[]>([]);
    const [message, setMessage] = useState('');
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(true);

    // Search filters
    const [searchName, setSearchName] = useState('');
    const [searchClass, setSearchClass] = useState('');
    const [searchRoll, setSearchRoll] = useState('');

    // Fetch students for dropdown
    const fetchStudents = async () => {
        const token = localStorage.getItem('token');
        const res = await axios.get(`${API_URL}/students/list`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        setStudents(res.data);
        setFilteredStudents(res.data);
    };

    // Fetch attendance records
    const fetchRecords = async () => {
        const res = await axios.get(`${API_URL}/attendance/list`);
        setRecords(res.data);
        setLoading(false);
    };

    useEffect(() => {
        fetchStudents();
        fetchRecords();
    }, []);

    // Filter students when search fields change
    useEffect(() => {
        let filtered = students;
        if (searchName) {
            filtered = filtered.filter((s: any) =>
                s.name.toLowerCase().includes(searchName.toLowerCase())
            );
        }
        if (searchClass) {
            filtered = filtered.filter((s: any) => s.class_grade === searchClass);
        }
        if (searchRoll) {
            filtered = filtered.filter((s: any) => s.roll_number === searchRoll);
        }
        setFilteredStudents(filtered);
    }, [searchName, searchClass, searchRoll, students]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setMessage('');
        try {
            const token = localStorage.getItem('token');
            await axios.post(`${API_URL}/attendance/mark`, { student_id: selectedStudent, status }, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMessage('Attendance marked!');
            setOpen(true);
            setSelectedStudent('');
            setStatus('entry');
            fetchRecords();
        } catch (err: any) {
            setMessage(err?.response?.data?.detail || 'Failed to mark attendance.');
            setOpen(true);
        }
    };

    // Helper to get student name by id for display in records
    const getStudentName = (student_id: string) => {
        const student = students.find((s: any) => s.student_id === student_id);
        return student
            ? `${student.name} (Class: ${student.class_grade}, Roll: ${student.roll_number})`
            : student_id;
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            <MyAppBar />
            <Box display="flex" justifyContent="center" alignItems="flex-start" minHeight="100vh" pt={6}>
                <Card sx={{ minWidth: 900, p: 4, boxShadow: 4 }}>
                    <CardContent>
                        <Typography variant="h4" align="center" gutterBottom color="primary">
                            Mark Attendance
                        </Typography>
                        {/* Search filters for student selection */}
                        <Stack direction="row" spacing={2} mb={3}>
                            <TextField
                                label="Search by Name"
                                value={searchName}
                                onChange={e => setSearchName(e.target.value)}
                                size="small"
                            />
                            <FormControl size="small" sx={{ minWidth: 140 }}>
                                <InputLabel>Class/Grade</InputLabel>
                                <Select
                                    value={searchClass}
                                    label="Class/Grade"
                                    onChange={e => setSearchClass(e.target.value)}
                                >
                                    <MenuItem value="">All</MenuItem>
                                    {classOptions.map(opt => (
                                        <MenuItem key={opt} value={opt}>{`Class ${opt}`}</MenuItem>
                                    ))}
                                </Select>
                            </FormControl>
                            <TextField
                                label="Roll Number"
                                value={searchRoll}
                                onChange={e => setSearchRoll(e.target.value)}
                                size="small"
                            />
                        </Stack>
                        <form onSubmit={handleSubmit}>
                            <Stack direction="row" spacing={2} alignItems="center" mb={3}>
                                <FormControl fullWidth sx={{ minWidth: 350 }}>
                                    <InputLabel>Student</InputLabel>
                                    <Select
                                        value={selectedStudent}
                                        label="Student"
                                        onChange={e => setSelectedStudent(e.target.value)}
                                        required
                                        renderValue={selected => {
                                            const student = filteredStudents.find((s: any) => s.student_id === selected);
                                            return student
                                                ? `${student.name} — Class: ${student.class_grade} — Roll: ${student.roll_number}`
                                                : '';
                                        }}
                                    >
                                        {filteredStudents.map((student: any) => (
                                            <MenuItem key={student.student_id} value={student.student_id}>
                                                <Box>
                                                    <Typography variant="body1" component="span">{student.name}</Typography>
                                                    <Typography variant="body2" color="text.secondary" component="span" sx={{ ml: 1 }}>
                                                        | Class: {student.class_grade} | Roll: {student.roll_number}
                                                    </Typography>
                                                </Box>
                                            </MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                <FormControl sx={{ minWidth: 140 }}>
                                    <InputLabel>Status</InputLabel>
                                    <Select
                                        value={status}
                                        label="Status"
                                        onChange={e => setStatus(e.target.value)}
                                    >
                                        <MenuItem value="entry">Entry</MenuItem>
                                        <MenuItem value="exit">Exit</MenuItem>
                                    </Select>
                                </FormControl>
                                <Button type="submit" variant="contained" color="primary" size="large">
                                    Mark
                                </Button>
                            </Stack>
                        </form>
                        <Snackbar
                            open={open}
                            autoHideDuration={4000}
                            onClose={() => setOpen(false)}
                            message={message}
                            anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
                        />
                        <Typography variant="h6" mt={4} mb={2}>
                            Attendance Records
                        </Typography>
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Student Name</TableCell>
                                        <TableCell>Status</TableCell>
                                        <TableCell>Timestamp</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {records.map((rec: any, idx: number) => (
                                        <TableRow key={idx}>
                                            <TableCell>{getStudentName(rec.student_id)}</TableCell>
                                            <TableCell>{rec.status}</TableCell>
                                            <TableCell>{rec.timestamp}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </CardContent>
                </Card>
            </Box>
        </Box>
    );
};

export default Attendance;
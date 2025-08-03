import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
    TextField,
    Button,
    Stack,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    FormControl,
    InputLabel,
    Select,
    MenuItem
} from '@mui/material';
import MyAppBar from '../components/MyAppBar';

const API_URL = process.env.REACT_APP_API_URL;

const classOptions = [
    "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"
];
const genderOptions = [
    "Male", "Female", "Other"
];

const StudentList: React.FC = () => {
    const [students, setStudents] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [searchClass, setSearchClass] = useState('');
    const [searchRoll, setSearchRoll] = useState('');
    const [editOpen, setEditOpen] = useState(false);
    const [editStudent, setEditStudent] = useState<any>(null);
    const [editFields, setEditFields] = useState<any>({});

    const fetchStudents = async (name = '', classGrade = '', rollNumber = '') => {
        setLoading(true);
        const token = localStorage.getItem('token');
        const res = await axios.get(`${API_URL}/students/list`, {
            params: { name, class_grade: classGrade, roll_number: rollNumber },
            headers: { Authorization: `Bearer ${token}` }
        });
        setStudents(res.data);
        setLoading(false);
    };

    useEffect(() => {
        fetchStudents();
    }, []);

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        fetchStudents(search, searchClass, searchRoll);
    };

    const handleExport = async () => {
        const token = localStorage.getItem('token');
        const res = await axios.get(`${API_URL}/students/export`, {
            responseType: 'blob',
            headers: { Authorization: `Bearer ${token}` }
        });
        const url = window.URL.createObjectURL(new Blob([res.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'students.csv');
        document.body.appendChild(link);
        link.click();
        link.remove();
    };

    // Edit logic
    const handleEditOpen = (student: any) => {
        setEditStudent(student);
        setEditFields({ ...student });
        setEditOpen(true);
    };

    const handleEditChange = (field: string, value: any) => {
        setEditFields((prev: any) => ({ ...prev, [field]: value }));
    };

    const handleEditSave = async () => {
        const token = localStorage.getItem('token');
        await axios.put(
            `${API_URL}/students/${editStudent.student_id}`,
            editFields,
            { headers: { Authorization: `Bearer ${token}` } }
        );
        setEditOpen(false);
        fetchStudents(search, searchClass, searchRoll);
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
                <Card sx={{ minWidth: 1200, p: 3, boxShadow: 3 }}>
                    <CardContent>
                        <Typography variant="h5" align="center" gutterBottom color="primary">
                            Student List
                        </Typography>
                        <form onSubmit={handleSearch}>
                            <Stack direction="row" spacing={2} mb={2}>
                                <TextField
                                    label="Search by Name"
                                    value={search}
                                    onChange={e => setSearch(e.target.value)}
                                    size="small"
                                />
                                <FormControl size="small" sx={{ minWidth: 120 }}>
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
                                <Button type="submit" variant="contained" color="primary">
                                    Search
                                </Button>
                                <Button variant="outlined" color="secondary" onClick={handleExport}>
                                    Export CSV
                                </Button>
                            </Stack>
                        </form>
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Student ID</TableCell>
                                        <TableCell>Roll Number</TableCell>
                                        <TableCell>Class/Grade</TableCell>
                                        <TableCell>Full Name</TableCell>
                                        <TableCell>Gender</TableCell>
                                        <TableCell>Date of Birth</TableCell>
                                        <TableCell>Father Name</TableCell>
                                        <TableCell>Mother Name</TableCell>
                                        <TableCell>Address</TableCell>
                                        <TableCell>Parent Mobile</TableCell>
                                        <TableCell>Emergency Contact</TableCell>
                                        <TableCell>Edit</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {students.map((student: any, idx: number) => (
                                        <TableRow key={idx}>
                                            <TableCell>{student.student_id}</TableCell>
                                            <TableCell>{student.roll_number}</TableCell>
                                            <TableCell>{student.class_grade}</TableCell>
                                            <TableCell>{student.name}</TableCell>
                                            <TableCell>{student.gender}</TableCell>
                                            <TableCell>{student.dob}</TableCell>
                                            <TableCell>{student.father_name}</TableCell>
                                            <TableCell>{student.mother_name}</TableCell>
                                            <TableCell>{student.address}</TableCell>
                                            <TableCell>{student.parent_mobile}</TableCell>
                                            <TableCell>{student.emergency_contact}</TableCell>
                                            <TableCell>
                                                <Button
                                                    variant="outlined"
                                                    color="primary"
                                                    size="small"
                                                    onClick={() => handleEditOpen(student)}
                                                >
                                                    Edit
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                        {/* Edit Modal */}
                        <Dialog open={editOpen} onClose={() => setEditOpen(false)} maxWidth="sm" fullWidth>
                            <DialogTitle>Edit Student</DialogTitle>
                            <DialogContent>
                                <Stack spacing={2} mt={1}>
                                    <TextField
                                        label="Full Name"
                                        value={editFields.name || ''}
                                        onChange={e => handleEditChange('name', e.target.value)}
                                        fullWidth
                                    />
                                    <TextField
                                        label="Roll Number"
                                        value={editFields.roll_number || ''}
                                        onChange={e => handleEditChange('roll_number', e.target.value)}
                                        fullWidth
                                    />
                                    <TextField
                                        label="Date of Birth"
                                        type="date"
                                        value={editFields.dob ? String(editFields.dob).slice(0, 10) : ''}
                                        onChange={e => handleEditChange('dob', e.target.value)}
                                        fullWidth
                                        InputLabelProps={{ shrink: true }}
                                    />
                                    <FormControl fullWidth>
                                        <InputLabel>Gender</InputLabel>
                                        <Select
                                            value={editFields.gender || ''}
                                            label="Gender"
                                            onChange={e => handleEditChange('gender', e.target.value)}
                                        >
                                            {genderOptions.map(opt => (
                                                <MenuItem key={opt} value={opt}>{opt}</MenuItem>
                                            ))}
                                        </Select>
                                    </FormControl>
                                    <FormControl fullWidth>
                                        <InputLabel>Class/Grade</InputLabel>
                                        <Select
                                            value={editFields.class_grade || ''}
                                            label="Class/Grade"
                                            onChange={e => handleEditChange('class_grade', e.target.value)}
                                        >
                                            {classOptions.map(opt => (
                                                <MenuItem key={opt} value={opt}>{`Class ${opt}`}</MenuItem>
                                            ))}
                                        </Select>
                                    </FormControl>
                                    <TextField
                                        label="Address"
                                        value={editFields.address || ''}
                                        onChange={e => handleEditChange('address', e.target.value)}
                                        fullWidth
                                    />
                                    <TextField
                                        label="Parent Mobile Number"
                                        value={editFields.parent_mobile || ''}
                                        onChange={e => handleEditChange('parent_mobile', e.target.value)}
                                        fullWidth
                                    />
                                    <TextField
                                        label="Father's Name"
                                        value={editFields.father_name || ''}
                                        onChange={e => handleEditChange('father_name', e.target.value)}
                                        fullWidth
                                    />
                                    <TextField
                                        label="Mother's Name"
                                        value={editFields.mother_name || ''}
                                        onChange={e => handleEditChange('mother_name', e.target.value)}
                                        fullWidth
                                    />
                                    <TextField
                                        label="Emergency Contact Number"
                                        value={editFields.emergency_contact || ''}
                                        onChange={e => handleEditChange('emergency_contact', e.target.value)}
                                        fullWidth
                                    />
                                </Stack>
                            </DialogContent>
                            <DialogActions>
                                <Button onClick={() => setEditOpen(false)} color="secondary">
                                    Cancel
                                </Button>
                                <Button onClick={handleEditSave} variant="contained" color="primary">
                                    Save
                                </Button>
                            </DialogActions>
                        </Dialog>
                    </CardContent>
                </Card>
            </Box>
        </Box>
    );
};

export default StudentList;
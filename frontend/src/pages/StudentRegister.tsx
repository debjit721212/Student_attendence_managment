import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import { registerStudent } from '../services/studentService';
import {
    Box,
    Card,
    CardContent,
    Typography,
    TextField,
    Button,
    Snackbar,
    Stack,
    FormControl,
    InputLabel,
    Select,
    MenuItem
} from '@mui/material';
import MyAppBar from '../components/MyAppBar';

const classOptions = [
    "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"
];

const genderOptions = [
    "Male", "Female", "Other"
];

const StudentRegister: React.FC = () => {
    const navigate = useNavigate();
    const webcamRef = useRef<any>(null);

    // Form state
    const [name, setName] = useState('');
    const [rollNumber, setRollNumber] = useState('');
    const [dob, setDob] = useState('');
    const [gender, setGender] = useState('');
    const [classGrade, setClassGrade] = useState('');
    const [photo, setPhoto] = useState<string | null>(null);
    const [address, setAddress] = useState('');
    const [parentMobile, setParentMobile] = useState('');
    const [fatherName, setFatherName] = useState('');
    const [motherName, setMotherName] = useState('');
    const [emergencyContact, setEmergencyContact] = useState('');
    const [success, setSuccess] = useState('');
    const [error, setError] = useState('');
    const [open, setOpen] = useState(false);

    useEffect(() => {
        const role = localStorage.getItem('role');
        if (role !== 'admin') {
            navigate('/dashboard');
        }
    }, [navigate]);

    const capturePhoto = () => {
        if (webcamRef.current) {
            const imageSrc = webcamRef.current.getScreenshot();
            setPhoto(imageSrc);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSuccess('');
        setError('');
        try {
            await registerStudent(
                name,
                fatherName,
                motherName,
                rollNumber,
                dob,
                gender,
                classGrade,
                photo,
                address,
                parentMobile,
                emergencyContact
            );
            setSuccess('Student registered successfully!');
            setOpen(true);
            setName('');
            setFatherName('');
            setMotherName('');
            setRollNumber('');
            setDob('');
            setGender('');
            setClassGrade('');
            setPhoto(null);
            setAddress('');
            setParentMobile('');
            setEmergencyContact('');
        } catch (err) {
            setError('Failed to register student.');
            setOpen(true);
        }
    };

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            <MyAppBar />
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <Card sx={{ minWidth: 400, p: 3, boxShadow: 3 }}>
                    <CardContent>
                        <Typography variant="h5" align="center" gutterBottom color="primary">
                            Register Student
                        </Typography>
                        <form onSubmit={handleSubmit}>
                            <Stack spacing={2}>
                                <TextField
                                    label="Full Name"
                                    value={name}
                                    onChange={e => setName(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <TextField
                                    label="Roll Number"
                                    value={rollNumber}
                                    onChange={e => setRollNumber(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <TextField
                                    label="Date of Birth"
                                    type="date"
                                    value={dob}
                                    onChange={e => setDob(e.target.value)}
                                    fullWidth
                                    required
                                    InputLabelProps={{ shrink: true }}
                                />
                                <FormControl fullWidth required>
                                    <InputLabel>Gender</InputLabel>
                                    <Select
                                        value={gender}
                                        label="Gender"
                                        onChange={e => setGender(e.target.value)}
                                    >
                                        {genderOptions.map(opt => (
                                            <MenuItem key={opt} value={opt}>{opt}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                <FormControl fullWidth required>
                                    <InputLabel>Class/Grade</InputLabel>
                                    <Select
                                        value={classGrade}
                                        label="Class/Grade"
                                        onChange={e => setClassGrade(e.target.value)}
                                    >
                                        {classOptions.map(opt => (
                                            <MenuItem key={opt} value={opt}>{`Class ${opt}`}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                                <Box textAlign="center">
                                    <Webcam
                                        audio={false}
                                        ref={webcamRef}
                                        screenshotFormat="image/jpeg"
                                        width={320}
                                        height={240}
                                        style={{ borderRadius: 8, border: '1px solid #ccc' }}
                                    />
                                    <br />
                                    <Button
                                        type="button"
                                        variant="outlined"
                                        color="primary"
                                        onClick={capturePhoto}
                                        sx={{ mt: 1 }}
                                    >
                                        Capture Photo
                                    </Button>
                                    {photo && (
                                        <Box mt={2}>
                                            <img src={photo} alt="Captured" width={100} style={{ borderRadius: 8 }} />
                                        </Box>
                                    )}
                                </Box>
                                <TextField
                                    label="Address"
                                    value={address}
                                    onChange={e => setAddress(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <TextField
                                    label="Parent Mobile Number"
                                    value={parentMobile}
                                    onChange={e => setParentMobile(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <TextField
                                    label="Father's Name"
                                    value={fatherName}
                                    onChange={e => setFatherName(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <TextField
                                    label="Mother's Name"
                                    value={motherName}
                                    onChange={e => setMotherName(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <TextField
                                    label="Emergency Contact Number"
                                    value={emergencyContact}
                                    onChange={e => setEmergencyContact(e.target.value)}
                                    fullWidth
                                    required
                                />
                                <Button type="submit" variant="contained" color="primary" fullWidth>
                                    Register Student
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

export default StudentRegister;
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
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

const API_URL = process.env.REACT_APP_API_URL;

const ParentLogin: React.FC = () => {
    const [phone, setPhone] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [open, setOpen] = useState(false);
    const navigate = useNavigate();

    const handleRequestOTP = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await axios.post(`${API_URL}/parent/request-otp`, { phone_number: phone });
            navigate('/parent-verify-otp', { state: { phone } });
        } catch (err) {
            setError('Failed to send OTP. Please try again.');
            setOpen(true);
        }
        setLoading(false);
    };

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f5f5f5">
            <Card sx={{ minWidth: 350, p: 3, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h5" align="center" gutterBottom color="primary">
                        Parent Login
                    </Typography>
                    <form onSubmit={handleRequestOTP}>
                        <Stack spacing={2}>
                            <TextField
                                label="Phone Number"
                                value={phone}
                                onChange={e => setPhone(e.target.value)}
                                fullWidth
                                required
                            />
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                fullWidth
                                disabled={loading}
                            >
                                {loading ? 'Sending OTP...' : 'Request OTP'}
                            </Button>
                        </Stack>
                    </form>
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

export default ParentLogin;
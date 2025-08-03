import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
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

const ParentOTPVerify: React.FC = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const phone = (location.state as any)?.phone || '';
    const [otp, setOtp] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [open, setOpen] = useState(false);

    const handleVerifyOTP = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/parent/verify-otp`, { phone_number: phone, otp });
            localStorage.setItem('parent_token', res.data.access_token || phone);
            navigate('/parent-dashboard');
        } catch (err) {
            setError('Invalid OTP. Please try again.');
            setOpen(true);
        }
        setLoading(false);
    };

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f5f5f5">
            <Card sx={{ minWidth: 350, p: 3, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h5" align="center" gutterBottom color="primary">
                        Verify OTP
                    </Typography>
                    <form onSubmit={handleVerifyOTP}>
                        <Stack spacing={2}>
                            <TextField
                                label="Enter OTP"
                                value={otp}
                                onChange={e => setOtp(e.target.value)}
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
                                {loading ? 'Verifying...' : 'Verify OTP'}
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

export default ParentOTPVerify;
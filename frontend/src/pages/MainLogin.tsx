import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Card, CardContent, Typography, Button, Stack } from '@mui/material';

const MainLogin: React.FC = () => (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" bgcolor="#f5f5f5">
        <Card sx={{ minWidth: 350, p: 3, boxShadow: 3 }}>
            <CardContent>
                <Typography variant="h4" align="center" gutterBottom color="primary">
                    Welcome to School Portal
                </Typography>
                <Stack spacing={2} mt={3}>
                    <Button
                        component={RouterLink}
                        to="/login"
                        variant="contained"
                        color="primary"
                        size="large"
                        fullWidth
                    >
                        Login as Admin/Teacher
                    </Button>
                    <Button
                        component={RouterLink}
                        to="/parent-login"
                        variant="outlined"
                        color="primary"
                        size="large"
                        fullWidth
                    >
                        Login as Parent
                    </Button>
                </Stack>
                <Typography align="center" mt={4}>
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
            </CardContent>
        </Card>
    </Box>
);

export default MainLogin;
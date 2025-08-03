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
    Avatar,
    CircularProgress
} from '@mui/material';

const API_URL = process.env.REACT_APP_API_URL;

const ParentDashboard: React.FC = () => {
    const [children, setChildren] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchChildren = async () => {
            const token = localStorage.getItem('parent_token');
            const res = await axios.get(`${API_URL}/parent/children`, {
                headers: { 'x-parent-token': token }
            });
            setChildren(res.data);
            setLoading(false);
        };
        fetchChildren();
    }, []);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box display="flex" justifyContent="center" alignItems="flex-start" minHeight="100vh" bgcolor="#f5f5f5" pt={6}>
            <Card sx={{ minWidth: 600, p: 3, boxShadow: 3 }}>
                <CardContent>
                    <Typography variant="h5" align="center" gutterBottom color="primary">
                        My Children
                    </Typography>
                    {children.length === 0 ? (
                        <Typography align="center" color="text.secondary">
                            No children found for this parent.
                        </Typography>
                    ) : (
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Name</TableCell>
                                        <TableCell>Class</TableCell>
                                        <TableCell>Photo</TableCell>
                                        <TableCell>Attendance</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {children.map((child: any, idx: number) => (
                                        <TableRow key={idx}>
                                            <TableCell>{child.name}</TableCell>
                                            <TableCell>{child.class || '-'}</TableCell>
                                            <TableCell>
                                                {child.photo ? (
                                                    <Avatar src={child.photo} alt="child" sx={{ width: 50, height: 50 }} />
                                                ) : (
                                                    <Avatar sx={{ width: 50, height: 50 }}>N/A</Avatar>
                                                )}
                                            </TableCell>
                                            <TableCell>
                                                {child.attendance ? child.attendance.length : 0} records
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    )}
                </CardContent>
            </Card>
        </Box>
    );
};

export default ParentDashboard;
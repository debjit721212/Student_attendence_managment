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
    CircularProgress
} from '@mui/material';

const API_URL = process.env.REACT_APP_API_URL;

const MyChild: React.FC = () => {
    const [children, setChildren] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchChild = async () => {
            const username = localStorage.getItem('username');
            const res = await axios.get(`${API_URL}/my-child`, {
                headers: { 'x-username': username }
            });
            setChildren(res.data);
            setLoading(false);
        };
        fetchChild();
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
                        My Child's Info
                    </Typography>
                    {children.length === 0 ? (
                        <Typography align="center" color="text.secondary">
                            No child info available.
                        </Typography>
                    ) : (
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Name</TableCell>
                                        <TableCell>Parent ID</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {children.map((child: any, idx: number) => (
                                        <TableRow key={idx}>
                                            <TableCell>{child.name}</TableCell>
                                            <TableCell>{child.parent_id}</TableCell>
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

export default MyChild;
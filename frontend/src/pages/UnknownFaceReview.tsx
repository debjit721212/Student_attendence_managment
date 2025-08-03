// src/pages/UnknownFaceReview.tsx
import React, { useEffect, useState } from 'react';
import { getUnknownFaces, labelUnknownFace, deleteUnknownFace } from '../services/unknownFaceService';
import {
    Box, Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer,
    TableHead, TableRow, Paper, Button, Stack, TextField, Snackbar, Alert
} from '@mui/material';
import MyAppBar from '../components/MyAppBar';

const UnknownFaceReview: React.FC = () => {
    const [faces, setFaces] = useState<any[]>([]);
    const [labelInput, setLabelInput] = useState<{ [key: number]: string }>({});
    const [snackbar, setSnackbar] = useState({ open: false, message: '', color: 'success' });

    const fetchFaces = async () => {
        const data = await getUnknownFaces();
        setFaces(data);
    };

    useEffect(() => {
        fetchFaces();
    }, []);

    const handleLabel = async (id: number) => {
        await labelUnknownFace(id, labelInput[id] || "");
        setSnackbar({ open: true, message: 'Face labeled!', color: 'success' });
        fetchFaces();
    };

    const handleDelete = async (id: number) => {
        await deleteUnknownFace(id);
        setSnackbar({ open: true, message: 'Face deleted!', color: 'error' });
        fetchFaces();
    };

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            <MyAppBar />
            <Box display="flex" justifyContent="center" alignItems="flex-start" minHeight="100vh" pt={6}>
                <Card sx={{ minWidth: 900, p: 4, boxShadow: 4 }}>
                    <CardContent>
                        <Typography variant="h4" align="center" gutterBottom color="primary">
                            Unknown Face Review
                        </Typography>
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Image</TableCell>
                                        <TableCell>Camera</TableCell>
                                        <TableCell>Timestamp</TableCell>
                                        <TableCell>Label</TableCell>
                                        <TableCell>Actions</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {faces.map((face: any) => (
                                        <TableRow key={face.id}>
                                            <TableCell>
                                                <img src={`/${face.image_path}`} alt="Unknown Face" width={80} />
                                            </TableCell>
                                            <TableCell>{face.camera_id}</TableCell>
                                            <TableCell>{face.timestamp}</TableCell>
                                            <TableCell>
                                                <TextField
                                                    value={labelInput[face.id] || ""}
                                                    onChange={e => setLabelInput({ ...labelInput, [face.id]: e.target.value })}
                                                    size="small"
                                                />
                                            </TableCell>
                                            <TableCell>
                                                <Stack direction="row" spacing={1}>
                                                    <Button variant="contained" color="success" onClick={() => handleLabel(face.id)}>
                                                        Label
                                                    </Button>
                                                    <Button variant="contained" color="error" onClick={() => handleDelete(face.id)}>
                                                        Delete
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

export default UnknownFaceReview;
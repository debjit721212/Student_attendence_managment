import React, { useEffect, useState } from 'react';
import {
    Box, Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer,
    TableHead, TableRow, Paper, Button, Stack, Dialog, DialogTitle, DialogContent,
    DialogActions, TextField, Select, MenuItem, FormControl, InputLabel, Chip
} from '@mui/material';
import MyAppBar from '../components/MyAppBar';
import { getCameras, addCamera, updateCamera, deleteCamera } from '../services/cameraService';

const statusColors: Record<string, "success" | "error" | "primary" | "secondary" | "info" | "warning" | "default" | undefined> = {
    active: 'success',
    inactive: 'error',
    online: 'success',
    offline: 'error'
};

const CameraConfig: React.FC = () => {
    const [cameras, setCameras] = useState<any[]>([]);
    const [modalOpen, setModalOpen] = useState(false);
    const [editCamera, setEditCamera] = useState<any>(null);
    const [form, setForm] = useState<any>({
        name: '',
        location: '',
        rtsp_url: '',
        status: 'active',
        gate: ''
    });

    const fetchCameras = async () => {
        const data = await getCameras();
        setCameras(data);
    };

    useEffect(() => {
        fetchCameras();
    }, []);

    const handleOpenModal = (camera: any = null) => {
        setEditCamera(camera);
        setForm(camera || {
            name: '',
            location: '',
            rtsp_url: '',
            status: 'active',
            gate: ''
        });
        setModalOpen(true);
    };

    const handleCloseModal = () => {
        setModalOpen(false);
        setEditCamera(null);
    };

    const handleChange = (field: string, value: any) => {
        setForm((prev: any) => ({ ...prev, [field]: value }));
    };

    const handleSave = async () => {
        if (editCamera) {
            await updateCamera(editCamera.id, form);
        } else {
            await addCamera(form);
        }
        handleCloseModal();
        fetchCameras();
    };

    const handleDelete = async (id: number) => {
        await deleteCamera(id);
        fetchCameras();
    };

    return (
        <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh' }}>
            <MyAppBar />
            <Box display="flex" justifyContent="center" alignItems="flex-start" minHeight="100vh" pt={6}>
                <Card sx={{ minWidth: 900, p: 4, boxShadow: 4 }}>
                    <CardContent>
                        <Typography variant="h4" align="center" gutterBottom color="primary">
                            Camera Configuration
                        </Typography>
                        <Button variant="contained" color="primary" onClick={() => handleOpenModal()} sx={{ mb: 2 }}>
                            Add Camera
                        </Button>
                        <TableContainer component={Paper}>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Name</TableCell>
                                        <TableCell>Location</TableCell>
                                        <TableCell>RTSP URL</TableCell>
                                        <TableCell>Status</TableCell>
                                        <TableCell>Gate/Area</TableCell>
                                        <TableCell>Last Seen</TableCell>
                                        <TableCell>Actions</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {cameras.map((camera: any) => (
                                        <TableRow key={camera.id}>
                                            <TableCell>{camera.name}</TableCell>
                                            <TableCell>{camera.location}</TableCell>
                                            <TableCell>{camera.rtsp_url}</TableCell>
                                            <TableCell>
                                                <Chip
                                                    label={camera.status}
                                                    color={statusColors[camera.status] as
                                                        "success" | "error" | "primary" | "secondary" | "info" | "warning" | "default" | undefined
                                                        || 'default'}
                                                    size="small"
                                                />
                                            </TableCell>
                                            <TableCell>{camera.gate || '-'}</TableCell>
                                            <TableCell>
                                                {camera.last_seen
                                                    ? new Date(camera.last_seen).toLocaleString()
                                                    : 'Never'}
                                            </TableCell>
                                            <TableCell>
                                                <Button
                                                    variant="outlined"
                                                    color="primary"
                                                    size="small"
                                                    onClick={() => handleOpenModal(camera)}
                                                    sx={{ mr: 1 }}
                                                >
                                                    Edit
                                                </Button>
                                                <Button
                                                    variant="outlined"
                                                    color="secondary"
                                                    size="small"
                                                    onClick={() => handleDelete(camera.id)}
                                                >
                                                    Delete
                                                </Button>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                        {/* Add/Edit Camera Modal */}
                        <Dialog open={modalOpen} onClose={handleCloseModal} maxWidth="sm" fullWidth>
                            <DialogTitle>{editCamera ? 'Edit Camera' : 'Add Camera'}</DialogTitle>
                            <DialogContent>
                                <Stack spacing={2} mt={1}>
                                    <TextField
                                        label="Camera Name"
                                        value={form.name}
                                        onChange={e => handleChange('name', e.target.value)}
                                        fullWidth
                                        required
                                    />
                                    <TextField
                                        label="Location"
                                        value={form.location}
                                        onChange={e => handleChange('location', e.target.value)}
                                        fullWidth
                                    />
                                    <TextField
                                        label="RTSP URL"
                                        value={form.rtsp_url}
                                        onChange={e => handleChange('rtsp_url', e.target.value)}
                                        fullWidth
                                        required
                                    />
                                    <FormControl fullWidth>
                                        <InputLabel>Status</InputLabel>
                                        <Select
                                            value={form.status}
                                            label="Status"
                                            onChange={e => handleChange('status', e.target.value)}
                                        >
                                            <MenuItem value="active">Active</MenuItem>
                                            <MenuItem value="inactive">Inactive</MenuItem>
                                        </Select>
                                    </FormControl>
                                    <TextField
                                        label="Gate/Area"
                                        value={form.gate}
                                        onChange={e => handleChange('gate', e.target.value)}
                                        fullWidth
                                    />
                                </Stack>
                            </DialogContent>
                            <DialogActions>
                                <Button onClick={handleCloseModal} color="secondary">
                                    Cancel
                                </Button>
                                <Button onClick={handleSave} variant="contained" color="primary">
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

export default CameraConfig;
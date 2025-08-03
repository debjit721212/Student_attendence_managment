import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link as RouterLink, useNavigate } from 'react-router-dom';

const MyAppBar = () => {
    const navigate = useNavigate();
    const username = localStorage.getItem('username');
    const role = localStorage.getItem('role');

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <AppBar position="static" color="primary">
            <Toolbar>
                <Typography variant="h6" sx={{ flexGrow: 1 }}>
                    School Portal
                </Typography>
                <Button color="inherit" component={RouterLink} to="/dashboard">
                    Dashboard
                </Button>
                {username && (
                    <Typography variant="body2" sx={{ mx: 2 }}>
                        {username} ({role})
                    </Typography>
                )}
                <Button color="inherit" onClick={handleLogout}>
                    Logout
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default MyAppBar;
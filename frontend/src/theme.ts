import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        mode: 'dark', // <-- This enables dark mode!
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#ff9800',
        },
        background: {
            default: '#121212', // Optional: dark background
            paper: '#1e1e1e',   // Optional: dark card background
        },
    },
    typography: {
        fontFamily: 'Roboto, Arial, sans-serif',
    },
});

export default theme;
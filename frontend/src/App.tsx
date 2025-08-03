import React from 'react';
import AppRoutes from './routes/AppRoutes';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme'; // Make sure you have a theme.ts file

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppRoutes />
    </ThemeProvider>
  );
};

export default App;
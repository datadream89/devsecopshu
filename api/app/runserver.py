// Success.jsx
import React from 'react';
import { Container, Typography, Box } from '@mui/material';

export default function Success() {
  return (
    <Container maxWidth="sm" sx={{ mt: 8, textAlign: 'center' }}>
      <Box>
        <Typography variant="h4" gutterBottom fontWeight="bold" color="success.main">
          Request submitted successfully
        </Typography>
      </Box>
    </Container>
  );
}

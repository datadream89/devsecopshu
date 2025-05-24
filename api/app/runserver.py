import React, { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';

const cignaBlue = '#0047A0';

const RequestSuccess = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const submittedData = location.state || {};
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    const previousRequests = JSON.parse(localStorage.getItem('requests')) || [];
    const lastRequestId = previousRequests.length > 0 ? previousRequests[previousRequests.length - 1].requestId : 0;
    const newRequestId = lastRequestId + 1;

    const newEntries = (submittedData.selectedIds || []).map(id => ({
      pscrfId: id,
      requestId: newRequestId,
      status: 'Success',
    }));

    const updatedRequests = [...previousRequests, ...newEntries];
    localStorage.setItem('requests', JSON.stringify(updatedRequests));
    setRequests(updatedRequests);
  }, [submittedData]);

  const handleBack = () => {
    navigate('/request');
  };

  return (
    <Box p={4}>
      <Typography variant="h5" fontWeight="bold" gutterBottom color={cignaBlue}>
        Request Submitted Successfully!
      </Typography>

      <Paper elevation={3} sx={{ mt: 3, mb: 2 }}>
        <Table>
          <TableHead>
            <TableRow sx={{ backgroundColor: cignaBlue }}>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>PSCRF ID</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Request ID</TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {requests.map((req, index) => (
              <TableRow key={index}>
                <TableCell>{req.pscrfId}</TableCell>
                <TableCell>{req.requestId}</TableCell>
                <TableCell>{req.status}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>

      <Box textAlign="center" mt={4}>
        <Button
          variant="contained"
          onClick={handleBack}
          sx={{ backgroundColor: cignaBlue, textTransform: 'none', fontWeight: 'bold' }}
        >
          Submit Again
        </Button>
      </Box>
    </Box>
  );
};

export default RequestSuccess;

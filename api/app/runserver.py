import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Typography, Table, TableHead, TableBody, TableRow, TableCell, Paper } from '@mui/material';

export default function SuccessPage() {
  const location = useLocation();
  const submittedData = location.state || {};
  const [requests, setRequests] = useState(() => {
    // Load previous requests from localStorage or start fresh
    const saved = localStorage.getItem('requests');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    if (submittedData && submittedData.selectedIds && submittedData.selectedIds.length > 0) {
      const newRequestId = requests.length + 1;
      const newRequest = {
        requestId: newRequestId,
        ids: submittedData.selectedIds.map((item) => item.id),
        status: 'Complete',
      };
      const updatedRequests = [...requests, newRequest];
      setRequests(updatedRequests);
      localStorage.setItem('requests', JSON.stringify(updatedRequests));
    }
  }, [submittedData]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h5" gutterBottom fontWeight="bold">
        Submission Success
      </Typography>

      {requests.length === 0 ? (
        <Typography>No submissions found.</Typography>
      ) : (
        <Paper sx={{ mt: 2, p: 2 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Request ID</TableCell>
                <TableCell>Submitted IDs</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {requests.map(({ requestId, ids, status }) => (
                <TableRow key={requestId}>
                  <TableCell>{requestId}</TableCell>
                  <TableCell>{ids.join(', ')}</TableCell>
                  <TableCell>{status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Container>
  );
}

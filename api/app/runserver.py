import React from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

const cignaBlue = '#004785';

export default function RequestSuccess() {
  const location = useLocation();
  const navigate = useNavigate();

  // Extract passed state from navigation
  const { selectedIds = [], requestId = 1 } = location.state || {};

  // Build table data: one row per selectedId with pscrfId, requestId, status
  const tableData =
    selectedIds.length > 0
      ? selectedIds.map((item) => ({
          pscrfId: item.id,
          requestId,
          status: 'Success',
        }))
      : [{ pscrfId: '-', requestId, status: 'Success' }];

  const handleBack = () => {
    navigate('/');
  };

  return (
    <Container maxWidth="md" sx={{ mt: 6 }}>
      <Typography
        variant="h4"
        color={cignaBlue}
        gutterBottom
        fontWeight="bold"
        align="center"
      >
        Request Submitted Successfully!
      </Typography>

      <Paper sx={{ mt: 4 }}>
        <Table>
          <TableHead sx={{ backgroundColor: cignaBlue }}>
            <TableRow>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>
                PSCRF ID
              </TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>
                Request ID
              </TableCell>
              <TableCell sx={{ color: 'white', fontWeight: 'bold' }}>
                Status
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tableData.map(({ pscrfId, requestId, status }, index) => (
              <TableRow key={index}>
                <TableCell>{pscrfId}</TableCell>
                <TableCell>{requestId}</TableCell>
                <TableCell>{status}</TableCell>
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
    </Container>
  );
}

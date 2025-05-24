import React, { useState } from 'react';
import {
  Box,
  Card,
  Typography,
  IconButton,
  Stack,
  Autocomplete,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button
} from '@mui/material';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { styled } from '@mui/system';
import options from './options.json';

const StyledCard = styled(Card)(({ theme, selected }) => ({
  padding: theme.spacing(2),
  minHeight: 180,
  minWidth: 280,
  border: selected ? `2px solid ${theme.palette.primary.main}` : '1px solid #ccc',
  boxShadow: selected ? theme.shadows[4] : theme.shadows[1],
  textAlign: 'center',
  transition: 'all 0.3s'
}));

const Request = () => {
  const [direction, setDirection] = useState('left-to-right');
  const [selectedOption, setSelectedOption] = useState(null);
  const [openModal, setOpenModal] = useState(false);

  const handleOptionChange = (event, value) => {
    setSelectedOption(value);
    if (value) setOpenModal(true);
  };

  const handleClose = () => {
    setOpenModal(false);
  };

  return (
    <Box display="flex" justifyContent="center" alignItems="flex-start" gap={4}>
      {/* Left Box - PSCRF Data */}
      <StyledCard selected={direction === 'right-to-left'}>
        <Typography variant="h6" gutterBottom>
          PSCRF Data
        </Typography>

        <Autocomplete
          options={options}
          getOptionLabel={(option) => option.label}
          onChange={handleOptionChange}
          renderInput={(params) => <TextField {...params} label="Select Option" />}
        />

        <Dialog open={openModal} onClose={handleClose}>
          <DialogTitle>{selectedOption?.label}</DialogTitle>
          <DialogContent>
            <Typography>{selectedOption?.description}</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      </StyledCard>

      {/* Arrows */}
      <Stack spacing={1} alignItems="center" pt={6}>
        <IconButton
          color={direction === 'left-to-right' ? 'primary' : 'default'}
          onClick={() => setDirection('left-to-right')}
        >
          <ArrowForwardIcon fontSize="large" />
        </IconButton>
        <IconButton
          color={direction === 'right-to-left' ? 'primary' : 'default'}
          onClick={() => setDirection('right-to-left')}
        >
          <ArrowBackIcon fontSize="large" />
        </IconButton>
      </Stack>

      {/* Right Box - Empty for now */}
      <StyledCard selected={direction === 'left-to-right'}>
        <Typography variant="h6">Pricing Version</Typography>
        {/* Placeholder for future content */}
      </StyledCard>
    </Box>
  );
};

export default Request;

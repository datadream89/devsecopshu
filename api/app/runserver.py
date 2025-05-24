import React, { useState } from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Modal,
  TextField,
  IconButton,
  Paper,
  Stack,
  Autocomplete,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import dropdownOptions from './data/options.json';

const cignaBlue = '#004785';

const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 420,
  bgcolor: 'background.paper',
  boxShadow: 24,
  borderRadius: 2,
  p: 3,
  maxHeight: '80vh',
  overflowY: 'auto',
};

export default function IdModalSelector() {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleRemove = (id) => {
    setSelectedOptions((prev) => prev.filter((opt) => opt.id !== id));
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
      <Button
        variant="contained"
        onClick={() => setModalOpen(true)}
        sx={{ backgroundColor: cignaBlue }}
      >
        Select IDs
      </Button>

      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        aria-labelledby="id-selector-modal-title"
        aria-describedby="id-selector-modal-description"
      >
        <Box sx={modalStyle}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography id="id-selector-modal-title" variant="h6" component="h2">
              Search and Select IDs
            </Typography>
            <IconButton onClick={() => setModalOpen(false)} size="small" sx={{ color: cignaBlue }}>
              <CloseIcon />
            </IconButton>
          </Box>

          <Autocomplete
            options={dropdownOptions}
            getOptionLabel={(option) => option.id}
            filterSelectedOptions
            onChange={(event, newValue) => {
              setSelectedOptions(newValue);
            }}
            multiple
            value={selectedOptions}
            renderInput={(params) => (
              <TextField {...params} label="Search and select IDs" variant="outlined" />
            )}
            sx={{ mb: 3 }}
          />

          {selectedOptions.length === 0 && (
            <Typography color="text.secondary" textAlign="center">
              No IDs selected
            </Typography>
          )}

          <Stack spacing={2}>
            {selectedOptions.map((option) => (
              <Paper
                key={option.id}
                elevation={3}
                sx={{
                  p: 2,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  backgroundColor: '#f5faff',
                  borderLeft: `5px solid ${cignaBlue}`,
                }}
              >
                <Box>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {option.id}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    SAM Version: {option.samVersion}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Pricing Version: {option.pricingVersion}
                  </Typography>
                </Box>
                <IconButton
                  onClick={() => handleRemove(option.id)}
                  size="small"
                  sx={{ color: cignaBlue }}
                  aria-label={`Remove ${option.id}`}
                >
                  <CloseIcon />
                </IconButton>
              </Paper>
            ))}
          </Stack>

          <Box mt={4} textAlign="right">
            <Button variant="contained" onClick={() => setModalOpen(false)} sx={{ backgroundColor: cignaBlue }}>
              Done
            </Button>
          </Box>
        </Box>
      </Modal>
    </Container>
  );
}

import React, { useState, useMemo } from 'react';
import {
  Box,
  Container,
  TextField,
  Typography,
  Paper,
  IconButton,
  Chip,
  Stack,
  Autocomplete,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import dropdownOptions from './data/options.json';

const cignaBlue = '#004785';

export default function IdSearchSelect() {
  const [selectedOptions, setSelectedOptions] = useState([]);

  // For search & filter, Autocomplete from MUI handles it nicely

  // Remove selected ID box
  const handleRemove = (id) => {
    setSelectedOptions((prev) => prev.filter((opt) => opt.id !== id));
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Autocomplete
        options={dropdownOptions}
        getOptionLabel={(option) => option.id}
        filterSelectedOptions
        onChange={(event, newValue) => {
          // Prevent duplicates by filtering already selected
          setSelectedOptions(newValue);
        }}
        multiple
        renderInput={(params) => (
          <TextField
            {...params}
            label="Search and select IDs"
            variant="outlined"
            placeholder="Type to search..."
          />
        )}
        value={selectedOptions}
      />

      <Box mt={3}>
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
      </Box>
    </Container>
  );
}

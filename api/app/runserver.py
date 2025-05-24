import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Paper,
  IconButton,
  Stack,
  Autocomplete,
  TextField,
  Grid,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import dropdownOptions from './data/options.json';

const cignaBlue = '#004785';

// Button data
const firstRowButtons = [
  'PSCRF Data',
  'Unsigned Approved Contract',
  'Signed Client Contract',
];
const secondRowButtons = ['One-Way', 'Bi-Directional'];

export default function IntegratedUI() {
  // First row multi-select (min 2)
  const [selectedFirstRow, setSelectedFirstRow] = useState([]);
  // Second row single select (exactly 1)
  const [selectedSecondRow, setSelectedSecondRow] = useState('');
  // Selected IDs from autocomplete
  const [selectedIds, setSelectedIds] = useState([]);

  // Validation messages
  const [validationMsg, setValidationMsg] = useState('');

  // Handle first row button toggle (multi-select)
  const toggleFirstRowButton = (label) => {
    setSelectedFirstRow((prev) => {
      if (prev.includes(label)) {
        return prev.filter((item) => item !== label);
      } else {
        return [...prev, label];
      }
    });
  };

  // Handle second row button select (single-select)
  const selectSecondRowButton = (label) => {
    setSelectedSecondRow(label);
  };

  // Remove selected ID
  const handleRemoveId = (id) => {
    setSelectedIds((prev) => prev.filter((opt) => opt.id !== id));
  };

  // Validate selections on every change
  useEffect(() => {
    if (selectedFirstRow.length < 2) {
      setValidationMsg('Please select at least two buttons in the first row.');
      return;
    }
    if (!selectedSecondRow) {
      setValidationMsg('Please select one button in the second row.');
      return;
    }
    if (
      selectedFirstRow.includes('PSCRF Data') &&
      selectedIds.length === 0
    ) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
      return;
    }
    setValidationMsg('');
  }, [selectedFirstRow, selectedSecondRow, selectedIds]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* First Row Buttons (multi-select) */}
      <Box display="flex" justifyContent="center" gap={2} mb={2} flexWrap="wrap">
        {firstRowButtons.map((label) => (
          <Button
            key={label}
            variant={selectedFirstRow.includes(label) ? 'contained' : 'outlined'}
            onClick={() => toggleFirstRowButton(label)}
            sx={{
              backgroundColor: selectedFirstRow.includes(label) ? cignaBlue : 'transparent',
              color: selectedFirstRow.includes(label) ? 'white' : cignaBlue,
              minWidth: 180,
              fontWeight: 'bold',
              textTransform: 'none',
              '&:hover': {
                backgroundColor: cignaBlue,
                color: 'white',
              },
            }}
          >
            {label}
          </Button>
        ))}
      </Box>

      {/* Second Row Buttons (single-select) */}
      <Box display="flex" justifyContent="center" gap={2} mb={4} flexWrap="wrap">
        {secondRowButtons.map((label) => (
          <Button
            key={label}
            variant={selectedSecondRow === label ? 'contained' : 'outlined'}
            onClick={() => selectSecondRowButton(label)}
            sx={{
              backgroundColor: selectedSecondRow === label ? cignaBlue : 'transparent',
              color: selectedSecondRow === label ? 'white' : cignaBlue,
              minWidth: 120,
              fontWeight: 'bold',
              textTransform: 'none',
              '&:hover': {
                backgroundColor: cignaBlue,
                color: 'white',
              },
            }}
          >
            {label}
          </Button>
        ))}
      </Box>

      {/* Show Autocomplete only if PSCRF Data is selected */}
      {selectedFirstRow.includes('PSCRF Data') && (
        <Box>
          <Autocomplete
            options={dropdownOptions}
            getOptionLabel={(option) => option.id}
            filterSelectedOptions
            onChange={(event, newValue) => {
              setSelectedIds(newValue);
            }}
            multiple
            value={selectedIds}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Search and select IDs"
                variant="outlined"
                placeholder="Type to search..."
              />
            )}
            sx={{ mb: 3 }}
          />

          {/* Selected IDs shown in grid (3 per row max) */}
          {selectedIds.length === 0 ? (
            <Typography color="text.secondary" textAlign="center">
              No IDs selected
            </Typography>
          ) : (
            <Grid container spacing={2}>
              {selectedIds.map((option) => (
                <Grid key={option.id} item xs={12} sm={6} md={4}>
                  <Paper
                    elevation={3}
                    sx={{
                      p: 2,
                      backgroundColor: '#f5faff',
                      borderLeft: `5px solid ${cignaBlue}`,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
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
                      onClick={() => handleRemoveId(option.id)}
                      size="small"
                      sx={{ color: cignaBlue }}
                      aria-label={`Remove ${option.id}`}
                    >
                      <CloseIcon />
                    </IconButton>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          )}
        </Box>
      )}

      {/* Validation message */}
      {validationMsg && (
        <Typography color="error" mt={3} textAlign="center" fontWeight="bold">
          {validationMsg}
        </Typography>
      )}
    </Container>
  );
}

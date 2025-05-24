import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Paper,
  IconButton,
  Grid,
  Autocomplete,
  TextField,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import dropdownOptions from './data/options.json';

const cignaBlue = '#004785';

// Button data renamed
const typeButtons = [
  'PSCRF Data',
  'Unsigned Approved Contract',
  'Signed Client Contract',
];
const compareDirectionButtons = ['One-Way', 'Bi-Directional'];

export default function IntegratedUI() {
  // Type (first row) multi-select (min 2)
  const [selectedTypes, setSelectedTypes] = useState([]);
  // Compare Direction (second row) single select (exactly 1)
  const [selectedCompareDirection, setSelectedCompareDirection] = useState('');
  // Selected IDs from autocomplete
  const [selectedIds, setSelectedIds] = useState([]);

  // Validation messages
  const [validationMsg, setValidationMsg] = useState('');

  // Handle Type button toggle (multi-select)
  const toggleTypeButton = (label) => {
    setSelectedTypes((prev) => {
      if (prev.includes(label)) {
        return prev.filter((item) => item !== label);
      } else {
        return [...prev, label];
      }
    });
  };

  // Handle Compare Direction button select (single-select)
  const selectCompareDirectionButton = (label) => {
    setSelectedCompareDirection(label);
  };

  // Remove selected ID
  const handleRemoveId = (id) => {
    setSelectedIds((prev) => prev.filter((opt) => opt.id !== id));
  };

  // Validate selections on every change
  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
      return;
    }
    if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
      return;
    }
    if (
      selectedTypes.includes('PSCRF Data') &&
      selectedIds.length === 0
    ) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
      return;
    }
    setValidationMsg('');
  }, [selectedTypes, selectedCompareDirection, selectedIds]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Type Buttons (multi-select) */}
      <Box display="flex" justifyContent="center" gap={2} mb={2} flexWrap="wrap">
        {typeButtons.map((label) => (
          <Button
            key={label}
            variant={selectedTypes.includes(label) ? 'contained' : 'outlined'}
            onClick={() => toggleTypeButton(label)}
            sx={{
              backgroundColor: selectedTypes.includes(label) ? cignaBlue : 'transparent',
              color: selectedTypes.includes(label) ? 'white' : cignaBlue,
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

      {/* Compare Direction Buttons (single-select) */}
      <Box display="flex" justifyContent="center" gap={2} mb={4} flexWrap="wrap">
        {compareDirectionButtons.map((label) => (
          <Button
            key={label}
            variant={selectedCompareDirection === label ? 'contained' : 'outlined'}
            onClick={() => selectCompareDirectionButton(label)}
            sx={{
              backgroundColor: selectedCompareDirection === label ? cignaBlue : 'transparent',
              color: selectedCompareDirection === label ? 'white' : cignaBlue,
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
      {selectedTypes.includes('PSCRF Data') && (
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

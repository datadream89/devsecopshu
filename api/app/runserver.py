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
import dropdownOptions from './data/options.json'; // Ensure this path is correct

const cignaBlue = '#004785';

const typeButtons = [
  'PSCRF Data',
  'Unsigned Approved Contract',
  'Signed Client Contract',
];

const compareDirectionButtons = ['One-Way', 'Bi-Directional'];

export default function IntegratedUI() {
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [selectedCompareDirection, setSelectedCompareDirection] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [validationMsg, setValidationMsg] = useState('');

  const toggleTypeButton = (label) => {
    setSelectedTypes((prev) =>
      prev.includes(label) ? prev.filter((item) => item !== label) : [...prev, label]
    );
  };

  const selectCompareDirectionButton = (label) => {
    setSelectedCompareDirection(label);
  };

  const handleRemoveId = (id) => {
    setSelectedIds((prev) => prev.filter((opt) => opt.id !== id));
  };

  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
    } else if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
    } else if (selectedTypes.includes('PSCRF Data') && selectedIds.length === 0) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
    } else {
      setValidationMsg('');
    }
  }, [selectedTypes, selectedCompareDirection, selectedIds]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Type Buttons */}
      <Typography variant="h6" gutterBottom>
        Type
      </Typography>
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
              '&:hover': { backgroundColor: cignaBlue, color: 'white' },
            }}
          >
            {label}
          </Button>
        ))}
      </Box>

      {/* Compare Direction Buttons */}
      <Typography variant="h6" gutterBottom mt={4}>
        Compare Direction
      </Typography>
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
              '&:hover': { backgroundColor: cignaBlue, color: 'white' },
            }}
          >
            {label}
          </Button>
        ))}
      </Box>

      {/* Searchable ID Selector */}
      {selectedTypes.includes('PSCRF Data') && (
        <Box>
          <Autocomplete
            options={dropdownOptions}
            getOptionLabel={(option) => option.id}
            filterSelectedOptions
            onChange={(e, newValue) => setSelectedIds(newValue)}
            multiple
            value={selectedIds}
            renderOption={(props, option) => (
              <Box
                component="li"
                {...props}
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  width: '100%',
                  px: 1,
                }}
              >
                <Typography fontWeight="bold">{option.id}</Typography>
                <Typography variant="body2" color="text.secondary">
                  SAM Version: {option.samVersion}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Pricing Version: {option.pricingVersion}
                </Typography>
              </Box>
            )}
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

          {/* Selected IDs */}
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

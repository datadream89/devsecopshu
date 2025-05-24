import React, { useState } from 'react';
import {
  Box,
  Grid,
  Button,
  Container,
  IconButton,
  Typography,
  TextField,
  FormHelperText,
} from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import Autocomplete from '@mui/material/Autocomplete';
import dropdownOptions from './data/options.json';

const cignaBlue = '#004785';

const firstRowButtons = ['PSCRF Data', 'Unsigned Approved Contract', 'Signed Client Contract'];
const secondRowButtons = ['One-Way', 'Bi-Directional'];

const Request = () => {
  const [firstSelection, setFirstSelection] = useState([]);
  const [secondSelection, setSecondSelection] = useState('');
  const [dropdowns, setDropdowns] = useState([{ id: 1, selected: null }]);
  const [validationError, setValidationError] = useState(false);

  // New state to control inputValue for each dropdown to enable search
  const [inputValues, setInputValues] = useState({ 1: '' });

  const firstRowValid = firstSelection.length >= 2;
  const showDropdowns =
    firstRowValid &&
    firstSelection.includes('PSCRF Data') &&
    (secondSelection === 'One-Way' || secondSelection === 'Bi-Directional');

  const handleAddDropdown = () => {
    const newId = dropdowns.length + 1;
    setDropdowns([...dropdowns, { id: newId, selected: null }]);
    setInputValues((prev) => ({ ...prev, [newId]: '' }));
  };

  const handleSelect = (dropdownId, value) => {
    setDropdowns((prev) =>
      prev.map((d) => (d.id === dropdownId ? { ...d, selected: value } : d))
    );
    // Reset input value to '' after select so input shows formatted text only
    setInputValues((prev) => ({ ...prev, [dropdownId]: '' }));

    if (validationError) {
      setValidationError(false);
    }
  };

  const toggleFirstSelection = (label) => {
    if (firstSelection.includes(label)) {
      if (firstSelection.length <= 2) return;
      setFirstSelection(firstSelection.filter((item) => item !== label));
    } else {
      setFirstSelection([...firstSelection, label]);
    }
  };

  // Control the input value for search
  const handleInputChange = (dropdownId, newInputValue) => {
    setInputValues((prev) => ({ ...prev, [dropdownId]: newInputValue }));
  };

  // Validation check
  const checkValidation = () => {
    if (showDropdowns) {
      const anyEmpty = dropdowns.some((d) => !d.selected);
      setValidationError(anyEmpty);
      return !anyEmpty;
    }
    setValidationError(false);
    return true;
  };

  // Format the selected value for display inside input box with newlines
  const formatSelectedValue = (selected) => {
    if (!selected) return '';
    return `${selected.id}\nSAM Version: ${selected.samVersion}\nPricing Version: ${selected.pricingVersion}`;
  };

  return (
    <Container maxWidth="md">
      <Box mt={4}>
        {/* First row buttons */}
        <Grid container spacing={2} justifyContent="center">
          {firstRowButtons.map((label) => (
            <Grid item key={label}>
              <Button
                variant={firstSelection.includes(label) ? 'contained' : 'outlined'}
                sx={{
                  backgroundColor: firstSelection.includes(label) ? cignaBlue : 'transparent',
                  color: firstSelection.includes(label) ? '#fff' : cignaBlue,
                  borderColor: cignaBlue,
                  '&:hover': {
                    backgroundColor: firstSelection.includes(label) ? '#00386A' : '#e3f2fd',
                  },
                }}
                onClick={() => toggleFirstSelection(label)}
              >
                {label}
              </Button>
            </Grid>
          ))}
        </Grid>

        {!firstRowValid && (
          <FormHelperText error sx={{ textAlign: 'center', mt: 1 }}>
            Please select at least two options in the first row.
          </FormHelperText>
        )}

        {/* Second row buttons */}
        <Box mt={4}>
          <Grid container spacing={2} justifyContent="center">
            {secondRowButtons.map((label) => (
              <Grid item key={label}>
                <Button
                  variant={secondSelection === label ? 'contained' : 'outlined'}
                  sx={{
                    backgroundColor: secondSelection === label ? cignaBlue : 'transparent',
                    color: secondSelection === label ? '#fff' : cignaBlue,
                    borderColor: cignaBlue,
                    '&:hover': {
                      backgroundColor: secondSelection === label ? '#00386A' : '#e3f2fd',
                    },
                  }}
                  onClick={() => setSecondSelection(label)}
                  onBlur={checkValidation}
                >
                  {label}
                </Button>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Dropdowns */}
        {showDropdowns && (
          <Box mt={4}>
            <Typography variant="h6" gutterBottom>
              Select ID:
            </Typography>

            {dropdowns.map((dropdown, index) => {
              const hasError = validationError && !dropdown.selected;

              return (
                <Box
                  key={dropdown.id}
                  display="flex"
                  alignItems="center"
                  gap={1}
                  mb={2}
                >
                  <Box sx={{ flexGrow: 1 }}>
                    <Autocomplete
                      options={dropdownOptions}
                      getOptionLabel={(option) => option.id}
                      value={dropdown.selected}
                      onChange={(event, newValue) => handleSelect(dropdown.id, newValue)}
                      inputValue={inputValues[dropdown.id] || ''}
                      onInputChange={(event, newInputValue) =>
                        handleInputChange(dropdown.id, newInputValue)
                      }
                      isOptionEqualToValue={(option, value) => option.id === value?.id}
                      renderOption={(props, option) => (
                        <li {...props} key={option.id}>
                          <Box>
                            <Typography variant="body1" fontWeight="bold">
                              {option.id}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              SAM Version: {option.samVersion} <br />
                              Pricing Version: {option.pricingVersion}
                            </Typography>
                          </Box>
                        </li>
                      )}
                      renderInput={(params) => (
                        <TextField
                          {...params}
                          label="Select ID"
                          variant="outlined"
                          error={hasError}
                          helperText={hasError ? 'Please select a value' : ''}
                          multiline
                          minRows={3}
                          value={
                            // Show formatted selected value if input is empty (not typing)
                            inputValues[dropdown.id]
                              ? inputValues[dropdown.id]
                              : formatSelectedValue(dropdown.selected)
                          }
                          inputProps={{
                            ...params.inputProps,
                            style: { whiteSpace: 'pre-line' },
                          }}
                        />
                      )}
                    />
                  </Box>

                  {/* + Button */}
                  <IconButton onClick={handleAddDropdown} sx={{ color: cignaBlue }}>
                    <AddCircleOutlineIcon />
                  </IconButton>

                  {/* X Button (only after first) */}
                  {index !== 0 && (
                    <IconButton
                      onClick={() => {
                        setDropdowns(dropdowns.filter((d) => d.id !== dropdown.id));
                        if (validationError) {
                          const stillEmpty = dropdowns
                            .filter((d) => d.id !== dropdown.id)
                            .some((d) => !d.selected);
                          if (!stillEmpty) setValidationError(false);
                        }
                      }}
                      sx={{ color: cignaBlue }}
                    >
                      X
                    </IconButton>
                  )}
                </Box>
              );
            })}
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default Request;

import React, { useState } from 'react';
import {
  Box,
  Grid,
  Button,
  Container,
  IconButton,
  Typography,
  TextField,
  List,
  ListItem,
  ListItemText,
  FormHelperText
} from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import CloseIcon from '@mui/icons-material/Close';
import dropdownOptions from './data/options.json';

const cignaBlue = '#004785';

const firstRowButtons = ['PSCRF Data', 'Unsigned Approved Contract', 'Signed Client Contract'];
const secondRowButtons = ['One-Way', 'Bi-Directional'];

const Request = () => {
  const [firstSelection, setFirstSelection] = useState([]);
  const [secondSelection, setSecondSelection] = useState('');
  const [dropdowns, setDropdowns] = useState([{ id: 1, query: '', filtered: [], selected: null }]);

  const firstRowValid = firstSelection.length >= 2;
  const showDropdowns =
    firstRowValid &&
    firstSelection.includes('PSCRF Data') &&
    (secondSelection === 'One-Way' || secondSelection === 'Bi-Directional');

  const handleAddDropdown = () => {
    setDropdowns([
      ...dropdowns,
      { id: dropdowns.length + 1, query: '', filtered: [], selected: null }
    ]);
  };

  const handleSearch = (id, value) => {
    const filtered = dropdownOptions.filter((opt) =>
      opt.id.startsWith(value)
    );

    setDropdowns((prev) =>
      prev.map((d) =>
        d.id === id ? { ...d, query: value, filtered } : d
      )
    );
  };

  const handleSelect = (dropdownId, option) => {
    setDropdowns((prev) =>
      prev.map((d) =>
        d.id === dropdownId ? { ...d, selected: option } : d
      )
    );
  };

  const toggleFirstSelection = (label) => {
    if (firstSelection.includes(label)) {
      if (firstSelection.length <= 2) return;
      setFirstSelection(firstSelection.filter((item) => item !== label));
    } else {
      setFirstSelection([...firstSelection, label]);
    }
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

        {/* Validation */}
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
              Search for ID:
            </Typography>

            {dropdowns.map((dropdown, index) => (
              <Box
                key={dropdown.id}
                display="flex"
                alignItems="center"
                gap={1}
                mb={2}
              >
                <TextField
                  fullWidth
                  label="Enter ID"
                  value={dropdown.query}
                  onChange={(e) => handleSearch(dropdown.id, e.target.value)}
                  variant="outlined"
                />

                {/* + button */}
                <IconButton onClick={handleAddDropdown} sx={{ color: cignaBlue }}>
                  <AddCircleOutlineIcon />
                </IconButton>

                {/* X button (not shown for first dropdown) */}
                {index !== 0 && (
                  <IconButton
                    onClick={() => {
                      if (dropdowns.length > 1) {
                        setDropdowns(dropdowns.filter((d) => d.id !== dropdown.id));
                      }
                    }}
                    sx={{ color: cignaBlue }}
                  >
                    <CloseIcon />
                  </IconButton>
                )}
              </Box>
            ))}

            {/* Search Results */}
            {dropdowns.map(
              (dropdown) =>
                dropdown.query && (
                  <List dense key={dropdown.id}>
                    {dropdown.filtered.length > 0 ? (
                      dropdown.filtered.map((item) => (
                        <ListItem
                          button
                          key={item.id}
                          selected={dropdown.selected?.id === item.id}
                          onClick={() => handleSelect(dropdown.id, item)}
                        >
                          <ListItemText
                            primary={`ID: ${item.id}`}
                            secondary={`SAM Version: ${item.samVersion}, Pricing Version: ${item.pricingVersion}`}
                          />
                        </ListItem>
                      ))
                    ) : (
                      <ListItem>
                        <ListItemText primary="ID not found" />
                      </ListItem>
                    )}
                  </List>
                )
            )}
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default Request;

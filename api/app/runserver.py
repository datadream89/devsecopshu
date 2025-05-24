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
  ListItemText
} from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import dropdownOptions from './options.json';

const cignaBlue = '#004785';

const Request = () => {
  const [firstSelection, setFirstSelection] = useState('');
  const [secondSelection, setSecondSelection] = useState('');
  const [dropdowns, setDropdowns] = useState([{ id: 1, query: '', filtered: [] }]);

  const showDropdowns = firstSelection === 'PSCRF Data' && (secondSelection === 'One-Way' || secondSelection === 'Bi-Directional');

  const handleAddDropdown = () => {
    setDropdowns([
      ...dropdowns,
      { id: dropdowns.length + 1, query: '', filtered: [] }
    ]);
  };

  const handleSearch = (id, value) => {
    const filtered = dropdownOptions.filter((opt) =>
      opt.value.startsWith(value)
    );

    setDropdowns((prev) =>
      prev.map((d) =>
        d.id === id ? { ...d, query: value, filtered } : d
      )
    );
  };

  return (
    <Container maxWidth="md">
      <Box mt={4}>
        {/* First row buttons */}
        <Grid container spacing={2} justifyContent="center">
          {['PSCRF Data', 'Unsigned Approved Contract', 'Signed Client Contract'].map((label) => (
            <Grid item key={label}>
              <Button
                variant="contained"
                sx={{
                  backgroundColor: cignaBlue,
                  color: '#fff',
                  '&:hover': { backgroundColor: '#00386A' },
                }}
                onClick={() => {
                  setFirstSelection(label);
                  setDropdowns([{ id: 1, query: '', filtered: [] }]); // reset
                }}
              >
                {label}
              </Button>
            </Grid>
          ))}
        </Grid>

        {/* Second row buttons */}
        <Box mt={4}>
          <Grid container spacing={2} justifyContent="center">
            {['One-Way', 'Bi-Directional'].map((label) => (
              <Grid item key={label}>
                <Button
                  variant="outlined"
                  sx={{
                    borderColor: cignaBlue,
                    color: cignaBlue,
                    '&:hover': {
                      borderColor: '#00386A',
                      backgroundColor: '#f0f8ff',
                    },
                  }}
                  onClick={() => {
                    setSecondSelection(label);
                    setDropdowns([{ id: 1, query: '', filtered: [] }]); // reset
                  }}
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
            {dropdowns.map((dropdown) => (
              <Box key={dropdown.id} mb={2}>
                <TextField
                  fullWidth
                  label="Enter ID"
                  value={dropdown.query}
                  onChange={(e) => handleSearch(dropdown.id, e.target.value)}
                  variant="outlined"
                />
                <List dense>
                  {dropdown.query.length > 0 &&
                    (dropdown.filtered.length > 0 ? (
                      dropdown.filtered.map((item) => (
                        <ListItem key={item.value}>
                          <ListItemText primary={`${item.value} - ${item.label}`} />
                        </ListItem>
                      ))
                    ) : (
                      <ListItem>
                        <ListItemText primary="ID not found" />
                      </ListItem>
                    ))}
                </List>
              </Box>
            ))}
            <IconButton onClick={handleAddDropdown} sx={{ color: cignaBlue }}>
              <AddCircleOutlineIcon />
            </IconButton>
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default Request;

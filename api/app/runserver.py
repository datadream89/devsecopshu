import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  IconButton,
  TextField,
  Autocomplete,
  ButtonGroup,
  Button,
  Grid
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import options from './options.json';

const Request = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [direction, setDirection] = useState('right'); // 'right' or 'left'

  const handleSelectionChange = (event, values) => {
    setSelectedOptions(values);
  };

  const removeOption = (idToRemove) => {
    setSelectedOptions(prev => prev.filter(opt => opt.id !== idToRemove));
  };

  const getBoxStyles = (box) => {
    if (direction === 'right') {
      return {
        border: `2px solid ${box === 1 ? 'red' : 'blue'}`,
        borderRadius: 2,
        p: 2,
        minHeight: 300
      };
    } else {
      return {
        border: `2px solid ${box === 1 ? 'blue' : 'red'}`,
        borderRadius: 2,
        p: 2,
        minHeight: 300
      };
    }
  };

  const arrowStyle = (dir) => ({
    backgroundColor: direction === dir ? '#424242' : '#BDBDBD',
    color: 'white',
    '&:hover': {
      backgroundColor: direction === dir ? '#424242' : '#9E9E9E'
    }
  });

  return (
    <Box sx={{ p: 4 }}>
      <Grid container spacing={4} alignItems="center" justifyContent="center">
        {/* First Box */}
        <Grid item xs={5}>
          <Box sx={getBoxStyles(1)}>
            <Typography variant="h6" gutterBottom>
              PSCRF Data
            </Typography>

            <Autocomplete
              multiple
              options={options}
              getOptionLabel={(option) =>
                `${option.id} | ${option.samVersion} | ${option.pricingVersion} | ${option.clientName}`
              }
              value={selectedOptions}
              onChange={handleSelectionChange}
              filterSelectedOptions
              isOptionEqualToValue={(option, value) => option.id === value.id}
              filterOptions={(options, { inputValue }) =>
                options.filter(
                  (opt) =>
                    opt.id.toLowerCase().includes(inputValue.toLowerCase()) ||
                    opt.samVersion.toLowerCase().includes(inputValue.toLowerCase()) ||
                    opt.pricingVersion.toLowerCase().includes(inputValue.toLowerCase()) ||
                    opt.clientName.toLowerCase().includes(inputValue.toLowerCase())
                )
              }
              renderInput={(params) => (
                <TextField {...params} label="Select PSCRF IDs" variant="outlined" />
              )}
              renderOption={(props, option) => (
                <li {...props} key={option.id}>
                  <strong>{option.id}</strong> — {option.samVersion}, {option.pricingVersion}, {option.clientName}
                </li>
              )}
            />

            {selectedOptions.map((opt) => (
              <Card
                key={opt.id}
                sx={{
                  mt: 2,
                  p: 2,
                  position: 'relative',
                  backgroundColor: '#f5f5f5',
                  borderRadius: 2,
                  boxShadow: 2
                }}
              >
                <IconButton
                  size="small"
                  onClick={() => removeOption(opt.id)}
                  sx={{ position: 'absolute', top: 8, right: 8 }}
                >
                  <CloseIcon />
                </IconButton>
                <Typography variant="subtitle1" fontWeight="bold">{opt.id}</Typography>
                <Typography variant="body2"><strong>Client:</strong> {opt.clientName}</Typography>
                <Typography variant="body2"><strong>SAM Version:</strong> {opt.samVersion}</Typography>
                <Typography variant="body2"><strong>Pricing Version:</strong> {opt.pricingVersion}</Typography>
              </Card>
            ))}
          </Box>
        </Grid>

        {/* Arrows */}
        <Grid item xs={2} sx={{ display: 'flex', justifyContent: 'center' }}>
          <ButtonGroup orientation="vertical">
            <Button
              onClick={() => setDirection('right')}
              sx={arrowStyle('right')}
              startIcon={<ArrowForwardIcon />}
            >
              →
            </Button>
            <Button
              onClick={() => setDirection('left')}
              sx={arrowStyle('left')}
              startIcon={<ArrowBackIcon />}
            >
              ←
            </Button>
          </ButtonGroup>
        </Grid>

        {/* Second Box */}
        <Grid item xs={5}>
          <Box sx={getBoxStyles(2)}>
            <Typography variant="h6" gutterBottom>
              Destination (Empty for now)
            </Typography>
            {/* Placeholder for future content */}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Request;

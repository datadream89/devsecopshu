import React, { useState } from 'react';
import {
  Box,
  Typography,
  Card,
  IconButton,
  TextField,
  Autocomplete
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import options from './options.json';

const Request = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleSelectionChange = (event, values) => {
    setSelectedOptions(values);
  };

  const removeOption = (idToRemove) => {
    setSelectedOptions(prev => prev.filter(opt => opt.id !== idToRemove));
  };

  return (
    <Box sx={{ p: 4, width: '100%', maxWidth: 800 }}>
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
  );
};

export default Request;

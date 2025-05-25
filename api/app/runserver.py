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
    <Box sx={{ p: 4, maxWidth: 600 }}>
      <Typography variant="h6" gutterBottom>
        PSCRF Data
      </Typography>

      <Autocomplete
        multiple
        options={options}
        getOptionLabel={(option) => option.id}
        value={selectedOptions}
        onChange={handleSelectionChange}
        filterSelectedOptions
        renderInput={(params) => (
          <TextField {...params} label="Select PSCRF IDs" variant="outlined" />
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

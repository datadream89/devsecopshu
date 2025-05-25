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
  Grid,
  Checkbox,
  FormControlLabel,
  Collapse,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import options from './options.json';

const Request = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [direction, setDirection] = useState('right');
  const [enabled, setEnabled] = useState(true);
  const [expanded, setExpanded] = useState(true);

  const handleSelectionChange = (event, values) => {
    setSelectedOptions(values);
  };

  const removeOption = (idToRemove, samVersionToRemove, pricingVersionToRemove) => {
    setSelectedOptions(prev =>
      prev.filter(
        (opt) =>
          !(
            opt.id === idToRemove &&
            opt.samVersion === samVersionToRemove &&
            opt.pricingVersion === pricingVersionToRemove
          )
      )
    );
  };

  const getBoxStyles = (box) => {
    if (!enabled) {
      return {
        border: `2px solid #E0E0E0`,
        borderRadius: 2,
        p: 2,
        minHeight: 300,
        backgroundColor: '#F5F5F5',
        color: '#9E9E9E',
      };
    }

    if (direction === 'right') {
      return {
        border: `2px solid ${box === 1 ? '#BDBDBD' : '#424242'}`,
        borderRadius: 2,
        p: 2,
        minHeight: 300,
      };
    } else {
      return {
        border: `2px solid ${box === 1 ? '#424242' : '#BDBDBD'}`,
        borderRadius: 2,
        p: 2,
        minHeight: 300,
      };
    }
  };

  const arrowStyle = (dir) => ({
    backgroundColor:
      !enabled ? '#E0E0E0' : direction === dir ? '#424242' : '#BDBDBD',
    color: !enabled ? '#9E9E9E' : 'white',
    cursor: !enabled ? 'default' : 'pointer',
    '&:hover': {
      backgroundColor:
        !enabled
          ? '#E0E0E0'
          : direction === dir
          ? '#424242'
          : '#9E9E9E',
    },
    pointerEvents: !enabled ? 'none' : 'auto',
  });

  return (
    <Box sx={{ p: 4 }}>
      {/* Always show toggle and (when expanded) enable compare */}
      <Box display="flex" flexDirection="column" alignItems="center" mb={2}>
        {expanded && (
          <FormControlLabel
            control={
              <Checkbox
                checked={enabled}
                onChange={(e) => setEnabled(e.target.checked)}
                color="primary"
              />
            }
            label="Enable Compare"
          />
        )}
        <Box>
          <IconButton onClick={() => setExpanded(false)} disabled={!expanded}>
            <RemoveIcon />
          </IconButton>
          <IconButton onClick={() => setExpanded(true)} disabled={expanded}>
            <AddIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Collapse entire comparison section */}
      <Collapse in={expanded}>
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
                isOptionEqualToValue={(option, value) =>
                  option.id === value.id &&
                  option.samVersion === value.samVersion &&
                  option.pricingVersion === value.pricingVersion
                }
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
                  <TextField
                    {...params}
                    label="Select PSCRF IDs"
                    variant="outlined"
                    disabled={!enabled}
                  />
                )}
                renderOption={(props, option) => (
                  <li
                    {...props}
                    key={`${option.id}-${option.samVersion}-${option.pricingVersion}`}
                  >
                    {`id: ${option.id}, clientName: ${option.clientName}, samVersion: ${option.samVersion}, pricingVersion: ${option.pricingVersion}`}
                  </li>
                )}
              />

              {selectedOptions.map((opt) => (
                <Card
                  key={`${opt.id}-${opt.samVersion}-${opt.pricingVersion}`}
                  sx={{
                    mt: 2,
                    p: 2,
                    position: 'relative',
                    backgroundColor: '#f5f5f5',
                    borderRadius: 2,
                    boxShadow: 2,
                    opacity: enabled ? 1 : 0.6,
                  }}
                >
                  <IconButton
                    size="small"
                    onClick={() =>
                      removeOption(opt.id, opt.samVersion, opt.pricingVersion)
                    }
                    sx={{ position: 'absolute', top: 8, right: 8 }}
                    disabled={!enabled}
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
          <Grid item xs={2} sx={{ textAlign: 'center' }}>
            <ButtonGroup orientation="vertical">
              <Button
                onClick={() => enabled && setDirection('right')}
                sx={arrowStyle('right')}
                startIcon={<ArrowForwardIcon />}
                disabled={!enabled}
              >
                →
              </Button>
              <Button
                onClick={() => enabled && setDirection('left')}
                sx={arrowStyle('left')}
                startIcon={<ArrowBackIcon />}
                disabled={!enabled}
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
            </Box>
          </Grid>
        </Grid>
      </Collapse>
    </Box>
  );
};

export default Request;

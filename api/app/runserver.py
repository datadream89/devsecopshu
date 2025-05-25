import React, { useState } from 'react';
import {
  Box,
  Typography,
  Checkbox,
  FormControlLabel,
  IconButton,
  Grid,
  TextField,
  Autocomplete,
  Radio,
  RadioGroup,
  FormControl,
  FormLabel,
  Button,
  Paper,
} from '@mui/material';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const options = [
  { id: '7001', clientName: 'Client A', samVersion: 'v1.2', pricingVersion: 'p1.0' },
  { id: '5002', clientName: 'Client B', samVersion: 'v2.0', pricingVersion: 'p2.3' },
  { id: '7005', clientName: 'Client C', samVersion: 'v1.0', pricingVersion: 'p1.2' },
  { id: '7020', clientName: 'Client D', samVersion: 'v3.1', pricingVersion: 'p3.0' },
  { id: '5010', clientName: 'Client E', samVersion: 'v1.4', pricingVersion: 'p1.5' },
];

const ApprovedContractSection = ({ index, section, handleTypeChange, handleFileChange, addSection, removeSection }) => (
  <Box
    key={section.id}
    sx={{
      mb: 2,
      p: 2,
      border: '1px solid #ccc',
      borderRadius: 2,
      position: 'relative',
    }}
  >
    <Typography fontWeight="bold" mb={1}>
      Approved Contract {index + 1}
    </Typography>
    <RadioGroup
      row
      value={section.contractType}
      onChange={(e) => handleTypeChange(section.id, e.target.value)}
    >
      <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
      <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
      <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
    </RadioGroup>
    <input
      accept=".pdf,.docx"
      style={{ display: 'none' }}
      id={`upload-button-${section.id}`}
      type="file"
      onChange={(e) => handleFileChange(section.id, e.target.files[0])}
    />
    <label htmlFor={`upload-button-${section.id}`}>
      <Button variant="outlined" component="span" startIcon={<CloudUploadIcon />}>
        Upload File
      </Button>
    </label>
    <Box sx={{ position: 'absolute', top: 10, right: 10, display: 'flex', gap: 1 }}>
      <IconButton size="small" onClick={addSection}>
        <AddIcon fontSize="small" />
      </IconButton>
      {index > 0 && (
        <IconButton size="small" onClick={() => removeSection(section.id)}>
          <CloseIcon fontSize="small" />
        </IconButton>
      )}
    </Box>
  </Box>
);

export default function Request() {
  const [enabled, setEnabled] = useState(true);
  const [direction, setDirection] = useState('right');
  const [collapsed, setCollapsed] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState([]);

  const [contractSections, setContractSections] = useState([
    { id: 0, contractType: 'Agreement', file: null },
  ]);

  const addSection = () => {
    const newId = contractSections.length ? Math.max(...contractSections.map(s => s.id)) + 1 : 0;
    setContractSections([...contractSections, { id: newId, contractType: 'Agreement', file: null }]);
  };

  const removeSection = (id) => {
    setContractSections(contractSections.filter((s) => s.id !== id));
  };

  const handleTypeChange = (id, newType) => {
    setContractSections(contractSections.map((s) => (s.id === id ? { ...s, contractType: newType } : s)));
  };

  const handleFileChange = (id, file) => {
    setContractSections(contractSections.map((s) => (s.id === id ? { ...s, file } : s)));
  };

  const getBoxBorder = (side) => {
    if (!enabled) return '1px solid lightgray';
    return direction === side ? '2px solid red' : '2px solid blue';
  };

  return (
    <Box sx={{ p: 2 }}>
      {!collapsed && (
        <FormControlLabel
          control={<Checkbox checked={enabled} onChange={(e) => setEnabled(e.target.checked)} />}
          label="Compare"
          sx={{ mb: 2 }}
        />
      )}

      <Grid container spacing={2} alignItems="flex-start">
        {!collapsed && (
          <>
            <Grid item xs={5}>
              <Paper sx={{ p: 2, border: getBoxBorder('right') }}>
                <Typography variant="h6">Pscerf Data</Typography>
                <Autocomplete
                  multiple
                  options={options}
                  getOptionLabel={(option) =>
                    `${option.id} (Client: ${option.clientName}, SAM: ${option.samVersion}, Pricing: ${option.pricingVersion})`
                  }
                  filterSelectedOptions
                  onChange={(e, value) => setSelectedOptions(value)}
                  renderInput={(params) => <TextField {...params} label="Select PSCRF IDs" />}
                />
              </Paper>
            </Grid>

            <Grid item xs={2} textAlign="center">
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 4 }}>
                <IconButton
                  onClick={() => setDirection('right')}
                  disabled={!enabled}
                  sx={{ color: direction === 'right' ? 'darkgray' : 'lightgray' }}
                >
                  <ArrowForwardIcon fontSize="large" />
                </IconButton>
                <IconButton
                  onClick={() => setDirection('left')}
                  disabled={!enabled}
                  sx={{ color: direction === 'left' ? 'darkgray' : 'lightgray' }}
                >
                  <ArrowBackIcon fontSize="large" />
                </IconButton>
              </Box>
            </Grid>

            <Grid item xs={5}>
              <Paper sx={{ p: 2, border: getBoxBorder('left') }}>
                <Typography variant="h6" gutterBottom>
                  Approved Contract
                </Typography>
                {contractSections.map((section, index) => (
                  <ApprovedContractSection
                    key={section.id}
                    index={index}
                    section={section}
                    handleTypeChange={handleTypeChange}
                    handleFileChange={handleFileChange}
                    addSection={addSection}
                    removeSection={removeSection}
                  />
                ))}
              </Paper>
            </Grid>
          </>
        )}
      </Grid>

      <Box mt={2} display="flex" alignItems="center" justifyContent="center" gap={1}>
        {collapsed && <Typography>Compare PSCRF and Approved Contract</Typography>}
        <IconButton onClick={() => setCollapsed(!collapsed)}>
          {collapsed ? <AddIcon /> : <CloseIcon />}
        </IconButton>
      </Box>
    </Box>
  );
}

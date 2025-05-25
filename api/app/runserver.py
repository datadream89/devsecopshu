import React, { useState } from 'react';
import { Button, IconButton, Box, Typography, RadioGroup, FormControlLabel, Radio, TextField, Autocomplete } from '@mui/material';
import UploadIcon from '@mui/icons-material/Upload';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const pscrfOptions = [
  { id: 'PS001', samVersion: 'v1', pricingVersion: 'p1', clientName: 'Client A' },
  { id: 'PS002', samVersion: 'v2', pricingVersion: 'p2', clientName: 'Client B' },
  { id: 'PS003', samVersion: 'v3', pricingVersion: 'p3', clientName: 'Client C' }
];

const PSCRFSection = ({ value, onChange }) => {
  const handleRemove = (index) => {
    const updated = [...value];
    updated.splice(index, 1);
    onChange(updated);
  };

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white">
      <Autocomplete
        multiple
        options={pscrfOptions}
        getOptionLabel={(option) => `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`}
        value={value}
        onChange={(event, newValue) => onChange(newValue)}
        renderInput={(params) => <TextField {...params} label="Select PSCRF" variant="outlined" />}
      />
      <Box display="flex" flexWrap="wrap" mt={2} gap={2}>
        {value.map((option, index) => (
          <Box key={index} border={1} borderRadius={2} borderColor="grey.400" p={2} width="calc(50% - 8px)" bgcolor="white" position="relative">
            <Typography variant="body2">
              <strong>ID:</strong> {option.id}<br />
              <strong>SAM:</strong> {option.samVersion}<br />
              <strong>Pricing:</strong> {option.pricingVersion}<br />
              <strong>Client:</strong> {option.clientName}
            </Typography>
            <IconButton size="small" onClick={() => handleRemove(index)} sx={{ position: 'absolute', top: 4, right: 4 }}>
              <CloseIcon fontSize="small" />
            </IconButton>
          </Box>
        ))}
      </Box>
    </Box>
  );
};

const ApprovedContractSection = () => {
  const [sections, setSections] = useState([{ id: Date.now(), type: 'Agreement', file: null, filename: '' }]);

  const handleAddSection = () => {
    setSections([...sections, { id: Date.now(), type: 'Agreement', file: null, filename: '' }]);
  };

  const handleRemoveSection = (id) => {
    setSections(sections.filter(section => section.id !== id));
  };

  const handleRadioChange = (id, type) => {
    setSections(sections.map(section => section.id === id ? { ...section, type, file: null, filename: '' } : section));
  };

  const handleFileChange = (id, file) => {
    setSections(sections.map(section => section.id === id ? { ...section, file, filename: file.name } : section));
  };

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white">
      <Typography variant="h6">Approved Contract</Typography>
      {sections.map(section => (
        <Box key={section.id} display="flex" alignItems="center" gap={2} mt={2}>
          <RadioGroup row value={section.type} onChange={(e) => handleRadioChange(section.id, e.target.value)}>
            <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
            <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
            <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
          </RadioGroup>
          <input type="file" id={`upload-${section.id}`} style={{ display: 'none' }} onChange={(e) => handleFileChange(section.id, e.target.files[0])} />
          <label htmlFor={`upload-${section.id}`}>
            <IconButton component="span">
              <UploadIcon />
            </IconButton>
          </label>
          {section.filename && <Typography>{section.filename}</Typography>}
          {sections.length > 1 && (
            <IconButton onClick={() => handleRemoveSection(section.id)}>
              <CloseIcon />
            </IconButton>
          )}
        </Box>
      ))}
      <Button startIcon={<AddIcon />} onClick={handleAddSection} sx={{ mt: 2 }}>Add Section</Button>
    </Box>
  );
};

const TitleBar = ({ title, expanded, toggleExpanded, checked, onCheckChange }) => (
  <Box display="flex" alignItems="center" bgcolor="#f5f5f5" px={2} py={1} border={1} borderColor="grey.400" borderRadius={1} mb={2}>
    <input type="checkbox" checked={checked} onChange={onCheckChange} style={{ marginRight: 10 }} />
    <Typography variant="subtitle1" flex={1}>{title}</Typography>
    <IconButton onClick={toggleExpanded}>
      {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
    </IconButton>
  </Box>
);

const HorizontalPair = ({ leftComponent, rightComponent, title }) => {
  const [expanded, setExpanded] = useState(true);
  const [checked, setChecked] = useState(true);

  return (
    <Box mb={4}>
      <TitleBar
        title={title}
        expanded={expanded}
        toggleExpanded={() => setExpanded(!expanded)}
        checked={checked}
        onCheckChange={(e) => setChecked(e.target.checked)}
      />
      {expanded && (
        <Box display="flex" gap={2} px={1} opacity={checked ? 1 : 0.5}>
          <Box flex={1}>{leftComponent}</Box>
          <Box flex={1}>{rightComponent}</Box>
        </Box>
      )}
    </Box>
  );
};

export default function MainLayout() {
  const [pscrfStates, setPscrfStates] = useState({
    'row1-left': [],
    'row3-right': [],
    'row4-left': [],
    'row4-right': []
  });

  const createPscrfComponent = (key) => (
    <PSCRFSection
      value={pscrfStates[key] || []}
      onChange={(newVal) => setPscrfStates({ ...pscrfStates, [key]: newVal })}
    />
  );

  return (
    <Box p={4}>
      <HorizontalPair
        title="Row 1"
        leftComponent={createPscrfComponent('row1-left')}
        rightComponent={<ApprovedContractSection />}
      />
      <HorizontalPair
        title="Row 2"
        leftComponent={<ApprovedContractSection />}
        rightComponent={<ApprovedContractSection />}
      />
      <HorizontalPair
        title="Row 3"
        leftComponent={<ApprovedContractSection />}
        rightComponent={createPscrfComponent('row3-right')}
      />
      <HorizontalPair
        title="Row 4"
        leftComponent={createPscrfComponent('row4-left')}
        rightComponent={createPscrfComponent('row4-right')}
      />
    </Box>
  );
}

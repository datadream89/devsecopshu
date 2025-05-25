import React, { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Upload } from '@mui/icons-material';
import { TextField, Autocomplete, IconButton, Box, Typography, RadioGroup, FormControlLabel, Radio, Divider } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const pscrfOptions = [
  { id: 'PS001', samVersion: 'v1', pricingVersion: 'p1', clientName: 'Client A' },
  { id: 'PS002', samVersion: 'v2', pricingVersion: 'p2', clientName: 'Client B' },
  { id: 'PS003', samVersion: 'v3', pricingVersion: 'p3', clientName: 'Client C' },
];

const PSCRFSection = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white">
      <Autocomplete
        multiple
        options={pscrfOptions}
        getOptionLabel={(option) => `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`}
        onChange={(event, value) => setSelectedOptions(value)}
        renderInput={(params) => <TextField {...params} label="Select PSCRF" variant="outlined" />}
      />
      <Box display="flex" flexWrap="wrap" mt={2} gap={2}>
        {selectedOptions.map((option, index) => (
          <Card key={index} sx={{ minWidth: '45%' }}>
            <CardContent>
              <Typography variant="body2">
                <strong>ID:</strong> {option.id}<br />
                <strong>SAM:</strong> {option.samVersion}<br />
                <strong>Pricing:</strong> {option.pricingVersion}<br />
                <strong>Client:</strong> {option.clientName}
              </Typography>
            </CardContent>
          </Card>
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
          <RadioGroup
            row
            value={section.type}
            onChange={(e) => handleRadioChange(section.id, e.target.value)}
          >
            <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
            <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
            <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
          </RadioGroup>
          <input
            type="file"
            style={{ display: 'none' }}
            id={`upload-${section.id}`}
            onChange={(e) => handleFileChange(section.id, e.target.files[0])}
          />
          <label htmlFor={`upload-${section.id}`}>
            <IconButton component="span">
              <Upload />
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
  <Box display="flex" alignItems="center" bgcolor="#f5f5f5" px={2} py={1} borderTop={1} borderBottom={1} borderColor="grey.400">
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
        <Box display="flex" gap={2} mt={2} px={1} opacity={checked ? 1 : 0.5}>
          <Box flex={1}>{leftComponent}</Box>
          <Box flex={1}>{rightComponent}</Box>
        </Box>
      )}
    </Box>
  );
};

export default function MainLayout() {
  return (
    <Box p={4}>
      <HorizontalPair title="Row 1" leftComponent={<PSCRFSection />} rightComponent={<ApprovedContractSection />} />
      <HorizontalPair title="Row 2" leftComponent={<ApprovedContractSection />} rightComponent={<ApprovedContractSection />} />
      <HorizontalPair title="Row 3" leftComponent={<ApprovedContractSection />} rightComponent={<PSCRFSection />} />
      <HorizontalPair title="Row 4" leftComponent={<PSCRFSection />} rightComponent={<PSCRFSection />} />
    </Box>
  );
}

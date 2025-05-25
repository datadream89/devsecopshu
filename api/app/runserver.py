import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Checkbox,
  IconButton,
  Collapse,
  Card,
  CardContent,
  TextField,
  Button,
  RadioGroup,
  FormControlLabel,
  Radio
} from '@mui/material';
import { ExpandLess, ExpandMore, Close, CloudUpload } from '@mui/icons-material';
import Autocomplete from '@mui/material/Autocomplete';

const PSCRFSection = () => {
  const [selectedItems, setSelectedItems] = useState([]);
  const [options, setOptions] = useState([]);

  useEffect(() => {
    fetch('/data/options.json')
      .then(res => res.json())
      .then(data => setOptions(data))
      .catch(err => console.error('Failed to load options:', err));
  }, []);

  const handleSelect = (event, newValue) => {
    setSelectedItems(newValue);
  };

  const handleRemove = (idToRemove) => {
    setSelectedItems(prev => prev.filter(item => item.id !== idToRemove));
  };

  return (
    <Box>
      <Autocomplete
        multiple
        options={options}
        getOptionLabel={(option) => `${option.id}`}
        onChange={handleSelect}
        value={selectedItems}
        renderInput={(params) => (
          <TextField {...params} label="Select PSCRF" variant="outlined" />
        )}
      />

      <Grid container spacing={2} mt={2}>
        {selectedItems.map((item) => (
          <Grid item xs={6} key={item.id}>
            <Card variant="outlined">
              <CardContent sx={{ position: 'relative' }}>
                <IconButton
                  size="small"
                  onClick={() => handleRemove(item.id)}
                  sx={{ position: 'absolute', top: 0, right: 0 }}
                >
                  <Close fontSize="small" />
                </IconButton>
                <Typography variant="subtitle1">{item.id}</Typography>
                <Typography variant="body2">SAM: {item.samVersion}</Typography>
                <Typography variant="body2">Pricing: {item.pricingVersion}</Typography>
                <Typography variant="body2">Client: {item.clientName}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

const ApprovedContractSection = () => {
  const [sections, setSections] = useState([
    { id: 0, type: 'Agreement', file: null }
  ]);

  const handleRadioChange = (id, value) => {
    setSections(sections.map(section =>
      section.id === id ? { ...section, type: value, file: null } : section
    ));
  };

  const handleFileUpload = (id, file) => {
    setSections(sections.map(section =>
      section.id === id ? { ...section, file } : section
    ));
  };

  const handleAddSection = () => {
    const newId = sections.length ? sections[sections.length - 1].id + 1 : 0;
    setSections([...sections, { id: newId, type: 'Agreement', file: null }]);
  };

  const handleRemoveSection = (id) => {
    setSections(sections.filter(section => section.id !== id));
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>Approved Contract</Typography>
      {sections.map(section => (
        <Box key={section.id} display="flex" alignItems="center" mb={2}>
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
            accept="*"
            style={{ display: 'none' }}
            id={`upload-${section.id}`}
            type="file"
            onChange={(e) => handleFileUpload(section.id, e.target.files[0])}
          />
          <label htmlFor={`upload-${section.id}`}>
            <Button component="span" startIcon={<CloudUpload />}>
              Upload
            </Button>
          </label>
          {section.file && <Typography ml={1}>{section.file.name}</Typography>}
          <IconButton onClick={() => handleRemoveSection(section.id)}>
            <Close />
          </IconButton>
        </Box>
      ))}
      <Button onClick={handleAddSection}>+ Add Section</Button>
    </Box>
  );
};

const HorizontalPair = ({ title, leftContent, rightContent }) => {
  const [expanded, setExpanded] = useState(true);
  const [checked, setChecked] = useState(true);

  return (
    <Box mb={4}>
      <Box display="flex" alignItems="center" mb={1}>
        <Checkbox checked={checked} onChange={(e) => setChecked(e.target.checked)} />
        <Box flexGrow={1} textAlign="center">
          <Button onClick={() => setExpanded(!expanded)}>
            {expanded ? <ExpandLess /> : <ExpandMore />}
            {title}
          </Button>
        </Box>
      </Box>
      <Collapse in={expanded}>
        <Grid container spacing={2} sx={{ opacity: checked ? 1 : 0.5 }}>
          <Grid item xs={6}>{leftContent}</Grid>
          <Grid item xs={6}>{rightContent}</Grid>
        </Grid>
      </Collapse>
    </Box>
  );
};

const MainComponent = () => {
  return (
    <Box p={4}>
      <HorizontalPair
        title="Row 1"
        leftContent={<PSCRFSection />}
        rightContent={<ApprovedContractSection />}
      />
      <HorizontalPair
        title="Row 2"
        leftContent={<ApprovedContractSection />}
        rightContent={<div>Signed Contract</div>}
      />
      <HorizontalPair
        title="Row 3"
        leftContent={<ApprovedContractSection />}
        rightContent={<PSCRFSection />}
      />
      <HorizontalPair
        title="Row 4"
        leftContent={<PSCRFSection />}
        rightContent={<PSCRFSection />}
      />
    </Box>
  );
};

export default MainComponent;

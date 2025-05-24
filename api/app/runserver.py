import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Typography,
  Paper,
  IconButton,
  Grid,
  Autocomplete,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  RadioGroup,
  FormControlLabel,
  Radio,
  Divider,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import dropdownOptions from './data/options.json'; // Ensure this file exists

const cignaBlue = '#004785';

const typeButtons = [
  'PSCRF Data',
  'Unsigned Approved Contract',
  'Signed Client Contract',
];

const compareDirectionButtons = ['One-Way', 'Bi-Directional'];

export default function IntegratedUI() {
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [selectedCompareDirection, setSelectedCompareDirection] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [validationMsg, setValidationMsg] = useState('');
  const [uploadSections, setUploadSections] = useState([{ id: Date.now(), fileName: '', type: '' }]);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [currentUploadId, setCurrentUploadId] = useState(null);

  const toggleTypeButton = (label) => {
    setSelectedTypes((prev) =>
      prev.includes(label) ? prev.filter((item) => item !== label) : [...prev, label]
    );
  };

  const selectCompareDirectionButton = (label) => {
    setSelectedCompareDirection(label);
  };

  const handleRemoveId = (id) => {
    setSelectedIds((prev) => prev.filter((opt) => opt.id !== id));
  };

  const handleRadioChange = (id, value) => {
    setUploadSections((prev) =>
      prev.map((section) =>
        section.id === id ? { ...section, type: value } : section
      )
    );
  };

  const handleOpenUploadDialog = (id) => {
    setCurrentUploadId(id);
    setUploadDialogOpen(true);
  };

  const handleCloseUploadDialog = () => {
    setUploadDialogOpen(false);
  };

  const handleFileUpload = () => {
    setUploadSections((prev) =>
      prev.map((section) =>
        section.id === currentUploadId
          ? { ...section, fileName: `File_${Date.now()}.pdf` }
          : section
      )
    );
    setUploadDialogOpen(false);
  };

  const handleAddSection = () => {
    setUploadSections((prev) => [...prev, { id: Date.now(), fileName: '', type: '' }]);
  };

  const handleRemoveSection = (id) => {
    setUploadSections((prev) => prev.filter((section) => section.id !== id));
  };

  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
    } else if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
    } else if (selectedTypes.includes('PSCRF Data') && selectedIds.length === 0) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
    } else {
      setValidationMsg('');
    }
  }, [selectedTypes, selectedCompareDirection, selectedIds]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Type Buttons */}
      <Typography variant="h6" gutterBottom>Type</Typography>
      <Box display="flex" justifyContent="center" gap={2} mb={2} flexWrap="wrap">
        {typeButtons.map((label) => (
          <Button
            key={label}
            variant={selectedTypes.includes(label) ? 'contained' : 'outlined'}
            onClick={() => toggleTypeButton(label)}
            sx={{
              backgroundColor: selectedTypes.includes(label) ? cignaBlue : 'transparent',
              color: selectedTypes.includes(label) ? 'white' : cignaBlue,
              minWidth: 180,
              fontWeight: 'bold',
              textTransform: 'none',
              '&:hover': { backgroundColor: cignaBlue, color: 'white' },
            }}
          >
            {label}
          </Button>
        ))}
      </Box>

      {/* Compare Direction Buttons */}
      <Typography variant="h6" gutterBottom mt={4}>Compare Direction</Typography>
      <Box display="flex" justifyContent="center" gap={2} mb={4} flexWrap="wrap">
        {compareDirectionButtons.map((label) => (
          <Button
            key={label}
            variant={selectedCompareDirection === label ? 'contained' : 'outlined'}
            onClick={() => selectCompareDirectionButton(label)}
            sx={{
              backgroundColor: selectedCompareDirection === label ? cignaBlue : 'transparent',
              color: selectedCompareDirection === label ? 'white' : cignaBlue,
              minWidth: 120,
              fontWeight: 'bold',
              textTransform: 'none',
              '&:hover': { backgroundColor: cignaBlue, color: 'white' },
            }}
          >
            {label}
          </Button>
        ))}
      </Box>

      {/* PSCRF ID Autocomplete */}
      {selectedTypes.includes('PSCRF Data') && (
        <Box>
          <Autocomplete
            options={dropdownOptions}
            getOptionLabel={(option) => option.id}
            filterSelectedOptions
            onChange={(e, newValue) => setSelectedIds(newValue)}
            multiple
            value={selectedIds}
            renderOption={(props, option) => {
              const { key, ...rest } = props;
              return (
                <li key={key} {...rest} style={{ display: 'block', width: '100%', padding: '8px 12px' }}>
                  <Box display="flex" flexDirection="column" alignItems="flex-start">
                    <Typography variant="subtitle2" fontWeight="bold">{option.id}</Typography>
                    <Typography variant="caption" color="text.secondary">SAM Version: {option.samVersion}</Typography>
                    <Typography variant="caption" color="text.secondary">Pricing Version: {option.pricingVersion}</Typography>
                  </Box>
                </li>
              );
            }}
            renderInput={(params) => (
              <TextField {...params} label="Search and select IDs" variant="outlined" placeholder="Type to search..." />
            )}
            sx={{ mb: 3 }}
          />

          {/* Selected ID Cards */}
          {selectedIds.length === 0 ? (
            <Typography color="text.secondary" textAlign="center">No IDs selected</Typography>
          ) : (
            <Grid container spacing={2}>
              {selectedIds.map((option) => (
                <Grid key={option.id} item xs={12} sm={6} md={4}>
                  <Paper
                    elevation={3}
                    sx={{
                      p: 2,
                      backgroundColor: '#f5faff',
                      borderLeft: `5px solid ${cignaBlue}`,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      height: '100%',
                    }}
                  >
                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold">{option.id}</Typography>
                      <Typography variant="body2" color="text.secondary">SAM Version: {option.samVersion}</Typography>
                      <Typography variant="body2" color="text.secondary">Pricing Version: {option.pricingVersion}</Typography>
                    </Box>
                    <IconButton
                      onClick={() => handleRemoveId(option.id)}
                      size="small"
                      sx={{ color: cignaBlue }}
                      aria-label={`Remove ${option.id}`}
                    >
                      <CloseIcon />
                    </IconButton>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          )}
        </Box>
      )}

      {/* Unsigned Approved Contract Upload Section */}
      {selectedTypes.includes('Unsigned Approved Contract') && (
        <Box mt={4}>
          <Typography variant="h6" gutterBottom>Upload Unsigned Approved Contract</Typography>
          {uploadSections.map((section, index) => (
            <Paper key={section.id} sx={{ p: 2, mb: 2, borderLeft: `5px solid ${cignaBlue}` }}>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <RadioGroup
                  row
                  value={section.type}
                  onChange={(e) => handleRadioChange(section.id, e.target.value)}
                >
                  {['Agreement', 'Supplement', 'Addendum'].map((option) => (
                    <FormControlLabel key={option} value={option} control={<Radio />} label={option} />
                  ))}
                </RadioGroup>
                {index > 0 && (
                  <IconButton onClick={() => handleRemoveSection(section.id)} sx={{ color: 'red' }}>
                    <CloseIcon />
                  </IconButton>
                )}
              </Box>
              <Divider sx={{ my: 1 }} />
              <Box display="flex" alignItems="center" gap={2}>
                <Button
                  variant="outlined"
                  endIcon={<MoreHorizIcon />}
                  onClick={() => handleOpenUploadDialog(section.id)}
                  sx={{ textTransform: 'none' }}
                >
                  {section.fileName || 'Upload File'}
                </Button>
                {index === uploadSections.length - 1 && (
                  <IconButton onClick={handleAddSection} sx={{ color: cignaBlue }}>
                    <AddIcon />
                  </IconButton>
                )}
              </Box>
            </Paper>
          ))}
        </Box>
      )}

      {/* Upload Dialog */}
      <Dialog open={uploadDialogOpen} onClose={handleCloseUploadDialog}>
        <DialogTitle>Upload File</DialogTitle>
        <DialogContent>
          <Typography>File selection simulated.</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseUploadDialog}>Cancel</Button>
          <Button onClick={handleFileUpload} variant="contained" color="primary">Upload</Button>
        </DialogActions>
      </Dialog>

      {/* Validation Message */}
      {validationMsg && (
        <Typography color="error" mt={3} textAlign="center" fontWeight="bold">
          {validationMsg}
        </Typography>
      )}
    </Container>
  );
}

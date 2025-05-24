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
  Radio,
  RadioGroup,
  FormControlLabel,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import FileUploadOutlinedIcon from '@mui/icons-material/FileUploadOutlined';
import dropdownOptions from './data/options.json';

const cignaBlue = '#004785';
const typeButtons = ['PSCRF Data', 'Unsigned Approved Contract', 'Signed Client Contract'];
const compareDirectionButtons = ['One-Way', 'Bi-Directional'];
const fileTypes = ['Agreement', 'Supplement', 'Addendum'];

export default function IntegratedUI() {
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [selectedCompareDirection, setSelectedCompareDirection] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [validationMsg, setValidationMsg] = useState('');
  const [fileSections, setFileSections] = useState([{ type: '', file: null, fileName: '' }]);
  const [dialogIndex, setDialogIndex] = useState(null);

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

  const handleRadioChange = (index, value) => {
    const updated = [...fileSections];
    updated[index].type = value;
    updated[index].file = null;
    updated[index].fileName = '';
    setFileSections(updated);
  };

  const handleFileUpload = (index, file) => {
    const updated = [...fileSections];
    updated[index].file = file;
    updated[index].fileName = file.name;
    setFileSections(updated);
  };

  const openDialog = (index) => setDialogIndex(index);
  const closeDialog = () => setDialogIndex(null);

  const addFileSection = () => setFileSections([...fileSections, { type: '', file: null, fileName: '' }]);
  const removeFileSection = (index) => setFileSections(fileSections.filter((_, i) => i !== index));

  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
    } else if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
    } else if (selectedTypes.includes('PSCRF Data') && selectedIds.length === 0) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
    } else if (
      selectedTypes.includes('Unsigned Approved Contract') &&
      fileSections.some((sec) => !sec.type || !sec.file)
    ) {
      setValidationMsg('Please ensure all file sections have a type selected and a file uploaded.');
    } else {
      setValidationMsg('');
    }
  }, [selectedTypes, selectedCompareDirection, selectedIds, fileSections]);

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      {/* Sticky Header */}
      <Box position="sticky" top={0} bgcolor="white" zIndex={2} pb={2}>
        {/* Type Buttons */}
        <Typography variant="h6" gutterBottom>
          Type
        </Typography>
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

        {/* Compare Direction */}
        <Typography variant="h6" gutterBottom mt={4}>
          Compare Direction
        </Typography>
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
      </Box>

      {/* Autocomplete */}
      {selectedTypes.includes('PSCRF Data') && (
        <Box>
          <Autocomplete
            options={dropdownOptions}
            getOptionLabel={(option) => option.id}
            filterSelectedOptions
            onChange={(e, newValue) => setSelectedIds(newValue)}
            multiple
            value={selectedIds}
            renderInput={(params) => (
              <TextField {...params} label="Search and select IDs" placeholder="Type to search..." />
            )}
            sx={{ mb: 3 }}
          />
          {selectedIds.length === 0 ? (
            <Typography color="text.secondary" textAlign="center">
              No IDs selected
            </Typography>
          ) : (
            <Grid container spacing={2}>
              {selectedIds.map((option) => (
                <Grid key={option.id} item xs={12} sm={6} md={4}>
                  <Paper elevation={3} sx={{ p: 2, borderLeft: `5px solid ${cignaBlue}` }}>
                    <Box>
                      <Typography variant="subtitle1" fontWeight="bold">
                        {option.id}
                      </Typography>
                      <Typography variant="body2">SAM Version: {option.samVersion}</Typography>
                      <Typography variant="body2">Pricing Version: {option.pricingVersion}</Typography>
                    </Box>
                    <IconButton onClick={() => handleRemoveId(option.id)} size="small">
                      <CloseIcon />
                    </IconButton>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          )}
        </Box>
      )}

      {/* File Uploads */}
      {selectedTypes.includes('Unsigned Approved Contract') && (
        <Box mt={4}>
          {fileSections.map((section, index) => (
            <Paper key={index} sx={{ p: 2, mb: 2, position: 'relative', borderLeft: `5px solid ${cignaBlue}` }}>
              {index > 0 && (
                <IconButton
                  onClick={() => removeFileSection(index)}
                  size="small"
                  sx={{ position: 'absolute', top: 8, right: 8 }}
                >
                  <CloseIcon />
                </IconButton>
              )}
              <RadioGroup
                row
                value={section.type}
                onChange={(e) => handleRadioChange(index, e.target.value)}
              >
                {fileTypes.map((type) => (
                  <FormControlLabel
                    key={type}
                    value={type}
                    control={<Radio sx={{ color: cignaBlue, '&.Mui-checked': { color: cignaBlue } }} />}
                    label={type}
                  />
                ))}
              </RadioGroup>
              <Box mt={2} display="flex" alignItems="center" gap={2}>
                <Button
                  variant="contained"
                  color="primary"
                  startIcon={<UploadFileIcon />}
                  onClick={() => openDialog(index)}
                >
                  {section.fileName ? section.fileName : 'Choose File'}
                </Button>
              </Box>
            </Paper>
          ))}
          <Button
            onClick={addFileSection}
            variant="outlined"
            startIcon={<AddIcon />}
            sx={{ color: cignaBlue, borderColor: cignaBlue }}
          >
            Add
          </Button>
        </Box>
      )}

      {/* File Upload Dialog */}
      <Dialog open={dialogIndex !== null} onClose={closeDialog}>
        <DialogTitle>Select File</DialogTitle>
        <DialogContent>
          <input
            type="file"
            accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            onChange={(e) => {
              if (e.target.files[0]) handleFileUpload(dialogIndex, e.target.files[0]);
              closeDialog();
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={closeDialog}>Cancel</Button>
        </DialogActions>
      </Dialog>

      {/* Validation */}
      {validationMsg && (
        <Typography color="error" mt={3} textAlign="center" fontWeight="bold">
          {validationMsg}
        </Typography>
      )}
    </Container>
  );
}

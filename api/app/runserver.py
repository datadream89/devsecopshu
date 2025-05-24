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
  RadioGroup,
  FormControlLabel,
  Radio,
  Modal,
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AddIcon from '@mui/icons-material/Add';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import dropdownOptions from './data/options.json'; // Your JSON with samVersion and pricingVersion

const cignaBlue = '#004785';

const typeButtons = [
  'PSCRF Data',
  'Unsigned Approved Contract',
  'Signed Client Contract',
];

const compareDirectionButtons = ['One-Way', 'Bi-Directional'];

const UploadModal = ({ open, onClose, onUpload }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUpload(file);
      onClose();
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 400,
          bgcolor: 'background.paper',
          border: '2px solid #000',
          boxShadow: 24,
          p: 4,
        }}
      >
        <Typography variant="h6" mb={2}>
          Upload File
        </Typography>
        <Button
          component="label"
          variant="contained"
          startIcon={<AttachFileIcon />}
          sx={{ backgroundColor: '#4caf50', color: '#fff' }}
        >
          Choose File
          <input type="file" hidden onChange={handleFileChange} />
        </Button>
      </Box>
    </Modal>
  );
};

export default function IntegratedUI() {
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [selectedCompareDirection, setSelectedCompareDirection] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [validationMsg, setValidationMsg] = useState('');
  const [contractSections, setContractSections] = useState([
    { id: Date.now(), type: '', file: null },
  ]);
  const [signedContractSections, setSignedContractSections] = useState([
    { id: Date.now() + 1, type: '', file: null },
  ]);
  const [modalOpenFor, setModalOpenFor] = useState(null);
  const [submitMsg, setSubmitMsg] = useState('');

  // Toggle Type buttons
  const toggleTypeButton = (label) => {
    setSelectedTypes((prev) =>
      prev.includes(label) ? prev.filter((item) => item !== label) : [...prev, label]
    );
  };

  // Select compare direction button
  const selectCompareDirectionButton = (label) => {
    setSelectedCompareDirection(label);
  };

  // Validation check on changes
  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
      setSubmitMsg('');
    } else if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
      setSubmitMsg('');
    } else if (selectedTypes.includes('PSCRF Data') && selectedIds.length === 0) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
      setSubmitMsg('');
    } else if (
      selectedTypes.includes('Unsigned Approved Contract') &&
      contractSections.some((s) => !s.file || !s.type)
    ) {
      setValidationMsg('Please select type and upload a file for each Unsigned Approved Contract section.');
      setSubmitMsg('');
    } else if (
      selectedTypes.includes('Signed Client Contract') &&
      signedContractSections.some((s) => !s.file || !s.type)
    ) {
      setValidationMsg('Please select type and upload a file for each Signed Client Contract section.');
      setSubmitMsg('');
    } else {
      setValidationMsg('');
    }
  }, [selectedTypes, selectedCompareDirection, selectedIds, contractSections, signedContractSections]);

  // Handle radio changes in contract sections
  const handleRadioChange = (id, value, setter) => {
    setter((prev) =>
      prev.map((s) => (s.id === id ? { ...s, type: value, file: null } : s))
    );
  };

  // Handle file upload (for both contract and signed contract)
  const handleFileUpload = (file) => {
    setContractSections((prev) =>
      prev.map((s) => (s.id === modalOpenFor ? { ...s, file } : s))
    );
    setSignedContractSections((prev) =>
      prev.map((s) => (s.id === modalOpenFor ? { ...s, file } : s))
    );
    setModalOpenFor(null);
  };

  // Add section
  const addSection = (setter) => {
    setter((prev) => [...prev, { id: Date.now(), type: '', file: null }]);
  };

  // Remove section
  const removeSection = (id, setter) => {
    setter((prev) => prev.filter((s) => s.id !== id));
  };

  // Remove selected PSCRF ID
  const removeSelectedId = (id) => {
    setSelectedIds((prev) => prev.filter((option) => option.id !== id));
  };

  // Render contract sections with vertical + and x buttons top-right
  const renderSections = (sections, setter) => (
    <Box mt={4}>
      {sections.map((section, idx) => (
        <Paper
          key={section.id}
          sx={{
            p: 2,
            mb: 2,
            position: 'relative',
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
          }}
        >
          {/* Add (+) and Remove (x) buttons vertically aligned top-right */}
          <Box
            sx={{
              position: 'absolute',
              top: 8,
              right: 8,
              display: 'flex',
              flexDirection: 'column',
              gap: 1,
            }}
          >
            <IconButton
              onClick={() => addSection(setter)}
              size="small"
              aria-label="Add Section"
            >
              <AddIcon />
            </IconButton>

            {idx > 0 && (
              <IconButton
                onClick={() => removeSection(section.id, setter)}
                size="small"
                aria-label="Remove Section"
              >
                <CloseIcon />
              </IconButton>
            )}
          </Box>

          {/* Radio buttons */}
          <RadioGroup
            row
            value={section.type}
            onChange={(e) => handleRadioChange(section.id, e.target.value, setter)}
            sx={{ mt: 1 }}
          >
            {['Agreement', 'Supplement', 'Addendum'].map((type) => (
              <FormControlLabel
                key={type}
                value={type}
                control={<Radio />}
                label={type}
                sx={{ m: 0, mr: 2 }}
              />
            ))}
          </RadioGroup>

          {/* Upload file button */}
          <Box display="flex" alignItems="center" gap={2}>
            <Button
              variant="outlined"
              onClick={() => setModalOpenFor(section.id)}
              startIcon={<UploadFileIcon />}
              sx={{
                color: '#673ab7',
                borderColor: '#673ab7',
                textTransform: 'none',
                fontWeight: 'bold',
                ':hover': { backgroundColor: '#ede7f6', borderColor: '#673ab7' },
              }}
            >
              {section.file ? section.file.name : 'Upload File'}
            </Button>
          </Box>
        </Paper>
      ))}
    </Box>
  );

  // Handle submit
  const handleSubmit = () => {
    if (!validationMsg) {
      setSubmitMsg('Submitted successfully request');
    } else {
      setSubmitMsg('');
      alert(validationMsg);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, pb: 4 }}>
      {/* Type Buttons */}
      <Typography variant="h5" gutterBottom fontWeight="bold" mb={3}>
        Select Types
      </Typography>
      <Box display="flex" justifyContent="center" gap={2} flexWrap="wrap" mb={4}>
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
      <Typography variant="h5" gutterBottom fontWeight="bold" mb={3}>
        Compare Direction
      </Typography>
      <Box display="flex" justifyContent="center" gap={2} flexWrap="wrap" mb={4}>
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

      {/* PSCRF Data Section */}
      {selectedTypes.includes('PSCRF Data') && (
        <Box mb={4}>
          <Autocomplete
            options={dropdownOptions}
            getOptionLabel={(option) =>
              `${option.pscrfId} (Sam: ${option.samVersion}, Pricing: ${option.pricingVersion})`
            }
            value={null}
            onChange={(event, newValue) => {
              if (newValue && !selectedIds.find((opt) => opt.id === newValue.id)) {
                setSelectedIds((prev) => [...prev, newValue]);
              }
            }}
            renderInput={(params) => (
              <TextField {...params} label="Select PSCRF ID" variant="outlined" />
            )}
            isOptionEqualToValue={(option, value) => option.id === value.id}
            sx={{ mb: 2 }}
          />

          {/* Selected IDs as cards with X button */}
          <Grid container spacing={2}>
            {selectedIds.map((option) => (
              <Grid item key={option.id}>
                <Paper
                  sx={{
                    p: 1,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                    minWidth: 200,
                    position: 'relative',
                    bgcolor: '#e0e0e0',
                  }}
                >
                  <Box>
                    <Typography variant="body1" fontWeight="bold">
                      {option.pscrfId}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Sam: {option.samVersion} | Pricing: {option.pricingVersion}
                    </Typography>
                  </Box>
                  <IconButton
                    size="small"
                    sx={{ position: 'absolute', top: 0, right: 0 }}
                    onClick={() => removeSelectedId(option.id)}
                    aria-label="Remove ID"
                  >
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* Unsigned Approved Contract Sections */}
      {selectedTypes.includes('Unsigned Approved Contract') && (
        <>
          <Typography variant="h5" gutterBottom fontWeight="bold" mt={4}>
            Unsigned Approved Contract Sections
          </Typography>
          {renderSections(contractSections, setContractSections)}
        </>
      )}

      {/* Signed Client Contract Sections */}
      {selectedTypes.includes('Signed Client Contract') && (
        <>
          <Typography variant="h5" gutterBottom fontWeight="bold" mt={4}>
            Signed Client Contract Sections
          </Typography>
          {renderSections(signedContractSections, setSignedContractSections)}
        </>
      )}

      {/* Submit and validation message */}
      <Box mt={4} textAlign="center">
        <Button
          variant="contained"
          onClick={handleSubmit}
          sx={{
            backgroundColor: cignaBlue,
            color: 'white',
            minWidth: 160,
            fontWeight: 'bold',
            textTransform: 'none',
            '&:hover': { backgroundColor: '#003666' },
          }}
          disabled={!!validationMsg}
        >
          Submit
        </Button>
        {validationMsg && (
          <Typography color="error" mt={2}>
            {validationMsg}
          </Typography>
        )}
        {submitMsg && (
          <Typography color="success.main" mt={2} fontWeight="bold">
            {submitMsg}
          </Typography>
        )}
      </Box>

      {/* Upload Modal */}
      <UploadModal
        open={!!modalOpenFor}
        onClose={() => setModalOpenFor(null)}
        onUpload={handleFileUpload}
      />
    </Container>
  );
}

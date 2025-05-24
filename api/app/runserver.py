import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
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
import dropdownOptions from './data/options.json'; // Your JSON options here

const cignaBlue = '#004785';

const typeButtons = [
  'PSCRF Data',
  'Unsigned Approved Contract',
  'Signed Client Contract',
];

const compareDirectionButtons = ['One-Way', 'Bi-Directional'];

// Incrementing request id stored in module-level variable
let requestCounter = 1;

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
          borderRadius: 1,
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

export default function Request() {
  const router = useRouter();

  const [selectedTypes, setSelectedTypes] = useState([]);
  const [selectedCompareDirection, setSelectedCompareDirection] = useState('');
  const [selectedIds, setSelectedIds] = useState([]);
  const [contractSections, setContractSections] = useState([
    { id: Date.now(), type: '', file: null },
  ]);
  const [signedContractSections, setSignedContractSections] = useState([
    { id: Date.now() + 1, type: '', file: null },
  ]);
  const [modalOpenFor, setModalOpenFor] = useState(null);
  const [validationMsg, setValidationMsg] = useState('');

  // Toggle types
  const toggleTypeButton = (label) => {
    setSelectedTypes((prev) =>
      prev.includes(label) ? prev.filter((i) => i !== label) : [...prev, label]
    );
  };

  // Select compare direction
  const selectCompareDirectionButton = (label) => {
    setSelectedCompareDirection(label);
  };

  // Validation
  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
      return;
    }
    if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
      return;
    }
    if (selectedTypes.includes('PSCRF Data') && selectedIds.length === 0) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
      return;
    }
    if (
      selectedTypes.includes('Unsigned Approved Contract') &&
      contractSections.some((s) => !s.file || !s.type)
    ) {
      setValidationMsg('Please select type and upload file for each Unsigned Approved Contract section.');
      return;
    }
    if (
      selectedTypes.includes('Signed Client Contract') &&
      signedContractSections.some((s) => !s.file || !s.type)
    ) {
      setValidationMsg('Please select type and upload file for each Signed Client Contract section.');
      return;
    }
    setValidationMsg('');
  }, [selectedTypes, selectedCompareDirection, selectedIds, contractSections, signedContractSections]);

  // Change contract section type
  const handleRadioChange = (id, value, setter) => {
    setter((prev) =>
      prev.map((s) => (s.id === id ? { ...s, type: value, file: null } : s))
    );
  };

  // File upload for contracts (both types)
  const handleFileUpload = (file) => {
    setContractSections((prev) =>
      prev.map((s) => (s.id === modalOpenFor ? { ...s, file } : s))
    );
    setSignedContractSections((prev) =>
      prev.map((s) => (s.id === modalOpenFor ? { ...s, file } : s))
    );
  };

  // Add contract section
  const addSection = (setter) => {
    setter((prev) => [...prev, { id: Date.now(), type: '', file: null }]);
  };

  // Remove contract section
  const removeSection = (id, setter) => {
    setter((prev) => prev.filter((s) => s.id !== id));
  };

  // Remove selected PSCRF ID
  const removeSelectedId = (idToRemove) => {
    setSelectedIds((prev) => prev.filter((item) => item.id !== idToRemove));
  };

  // Render contract sections UI
  const renderSections = (sections, setter) => (
    <Box mt={4}>
      {sections.map((section, idx) => (
        <Paper key={section.id} sx={{ p: 2, mb: 2, position: 'relative' }}>
          <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap">
            <RadioGroup
              row
              value={section.type}
              onChange={(e) => handleRadioChange(section.id, e.target.value, setter)}
              sx={{ flexGrow: 1, minWidth: 200 }}
            >
              {['Agreement', 'Supplement', 'Addendum'].map((type) => (
                <FormControlLabel
                  key={type}
                  value={type}
                  control={<Radio />}
                  label={type}
                />
              ))}
            </RadioGroup>

            <Box display="flex" flexDirection="column" alignItems="center" gap={1} ml={2} mb={1}>
              <IconButton
                onClick={() => addSection(setter)}
                size="small"
                aria-label="Add Section"
                sx={{ alignSelf: 'flex-start' }}
              >
                <AddIcon />
              </IconButton>
              {idx > 0 && (
                <IconButton
                  onClick={() => removeSection(section.id, setter)}
                  size="small"
                  aria-label="Remove Section"
                  sx={{ alignSelf: 'flex-start' }}
                >
                  <CloseIcon />
                </IconButton>
              )}
            </Box>
          </Box>

          <Box display="flex" alignItems="center" mt={2} gap={2} flexWrap="wrap">
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
                minWidth: 150,
              }}
            >
              {section.file ? section.file.name : 'Upload File'}
            </Button>
          </Box>
        </Paper>
      ))}
    </Box>
  );

  // Submit handler
  const handleSubmit = (e) => {
    e.preventDefault();

    if (validationMsg) {
      alert(validationMsg);
      return;
    }

    const pscrfIdString = selectedIds.map((i) => i.id).join('|');
    const pscrfIds = pscrfIdString.split('|');
    const timestamp = new Date().toISOString();
    const requestId = requestCounter++;

    // Build results array as requested
    const results = pscrfIds.map((id) => ({
      pscrfId: id,
      requestId,
      status: 'complete',
      timestamp,
    }));

    // Redirect with results in query string (stringified JSON)
    router.push({
      pathname: '/results',
      query: { data: JSON.stringify(results) },
    });
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, pb: 4 }}>
      <Typography variant="h4" gutterBottom fontWeight="bold" mb={3}>
        Request Form
      </Typography>

      {/* PSCRF ID Multi-select */}
      <Autocomplete
        multiple
        options={dropdownOptions}
        getOptionLabel={(option) => option.label}
        value={selectedIds}
        onChange={(event, newValue) => setSelectedIds(newValue)}
        renderInput={(params) => (
          <TextField {...params} label="Select PSCRF IDs" placeholder="Choose PSCRF IDs" />
        )}
        sx={{ mb: 4 }}
      />

      {/* Display selected PSCRF IDs with remove button */}
      <Box sx={{ mb: 4 }}>
        {selectedIds.map((item) => (
          <Paper
            key={item.id}
            sx={{
              display: 'inline-flex',
              alignItems: 'center',
              mr: 1,
              mb: 1,
              p: '4px 8px',
              borderRadius: 1,
              backgroundColor: '#e3f2fd',
            }}
          >
            <Typography variant="body2" mr={1}>
              {item.label}
            </Typography>
            <IconButton
              size="small"
              onClick={() => removeSelectedId(item.id)}
              aria-label="Remove ID"
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Paper>
        ))}
      </Box>

      {/* Type selection (multi toggle) */}
      <Box mb={4}>
        <Typography variant="h6" mb={1}>
          Select Types (min 2)
        </Typography>
        <Box display="flex" gap={2} flexWrap="wrap">
          {typeButtons.map((label) => (
            <Button
              key={label}
              variant={selectedTypes.includes(label) ? 'contained' : 'outlined'}
              onClick={() => toggleTypeButton(label)}
              sx={{
                backgroundColor: selectedTypes.includes(label) ? cignaBlue : 'inherit',
                color: selectedTypes.includes(label) ? '#fff' : cignaBlue,
                textTransform: 'none',
                fontWeight: 'bold',
                minWidth: 180,
                '&:hover': {
                  backgroundColor: selectedTypes.includes(label) ? '#003d72' : '#cfe3f6',
                },
              }}
            >
              {label}
            </Button>
          ))}
        </Box>
      </Box>

      {/* Compare Direction (single select) */}
      <Box mb={4}>
        <Typography variant="h6" mb={1}>
          Compare Direction (select one)
        </Typography>
        <Box display="flex" gap={2} flexWrap="wrap">
          {compareDirectionButtons.map((label) => (
            <Button
              key={label}
              variant={selectedCompareDirection === label ? 'contained' : 'outlined'}
              onClick={() => selectCompareDirectionButton(label)}
              sx={{
                backgroundColor: selectedCompareDirection === label ? cignaBlue : 'inherit',
                color: selectedCompareDirection === label ? '#fff' : cignaBlue,
                textTransform: 'none',
                fontWeight: 'bold',
                minWidth: 120,
                '&:hover': {
                  backgroundColor: selectedCompareDirection === label ? '#003d72' : '#cfe3f6',
                },
              }}
            >
              {label}
            </Button>
          ))}
        </Box>
      </Box>

      {/* Contract Sections for Unsigned Approved Contract */}
      {selectedTypes.includes('Unsigned Approved Contract') && (
        <>
          <Typography variant="h6" mb={2}>
            Unsigned Approved Contract Sections
          </Typography>
          {renderSections(contractSections, setContractSections)}
        </>
      )}

      {/* Contract Sections for Signed Client Contract */}
      {selectedTypes.includes('Signed Client Contract') && (
        <>
          <Typography variant="h6" mb={2} mt={4}>
            Signed Client Contract Sections
          </Typography>
          {renderSections(signedContractSections, setSignedContractSections)}
        </>
      )}

      {/* Validation Message */}
      {validationMsg && (
        <Typography color="error" mt={2} mb={2}>
          {validationMsg}
        </Typography>
      )}

      {/* Submit Button */}
      <Box textAlign="center" mt={4}>
        <Button
          variant="contained"
          size="large"
          onClick={handleSubmit}
          disabled={!!validationMsg}
          sx={{
            backgroundColor: cignaBlue,
            color: '#fff',
            fontWeight: 'bold',
            px: 6,
            ':hover': { backgroundColor: '#003d72' },
          }}
        >
          Submit
        </Button>
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

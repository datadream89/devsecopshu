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
import dropdownOptions from './data/options.json';

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

  const toggleTypeButton = (label) => {
    setSelectedTypes((prev) =>
      prev.includes(label) ? prev.filter((item) => item !== label) : [...prev, label]
    );
  };

  const selectCompareDirectionButton = (label) => {
    setSelectedCompareDirection(label);
  };

  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
    } else if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
    } else if (selectedTypes.includes('PSCRF Data') && selectedIds.length === 0) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
    } else if (
      selectedTypes.includes('Unsigned Approved Contract') &&
      contractSections.some((s) => !s.file || !s.type)
    ) {
      setValidationMsg('Please select type and upload a file for each Unsigned Approved Contract section.');
    } else if (
      selectedTypes.includes('Signed Client Contract') &&
      signedContractSections.some((s) => !s.file || !s.type)
    ) {
      setValidationMsg('Please select type and upload a file for each Signed Client Contract section.');
    } else {
      setValidationMsg('');
    }
  }, [selectedTypes, selectedCompareDirection, selectedIds, contractSections, signedContractSections]);

  const handleRadioChange = (id, value, setter) => {
    setter((prev) =>
      prev.map((s) => (s.id === id ? { ...s, type: value, file: null } : s))
    );
  };

  const handleFileUpload = (file) => {
    setContractSections((prev) =>
      prev.map((s) => (s.id === modalOpenFor ? { ...s, file } : s))
    );
    setSignedContractSections((prev) =>
      prev.map((s) => (s.id === modalOpenFor ? { ...s, file } : s))
    );
  };

  const addSection = (setter) => {
    setter((prev) => [...prev, { id: Date.now(), type: '', file: null }]);
  };

  const removeSection = (id, setter) => {
    setter((prev) => prev.filter((s) => s.id !== id));
  };

  const renderSections = (sections, setter) => (
    <Box mt={4}>
      {sections.map((section, idx) => (
        <Paper key={section.id} sx={{ p: 2, mb: 2, position: 'relative' }}>
          <Box display="flex" justifyContent="space-between" alignItems="flex-start">
            <RadioGroup
              row
              value={section.type}
              onChange={(e) => handleRadioChange(section.id, e.target.value, setter)}
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
            <Box sx={{ position: 'relative', width: 36, height: 36 }}>
              <IconButton
                onClick={() => addSection(setter)}
                sx={{ position: 'absolute', top: 0, right: 0 }}
                size="small"
                aria-label="Add Section"
              >
                <AddIcon />
              </IconButton>
            </Box>
          </Box>
          <Box display="flex" alignItems="center" mt={2} gap={2}>
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
          {idx > 0 && (
            <IconButton
              onClick={() => removeSection(section.id, setter)}
              sx={{ position: 'absolute', top: 8, right: 8 }}
              size="small"
              aria-label="Remove Section"
            >
              <CloseIcon />
            </IconButton>
          )}
        </Paper>
      ))}
    </Box>
  );

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
      <Typography variant="h5" gutterBottom fontWeight="bold" mb={3}>
        PSCRF Data
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

      {selectedTypes.includes('PSCRF Data') && (
        <Box mb={4}>
          <Autocomplete
            options={dropdownOptions}
            getOptionLabel={(option) => option.id}
            filterSelectedOptions
            onChange={(e, newValue) => setSelectedIds(newValue)}
            multiple
            value={selectedIds}
            renderInput={(params) => (
              <TextField {...params} label="Search and select IDs" variant="outlined" />
            )}
          />

          {/* Cards showing selected IDs and versions */}
          <Grid container spacing={2} mt={2}>
            {selectedIds.map((item) => (
              <Grid item xs={12} sm={4} key={item.id}>
                <Paper sx={{ p: 2 }}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    ID: {item.id}
                  </Typography>
                  <Typography variant="body2">Version: {item.version || 'N/A'}</Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {selectedTypes.includes('Unsigned Approved Contract') && (
        <>
          <Typography variant="h5" gutterBottom fontWeight="bold" mb={2}>
            Unsigned Approved Contract
          </Typography>
          {renderSections(contractSections, setContractSections)}
        </>
      )}

      {selectedTypes.includes('Signed Client Contract') && (
        <>
          <Typography variant="h5" gutterBottom fontWeight="bold" mb={2}>
            Signed Client Contract
          </Typography>
          {renderSections(signedContractSections, setSignedContractSections)}
        </>
      )}

      {validationMsg && (
        <Typography color="error" mt={3} textAlign="center" fontWeight="bold">
          {validationMsg}
        </Typography>
      )}

      {submitMsg && (
        <Typography color="success.main" mt={3} textAlign="center" fontWeight="bold">
          {submitMsg}
        </Typography>
      )}

      <Box display="flex" justifyContent="center" mt={4}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          sx={{ minWidth: 160, fontWeight: 'bold' }}
        >
          Submit
        </Button>
      </Box>

      <UploadModal
        open={!!modalOpenFor}
        onClose={() => setModalOpenFor(null)}
        onUpload={handleFileUpload}
      />
    </Container>
  );
}

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
          Choose and Upload File
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
  const [modalOpenFor, setModalOpenFor] = useState(null);

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

  useEffect(() => {
    if (selectedTypes.length < 2) {
      setValidationMsg('Select at least 2 Types.');
    } else if (!selectedCompareDirection) {
      setValidationMsg('Select one Compare Direction.');
    } else if (selectedTypes.includes('PSCRF Data') && selectedIds.length === 0) {
      setValidationMsg('Please select at least one ID when PSCRF Data is selected.');
    } else if (
      selectedTypes.includes('Unsigned Approved Contract') &&
      contractSections.some((s) => !s.file)
    ) {
      setValidationMsg('Please upload a file for each contract section.');
    } else {
      setValidationMsg('');
    }
  }, [selectedTypes, selectedCompareDirection, selectedIds, contractSections]);

  const handleRadioChange = (id, value) => {
    setContractSections((prev) =>
      prev.map((s) =>
        s.id === id ? { ...s, type: value, file: null } : s
      )
    );
  };

  const handleFileUpload = (file) => {
    setContractSections((prev) =>
      prev.map((s) =>
        s.id === modalOpenFor ? { ...s, file } : s
      )
    );
  };

  const addContractSection = () => {
    setContractSections((prev) => [
      ...prev,
      { id: Date.now(), type: '', file: null },
    ]);
  };

  const removeContractSection = (id) => {
    setContractSections((prev) => prev.filter((s) => s.id !== id));
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h6" gutterBottom>
        Type
      </Typography>
      <Box display="flex" justifyContent="center" gap={2} flexWrap="wrap">
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

      <Typography variant="h6" gutterBottom mt={4}>
        Compare Direction
      </Typography>
      <Box display="flex" justifyContent="center" gap={2} flexWrap="wrap">
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
        <Box mt={4}>
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
        </Box>
      )}

      {selectedTypes.includes('Unsigned Approved Contract') && (
        <Box mt={4}>
          {contractSections.map((section, idx) => (
            <Paper key={section.id} sx={{ p: 2, mb: 2, position: 'relative' }}>
              <Box display="flex" justifyContent="space-between" alignItems="flex-start">
                <RadioGroup
                  row
                  value={section.type}
                  onChange={(e) => handleRadioChange(section.id, e.target.value)}
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
                <Box>
                  <IconButton onClick={addContractSection}>
                    <AddIcon />
                  </IconButton>
                </Box>
              </Box>
              <Box display="flex" alignItems="center" mt={2} gap={2}>
                {section.file ? (
                  <Typography variant="body2" color="text.secondary">
                    {section.file.name}
                  </Typography>
                ) : (
                  <Button
                    variant="outlined"
                    onClick={() => setModalOpenFor(section.id)}
                    startIcon={<UploadFileIcon />}
                    sx={{ color: '#673ab7', borderColor: '#673ab7' }}
                  >
                    Upload File
                  </Button>
                )}
              </Box>
              {idx > 0 && (
                <IconButton
                  onClick={() => removeContractSection(section.id)}
                  sx={{ position: 'absolute', top: 8, right: 40 }}
                >
                  <CloseIcon />
                </IconButton>
              )}
            </Paper>
          ))}
        </Box>
      )}

      {validationMsg && (
        <Typography color="error" mt={3} textAlign="center" fontWeight="bold">
          {validationMsg}
        </Typography>
      )}

      <UploadModal
        open={!!modalOpenFor}
        onClose={() => setModalOpenFor(null)}
        onUpload={handleFileUpload}
      />
    </Container>
  );
}

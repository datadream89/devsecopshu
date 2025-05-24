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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
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
  const [submitted, setSubmitted] = useState(false);
  const [submissionData, setSubmissionData] = useState([]);

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
      setValidationMsg('Please upload a file for each Unsigned Approved Contract section.');
    } else if (
      selectedTypes.includes('Signed Client Contract') &&
      signedContractSections.some((s) => !s.file)
    ) {
      setValidationMsg('Please upload a file for each Signed Client Contract section.');
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
    if (!modalOpenFor) return;
    const { id, type } = modalOpenFor;
    if (type === 'Unsigned Approved Contract') {
      setContractSections((prev) =>
        prev.map((s) => (s.id === id ? { ...s, file } : s))
      );
    } else if (type === 'Signed Client Contract') {
      setSignedContractSections((prev) =>
        prev.map((s) => (s.id === id ? { ...s, file } : s))
      );
    }
  };

  const addSection = (setter) => {
    setter((prev) => [...prev, { id: Date.now(), type: '', file: null }]);
  };

  const removeSection = (id, setter) => {
    setter((prev) => prev.filter((s) => s.id !== id));
  };

  const renderSections = (sections, setter, sectionTitle) => (
    <Box mt={4}>
      <Typography variant="h6" fontWeight="bold" mb={2}>
        {sectionTitle}
      </Typography>
      {sections.map((section, idx) => (
        <Paper key={section.id} sx={{ p: 2, mb: 2, position: 'relative' }}>
          <Box display="flex" justifyContent="space-between" gap={2}>
            <RadioGroup
              row
              value={section.type}
              onChange={(e) => handleRadioChange(section.id, e.target.value, setter)}
              sx={{ flexGrow: 1 }}
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

            <Box display="flex" flexDirection="column" alignItems="flex-end">
              <IconButton onClick={() => addSection(setter)} aria-label="Add section">
                <AddIcon />
              </IconButton>
              {idx > 0 && (
                <IconButton
                  onClick={() => removeSection(section.id, setter)}
                  aria-label="Remove section"
                >
                  <CloseIcon />
                </IconButton>
              )}
            </Box>
          </Box>

          <Box display="flex" alignItems="center" gap={2} mt={2}>
            <Button
              variant="outlined"
              onClick={() => setModalOpenFor({ id: section.id, type: sectionTitle })}
              startIcon={<UploadFileIcon />}
              sx={{
                color: '#673ab7',
                borderColor: '#673ab7',
                textTransform: 'none',
                fontWeight: 'bold',
                minWidth: 140,
                '&:hover': {
                  backgroundColor: '#673ab7',
                  color: '#fff',
                },
              }}
            >
              {section.file ? section.file.name : 'Upload File'}
            </Button>
          </Box>
        </Paper>
      ))}
    </Box>
  );

  const handleSubmit = () => {
    const newRequest = {
      pscrfId: selectedIds.map((id) => id.label).join(', '),
      requestId: 'REQ-' + Math.floor(Math.random() * 10000),
      status: 'C'
    };
    setSubmissionData((prev) => [...prev, newRequest]);
    setSubmitted(true);
  };

  const handleBack = () => {
    setSubmitted(false);
    setSelectedTypes([]);
    setSelectedCompareDirection('');
    setSelectedIds([]);
    setContractSections([{ id: Date.now(), type: '', file: null }]);
    setSignedContractSections([{ id: Date.now() + 1, type: '', file: null }]);
  };

  if (submitted) {
    return (
      <Container>
        <Typography variant="h5" mt={4} mb={2}>Request Submitted Successfully</Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>PSCRF ID</strong></TableCell>
                <TableCell><strong>Request ID</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {submissionData.map((row, index) => (
                <TableRow key={index}>
                  <TableCell>{row.pscrfId}</TableCell>
                  <TableCell>{row.requestId}</TableCell>
                  <TableCell>{row.status}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <Button variant="contained" onClick={handleBack} sx={{ mt: 3 }}>
          Submit New Request
        </Button>
      </Container>
    );
  }

  return (
    <Container>
      {/* UI elements and form inputs */}
      <Button
        variant="contained"
        onClick={handleSubmit}
        sx={{ mt: 4 }}
        disabled={!!validationMsg}
      >
        Submit
      </Button>
      {validationMsg && <Typography color="error" mt={2}>{validationMsg}</Typography>}
    </Container>
  );
}

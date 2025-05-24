import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Modal,
  Box,
  IconButton,
  Grid,
  ToggleButton,
  ToggleButtonGroup,
  RadioGroup,
  FormControlLabel,
  Radio,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';
import AttachFileIcon from '@mui/icons-material/AttachFile';

const contractTypes = ['Firm Fixed Price', 'Cost Plus Award Fee', 'Cost', 'Time & Material', 'Labor Hour'];

const PSCRFCard = ({ id, onUploadClick }) => (
  <Card
    sx={{ width: 260, m: 1, borderRadius: 3, boxShadow: 2, backgroundColor: '#f5f5f5' }}
    onClick={() => onUploadClick(id)}
  >
    <CardContent>
      <Typography variant="h6" fontWeight="bold">
        PSCRF ID: {id}
      </Typography>
      <Typography variant="subtitle1">SAM Version</Typography>
      <Typography variant="subtitle1">Pricing Version</Typography>
    </CardContent>
  </Card>
);

const ContractSection = ({ section, onRemove }) => (
  <Box
    sx={{
      display: 'flex',
      alignItems: 'center',
      gap: 2,
      mb: 1,
    }}
  >
    <Typography>{section}</Typography>
    <IconButton onClick={() => onRemove(section)} size="small">
      <CloseIcon fontSize="small" />
    </IconButton>
  </Box>
);

const UploadModal = ({ open, onClose, onUpload }) => {
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const validTypes = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      ];
      if (!validTypes.includes(file.type)) {
        setError('Only .pdf and .docx files are allowed.');
        return;
      }
      setError('');
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
          width: 360,
          bgcolor: 'background.paper',
          border: '2px solid #000',
          boxShadow: 24,
          p: 3,
        }}
      >
        <Typography variant="h6" mb={1}>
          Upload File
        </Typography>
        <Button
          component="label"
          variant="contained"
          startIcon={<AttachFileIcon />}
          sx={{ backgroundColor: '#4caf50', color: '#fff', textTransform: 'none' }}
        >
          Choose File (.pdf, .docx)
          <input type="file" hidden onChange={handleFileChange} accept=".pdf,.docx" />
        </Button>
        {error && (
          <Typography color="error" mt={1} fontSize="0.85rem">
            {error}
          </Typography>
        )}
      </Box>
    </Modal>
  );
};

const PSCRFUI = () => {
  const [selectedType, setSelectedType] = useState('sam');
  const [comparisonDirection, setComparisonDirection] = useState('sam_to_pricing');
  const [contractType, setContractType] = useState(contractTypes[0]);
  const [sections, setSections] = useState(['Section 1']);
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [currentPSCRFId, setCurrentPSCRFId] = useState(null);

  const handleAddSection = () => {
    const nextNum = sections.length + 1;
    setSections([...sections, `Section ${nextNum}`]);
  };

  const handleRemoveSection = (sectionToRemove) => {
    setSections(sections.filter((section) => section !== sectionToRemove));
  };

  const handleUploadClick = (id) => {
    setCurrentPSCRFId(id);
    setUploadModalOpen(true);
  };

  const handleFileUpload = (file) => {
    console.log(`File uploaded for PSCRF ID ${currentPSCRFId}:`, file);
  };

  return (
    <Box sx={{ p: 3, maxWidth: 900, mx: 'auto' }}>
      <Typography variant="h5" mb={2} fontWeight="bold">
        PSCRF Data Upload and Configuration
      </Typography>

      <Box display="flex" alignItems="center" gap={2} mb={2}>
        <Typography>Type:</Typography>
        <ToggleButtonGroup
          value={selectedType}
          exclusive
          onChange={(e, newType) => newType && setSelectedType(newType)}
          size="small"
        >
          <ToggleButton value="sam">SAM</ToggleButton>
          <ToggleButton value="pricing">Pricing</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      <Box display="flex" alignItems="center" gap={2} mb={2}>
        <Typography>Comparison:</Typography>
        <ToggleButtonGroup
          value={comparisonDirection}
          exclusive
          onChange={(e, newDir) => newDir && setComparisonDirection(newDir)}
          size="small"
        >
          <ToggleButton value="sam_to_pricing">SAM → Pricing</ToggleButton>
          <ToggleButton value="pricing_to_sam">Pricing → SAM</ToggleButton>
        </ToggleButtonGroup>
      </Box>

      <Box mb={2}>
        <Typography variant="subtitle1" fontWeight="medium" mb={1}>
          PSCRF IDs:
        </Typography>
        <Grid container spacing={1}>
          {[101, 102].map((id) => (
            <Grid item key={id}>
              <PSCRFCard id={id} onUploadClick={handleUploadClick} />
            </Grid>
          ))}
        </Grid>
      </Box>

      <Box mb={2}>
        <Typography variant="subtitle1" fontWeight="medium" mb={1}>
          Contract Type:
        </Typography>
        <RadioGroup
          row
          value={contractType}
          onChange={(e) => setContractType(e.target.value)}
        >
          {contractTypes.map((type) => (
            <FormControlLabel
              key={type}
              value={type}
              control={<Radio size="small" />}
              label={<Typography variant="body2">{type}</Typography>}
            />
          ))}
        </RadioGroup>
      </Box>

      <Box mb={2}>
        <Typography variant="subtitle1" fontWeight="medium" mb={1}>
          Sections:
        </Typography>
        {sections.map((section) => (
          <ContractSection key={section} section={section} onRemove={handleRemoveSection} />
        ))}
        <Button
          variant="outlined"
          startIcon={<AddIcon />}
          onClick={handleAddSection}
          size="small"
        >
          Add Section
        </Button>
      </Box>

      <UploadModal
        open={uploadModalOpen}
        onClose={() => setUploadModalOpen(false)}
        onUpload={handleFileUpload}
      />
    </Box>
  );
};

export default PSCRFUI;

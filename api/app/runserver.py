import React, { useState } from "react";
import {
  Box,
  Typography,
  Checkbox,
  IconButton,
  TextField,
  Autocomplete,
  Card,
  CardContent,
  RadioGroup,
  FormControlLabel,
  Radio,
  Button,
} from "@mui/material";
import {
  Add as AddIcon,
  Close as CloseIcon,
  Upload as UploadIcon,
  ExpandLess as ExpandLessIcon,
  ExpandMore as ExpandMoreIcon,
  ArrowBackIosNew,
  ArrowForwardIos,
} from "@mui/icons-material";

// ... (keep pscrfOptions and FILE_TYPES as before)

const PSCRFSection = ({ selectedOptions, onChange }) => {
  // Removed internal state - fully controlled by parent
  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white" minHeight={220}>
      <Autocomplete
        multiple
        options={pscrfOptions}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        value={selectedOptions}
        onChange={(event, value) => onChange(value)}
        renderInput={(params) => <TextField {...params} label="Select PSCRF" variant="outlined" />}
      />
      <Box display="flex" flexWrap="wrap" mt={2} gap={2} sx={{ maxHeight: 300, overflowY: "auto" }}>
        {selectedOptions.map((option, index) => (
          <Card key={index} sx={{ width: "48%", position: "relative", boxSizing: "border-box" }}>
            <CardContent sx={{ padding: "8px !important" }}>
              <Typography variant="body2" component="div" whiteSpace="normal">
                <strong>ID:</strong> {option.id}
                <br />
                <strong>SAM:</strong> {option.samVersion}
                <br />
                <strong>Pricing:</strong> {option.pricingVersion}
                <br />
                <strong>Client:</strong> {option.clientName}
              </Typography>
              <IconButton
                size="small"
                onClick={() => {
                  const newSelected = selectedOptions.filter((_, i) => i !== index);
                  onChange(newSelected);
                }}
                sx={{ position: "absolute", top: 4, right: 4 }}
                aria-label="remove card"
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

const ContractSection = ({ title, sections, setSections }) => {
  const handleAddSection = () => {
    setSections([
      ...sections,
      { id: Date.now() + Math.random(), type: "Agreement", file: null, filename: "" },
    ]);
  };

  const handleRemoveSection = (id) => {
    setSections(sections.filter((section) => section.id !== id));
  };

  const handleRadioChange = (id, type) => {
    setSections(
      sections.map((section) =>
        section.id === id ? { ...section, type, file: null, filename: "" } : section
      )
    );
  };

  const handleFileChange = (id, file) => {
    if (!file) return;
    if (!FILE_TYPES.includes(file.type)) {
      alert("Only PDF and Word files are allowed.");
      return;
    }
    setSections(
      sections.map((section) =>
        section.id === id ? { ...section, file, filename: file.name } : section
      )
    );
  };

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white" minHeight={220} sx={{ overflowY: "auto" }}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      {sections.map((section, idx) => (
        <Box
          key={section.id}
          display="flex"
          alignItems="center"
          gap={1}
          mt={idx === 0 ? 0 : 2}
          flexWrap="wrap"
          position="relative"
          border={1}
          borderColor="grey.200"
          borderRadius={1}
          p={1}
          bgcolor="#fafafa"
        >
          <RadioGroup
            row
            value={section.type}
            onChange={(e) => handleRadioChange(section.id, e.target.value)}
            sx={{ flexGrow: 1, minWidth: 240 }}
          >
            <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
            <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
            <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
          </RadioGroup>
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            style={{ display: "none" }}
            id={`upload-${section.id}`}
            onChange={(e) => handleFileChange(section.id, e.target.files[0])}
          />
          <label htmlFor={`upload-${section.id}`}>
            <IconButton component="span" title="Upload File">
              <UploadIcon />
            </IconButton>
          </label>
          <Typography
            sx={{
              fontSize: 12,
              maxWidth: 180,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
            title={section.filename}
          >
            {section.filename || "No file chosen"}
          </Typography>
          {sections.length > 1 && (
            <IconButton aria-label="remove section" onClick={() => handleRemoveSection(section.id)} sx={{ ml: 1 }}>
              <CloseIcon />
            </IconButton>
          )}
        </Box>
      ))}
      <Button startIcon={<AddIcon />} onClick={handleAddSection} size="small" sx={{ mt: 2 }}>
        Add Section
      </Button>
    </Box>
  );
};

// ... BidirectionalArrow and TitleBar components stay unchanged

const BoxPair = ({
  leftComponent,
  rightComponent,
  title,
  checked,
  onCheckChange,
  leftArrowSelected,
  rightArrowSelected,
  toggleLeftArrow,
  toggleRightArrow,
  expanded,
  toggleExpanded,
}) => {
  const leftBoxStyle = {
    opacity: checked ? 1 : 0.4,
    borderColor: leftArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };
  const rightBoxStyle = {
    opacity: checked ? 1 : 0.4,
    borderColor: rightArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };

  return (
    <Box mb={3}>
      <TitleBar title={title} expanded={expanded} toggleExpanded={toggleExpanded} checked={checked} onCheckChange={onCheckChange} />
      {expanded && (
        <Box display="flex" alignItems="center" gap={1}>
          <Box flex={1} border={1} borderRadius={2} sx={leftBoxStyle} minHeight={250} bgcolor="white">
            {leftComponent}
          </Box>
          <BidirectionalArrow
            leftSelected={leftArrowSelected}
            rightSelected={rightArrowSelected}
            onLeftClick={toggleLeftArrow}
            onRightClick={toggleRightArrow}
          />
          <Box flex={1} border={1} borderRadius={2} sx={rightBoxStyle} minHeight={250} bgcolor="white">
            {rightComponent}
          </Box>
        </Box>
      )}
    </Box>
  );
};

const ComparisonLayout = () => {
  // Track checkbox states
  const [rowChecks, setRowChecks] = useState([true, true, true, true]);

  // For validation, keep PSCRF selections and Contract sections lifted for each row and side
  // Row 0 left: PSCRFSection
  const [row0LeftSelected, setRow0LeftSelected] = useState([]);
  // Row 0 right: ContractSection
  const [row0RightSections, setRow0RightSections] = useState([
    { id: Date.now(), type: "Agreement", file: null, filename: "" },
  ]);

  // Row 1 left: ContractSection
  const [row1LeftSections, setRow1LeftSections] = useState([
    { id: Date.now(), type: "Agreement", file: null, filename: "" },
  ]);
  // Row 1 right: ContractSection
  const [row1RightSections, setRow1RightSections] = useState([
    { id: Date.now(), type: "Agreement", file: null, filename: "" },
  ]);

  // Row 2 left: ContractSection
  const [row2LeftSections, setRow2LeftSections] = useState([
    { id: Date.now(), type: "Agreement", file: null, filename: "" },
  ]);
  // Row 2 right: PSCRFSection
  const [row2RightSelected, setRow2RightSelected] = useState([]);

  // Row 3 left: PSCRFSection
  const [row3LeftSelected, setRow3LeftSelected] = useState([]);
  // Row 3 right: PSCRFSection
  const [row3RightSelected, setRow3RightSelected] = useState([]);

  const toggleRowCheck = (index) => {
    const newChecks = [...rowChecks];
    newChecks[index] = !newChecks[index];
    setRowChecks(newChecks);
  };

  // Validation funcs for each pair, only if checked
  // PSCRFSection valid if selectedOptions.length > 0
  // ContractSection valid if at least one section has file !== null

  const validatePSCRF = (selectedOptions) => selectedOptions.length > 0;

  const validateContract = (sections) => sections.some((sec) => sec.file !== null);

  // Validate pairs by index:
  const isRow0Valid = !rowChecks[0] || (validatePSCRF(row0LeftSelected) && validateContract(row0RightSections));
  const isRow1Valid = !rowChecks[1] || (validateContract(row1LeftSections) && validateContract(row1RightSections));
  const isRow2Valid = !rowChecks[2] || (validateContract(row2LeftSections) && validatePSCRF(row2RightSelected));
  const isRow3Valid = !rowChecks[3] || (validatePSCRF(row3LeftSelected) && validatePSCRF(row3RightSelected));

  const isFormValid = isRow0Valid && isRow1Valid && isRow2Valid && isRow3Valid;

  // For arrows and expansion states for each row, keep them local here:
  const [expandedStates, setExpandedStates] = useState([true, true, true, true]);
  const [leftArrowStates, setLeftArrowStates] = useState([false, false, false, false]);
  const [rightArrowStates, setRightArrowStates] = useState([false, false, false, false]);

  const toggleExpanded = (index) => {
    const newExpanded = [...expandedStates];
    newExpanded[index] = !newExpanded[index];
    setExpandedStates(newExpanded);
  };
  const toggleLeftArrow = (index) => {
    const newLeft = [...leftArrowStates];
    newLeft[index] = !newLeft[index];
    setLeftArrowStates(newLeft);
  };
  const toggleRightArrow = (index) => {
    const newRight = [...rightArrowStates];
    newRight[index] = !newRight[index];
    setRightArrowStates(newRight);
  };

  const handleSubmit = () => {
    alert("Submitted successfully!");
    // Add your submit logic here
  };

  return (
    <Box
      sx={{
        width: "95vw",
        maxWidth: 1200,
    margin: "auto",
    backgroundColor: "grey.100",
    borderRadius: 3,
    p: 3,
    overflowY: "auto",
    maxHeight: "90vh",
  }}
>
  <BoxPair
    title="Row 1"
    checked={rowChecks[0]}
    onCheckChange={() => toggleRowCheck(0)}
    leftArrowSelected={leftArrowStates[0]}
    rightArrowSelected={rightArrowStates[0]}
    toggleLeftArrow={() => toggleLeftArrow(0)}
    toggleRightArrow={() => toggleRightArrow(0)}
    expanded={expandedStates[0]}
    toggleExpanded={() => toggleExpanded(0)}
    leftComponent={
      <PSCRFSection selectedOptions={row0LeftSelected} onChange={setRow0LeftSelected} />
    }
    rightComponent={
      <ContractSection title="Contract Section Right" sections={row0RightSections} setSections={setRow0RightSections} />
    }
  />
  <BoxPair
    title="Row 2"
    checked={rowChecks[1]}
    onCheckChange={() => toggleRowCheck(1)}
    leftArrowSelected={leftArrowStates[1]}
    rightArrowSelected={rightArrowStates[1]}
    toggleLeftArrow={() => toggleLeftArrow(1)}
    toggleRightArrow={() => toggleRightArrow(1)}
    expanded={expandedStates[1]}
    toggleExpanded={() => toggleExpanded(1)}
    leftComponent={
      <ContractSection title="Contract Section Left" sections={row1LeftSections} setSections={setRow1LeftSections} />
    }
    rightComponent={
      <ContractSection title="Contract Section Right" sections={row1RightSections} setSections={setRow1RightSections} />
    }
  />
  <BoxPair
    title="Row 3"
    checked={rowChecks[2]}
    onCheckChange={() => toggleRowCheck(2)}
    leftArrowSelected={leftArrowStates[2]}
    rightArrowSelected={rightArrowStates[2]}
    toggleLeftArrow={() => toggleLeftArrow(2)}
    toggleRightArrow={() => toggleRightArrow(2)}
    expanded={expandedStates[2]}
    toggleExpanded={() => toggleExpanded(2)}
    leftComponent={
      <ContractSection title="Contract Section Left" sections={row2LeftSections} setSections={setRow2LeftSections} />
    }
    rightComponent={<PSCRFSection selectedOptions={row2RightSelected} onChange={setRow2RightSelected} />}
  />
  <BoxPair
    title="Row 4"
    checked={rowChecks[3]}
    onCheckChange={() => toggleRowCheck(3)}
    leftArrowSelected={leftArrowStates[3]}
    rightArrowSelected={rightArrowStates[3]}
    toggleLeftArrow={() => toggleLeftArrow(3)}
    toggleRightArrow={() => toggleRightArrow(3)}
    expanded={expandedStates[3]}
    toggleExpanded={() => toggleExpanded(3)}
    leftComponent={<PSCRFSection selectedOptions={row3LeftSelected} onChange={setRow3LeftSelected} />}
    rightComponent={<PSCRFSection selectedOptions={row3RightSelected} onChange={setRow3RightSelected} />}
  />

  <Box mt={3} display="flex" justifyContent="flex-end">
    <Button variant="contained" disabled={!isFormValid} onClick={handleSubmit}>
      Submit
    </Button>
  </Box>
</Box>
);

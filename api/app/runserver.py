import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  Button,
  Select,
  MenuItem,
  FormHelperText,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

const BidirectionalArrow = ({
  leftSelected,
  rightSelected,
  onLeftClick,
  onRightClick,
}) => (
  <Box
    display="flex"
    flexDirection="column"
    justifyContent="center"
    alignItems="center"
    mx={1}
  >
    <IconButton
      size="small"
      onClick={onLeftClick}
      sx={{ color: leftSelected ? "grey.800" : "grey.400" }}
      aria-label="Highlight left box"
    >
      <ArrowBackIcon />
    </IconButton>
    <IconButton
      size="small"
      onClick={onRightClick}
      sx={{ color: rightSelected ? "grey.800" : "grey.400" }}
      aria-label="Highlight right box"
    >
      <ArrowForwardIcon />
    </IconButton>
  </Box>
);

const TitleBar = ({ title, expanded, toggleExpanded }) => (
  <Box
    display="flex"
    alignItems="center"
    bgcolor="#f5f5f5"
    px={2}
    py={1}
    borderTop={1}
    borderBottom={1}
    borderColor="grey.400"
    mb={1}
    sx={{ userSelect: "none" }}
  >
    <Typography
      variant="subtitle1"
      flex={1}
      sx={{ userSelect: "none", fontWeight: 600 }}
    >
      {title}
    </Typography>
    <IconButton
      onClick={toggleExpanded}
      aria-label={expanded ? "Collapse section" : "Expand section"}
      size="small"
    >
      {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
    </IconButton>
  </Box>
);

const PSCRFSection = ({
  value,
  onChange,
  error,
  helperText,
}) => (
  <Box p={2}>
    <Select
      fullWidth
      multiple
      value={value}
      onChange={onChange}
      error={error}
      displayEmpty
      renderValue={(selected) =>
        selected.length === 0 ? "Select PSCRF IDs" : selected.join(", ")
      }
    >
      {/* Sample options */}
      <MenuItem value="PSCRF1">PSCRF1</MenuItem>
      <MenuItem value="PSCRF2">PSCRF2</MenuItem>
      <MenuItem value="PSCRF3">PSCRF3</MenuItem>
    </Select>
    {error && (
      <FormHelperText error sx={{ mt: 0.5 }}>
        {helperText}
      </FormHelperText>
    )}
  </Box>
);

const ContractSection = ({
  title,
  file,
  onFileUpload,
  error,
  helperText,
}) => (
  <Box p={2}>
    <Button
      variant="outlined"
      color={error ? "error" : "primary"}
      component="label"
    >
      Upload File
      <input
        type="file"
        hidden
        onChange={onFileUpload}
        accept="*"
      />
    </Button>
    {file && (
      <Typography variant="body2" mt={1}>
        {file.name}
      </Typography>
    )}
    {error && (
      <FormHelperText error sx={{ mt: 0.5 }}>
        {helperText}
      </FormHelperText>
    )}
  </Box>
);

const BoxPair = ({
  leftComponent,
  rightComponent,
  title,
  visible,
}) => {
  const [expanded, setExpanded] = useState(true);
  const [leftArrowSelected, setLeftArrowSelected] = useState(false);
  const [rightArrowSelected, setRightArrowSelected] = useState(false);

  if (!visible) return null;

  const toggleExpanded = () => setExpanded((v) => !v);
  const toggleLeftArrow = () => setLeftArrowSelected((v) => !v);
  const toggleRightArrow = () => setRightArrowSelected((v) => !v);

  const leftBoxStyle = {
    opacity: 1,
    borderColor: leftArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };
  const rightBoxStyle = {
    opacity: 1,
    borderColor: rightArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };

  return (
    <Box mb={3}>
      <TitleBar title={title} expanded={expanded} toggleExpanded={toggleExpanded} />
      {expanded && (
        <Box display="flex" alignItems="center" gap={1}>
          <Box
            flex={1}
            border={1}
            borderRadius={2}
            sx={leftBoxStyle}
            minHeight={250}
            bgcolor="white"
          >
            {leftComponent}
          </Box>
          <BidirectionalArrow
            leftSelected={leftArrowSelected}
            rightSelected={rightArrowSelected}
            onLeftClick={toggleLeftArrow}
            onRightClick={toggleRightArrow}
          />
          <Box
            flex={1}
            border={1}
            borderRadius={2}
            sx={rightBoxStyle}
            minHeight={250}
            bgcolor="white"
          >
            {rightComponent}
          </Box>
        </Box>
      )}
    </Box>
  );
};

const ComparisonLayout = () => {
  const [visibleRows, setVisibleRows] = useState([true, true, true, true]);

  // State for dropdown selections per row (assuming left PSCRFSection)
  const [pscrfSelections, setPscrfSelections] = useState({
    0: [],
    2: [],
    3: [],
  });

  // State for uploaded files per row (assuming right ContractSection)
  const [uploadedFiles, setUploadedFiles] = useState({
    0: null,
    1: null,
    2: null,
  });

  // Validation errors per row
  const [validationErrors, setValidationErrors] = useState({});

  const toggleRowVisibility = (index) => {
    setVisibleRows((prev) => prev.map((v, i) => (i === index ? !v : v)));
  };

  // Dropdown change handlers for PSCRFSections
  const handlePscrfChange = (row) => (event) => {
    const value = event.target.value;
    setPscrfSelections((prev) => ({ ...prev, [row]: value }));
  };

  // File upload handlers for ContractSections
  const handleFileUpload = (row) => (event) => {
    const file = event.target.files[0] || null;
    setUploadedFiles((prev) => ({ ...prev, [row]: file }));
  };

  const validate = () => {
    const errors = {};

    visibleRows.forEach((visible, idx) => {
      if (!visible) return;

      // Validate PSCRFSection for rows that have it (rows 0,2,3 left side)
      const needsPscrfValidation = [0, 2, 3].includes(idx);
      if (needsPscrfValidation) {
        const pscrfValue = pscrfSelections[idx] || [];
        errors[idx] = {
          ...(errors[idx] || {}),
          dropdown: pscrfValue.length === 0,
        };
      }

      // Validate ContractSection for rows that have it (rows 0,1,2 right side)
      const needsFileValidation = [0, 1, 2].includes(idx);
      if (needsFileValidation) {
        const file = uploadedFiles[idx];
        errors[idx] = {
          ...(errors[idx] || {}),
          file: !file,
        };
      }
    });

    setValidationErrors(errors);

    // Check if any visible row has errors
    return !Object.entries(errors).some(
      ([idx, err]) =>
        visibleRows[parseInt(idx)] &&
        (err.dropdown || err.file)
    );
  };

  const handleSubmit = () => {
    if (validate()) {
      alert("Validation passed! Proceed to next page.");
      // Navigate or logic to go next page here
    } else {
      alert("Please fix validation errors before submitting.");
    }
  };

  // Disable submit button if validation fails for visible rows
  const isSubmitEnabled = validate();

  const rowTitles = ["Row 1", "Row 2", "Row 3", "Row 4"];

  return (
    <Box
      sx={{
        width: "95vw",
        maxWidth: 1200,
        mx: "auto",
        mt: 3,
        mb: 6,
        px: 1,
        userSelect: "none",
      }}
    >
      {/* Buttons to toggle row visibility */}
      <Box mb={2} display="flex" justifyContent="center" gap={2}>
        {rowTitles.map((title, i) => (
          <Button
            key={title}
            variant={visibleRows[i] ? "contained" : "outlined"}
            onClick={() => toggle

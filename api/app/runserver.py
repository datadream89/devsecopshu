import React, { useState } from "react";
import {
  Box,
  Grid,
  Typography,
  Checkbox,
  FormControlLabel,
  Autocomplete,
  TextField,
  Paper,
  RadioGroup,
  Radio,
  FormControlLabel as RadioFormControlLabel,
  Button,
  IconButton,
} from "@mui/material";

import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

// Sample PSCRF options
const options = [
  { id: "PSCRF-001", clientName: "ABC Corp", samVersion: "v1", pricingVersion: "p1" },
  { id: "PSCRF-002", clientName: "XYZ Ltd", samVersion: "v2", pricingVersion: "p2" },
  { id: "PSCRF-003", clientName: "DEF Inc", samVersion: "v3", pricingVersion: "p3" },
];

// Contract Section Component
function ContractSection({
  index,
  section,
  handleTypeChange,
  handleFileChange,
  addSection,
  removeSection,
  disabled,
  boxSide,
}) {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 2,
        position: "relative",
        borderRadius: 2,
        border: "1px solid #ccc",
        backgroundColor: disabled ? "#f0f0f0" : "inherit",
        pointerEvents: disabled ? "none" : "auto",
        opacity: disabled ? 0.6 : 1,
      }}
      elevation={1}
    >
      <Typography variant="subtitle1" fontWeight="bold" mb={1}>
        {`Contract Section ${index + 1}`}
      </Typography>

      <RadioGroup
        row
        value={section.contractType}
        onChange={(e) => {
          handleTypeChange(section.id, e.target.value);
          handleFileChange(section.id, null);
        }}
        sx={{
          "& .Mui-checked": {
            color: "darkgrey",
          },
        }}
      >
        <RadioFormControlLabel
          value="Agreement"
          control={<Radio disabled={disabled} />}
          label="Agreement"
        />
        <RadioFormControlLabel
          value="Supplement"
          control={<Radio disabled={disabled} />}
          label="Supplement"
        />
        <RadioFormControlLabel
          value="Addendum"
          control={<Radio disabled={disabled} />}
          label="Addendum"
        />
      </RadioGroup>

      <input
        id={`${boxSide}-file-upload-${section.id}`}
        type="file"
        accept=".pdf,.docx"
        style={{ display: "none" }}
        onChange={(e) => handleFileChange(section.id, e.target.files[0])}
        disabled={disabled}
      />
      <label htmlFor={`${boxSide}-file-upload-${section.id}`}>
        <Button
          variant="outlined"
          startIcon={<CloudUploadIcon />}
          component="span"
          sx={{
            mt: 1,
            color: "darkgrey",
            borderColor: "darkgrey",
            "&:hover": {
              borderColor: "black",
              color: "black",
            },
          }}
          disabled={disabled}
        >
          Upload File
        </Button>
      </label>
      {section.file && (
        <Typography variant="body2" mt={1}>
          Selected: {section.file.name}
        </Typography>
      )}

      <Box
        sx={{
          position: "absolute",
          top: 8,
          right: 8,
          display: "flex",
          gap: 1,
          pointerEvents: disabled ? "none" : "auto",
          opacity: disabled ? 0.6 : 1,
        }}
      >
        <IconButton size="small" onClick={addSection} title="Add section" disabled={disabled}>
          <AddIcon fontSize="small" />
        </IconButton>
        {index > 0 && (
          <IconButton
            size="small"
            onClick={() => removeSection(section.id)}
            title="Remove section"
            disabled={disabled}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        )}
      </Box>
    </Paper>
  );
}

function ComparisonUnit({
  unitNumber,
  leftBoxType = "pscerf", // "pscerf" or "approved"
  rightBoxTitle = "Approved Contract",
}) {
  // State
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [direction, setDirection] = useState("right");
  const [collapsed, setCollapsed] = useState(false);

  // PSCRF selections (if leftBoxType === 'pscerf')
  const [selectedOptions, setSelectedOptions] = useState([]);

  // Left contract sections (if leftBoxType === 'approved')
  const [leftContractSections, setLeftContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // Right contract sections
  const [rightContractSections, setRightContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // PSCRF dropdown change
  const handleSelect = (event, values) => {
    setSelectedOptions(values);
  };

  // Left contract handlers
  const addLeftSection = () => {
    const newId = leftContractSections.length
      ? Math.max(...leftContractSections.map((s) => s.id)) + 1
      : 0;
    setLeftContractSections([
      ...leftContractSections,
      { id: newId, contractType: "Agreement", file: null },
    ]);
  };
  const removeLeftSection = (id) => {
    setLeftContractSections(leftContractSections.filter((s) => s.id !== id));
  };
  const handleLeftTypeChange = (id, newType) => {
    setLeftContractSections(
      leftContractSections.map((s) =>
        s.id === id ? { ...s, contractType: newType, file: null } : s
      )
    );
  };
  const handleLeftFileChange = (id, file) => {
    setLeftContractSections(
      leftContractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  // Right contract handlers
  const addRightSection = () => {
    const newId = rightContractSections.length
      ? Math.max(...rightContractSections.map((s) => s.id)) + 1
      : 0;
    setRightContractSections([
      ...rightContractSections,
      { id: newId, contractType: "Agreement", file: null },
    ]);
  };
  const removeRightSection = (id) => {
    setRightContractSections(rightContractSections.filter((s) => s.id !== id));
  };
  const handleRightTypeChange = (id, newType) => {
    setRightContractSections(
      rightContractSections.map((s) =>
        s.id === id ? { ...s, contractType: newType, file: null } : s
      )
    );
  };
  const handleRightFileChange = (id, file) => {
    setRightContractSections(
      rightContractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  // Border style
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "2px solid lightgray";
    if (direction === "right") {
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  // Arrow colors
  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (direction === arrowDirection) return "black";
    return "lightgray";
  };

  // Render PSCRF selections as comma-separated with metadata
  const renderSelectedPscerfText = () => {
    if (selectedOptions.length === 0) return "None selected";
    return selectedOptions
      .map(
        (o) =>
          `${o.id} (Client: ${o.clientName}, SAM: ${o.samVersion}, Pricing: ${o.pricingVersion})`
      )
      .join(", ");
  };

  return (
    <Box sx={{ mb: 4, border: "1px solid #ccc", borderRadius: 2, p: 2 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 2,
          cursor: "pointer",
        }}
        onClick={() => setCollapsed(!collapsed)}
      >
        <Typography variant="h6" fontWeight="bold">
          {`Comparison Unit ${unitNumber}`}
        </Typography>
        <Button variant="outlined" size="small">
          {collapsed ? "Expand" : "Collapse"}
        </Button>
      </Box>

      {!collapsed && (
        <>
          <Grid container spacing={2} alignItems="center">
            {/* Compare checkbox on left */}
            <Grid item xs={12} sm={2} md={1}>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={compareEnabled}
                    onChange={(e) => setCompareEnabled(e.target.checked)}
                    size="small"
                  />
                }
                label="Compare"
              />
            </Grid>

            {/* Left Box */}
            <Grid
              item
              xs={12}
              sm={4}
              md={5}
              sx={{
                border: getBoxBorder("left"),
                borderRadius: 1,
                p: 2,
                minHeight: 160,
              }}
            >
              <Typography variant="subtitle1" fontWeight="bold" mb={2}>
                {leftBoxType === "pscerf" ? "Pscerf Data" : "Approved Contract"}
              </Typography>

              {/* If pscerf type show dropdown and comma-separated text */}
              {leftBoxType === "pscerf" ? (
                <>
                  <Autocomplete
                    multiple
                    options={options}
                    getOptionLabel={(option) => option.id}
                    value={selectedOptions}
                    onChange={handleSelect}
                    renderInput={(params) => (
                      <TextField {...params} label="Select PSCRF IDs" size="small" />
                    )}
                  />
                  <Typography
                    variant="body2"
                    mt={1}
                    sx={{ whiteSpace: "pre-wrap", userSelect: "text" }}
                  >
                    {renderSelectedPscerfText()}
                  </Typography>
                </>
              ) : (
                // Show approved contract sections on left box if applicable
                leftContractSections.map((section, i) => (
                  <ContractSection
                    key={section.id}
                    index={i}
                    section={section}
                    handleTypeChange={handleLeftTypeChange}
                    handleFileChange={handleLeftFileChange}
                    addSection={addLeftSection}
                    removeSection={removeLeftSection}
                    disabled={!compareEnabled}
                    boxSide="left"
                  />
                ))
              )}
            </Grid>

            {/* Arrows in middle */}
            <Grid
              item
              xs={12}
              sm={1}
              md={1}
              sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                gap: 1,
                minHeight: 160,
              }}
            >
              <ArrowBackIcon
                sx={{
                  cursor: "pointer",
                  color: getArrowColor("left"),
                  fontSize: 32,
                  userSelect: "none",
                }}
                onClick={() => compareEnabled && setDirection("left")}
              />
              <ArrowForwardIcon
                sx={{
                  cursor: "pointer",
                  color: getArrowColor("right"),
                  fontSize: 32,
                  userSelect: "none",
                }}
                onClick={() => compareEnabled && setDirection("right")}
              />
            </Grid>

            {/* Right Box */}
            <Grid
              item
              xs={12}
              sm={4}
              md={5}
              sx={{
                border: getBoxBorder("right"),
                borderRadius: 1,
                p: 2,
                minHeight: 160,
              }}
            >
              <Typography variant="subtitle1" fontWeight="bold" mb={2}>
                {rightBoxTitle || "Signed Contract"}
              </Typography>

              {rightContractSections.map((section, i) => (
                <ContractSection
                  key={section.id}
                  index={i}
                  section={section}
                  handleTypeChange={handleRightTypeChange}
                  handleFileChange={handleRightFileChange}
                  addSection={addRightSection}
                  removeSection={removeRightSection}
                  disabled={!compareEnabled}
                  boxSide="right"
                />
              ))}
            </Grid>
          </Grid>
        </>
      )}
    </Box>
  );
}

// Example usage for unit 2 as you mentioned
export default function App() {
  return (
    <Box sx={{ p: 4 }}>
      {/* Unit 1 - left box pscerf, right box approved contract */}
      <ComparisonUnit unitNumber={1} leftBoxType="pscerf" rightBoxTitle="Approved Contract" />

      {/* Unit 2 - left box approved contract, right box signed contract */}
      <ComparisonUnit unitNumber={2} leftBoxType="approved" rightBoxTitle="Signed Contract" />
    </Box>
  );
}

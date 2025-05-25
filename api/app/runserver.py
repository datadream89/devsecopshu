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

// Sample options for PSCRF dropdown
const options = [
  { id: "PSCRF-001", clientName: "ABC Corp", samVersion: "v1", pricingVersion: "p1" },
  { id: "PSCRF-002", clientName: "XYZ Ltd", samVersion: "v2", pricingVersion: "p2" },
  { id: "PSCRF-003", clientName: "DEF Inc", samVersion: "v3", pricingVersion: "p3" },
];

// Left box card (for Pscerf Data)
function LeftBoxCard({ item, onRemove }) {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 1,
        borderRadius: 1,
        border: "1px solid #ccc",
        backgroundColor: "#f9f9f9",
        position: "relative",
      }}
      elevation={1}
    >
      <Typography variant="subtitle2" fontWeight="bold">
        {item.id}
      </Typography>
      <Typography variant="body2">Client: {item.clientName}</Typography>
      <Typography variant="body2">SAM Version: {item.samVersion}</Typography>
      <Typography variant="body2">Pricing Version: {item.pricingVersion}</Typography>
      <IconButton
        size="small"
        onClick={() => onRemove(item)}
        sx={{ position: "absolute", top: 4, right: 4 }}
        aria-label="Remove"
      >
        <CloseIcon fontSize="small" />
      </IconButton>
    </Paper>
  );
}

// Contract section for approved or signed contracts
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
  // State for compare enable checkbox and direction
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [direction, setDirection] = useState("right");
  const [collapsed, setCollapsed] = useState(false);

  // PSCRF dropdown selection for left box if leftBoxType === 'pscerf'
  const [selectedOptions, setSelectedOptions] = useState([]);

  // Approved Contract sections on left if leftBoxType === 'approved'
  const [leftContractSections, setLeftContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // Contract sections on right box
  const [rightContractSections, setRightContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // Handlers for PSCRF dropdown
  const handleSelect = (event, values) => {
    setSelectedOptions(values);
  };

  const removeOption = (item) => {
    setSelectedOptions(selectedOptions.filter((o) => o.id !== item.id));
  };

  // Add/remove/change handlers for left contract sections (only if leftBoxType === 'approved')
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

  // Add/remove/change handlers for right contract sections
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

  // Border style helpers
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "2px solid lightgray";

    if (direction === "right") {
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (direction === arrowDirection) return "black";
    return "lightgray";
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
          {/* Top controls: Compare enabled checkbox + direction */}
          <Box sx={{ mb: 2, display: "flex", alignItems: "center", gap: 3 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={compareEnabled}
                  onChange={(e) => setCompareEnabled(e.target.checked)}
                />
              }
              label="Compare enabled"
            />
            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              <ArrowBackIcon
                sx={{
                  cursor: "pointer",
                  color: getArrowColor("left"),
                }}
                onClick={() => compareEnabled && setDirection("left")}
                aria-label="Direction left"
              />
              <ArrowForwardIcon
                sx={{
                  cursor: "pointer",
                  color: getArrowColor("right"),
                }}
                onClick={() => compareEnabled && setDirection("right")}
                aria-label="Direction right"
              />
            </Box>
          </Box>

          <Grid container spacing={2}>
            {/* Left Box */}
            <Grid
              item
              xs={6}
              sx={{
                border: getBoxBorder("left"),
                borderRadius: 1,
                p: 2,
                minHeight: 300,
              }}
            >
              <Typography
                variant="subtitle1"
                fontWeight="bold"
                mb={2}
                sx={{ userSelect: "none" }}
              >
                {leftBoxType === "pscerf" ? "Pscerf Data" : "Approved Contract"}
              </Typography>

              {/* Left box content */}
              {leftBoxType === "pscerf" ? (
                <>
                  <Autocomplete
                    multiple
                    options={options}
                    getOptionLabel={(option) => option.id}
                    value={selectedOptions}
                    onChange={handleSelect}
                    renderInput={(params) => (
                      <TextField {...params} label="Select PSCRF IDs" placeholder="Select" />
                    )}
                    disableCloseOnSelect
                    sx={{ mb: 2 }}
                  />
                  {selectedOptions.map((item) => (
                    <LeftBoxCard key={item.id} item={item} onRemove={removeOption} />
                  ))}
                </>
              ) : (
                // Approved Contract Sections on left (unit 2)
                leftContractSections.map((section, idx) => (
                  <ContractSection
                    key={section.id}
                    index={idx}
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

            {/* Right Box */}
            <Grid
              item
              xs={6}
              sx={{
                border: getBoxBorder("right"),
                borderRadius: 1,
                p: 2,
                minHeight: 300,
              }}
            >
              <Typography
                variant="subtitle1"
                fontWeight="bold"
                mb={2}
                sx={{ userSelect: "none" }}
              >
                {rightBoxTitle}
              </Typography>

              {/* Right box contract sections */}
              {rightContractSections.map((section, idx) => (
                <ContractSection
                  key={section.id}
                  index={idx}
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

export default function ComparisonUnitsPanel() {
  return (
    <Box sx={{ maxWidth: 1200, mx: "auto", p: 3 }}>
      {/* Unit 1: Left = Pscerf Data, Right = Approved Contract */}
      <ComparisonUnit unitNumber={1} leftBoxType="pscerf" rightBoxTitle="Approved Contract" />

      {/* Unit 2: Left = Approved Contract, Right = Signed Contract */}
      <ComparisonUnit unitNumber={2} leftBoxType="approved" rightBoxTitle="Signed Contract" />
    </Box>
  );
}

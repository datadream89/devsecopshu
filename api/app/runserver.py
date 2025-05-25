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

import options from "./options.json";

function ApprovedContractSection({
  index,
  section,
  handleTypeChange,
  handleFileChange,
  addSection,
  removeSection,
}) {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 2,
        position: "relative",
        borderRadius: 2,
        border: "1px solid #ccc",
      }}
      elevation={1}
    >
      <Typography variant="subtitle1" fontWeight="bold" mb={1}>
        Approved Contract {index + 1}
      </Typography>

      <RadioGroup
        row
        value={section.contractType}
        onChange={(e) => handleTypeChange(section.id, e.target.value)}
      >
        <RadioFormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
        <RadioFormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
        <RadioFormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
      </RadioGroup>

      <input
        id={`file-upload-${section.id}`}
        type="file"
        accept=".pdf,.docx"
        style={{ display: "none" }}
        onChange={(e) => handleFileChange(section.id, e.target.files[0])}
      />
      <label htmlFor={`file-upload-${section.id}`}>
        <Button
          variant="outlined"
          startIcon={<CloudUploadIcon />}
          component="span"
          sx={{ mt: 1 }}
        >
          Upload File
        </Button>
        {section.file && (
          <Typography variant="body2" mt={1}>
            Selected: {section.file.name}
          </Typography>
        )}
      </label>

      <Box
        sx={{
          position: "absolute",
          top: 8,
          right: 8,
          display: "flex",
          gap: 1,
        }}
      >
        <IconButton size="small" onClick={addSection} title="Add section">
          <AddIcon fontSize="small" />
        </IconButton>
        {index > 0 && (
          <IconButton
            size="small"
            onClick={() => removeSection(section.id)}
            title="Remove section"
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        )}
      </Box>
    </Paper>
  );
}

function LeftBoxCard({ item }) {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 1,
        borderRadius: 1,
        border: "1px solid #ccc",
        backgroundColor: "#f9f9f9",
      }}
      elevation={1}
    >
      <Typography variant="subtitle2" fontWeight="bold">
        {item.id}
      </Typography>
      <Typography variant="body2">Client: {item.clientName}</Typography>
      <Typography variant="body2">SAM Version: {item.samVersion}</Typography>
      <Typography variant="body2">Pricing Version: {item.pricingVersion}</Typography>
    </Paper>
  );
}

export default function Request() {
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [direction, setDirection] = useState("right");
  const [collapsed, setCollapsed] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [contractSections, setContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  const addSection = () => {
    const newId = contractSections.length
      ? Math.max(...contractSections.map((s) => s.id)) + 1
      : 0;
    setContractSections([
      ...contractSections,
      { id: newId, contractType: "Agreement", file: null },
    ]);
  };

  const removeSection = (id) => {
    setContractSections(contractSections.filter((s) => s.id !== id));
  };

  const handleTypeChange = (id, newType) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, contractType: newType } : s))
    );
  };

  const handleFileChange = (id, file) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  // Border colors for boxes (darkgrey/lightgrey)
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "2px solid lightgray";

    if (direction === "right") {
      // Flip outline direction: left box lightgrey, right box darkgrey
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      // left box darkgrey, right box lightgrey
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  // Arrow colors
  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: "auto" }}>
      {/* Collapsible container header */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          mb: collapsed ? 0 : 2,
          cursor: "pointer",
          userSelect: "none",
          border: "1px solid #ccc",
          borderRadius: 1,
          p: 1,
          backgroundColor: "#f5f5f5",
        }}
        onClick={() => setCollapsed(!collapsed)}
      >
        <Typography variant="subtitle1" fontWeight="bold" sx={{ ml: 1 }}>
          Compare PSCRF and Approved Contract
        </Typography>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            setCollapsed(!collapsed);
          }}
          aria-label={collapsed ? "Expand" : "Collapse"}
        >
          {collapsed ? <AddIcon /> : <CloseIcon />}
        </IconButton>
      </Box>

      {/* The collapsible content */}
      {!collapsed && (
        <Box sx={{ mt: 2 }}>
          {/* Compare Checkbox on left */}
          <Box sx={{ mb: 2, display: "flex", alignItems: "center" }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={compareEnabled}
                  onChange={(e) => setCompareEnabled(e.target.checked)}
                />
              }
              label="Compare"
            />
          </Box>

          {/* Main Grid */}
          <Grid container spacing={2} alignItems="flex-start">
            {/* Left Box */}
            <Grid item xs={5}>
              <Paper
                sx={{
                  p: 2,
                  border: getBoxBorder("left"),
                  minHeight: 360,
                  boxSizing: "border-box",
                  overflowY: "auto",
                }}
                elevation={2}
              >
                <Typography variant="h6" mb={2}>
                  Pscerf Data
                </Typography>
                <Autocomplete
                  multiple
                  options={options}
                  filterSelectedOptions
                  value={selectedOptions}
                  onChange={(e, newValue) => setSelectedOptions(newValue)}
                  getOptionLabel={(option) =>
                    `${option.id} (Client: ${option.clientName}, SAM: ${option.samVersion}, Pricing: ${option.pricingVersion})`
                  }
                  renderInput={(params) => (
                    <TextField {...params} label="Select PSCRF IDs" />
                  )}
                  disabled={!compareEnabled}
                  sx={{ width: "100%" }}
                />

                {/* Render selected items as cards */}
                {selectedOptions.length > 0 && (
                  <Box mt={2} sx={{ maxHeight: 200, overflowY: "auto" }}>
                    {selectedOptions.map((item) => (
                      <LeftBoxCard
                        key={item.id + item.samVersion + item.pricingVersion}
                        item={item}
                      />
                    ))}
                  </Box>
                )}
              </Paper>
            </Grid>

            {/* Arrow Section */}
            <Grid item xs={2} textAlign="center" sx={{ position: "relative" }}>
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  mt: 8,
                  gap: 1,
                }}
              >
                <IconButton
                  onClick={() => compareEnabled && setDirection("right")}
                  disabled={!compareEnabled}
                  sx={{ color: getArrowColor("right") }}
                  aria-label="Arrow right"
                >
                  <ArrowForwardIcon fontSize="large" />
                </IconButton>
                <IconButton
                  onClick={() => compareEnabled && setDirection("left")}
                  disabled={!compareEnabled}
                  sx={{ color: getArrowColor("left") }}
                  aria-label="Arrow left"
                >
                  <ArrowBackIcon fontSize="large" />
                </IconButton>
              </Box>
            </Grid>

            {/* Right Box */}
            <Grid item xs={5}>
              <Paper
                sx={{
                  p: 2,
                  border: getBoxBorder("right"),
                  minHeight: 360,
                  boxSizing: "border-box",
                  overflowY: "auto",
                }}
                elevation={2}
              >
                {contractSections.map((section, idx) => (
                  <ApprovedContractSection
                    key={section.id}
                    index={idx}
                    section={section}
                    handleTypeChange={handleTypeChange}
                    handleFileChange={handleFileChange}
                    addSection={addSection}
                    removeSection={removeSection}
                  />
                ))}
              </Paper>
            </Grid>
          </Grid>
        </Box>
      )}
    </Box>
  );
}

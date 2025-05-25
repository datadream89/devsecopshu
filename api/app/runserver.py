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

// import your options.json - adjust the path accordingly
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

export default function Request() {
  // Compare enabled checkbox
  const [compareEnabled, setCompareEnabled] = useState(true);
  // Arrow direction: "right" or "left"
  const [direction, setDirection] = useState("right");
  // Collapse state
  const [collapsed, setCollapsed] = useState(false);
  // Selected PSCRF options (multiple)
  const [selectedOptions, setSelectedOptions] = useState([]);
  // Approved Contract dynamic sections
  const [contractSections, setContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // Add new approved contract section
  const addSection = () => {
    const newId = contractSections.length
      ? Math.max(...contractSections.map((s) => s.id)) + 1
      : 0;
    setContractSections([
      ...contractSections,
      { id: newId, contractType: "Agreement", file: null },
    ]);
  };

  // Remove a section by id
  const removeSection = (id) => {
    setContractSections(contractSections.filter((s) => s.id !== id));
  };

  // Change contract type for a section
  const handleTypeChange = (id, newType) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, contractType: newType } : s))
    );
  };

  // Change file for a section
  const handleFileChange = (id, file) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  // Helper for border colors on boxes
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "1px solid lightgray";

    // Flip outline direction as you requested previously
    // So if arrow points right, left box = blue, right box = red
    if (direction === "right") {
      return boxSide === "left" ? "2px solid blue" : "2px solid red";
    } else {
      return boxSide === "left" ? "2px solid red" : "2px solid blue";
    }
  };

  // Helper for arrow colors
  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
  };

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: "auto" }}>
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

      {/* Main Grid: two boxes and arrow section */}
      {!collapsed && (
        <Grid container spacing={2} alignItems="flex-start">
          {/* Left Box: Pscerf Data */}
          <Grid item xs={5}>
            <Paper
              sx={{
                p: 2,
                border: getBoxBorder("left"),
                minHeight: 360,
                boxSizing: "border-box",
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
              {/* Show selected items as comma separated metadata */}
              {selectedOptions.length > 0 && (
                <Box mt={2}>
                  <Typography variant="subtitle2" gutterBottom>
                    Selected:
                  </Typography>
                  <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
                    {selectedOptions
                      .map(
                        (o) =>
                          `id: ${o.id}, clientName: ${o.clientName}, SAM ver: ${o.samVersion}, pricing ver: ${o.pricingVersion}`
                      )
                      .join(",\n")}
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>

          {/* Arrow section */}
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

            {/* + / - toggle below the arrows */}
            <Box
              sx={{
                position: "absolute",
                bottom: 0,
                left: "50%",
                transform: "translateX(-50%)",
                display: "flex",
                alignItems: "center",
                gap: 1,
                mb: 1,
              }}
            >
              <Typography
                variant="body2"
                sx={{ userSelect: "none" }}
                color="textSecondary"
              >
                Compare PSCRF and Approved Contract
              </Typography>
              <IconButton
                size="small"
                onClick={() => setCollapsed(true)}
                aria-label="Collapse"
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            </Box>
          </Grid>

          {/* Right Box: Approved Contract */}
          <Grid item xs={5}>
            <Paper
              sx={{
                p: 2,
                border: getBoxBorder("right"),
                minHeight: 360,
                boxSizing: "border-box",
              }}
              elevation={2}
            >
              <Typography variant="h6" gutterBottom>
                Approved Contract
              </Typography>

              {contractSections.map((section, index) => (
                <ApprovedContractSection
                  key={section.id}
                  index={index}
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
      )}

      {/* Expand + label when collapsed */}
      {collapsed && (
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            mt: 1,
            gap: 1,
          }}
        >
          <Typography>Compare PSCRF and Approved Contract</Typography>
          <IconButton onClick={() => setCollapsed(false)} aria-label="Expand">
            <AddIcon />
          </IconButton>
        </Box>
      )}
    </Box>
  );
}

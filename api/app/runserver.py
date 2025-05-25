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

// Sample options JSON (replace or import your own)
const options = [
  { id: "PSCRF-001", clientName: "ABC Corp", samVersion: "v1", pricingVersion: "p1" },
  { id: "PSCRF-002", clientName: "XYZ Ltd", samVersion: "v2", pricingVersion: "p2" },
  { id: "PSCRF-003", clientName: "DEF Inc", samVersion: "v3", pricingVersion: "p3" },
];

// Left box card
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

// Approved contract upload section
function ApprovedContractSection({
  index,
  section,
  handleTypeChange,
  handleFileChange,
  addSection,
  removeSection,
  disabled,
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
        Approved Contract {index + 1}
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
        id={`file-upload-${section.id}`}
        type="file"
        accept=".pdf,.docx"
        style={{ display: "none" }}
        onChange={(e) => handleFileChange(section.id, e.target.files[0])}
        disabled={disabled}
      />
      <label htmlFor={`file-upload-${section.id}`}>
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

// Comparison unit with all UI and logic
function ComparisonUnit({ title }) {
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [direction, setDirection] = useState("right");
  const [collapsed, setCollapsed] = useState(false);
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [contractSections, setContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // Add new section
  const addSection = () => {
    const newId = contractSections.length
      ? Math.max(...contractSections.map((s) => s.id)) + 1
      : 0;
    setContractSections([
      ...contractSections,
      { id: newId, contractType: "Agreement", file: null },
    ]);
  };

  // Remove section
  const removeSection = (id) => {
    setContractSections(contractSections.filter((s) => s.id !== id));
  };

  // Change contract type
  const handleTypeChange = (id, newType) => {
    setContractSections(
      contractSections.map((s) =>
        s.id === id ? { ...s, contractType: newType, file: null } : s
      )
    );
  };

  // Change file for section
  const handleFileChange = (id, file) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  // Box border color based on direction & enabled
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "2px solid lightgray";

    if (direction === "right") {
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  // Arrow color based on direction & enabled
  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
  };

  // Remove option from selected
  const removeOption = (item) => {
    setSelectedOptions(
      selectedOptions.filter(
        (o) =>
          o.id !== item.id ||
          o.samVersion !== item.samVersion ||
          o.pricingVersion !== item.pricingVersion
      )
    );
  };

  return (
    <Box sx={{ mb: 5, border: "1px solid #ccc", borderRadius: 1 }}>
      {/* Header */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          p: 1,
          backgroundColor: "#f5f5f5",
          userSelect: "none",
          cursor: "pointer",
        }}
        onClick={() => setCollapsed(!collapsed)}
      >
        <Typography variant="subtitle1" fontWeight="bold" sx={{ ml: 1 }}>
          {title}
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

      {!collapsed && (
        <>
          {/* Compare checkbox */}
          <Box sx={{ display: "flex", alignItems: "center", p: 1 }}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={compareEnabled}
                  onChange={(e) => setCompareEnabled(e.target.checked)}
                  sx={{
                    color: "darkgrey",
                    "&.Mui-checked": {
                      color: "darkgrey",
                    },
                  }}
                />
              }
              label="Compare"
              sx={{ mr: 4 }}
            />

            {/* Boxes and arrows */}
            <Grid container spacing={2} alignItems="center" sx={{ minHeight: 420 }}>
              {/* Left Box */}
              <Grid item xs={5}>
                <Paper
                  sx={{
                    p: 2,
                    border: getBoxBorder("left"),
                    minHeight: 400,
                    boxSizing: "border-box",
                    overflowY: "auto",
                    backgroundColor: compareEnabled ? "inherit" : "#f0f0f0",
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
                      <TextField
                        {...params}
                        label="Select PSCRF IDs"
                        placeholder="Start typing..."
                        size="small"
                      />
                    )}
                    disabled={!compareEnabled}
                    sx={{ mb: 2 }}
                  />

                  {selectedOptions.length === 0 && (
                    <Typography variant="body2" color="text.secondary">
                      No selections yet.
                    </Typography>
                  )}

                  {selectedOptions.map((item) => (
                    <LeftBoxCard key={`${item.id}-${item.samVersion}-${item.pricingVersion}`} item={item} onRemove={removeOption} />
                  ))}
                </Paper>
              </Grid>

              {/* Arrows and Direction Buttons */}
              <Grid
                item
                xs={2}
                container
                direction="column"
                justifyContent="center"
                alignItems="center"
                sx={{ height: 400 }}
              >
                <ArrowBackIcon
                  sx={{
                    fontSize: 50,
                    color: getArrowColor("left"),
                    cursor: compareEnabled ? "pointer" : "default",
                    mb: 2,
                  }}
                  onClick={() => {
                    if (compareEnabled) setDirection("left");
                  }}
                />
                <ArrowForwardIcon
                  sx={{
                    fontSize: 50,
                    color: getArrowColor("right"),
                    cursor: compareEnabled ? "pointer" : "default",
                    mt: 2,
                  }}
                  onClick={() => {
                    if (compareEnabled) setDirection("right");
                  }}
                />
              </Grid>

              {/* Right Box */}
              <Grid item xs={5}>
                <Paper
                  sx={{
                    p: 2,
                    border: getBoxBorder("right"),
                    minHeight: 400,
                    boxSizing: "border-box",
                    overflowY: "auto",
                    backgroundColor: compareEnabled ? "inherit" : "#f0f0f0",
                  }}
                  elevation={2}
                >
                  <Typography variant="h6" mb={2}>
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
                      disabled={!compareEnabled}
                    />
                  ))}
                </Paper>
              </Grid>
            </Grid>
          </Box>
        </>
      )}
    </Box>
  );
}

// Main component with two comparison units
export default function ComparisonPage() {
  return (
    <Box sx={{ p: 4 }}>
      <ComparisonUnit title="Comparison Unit 1" />
      <ComparisonUnit title="Comparison Unit 2" />
    </Box>
  );
}

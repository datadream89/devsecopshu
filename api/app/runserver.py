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

import options from "./options.json"; // Your PSCRF options list JSON file

// Left box card showing selected PSCRF items with remove button
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
        aria-label={`Remove ${item.id}`}
      >
        <CloseIcon fontSize="small" />
      </IconButton>
    </Paper>
  );
}

// Approved Contract Section card with contract type radios, file upload, add/remove section buttons
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

// The entire pair UI component
function ComparePair({ pairIndex }) {
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
      contractSections.map((s) =>
        s.id === id ? { ...s, contractType: newType, file: null } : s
      )
    );
  };

  const handleFileChange = (id, file) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

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
    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
  };

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
    <Box
      sx={{
        p: 3,
        mb: 5,
        border: "1px solid #ccc",
        borderRadius: 2,
        backgroundColor: "#fafafa",
      }}
    >
      {/* Header with collapse toggle */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          mb: 1,
          userSelect: "none",
          cursor: "pointer",
        }}
        onClick={() => setCollapsed(!collapsed)}
      >
        <Typography variant="subtitle1" fontWeight="bold" sx={{ ml: 1 }}>
          Compare PSCRF and Approved Contract #{pairIndex + 1}
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
          <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
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
                    <LeftBoxCard
                      key={`${item.id}-${item.samVersion}-${item.pricingVersion}`}
                      item={item}
                      onRemove={removeOption}
                    />
                  ))}
                </Paper>
              </Grid>

              {/* Center arrows */}
              <Grid
                item
                xs={2}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  height: 400,
                  position: "relative",
                }}
              >
                <IconButton
                  onClick={() => setDirection("left")}
                  sx={{ color: getArrowColor("left") }}
                  disabled={!compareEnabled}
                  aria-label="Left direction"
                >
                  <ArrowBackIcon fontSize="large" />
                </IconButton>
                <IconButton
                  onClick={() => setDirection("right")}
                  sx={{ color: getArrowColor("right") }}
                  disabled={!compareEnabled}
                  aria-label="Right direction"
                >
                  <ArrowForwardIcon fontSize="large" />
                </IconButton>
              </Grid>

              {/* Right Box */}
              <Grid item xs={5}>
                {contractSections.length === 0 && (
                  <Typography variant="body2" color="text.secondary">
                    No approved contract sections.
                  </Typography>
                )}

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
              </Grid>
            </Grid>
          </Box>
        </>
      )}
    </Box>
  );
}

// Main component rendering 4 pairs
export default function Request() {
  return (
    <Box sx={{ p: 3 }}>
      {[...Array(4)].map((_, i) => (
        <ComparePair key={i} pairIndex={i} />
      ))}
    </Box>
  );
}

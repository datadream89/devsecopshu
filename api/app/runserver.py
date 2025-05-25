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
  Button,
  IconButton,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";

import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

import options from "./options.json"; // Your PSCRF options data

// Left box card representing one PSCRF selection
function LeftBoxCard({ item, onRemove, disabled }) {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 1,
        borderRadius: 1,
        border: "1px solid #ccc",
        backgroundColor: disabled ? "#e0e0e0" : "#f9f9f9",
        position: "relative",
        opacity: disabled ? 0.6 : 1,
        pointerEvents: disabled ? "none" : "auto",
      }}
      elevation={1}
    >
      <Typography variant="subtitle2" fontWeight="bold">
        {item.id}
      </Typography>
      <Typography variant="body2">Client: {item.clientName}</Typography>
      <Typography variant="body2">SAM Version: {item.samVersion}</Typography>
      <Typography variant="body2">Pricing Version: {item.pricingVersion}</Typography>
      {!disabled && (
        <IconButton
          size="small"
          onClick={() => onRemove(item)}
          sx={{ position: "absolute", top: 4, right: 4 }}
          aria-label="Remove"
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      )}
    </Paper>
  );
}

// Right box: approved contract section UI
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
        backgroundColor: disabled ? "#e0e0e0" : "inherit",
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
            color: disabled ? "gray" : "darkgrey",
          },
        }}
      >
        <FormControlLabel
          value="Agreement"
          control={<Radio disabled={disabled} />}
          label="Agreement"
        />
        <FormControlLabel
          value="Supplement"
          control={<Radio disabled={disabled} />}
          label="Supplement"
        />
        <FormControlLabel
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
            color: disabled ? "gray" : "darkgrey",
            borderColor: disabled ? "gray" : "darkgrey",
            "&:hover": {
              borderColor: disabled ? "gray" : "black",
              color: disabled ? "gray" : "black",
            },
          }}
          disabled={disabled}
        >
          Upload File
        </Button>
      </label>
      {section.file && (
        <Typography variant="body2" mt={1} sx={{ opacity: disabled ? 0.6 : 1 }}>
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

// One full pair setup: checkbox + two boxes + arrows
function ComparePair({ pairIndex, globalDirection, globalContractType }) {
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [contractSections, setContractSections] = useState([
    { id: 0, contractType: globalContractType, file: null },
  ]);

  // Update contractSections if globalContractType changes
  React.useEffect(() => {
    setContractSections((oldSections) =>
      oldSections.map((s) => ({ ...s, contractType: globalContractType, file: null }))
    );
  }, [globalContractType]);

  const addSection = () => {
    const newId = contractSections.length
      ? Math.max(...contractSections.map((s) => s.id)) + 1
      : 0;
    setContractSections([
      ...contractSections,
      { id: newId, contractType: globalContractType, file: null },
    ]);
  };

  const removeSection = (id) => {
    setContractSections(contractSections.filter((s) => s.id !== id));
  };

  const handleTypeChange = (id, newType) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, contractType: newType, file: null } : s))
    );
  };

  const handleFileChange = (id, file) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  // Border styles for boxes
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "2px solid lightgray";

    if (globalDirection === "right") {
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  // Arrow colors
  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (globalDirection === arrowDirection) return "darkgray";
    return "lightgray";
  };

  // Remove selected option from dropdown
  const removeOption = (item) => {
    setSelectedOptions(
      selectedOptions.filter(
        (o) =>
          !(
            o.id === item.id &&
            o.samVersion === item.samVersion &&
            o.pricingVersion === item.pricingVersion
          )
      )
    );
  };

  return (
    <Box
      key={pairIndex}
      sx={{
        border: "1px solid #ddd",
        borderRadius: 2,
        p: 2,
        mb: 4,
        userSelect: "none",
      }}
    >
      <Grid container spacing={2} alignItems="center" sx={{ minHeight: 420 }}>
        {/* Checkbox on left */}
        <Grid item xs={1}>
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
                inputProps={{ "aria-label": `Compare checkbox ${pairIndex + 1}` }}
              />
            }
            label="Compare"
          />
        </Grid>

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
              opacity: compareEnabled ? 1 : 0.6,
              pointerEvents: compareEnabled ? "auto" : "none",
            }}
            elevation={2}
          >
            <Typography variant="h6" mb={2}>
              Pscerf Data (Pair {pairIndex + 1})
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
                disabled={!compareEnabled}
              />
            ))}
          </Paper>
        </Grid>

        {/* Center arrows */}
        <Grid
          item
          xs={1}
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            height: 400,
            position: "relative",
            pointerEvents: compareEnabled ? "auto" : "none",
            opacity: compareEnabled ? 1 : 0.6,
          }}
        >
          <ArrowBackIcon
            fontSize="large"
            sx={{ color: getArrowColor("left"), cursor: "default", mb: 1 }}
          />
          <ArrowForwardIcon
            fontSize="large"
            sx={{ color: getArrowColor("right"), cursor: "default" }}
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
              opacity: compareEnabled ? 1 : 0.6,
              pointerEvents: compareEnabled ? "auto" : "none",
            }}
            elevation={2}
          >
            <Typography variant="h6" mb={2} fontWeight="bold">
              Approved Contract (Pair {pairIndex + 1})
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
    </

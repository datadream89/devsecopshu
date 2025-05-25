import React, { useState } from "react";
import {
  Box,
  Grid,
  Paper,
  Typography,
  Checkbox,
  TextField,
  Autocomplete,
  IconButton,
  Button,
} from "@mui/material";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";

const options = [
  { id: "pscrf1", samVersion: "SAMv1", pricingVersion: "P1", clientName: "Client A" },
  { id: "pscrf2", samVersion: "SAMv2", pricingVersion: "P2", clientName: "Client B" },
  { id: "pscrf3", samVersion: "SAMv3", pricingVersion: "P3", clientName: "Client C" },
];

// Card component shown below Autocomplete selected options for Comparison Unit 1 left box
function LeftBoxCard({ item, onRemove }) {
  return (
    <Paper
      elevation={1}
      sx={{
        p: 1,
        mb: 1,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}
    >
      <Box>
        <Typography variant="body2">{item.id}</Typography>
        <Typography variant="caption">SAM: {item.samVersion}</Typography> |{" "}
        <Typography variant="caption">Pricing: {item.pricingVersion}</Typography> |{" "}
        <Typography variant="caption">{item.clientName}</Typography>
      </Box>
      <IconButton size="small" onClick={() => onRemove(item.id)}>
        <CloseIcon fontSize="small" />
      </IconButton>
    </Paper>
  );
}

// Contract section component used in contract boxes for adding/removing sections with type dropdown and file upload
function ContractSection({
  index,
  section,
  handleTypeChange,
  handleFileChange,
  addSection,
  removeSection,
  disabled,
  isLeftBox,
}) {
  return (
    <Box
      sx={{
        mb: 2,
        border: "1px solid #ccc",
        borderRadius: 1,
        p: 1,
        position: "relative",
      }}
    >
      <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
        <Typography sx={{ flexGrow: 1, fontWeight: "bold" }}>
          Section {index + 1}
        </Typography>
        <IconButton
          size="small"
          onClick={() => removeSection(index)}
          disabled={disabled}
        >
          <CloseIcon fontSize="small" />
        </IconButton>
        <IconButton
          size="small"
          onClick={() => addSection(index + 1)}
          disabled={disabled}
        >
          <AddIcon fontSize="small" />
        </IconButton>
      </Box>

      <TextField
        select
        label="Contract Type"
        value={section.type}
        onChange={(e) => handleTypeChange(index, e.target.value)}
        SelectProps={{ native: true }}
        fullWidth
        disabled={disabled}
        size="small"
        sx={{ mb: 1 }}
      >
        <option value="Type A">Type A</option>
        <option value="Type B">Type B</option>
        <option value="Type C">Type C</option>
      </TextField>

      <Button
        variant="outlined"
        component="label"
        fullWidth
        disabled={disabled}
        size="small"
      >
        Upload File {section.file ? `(${section.file.name})` : ""}
        <input
          type="file"
          hidden
          onChange={(e) => handleFileChange(index, e.target.files[0])}
        />
      </Button>
    </Box>
  );
}

function ComparisonUnit({ title, leftBoxIsSignedContract }) {
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [selectedOptions, setSelectedOptions] = useState([]);

  // For contract sections, init with one section each
  const [contractSectionsLeft, setContractSectionsLeft] = useState([
    { id: 1, type: "Type A", file: null },
  ]);
  const [contractSectionsRight, setContractSectionsRight] = useState([
    { id: 1, type: "Type A", file: null },
  ]);

  // Remove PSCRF option from Autocomplete
  const removeOption = (id) => {
    setSelectedOptions((prev) => prev.filter((item) => item.id !== id));
  };

  // Handlers for contract sections left box
  const handleTypeChangeLeft = (index, newType) => {
    setContractSectionsLeft((prev) =>
      prev.map((sec, i) => (i === index ? { ...sec, type: newType } : sec))
    );
  };
  const handleFileChangeLeft = (index, file) => {
    setContractSectionsLeft((prev) =>
      prev.map((sec, i) => (i === index ? { ...sec, file } : sec))
    );
  };
  const addSectionLeft = (index) => {
    const newSection = {
      id: Math.random(),
      type: "Type A",
      file: null,
    };
    setContractSectionsLeft((prev) => [
      ...prev.slice(0, index),
      newSection,
      ...prev.slice(index),
    ]);
  };
  const removeSectionLeft = (index) => {
    setContractSectionsLeft((prev) => prev.filter((_, i) => i !== index));
  };

  // Handlers for contract sections right box
  const handleTypeChangeRight = (index, newType) => {
    setContractSectionsRight((prev) =>
      prev.map((sec, i) => (i === index ? { ...sec, type: newType } : sec))
    );
  };
  const handleFileChangeRight = (index, file) => {
    setContractSectionsRight((prev) =>
      prev.map((sec, i) => (i === index ? { ...sec, file } : sec))
    );
  };
  const addSectionRight = (index) => {
    const newSection = {
      id: Math.random(),
      type: "Type A",
      file: null,
    };
    setContractSectionsRight((prev) => [
      ...prev.slice(0, index),
      newSection,
      ...prev.slice(index),
    ]);
  };
  const removeSectionRight = (index) => {
    setContractSectionsRight((prev) => prev.filter((_, i) => i !== index));
  };

  // Helper for border color of boxes when disabled
  const getBoxBorder = (side) => {
    if (!compareEnabled) {
      return "2px solid grey";
    }
    return side === "left"
      ? "2px solid #1976d2" // blue
      : "2px solid #d32f2f"; // red
  };

  return (
    <Box sx={{ mb: 5 }}>
      <Typography variant="h5" mb={2}>
        {title}
      </Typography>

      {/* Checkbox to enable/disable comparison */}
      <Box sx={{ mb: 2 }}>
        <Checkbox
          checked={compareEnabled}
          onChange={() => setCompareEnabled(!compareEnabled)}
          id={`compare-checkbox-${title}`}
        />
        <label htmlFor={`compare-checkbox-${title}`}>
          Enable Comparison
        </label>
      </Box>

      {compareEnabled && (
        <>
          <Grid container spacing={2} alignItems="stretch">
            {/* Left box */}
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
                  {leftBoxIsSignedContract
                    ? "Signed Contract"
                    : "Approved Contract"}
                </Typography>

                {/* For left box of Comparison Unit 1, show Autocomplete multi-select */}
                {!leftBoxIsSignedContract && (
                  <Autocomplete
                    multiple
                    options={options}
                    getOptionLabel={(option) => option.id}
                    value={selectedOptions}
                    onChange={(event, newValue) => setSelectedOptions(newValue)}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        variant="outlined"
                        label="Select PSCRF Id(s)"
                        placeholder="PSCRF Id"
                        size="small"
                      />
                    )}
                    disabled={!compareEnabled}
                    sx={{ mb: 2 }}
                  />
                )}

                {/* Show modals/cards for each selected option (only for left box in unit 1) */}
                {!leftBoxIsSignedContract &&
                  selectedOptions.map((item) => (
                    <LeftBoxCard
                      key={`${item.id}-${item.samVersion}-${item.pricingVersion}`}
                      item={item}
                      onRemove={removeOption}
                    />
                  ))}

                {/* Contract sections - Left box */}
                {contractSectionsLeft.map((section, index) => (
                  <ContractSection
                    key={section.id}
                    index={index}
                    section={section}
                    handleTypeChange={handleTypeChangeLeft}
                    handleFileChange={handleFileChangeLeft}
                    addSection={addSectionLeft}
                    removeSection={removeSectionLeft}
                    disabled={!compareEnabled}
                    isLeftBox={true}
                  />
                ))}
              </Paper>
            </Grid>

            {/* Horizontal bar with arrows and title */}
            <Grid
              item
              xs={2}
              sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <ArrowBackIosNewIcon fontSize="large" />
              <Typography variant="subtitle1" sx={{ my: 1 }}>
                Comparison
              </Typography>
              <ArrowForwardIosIcon fontSize="large" />
            </Grid>

            {/* Right box */}
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

                {/* Contract sections - Right box */}
                {contractSectionsRight.map((section, index) => (
                  <ContractSection
                    key={section.id}
                    index={index}
                    section={section}
                    handleTypeChange={handleTypeChangeRight}
                    handleFileChange={handleFileChangeRight}
                    addSection={addSectionRight}
                    removeSection={removeSectionRight}
                    disabled={!compareEnabled}
                    isLeftBox={false}
                  />
                ))}
              </Paper>
            </Grid>
          </Grid>
        </>
      )}
    </Box>
  );
}

export default function PscrfDataUI() {
  return (
    <Box sx={{ p: 3, maxWidth: 1300, mx: "auto" }}>
      {/* Comparison Unit 1: Left box is Approved Contract */}
      <ComparisonUnit
        title="Comparison Unit 1"
        leftBoxIsSignedContract={false} // left box title is Approved Contract
      />

      {/* Comparison Unit 2: Left box is Signed Contract */}
      <ComparisonUnit
        title="Comparison Unit 2"
        leftBoxIsSignedContract={true} // left box title changed to Signed Contract
      />
    </Box>
  );
}

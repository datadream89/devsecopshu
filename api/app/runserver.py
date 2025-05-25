import React, { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Checkbox,
  Collapse,
  FormControlLabel,
  IconButton,
  Paper,
  Radio,
  RadioGroup,
  Stack,
  TextField,
  Typography,
  Autocomplete,
  Tooltip,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import CloseIcon from "@mui/icons-material/Close";

// Sample options JSON data
const options = [
  { id: "7", samVersion: "v1.0", pricingVersion: "pv1.1", clientName: "Client A" },
  { id: "5", samVersion: "v2.0", pricingVersion: "pv2.1", clientName: "Client B" },
  { id: "7", samVersion: "v1.1", pricingVersion: "pv1.2", clientName: "Client A" },
];

function ApprovedContractSection({
  section,
  onTypeChange,
  onFileChange,
  disabled,
}) {
  const handleTypeChange = (e) => {
    onTypeChange(section.id, e.target.value);
    onFileChange(section.id, null); // Clear file on radio change
  };

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        mb: 1,
        opacity: disabled ? 0.5 : 1,
      }}
    >
      <RadioGroup
        row
        value={section.contractType}
        onChange={handleTypeChange}
        sx={{
          "& .Mui-checked": {
            color: "gray",
          },
          mb: 1,
        }}
        disabled={disabled}
      >
        <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
        <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
        <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
      </RadioGroup>

      <Button
        variant="outlined"
        startIcon={<CloudUploadIcon />}
        component="span"
        sx={{
          mt: 1,
          color: "rgb(64,64,64)",
          borderColor: "rgb(64,64,64)",
          "&:hover": {
            borderColor: "black",
            color: "black",
          },
        }}
        disabled={disabled}
        onClick={() => {
          if (!disabled) {
            document.getElementById(`file-input-${section.id}`).click();
          }
        }}
      >
        Upload File
      </Button>
      <input
        type="file"
        id={`file-input-${section.id}`}
        style={{ display: "none" }}
        accept=".pdf,.docx"
        onChange={(e) => {
          const file = e.target.files[0];
          onFileChange(section.id, file);
          e.target.value = null; // reset input
        }}
        disabled={disabled}
      />
      {section.file && (
        <Typography variant="body2" mt={1}>
          Selected file: {section.file.name}
        </Typography>
      )}
    </Paper>
  );
}

export default function Request() {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [compare, setCompare] = useState(false);
  const [direction, setDirection] = useState("right"); // 'right' or 'left'
  const [collapsed, setCollapsed] = useState(false);
  const [approvedSections, setApprovedSections] = useState([
    {
      id: 1,
      contractType: "Agreement",
      file: null,
    },
  ]);

  // Handle autocomplete changes
  const handleSelect = (event, values) => {
    setSelectedOptions(values);
  };

  // Toggle direction left/right
  const toggleDirection = (dir) => {
    if (compare) {
      setDirection(dir);
    }
  };

  // Add approved contract section
  const addApprovedSection = () => {
    setApprovedSections((prev) => [
      ...prev,
      {
        id: prev.length ? prev[prev.length - 1].id + 1 : 1,
        contractType: "Agreement",
        file: null,
      },
    ]);
  };

  // Change contract type in approved contract section
  const changeContractType = (id, type) => {
    setApprovedSections((prev) =>
      prev.map((sec) =>
        sec.id === id ? { ...sec, contractType: type, file: null } : sec
      )
    );
  };

  // Change uploaded file in approved contract section
  const changeFile = (id, file) => {
    setApprovedSections((prev) =>
      prev.map((sec) => (sec.id === id ? { ...sec, file } : sec))
    );
  };

  // Remove the entire comparison (clear all selections and approved sections)
  const clearAll = () => {
    setSelectedOptions([]);
    setApprovedSections([
      {
        id: 1,
        contractType: "Agreement",
        file: null,
      },
    ]);
    setCompare(false);
  };

  // Toggle compare checkbox
  const toggleCompare = () => {
    if (compare) {
      clearAll();
    } else {
      setCompare(true);
    }
  };

  // Styles for outlines depending on direction and compare enabled (flipped)
  const getOutlineColor = (box) => {
    if (!compare) return "lightgray";
    if (direction === "right") {
      if (box === 1) return "darkgray"; // flipped
      if (box === 2) return "lightgray";
    }
    if (direction === "left") {
      if (box === 1) return "lightgray"; // flipped
      if (box === 2) return "darkgray";
    }
    return "lightgray";
  };

  // Styles for arrow colors depending on selected direction and compare enabled
  const arrowColor = (arrowDirection) => {
    if (!compare) return "lightgray";
    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
  };

  return (
    <Box sx={{ width: "100%", maxWidth: 900, m: "auto", mt: 4 }}>
      <Paper variant="outlined" sx={{ p: 2 }}>
        {/* Compare Checkbox on top left */}
        <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
          <FormControlLabel
            control={
              <Checkbox
                checked={compare}
                onChange={toggleCompare}
                sx={{
                  color: "gray",
                  "&.Mui-checked": {
                    color: "gray",
                  },
                }}
              />
            }
            label="Compare"
          />
        </Box>

        {/* Collapsible container */}
        <Collapse in={!collapsed}>
          <Stack
            direction="row"
            spacing={2}
            alignItems="center"
            justifyContent="center"
            sx={{ mb: 1 }}
          >
            {/* Left Box */}
            <Box
              sx={{
                flex: 1,
                minHeight: 280,
                border: `2px solid ${getOutlineColor(1)}`,
                p: 2,
                borderRadius: 1,
                overflowY: "auto",
                opacity: compare ? 1 : 0.5,
              }}
            >
              <Typography variant="h6" gutterBottom>
                Pscerf Data
              </Typography>

              <Autocomplete
                multiple
                options={options}
                getOptionLabel={(option) =>
                  `${option.id} - client: ${option.clientName}, SAM: ${option.samVersion}, Pricing: ${option.pricingVersion}`
                }
                value={selectedOptions}
                onChange={handleSelect}
                filterSelectedOptions
                disabled={!compare}
                renderInput={(params) => (
                  <TextField {...params} label="Select PSCRF IDs" variant="outlined" />
                )}
                sx={{ mb: 2 }}
              />

              {/* Cards for selected options */}
              {selectedOptions.map((opt) => (
                <Card key={`${opt.id}-${opt.samVersion}`} sx={{ mb: 1 }}>
                  <CardContent>
                    <Typography variant="body2">
                      <strong>id:</strong> {opt.id}, <strong>clientName:</strong>{" "}
                      {opt.clientName}, <strong>SAM Version:</strong> {opt.samVersion},{" "}
                      <strong>Pricing Version:</strong> {opt.pricingVersion}
                    </Typography>
                  </CardContent>
                </Card>
              ))}
            </Box>

            {/* Middle: arrows and X */}
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 1,
                position: "relative",
              }}
            >
              {/* X near arrows top center */}
              {compare && (
                <Tooltip title="Clear Comparison">
                  <IconButton
                    aria-label="clear comparison"
                    onClick={clearAll}
                    size="small"
                    sx={{
                      position: "absolute",
                      top: -24,
                      bgcolor: "white",
                      border: "1px solid gray",
                      "&:hover": { bgcolor: "#eee" },
                    }}
                  >
                    <CloseIcon fontSize="small" />
                  </IconButton>
                </Tooltip>
              )}

              {/* Left arrow */}
              <IconButton
                onClick={() => toggleDirection("left")}
                sx={{ color: arrowColor("left") }}
                disabled={!compare}
              >
                ←
              </IconButton>

              {/* Right arrow */}
              <IconButton
                onClick={() => toggleDirection("right")}
                sx={{ color: arrowColor("right") }}
                disabled={!compare}
              >
                →
              </IconButton>
            </Box>

            {/* Right Box */}
            <Box
              sx={{
                flex: 1,
                minHeight: 280,
                border: `2px solid ${getOutlineColor(2)}`,
                p: 2,
                borderRadius: 1,
                overflowY: "auto",
                opacity: compare ? 1 : 0.5,
              }}
            >
              <Typography variant="h6" gutterBottom>
                Approved Contract
              </Typography>

              {/* Render all approved contract sections */}
              {approvedSections.map((section) => (
                <ApprovedContractSection
                  key={section.id}
                  section={section}
                  onTypeChange={changeContractType}
                  onFileChange={changeFile}
                  disabled={!compare}
                />
              ))}

              {/* Plus (+) button to add section */}
              <Button
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={addApprovedSection}
                disabled={!compare}
                sx={{
                  color: "rgb(64,64,64)",
                  borderColor: "rgb(64,64,64)",
                  "&:hover": {
                    borderColor: "black",
                    color: "black",
                  },
                  mt: 1,
                }}
              >
                Add Section
              </Button>
            </Box>
          </Stack>
        </Collapse>

        {/* Collapse/Expand toggle below arrows */}
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 1,
            mt: 1,
            userSelect: "none",
          }}
        >
          <Button
            size="small"
            variant="outlined"
            startIcon={collapsed ? <AddIcon /> : <RemoveIcon />}
            onClick={() => setCollapsed(!collapsed)}
            sx={{
              minWidth: 32,
              color: "gray",
              borderColor: "gray",
              "&:hover": {
                borderColor: "black",
                color: "black",
              },
            }}
          />
          {collapsed && (
            <Typography
              variant="body2"
              sx={{ color: "gray", userSelect: "none" }}
            >
              Compare Pscrf and Approved contract
            </Typography>
          )}
        </Box>
      </Paper>
    </Box>
  );
}

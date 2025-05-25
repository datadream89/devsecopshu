import React, { useState } from "react";
import {
  Box,
  Button,
  Checkbox,
  Collapse,
  FormControlLabel,
  IconButton,
  Paper,
  Radio,
  RadioGroup,
  Stack,
  Typography,
  Autocomplete,
  TextField,
  Card,
  CardContent,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import ArrowRightAltIcon from "@mui/icons-material/ArrowRightAlt";
import ArrowLeftIcon from "@mui/icons-material/ArrowLeft";

const options = [
  {
    id: "7",
    samVersion: "v1.0",
    pricingVersion: "pv1.1",
    clientName: "Client A",
  },
  {
    id: "5",
    samVersion: "v2.0",
    pricingVersion: "pv2.1",
    clientName: "Client B",
  },
  {
    id: "7",
    samVersion: "v1.1",
    pricingVersion: "pv1.2",
    clientName: "Client A",
  },
];

function ApprovedContractSection({
  section,
  onTypeChange,
  onFileChange,
  onRemove,
  disabled,
  isFirst,
}) {
  const handleTypeChange = (e) => {
    onTypeChange(section.id, e.target.value);
    onFileChange(section.id, null); // clear file on radio change
  };

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        mb: 1,
        opacity: disabled ? 0.5 : 1,
        position: "relative",
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

      {!isFirst && !disabled && (
        <IconButton
          aria-label="remove section"
          onClick={() => onRemove(section.id)}
          size="small"
          sx={{ position: "absolute", top: 8, right: 8 }}
        >
          ✕
        </IconButton>
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

  // Direction toggle
  const toggleDirection = () => {
    setDirection(direction === "right" ? "left" : "right");
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

  // Remove approved contract section
  const removeApprovedSection = (id) => {
    setApprovedSections((prev) => prev.filter((sec) => sec.id !== id));
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

  // Toggle compare checkbox
  const toggleCompare = () => {
    setCompare(!compare);
    if (compare) {
      // If turning off compare, reset direction outline and such if needed
    }
  };

  // Styles for outlines depending on direction and compare enabled
  const getOutlineColor = (box) => {
    if (!compare) return "lightgray";
    if (direction === "right") {
      if (box === 1) return "lightgray";
      if (box === 2) return "darkgray";
    }
    if (direction === "left") {
      if (box === 1) return "darkgray";
      if (box === 2) return "lightgray";
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
        {/* Compare Checkbox on left */}
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
            {/* Box 1 */}
            <Box
              sx={{
                flex: 1,
                minHeight: 280,
                border: `2px solid ${getOutlineColor(1)}`,
                p: 2,
                borderRadius: 1,
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

              {/* Render cards for each selected */}
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

            {/* Arrows and toggle direction */}
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 1,
              }}
            >
              <IconButton
                size="small"
                onClick={toggleDirection}
                sx={{ color: arrowColor("right") }}
                disabled={!compare}
                aria-label="Toggle direction"
              >
                {direction === "right" ? <ArrowRightAltIcon /> : <ArrowLeftIcon />}
              </IconButton>

              {/* Plus and minus buttons under arrows */}
              <Box sx={{ mt: 1, display: "flex", alignItems: "center", gap: 1 }}>
                {/* Show + only when collapsed */}
                {collapsed && (
                  <IconButton
                    size="small"
                    onClick={() => setCollapsed(false)}
                    aria-label="Expand"
                  >
                    <AddIcon />
                  </IconButton>
                )}
                {!collapsed && (
                  <IconButton
                    size="small"
                    onClick={() => setCollapsed(true)}
                    aria-label="Collapse"
                  >
                    <RemoveIcon />
                  </IconButton>
                )}
              </Box>
            </Box>

            {/* Box 2 */}
            <Box
              sx={{
                flex: 1,
                minHeight: 280,
                border: `2px solid ${getOutlineColor(2)}`,
                p: 2,
                borderRadius: 1,
              }}
            >
              <Typography variant="h6" gutterBottom>
                Approved Contract
              </Typography>

              {approvedSections.map((section, index) => (
                <ApprovedContractSection
                  key={section.id}
                  section={section}
                  onTypeChange={changeContractType}
                  onFileChange={changeFile}
                  onRemove={removeApprovedSection}
                  disabled={!compare}
                  isFirst={index === 0}
                />
              ))}

              <Box sx={{ mt: 1 }}>
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<AddIcon />}
                  onClick={addApprovedSection}
                  disabled={!compare}
                >
                  Add Section
                </Button>
              </Box>
            </Box>
          </Stack>
        </Collapse>

        {/* Collapsed label and expand button */}
        {collapsed && (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              gap: 1,
              mt: 1,
              justifyContent: "center",
            }}
          >
            <Typography>Compare Pscrf and Approved contract</Typography>
            <IconButton
              size="small"
              onClick={() => setCollapsed(false)}
              aria-label="Expand"
            >
              <AddIcon />
            </IconButton>
          </Box>
        )}
      </Paper>
    </Box>
  );
}

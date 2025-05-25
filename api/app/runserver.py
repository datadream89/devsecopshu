import React, { useState } from "react";
import {
  Box,
  Typography,
  Checkbox,
  FormControlLabel,
  Autocomplete,
  TextField,
  Card,
  IconButton,
  Button,
  RadioGroup,
  Radio,
  FormControl,
  FormLabel,
  Stack,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";

import options from "./options.json"; // Adjust path as needed

export default function Request() {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [compare, setCompare] = useState(false);
  const [direction, setDirection] = useState(null); // 'left' or 'right'
  const [collapsed, setCollapsed] = useState(false);

  // Approved Contract Sections state
  const [sections, setSections] = useState([
    {
      id: 1,
      contractType: "Agreement",
      file: null,
    },
  ]);

  // Handle dropdown selection
  const handleSelectOption = (event, values) => {
    setSelectedOptions(values);
  };

  // Remove selected option card
  const handleRemoveOption = (optionToRemove) => {
    setSelectedOptions((prev) =>
      prev.filter(
        (opt) =>
          !(
            opt.id === optionToRemove.id &&
            opt.samVersion === optionToRemove.samVersion &&
            opt.pricingVersion === optionToRemove.pricingVersion
          )
      )
    );
  };

  // Toggle compare checkbox
  const handleCompareToggle = () => {
    setCompare((prev) => !prev);
    if (compare) {
      setDirection(null);
    }
  };

  // Toggle direction and outlines
  const handleDirection = (dir) => {
    setDirection(dir);
  };

  // Collapse / Expand container
  const toggleCollapse = () => {
    setCollapsed((prev) => !prev);
  };

  // Handle contract type change & clear file
  const handleTypeChange = (id, value) => {
    setSections((prev) =>
      prev.map((sec) =>
        sec.id === id ? { ...sec, contractType: value, file: null } : sec
      )
    );
  };

  // Handle file upload change
  const handleFileChange = (id, e) => {
    const file = e.target.files[0] || null;
    if (file && !["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"].includes(file.type)) {
      alert("Only PDF and DOCX files are allowed.");
      e.target.value = null;
      return;
    }
    setSections((prev) =>
      prev.map((sec) => (sec.id === id ? { ...sec, file } : sec))
    );
  };

  // Add new approved contract section
  const addSection = () => {
    const newId = sections.length > 0 ? Math.max(...sections.map((s) => s.id)) + 1 : 1;
    setSections((prev) => [...prev, { id: newId, contractType: "Agreement", file: null }]);
  };

  // Remove a section by id
  const removeSection = (id) => {
    setSections((prev) => prev.filter((sec) => sec.id !== id));
  };

  // Filter options for Autocomplete
  const filterOptions = (options, state) => {
    const input = state.inputValue.toLowerCase();
    return options.filter(
      (opt) =>
        opt.id.toLowerCase().includes(input) ||
        opt.clientName.toLowerCase().includes(input) ||
        opt.samVersion.toLowerCase().includes(input) ||
        opt.pricingVersion.toLowerCase().includes(input)
    );
  };

  return (
    <Box sx={{ maxWidth: 900, mx: "auto", mt: 4, fontFamily: "Roboto, sans-serif" }}>
      <Box
        sx={{
          border: "1px solid #999",
          borderRadius: 2,
          p: 2,
          userSelect: "none",
          backgroundColor: "#fafafa",
        }}
      >
        {/* Collapse Header */}
        {collapsed ? (
          <Box
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-start",
              gap: 1,
              cursor: "pointer",
              pb: 1,
            }}
            onClick={toggleCollapse}
          >
            <Button size="small" variant="outlined" sx={{ minWidth: 0, px: 1 }}>
              +
            </Button>
            <Typography variant="subtitle1" color="textSecondary" sx={{ userSelect: "none" }}>
              Compare Pscrf and Approved contract
            </Typography>
          </Box>
        ) : (
          <>
            {/* Top row: Compare checkbox + two boxes + arrows + close X */}
            <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 2 }}>
              {/* Compare checkbox */}
              <FormControlLabel
                control={
                  <Checkbox
                    checked={compare}
                    onChange={handleCompareToggle}
                    sx={{
                      color: compare ? "rgb(64,64,64)" : "lightgray",
                      "&.Mui-checked": { color: "rgb(64,64,64)" },
                    }}
                  />
                }
                label="Compare"
                sx={{ userSelect: "none" }}
              />

              {/* Boxes container */}
              <Box
                sx={{
                  display: "flex",
                  flexGrow: 1,
                  gap: 2,
                  alignItems: "center",
                  justifyContent: "space-between",
                }}
              >
                {/* Box 1: PSCRF Data */}
                <Box
                  sx={{
                    flex: 1,
                    minHeight: 300,
                    border: `3px solid ${
                      !compare
                        ? "lightgray"
                        : direction === "left"
                        ? "lightgray"
                        : "darkgray"
                    }`,
                    borderRadius: 2,
                    p: 2,
                    bgcolor: "white",
                    display: "flex",
                    flexDirection: "column",
                    opacity: compare ? 1 : 0.5,
                    pointerEvents: compare ? "auto" : "none",
                  }}
                >
                  <Typography variant="h6" gutterBottom>
                    PSCRF Data
                  </Typography>

                  {/* Dropdown */}
                  <Autocomplete
                    multiple
                    options={options}
                    getOptionLabel={(opt) =>
                      `${opt.id} (Client: ${opt.clientName}, SAM: ${opt.samVersion}, Pricing: ${opt.pricingVersion})`
                    }
                    value={selectedOptions}
                    filterOptions={filterOptions}
                    onChange={handleSelectOption}
                    disabled={!compare}
                    renderInput={(params) => (
                      <TextField {...params} label="Select PSCRF IDs" placeholder="Search..." />
                    )}
                    sx={{ mb: 2 }}
                  />

                  {/* Cards container */}
                  <Box
                    sx={{
                      flexGrow: 1,
                      overflowY: "auto",
                    }}
                  >
                    {selectedOptions.map((option) => (
                      <Card
                        key={`${option.id}-${option.samVersion}-${option.pricingVersion}`}
                        sx={{
                          mb: 1,
                          p: 1,
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          opacity: compare ? 1 : 0.5,
                          pointerEvents: compare ? "auto" : "none",
                        }}
                      >
                        <Typography variant="body2" sx={{ flexGrow: 1 }}>
                          ID: {option.id}, Client: {option.clientName}, SAM: {option.samVersion}, Pricing:{" "}
                          {option.pricingVersion}
                        </Typography>
                        <IconButton
                          size="small"
                          onClick={() => handleRemoveOption(option)}
                          aria-label="remove"
                          disabled={!compare}
                        >
                          <CloseIcon fontSize="small" />
                        </IconButton>
                      </Card>
                    ))}
                  </Box>
                </Box>

                {/* Arrows between boxes */}
                <Box
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    gap: 1,
                    userSelect: "none",
                  }}
                >
                  <IconButton
                    size="small"
                    onClick={() => handleDirection("left")}
                    sx={{
                      color:
                        direction === "left"
                          ? "darkgray"
                          : !compare
                          ? "lightgray"
                          : "gray",
                      bgcolor: "transparent",
                      "&:hover": { bgcolor: "transparent" },
                      p: 0.5,
                    }}
                    disabled={!compare}
                    aria-label="arrow to left"
                  >
                    <ArrowBackIosNewIcon />
                  </IconButton>
                  <IconButton
                    size="small"
                    onClick={() => handleDirection("right")}
                    sx={{
                      color:
                        direction === "right"
                          ? "darkgray"
                          : !compare
                          ? "lightgray"
                          : "gray",
                      bgcolor: "transparent",
                      "&:hover": { bgcolor: "transparent" },
                      p: 0.5,
                    }}
                    disabled={!compare}
                    aria-label="arrow to right"
                  >
                    <ArrowForwardIosIcon />
                  </IconButton>
                </Box>

                {/* Box 2: Approved Contract */}
                <Box
                  sx={{
                    flex: 1,
                    minHeight: 300,
                    border: `3px solid ${
                      !compare
                        ? "lightgray"
                        : direction === "right"
                        ? "lightgray"
                        : "darkgray"
                    }`,
                    borderRadius: 2,
                    p: 2,
                    bgcolor: "white",
                    display: "flex",
                    flexDirection: "column",
                    opacity: compare ? 1 : 0.5,
                    pointerEvents: compare ? "auto" : "none",
                  }}
                >
                  <Typography variant="h6" gutterBottom>
                    Approved Contract
                  </Typography>

                  {/* Sections with contract types and upload */}
                  {sections.map((section, index) => (
                    <Box
                      key={section.id}
                      sx={{
                        border: "1px solid #ccc",
                        borderRadius: 1,
                        p: 1,
                        mb: 2,
                        position: "relative",
                        bgcolor: "whitesmoke",
                      }}
                    >
                      {/* Remove Section X - only if more than 1 */}
                      {sections.length > 1 && (
                        <IconButton
                          size="small"
                          onClick={() => removeSection(section.id)}
                          sx={{
                            position: "absolute",
                            top: 4,
                            right: 4,
                          }}
                          aria-label="remove section"
                          disabled={!compare}
                        >
                          <CloseIcon fontSize="small" />
                        </IconButton>
                      )}

                      <FormControl
                        component="fieldset"
                        disabled={!compare}
                        sx={{ mb: 1 }}
                      >
                        <FormLabel component="legend">Contract Type</FormLabel>
                        <RadioGroup
                          row
                          value={section.contractType}
                          onChange={(e) =>
                            handleTypeChange(section.id, e.target.value)
                          }
                          sx={{
                            "& .Mui-checked": { color: "gray" },
                          }}
                        >
                          {["Agreement", "MOU", "NDA"].map((type) => (
                            <FormControlLabel
                              key={type}
                              value={type}
                              control={<Radio />}
                              label={type}
                              sx={{
                                color:
                                  section.contractType === type
                                    ? "gray"
                                    : "inherit",
                              }}
                            />
                          ))}
                        </RadioGroup>
                      </FormControl>

                      {/* File Upload */}
                      <Button
                        variant="contained"
                        component="label"
                        startIcon={<CloudUploadIcon />}
                        disabled={!compare}
                        sx={{
                          bgcolor: "darkgray",
                          "&:hover": { bgcolor: "dimgray" },
                          textTransform: "none",
                        }}
                      >
                        {section.file ? section.file.name : "Upload File"}
                        <input
                          type="file"
                          hidden
                          accept=".pdf, .docx"
                          onChange={(e) => handleFileChange(section.id, e)}
                          key={section.id + "-" + (section.file?.name || "none")} // reset input on file change or clear
                        />
                      </Button>
                    </Box>
                  ))}

                  {/* Add section button */}
                  <Button
                    onClick={addSection}
                    disabled={!compare}
                    size="small"
                    variant="outlined"
                    sx={{ mt: 1 }}
                  >
                    + Add Section
                  </Button>
                </Box>
              </Box>

              {/* Close X button between the boxes (centered vertically) */}
              <Box
                sx={{
                  position: "relative",
                  display: "flex",
                  justifyContent: "center",
                  width: 30,
                  userSelect: "none",
                  alignItems: "center",
                  ml: 1,
                }}
              >
                <IconButton
                  aria-label="close"
                  size="small"
                  sx={{ p: 0 }}
                  disabled={!compare}
                  onClick={() => {
                    setSelectedOptions([]);
                    setSections([{ id: 1, contractType: "Agreement", file: null }]);
                    setDirection(null);
                    setCompare(false);
                  }}
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              </Box>
            </Box>

            {/* Collapse/Expand buttons */}
            <Box sx={{ display: "flex", justifyContent: "center", gap: 1 }}>
              <Button
                size="small"
                variant="outlined"
                onClick={() => setCollapsed(true)}
                sx={{ minWidth: 0, px: 1 }}
              >
                -
              </Button>
              <Button
                size="small"
                variant="outlined"
                onClick={toggleCollapse}
                sx={{ minWidth: 0, px: 1 }}
              >
                +
              </Button>
            </Box>
          </>
        )}
      </Box>
    </Box>
  );
}

import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  Checkbox,
  FormControlLabel,
  Stack,
  Card,
  CardContent,
  Autocomplete,
  TextField,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const titles = ["Section 1", "Section 2", "Section 3", "Section 4"];

const pscrfData = [
  { id: "PSCRF001", samVersion: "v1.2", pricingVersion: "p3.4", clientName: "Client A" },
  { id: "PSCRF002", samVersion: "v2.1", pricingVersion: "p2.8", clientName: "Client B" },
  { id: "PSCRF003", samVersion: "v1.5", pricingVersion: "p4.0", clientName: "Client C" },
];

// PSCRF Section Component
function PSCRFSection() {
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleRemove = (id) => {
    setSelectedOptions((prev) => prev.filter((option) => option.id !== id));
  };

  return (
    <Box
      sx={{
        height: "100%",
        bgcolor: "#e9f0ff",
        borderRadius: 2,
        p: 1,
        overflowY: "auto",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Autocomplete
        multiple
        options={pscrfData}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        value={selectedOptions}
        onChange={(event, newValue) => setSelectedOptions(newValue)}
        renderInput={(params) => (
          <TextField {...params} label="Search PSCRF" variant="outlined" size="small" />
        )}
        sx={{ mb: 1 }}
      />

      <Box
        sx={{
          maxHeight: 230,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 1,
        }}
      >
        {selectedOptions.map((option) => (
          <Card
            key={option.id}
            variant="outlined"
            sx={{ position: "relative", bgcolor: "#dbe9ff" }}
          >
            <CardContent sx={{ pr: 5 }}>
              <Typography variant="subtitle1" fontWeight="bold">
                {option.id}
              </Typography>
              <Typography variant="body2">Sam Version: {option.samVersion}</Typography>
              <Typography variant="body2">Pricing Version: {option.pricingVersion}</Typography>
              <Typography variant="body2">Client: {option.clientName}</Typography>
            </CardContent>

            <IconButton
              size="small"
              onClick={() => handleRemove(option.id)}
              sx={{ position: "absolute", top: 4, right: 4 }}
              aria-label="remove"
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Card>
        ))}
      </Box>
    </Box>
  );
}

// Approved Contract Section
function ApprovedContractSection() {
  return (
    <Box
      sx={{
        height: "100%",
        bgcolor: "#fff7e6",
        borderRadius: 2,
        p: 2,
        overflowY: "auto",
      }}
    >
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Approved Contract
      </Typography>
      <Typography variant="body2">Content for Approved Contract goes here.</Typography>
    </Box>
  );
}

// Signed Contract Section
function SignedContractSection() {
  return (
    <Box
      sx={{
        height: "100%",
        bgcolor: "#e6fff7",
        borderRadius: 2,
        p: 2,
        overflowY: "auto",
      }}
    >
      <Typography variant="h6" fontWeight="bold" gutterBottom>
        Signed Contract
      </Typography>
      <Typography variant="body2">Content for Signed Contract goes here.</Typography>
    </Box>
  );
}

// Main component
export default function BoxPairs() {
  // Expanded/collapsed state per row
  const [expanded, setExpanded] = useState([true, true, true, true]);

  // Highlight state per row and side ('left' and 'right' booleans)
  const [highlight, setHighlight] = useState(
    Array(4)
      .fill(0)
      .map(() => ({ left: false, right: false }))
  );

  // Compare checkbox state per row
  const [compareChecked, setCompareChecked] = useState(Array(4).fill(true));

  // Toggle collapse/expand title bar
  const toggleExpand = (index) => {
    const newExpanded = [...expanded];
    newExpanded[index] = !newExpanded[index];
    setExpanded(newExpanded);
  };

  // Toggle highlight on arrows (independent for left/right)
  const toggleHighlight = (index, side) => {
    setHighlight((prev) =>
      prev.map((item, idx) => {
        if (idx === index) {
          return { ...item, [side]: !item[side] };
        }
        return item;
      })
    );
  };

  // Toggle compare checkbox
  const toggleCompare = (index) => {
    const updated = [...compareChecked];
    updated[index] = !updated[index];
    setCompareChecked(updated);
  };

  // Content map for each row and side
  // Row 0: left=PSCRF, right=Approved Contract
  // Row 1: left=Approved Contract, right=Signed Contract
  // Row 2: left=PSCRF, right=Signed Contract
  // Row 3: left=PSCRF, right=PSCRF
  const boxContentMap = {
    0: { left: <PSCRFSection />, right: <ApprovedContractSection /> },
    1: { left: <ApprovedContractSection />, right: <SignedContractSection /> },
    2: { left: <PSCRFSection />, right: <SignedContractSection /> },
    3: { left: <PSCRFSection />, right: <PSCRFSection /> },
  };

  return (
    <Box sx={{ maxWidth: 1000, mx: "auto", mt: 4, userSelect: "none" }}>
      {titles.map((title, rowIndex) => (
        <Box key={rowIndex} sx={{ mb: 5 }}>
          {/* Title bar */}
          <Box
            sx={{
              bgcolor: "#ccc",
              px: 2,
              py: 1.5,
              fontWeight: "bold",
              borderRadius: 1,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 2,
              userSelect: "none",
              cursor: "pointer",
              boxShadow: 1,
            }}
            onClick={() => toggleExpand(rowIndex)}
          >
            <Typography>{title}</Typography>
            <IconButton
              size="small"
              edge="end"
              aria-label="toggle expand"
              onClick={(e) => {
                e.stopPropagation();
                toggleExpand(rowIndex);
              }}
            >
              {expanded[rowIndex] ? (
                <CloseIcon fontSize="small" />
              ) : (
                <AddIcon fontSize="small" />
              )}
            </IconButton>
          </Box>

          {/* Boxes & controls, shown only if expanded */}
          {expanded[rowIndex] && (
            <Box
              sx={{
                border: "1px solid #ccc",
                borderRadius: 1,
                bgcolor: "#f0f4ff",
                boxShadow: 1,
                p: 2,
              }}
            >
              <Stack
                direction="row"
                spacing={2}
                alignItems="center"
                sx={{ position: "relative" }}
              >
                {/* Compare checkbox left of pair */}
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={compareChecked[rowIndex]}
                      onChange={() => toggleCompare(rowIndex)}
                    />
                  }
                  label="Compare"
                  sx={{ userSelect: "none" }}
                />

                {/* Left box */}
                <Box
                  sx={{
                    width: 320,
                    height: 320,
                    border: 2,
                    borderColor:
                      highlight[rowIndex]?.left && compareChecked[rowIndex]
                        ? "gray"
                        : highlight[rowIndex]?.right && compareChecked[rowIndex]
                        ? "lightgray"
                        : "#ccc",
                    borderRadius: 2,
                    p: 1.5,
                    overflowY: "auto",
                    bgcolor: compareChecked[rowIndex] ? "#fff" : "#eee",
                    color: compareChecked[rowIndex] ? "inherit" : "gray",
                    filter: compareChecked[rowIndex] ? "none" : "grayscale(1)",
                    transition: "all 0.3s ease",
                    pointerEvents: compareChecked[rowIndex] ? "auto" : "none",
                  }}
                >
                  {boxContentMap[rowIndex].left}
                </Box>

                {/* Arrows between */}
                <Stack spacing={1} alignItems="center" sx={{ userSelect: "none" }}>
                  <ArrowBackIcon
                    onClick={() => toggleHighlight(rowIndex, "left")}
                    sx={{
                      cursor: "pointer",
                      fontSize: 36,
                      color:
                        highlight[rowIndex]?.left && compareChecked[rowIndex]
                          ? "#424242"
                          : "lightgray",
                      userSelect: "none",
                    }}
                    aria-label={`Highlight left arrow row ${rowIndex + 1}`}
                  />
                  <ArrowForwardIcon
                    onClick={() => toggleHighlight(rowIndex, "right")}
                    sx={{
                      cursor: "pointer",
                      fontSize: 36,
                      color:
                        highlight[rowIndex]?.right && compareChecked[rowIndex]
                          ? "#424242"
                          : "lightgray",
                      userSelect: "none",
                    }}
                    aria-label={`Highlight right arrow row ${rowIndex + 1}`}
                  />
                </Stack>

                {/* Right box */}
                <Box
                  sx={{
                    width: 320,
                    height: 320,
                    border: 2,
                    borderColor:
                      highlight[rowIndex]?.right && compareChecked[rowIndex]
                        ? "gray"
                        : highlight[rowIndex]?.left && compareChecked[rowIndex]
                        ? "lightgray"
                        : "#ccc",
                    borderRadius: 2,
                    p: 1.5,
                    overflowY: "auto",
                    bgcolor: compareChecked[rowIndex] ? "#fff" : "#eee",
                    color: compareChecked[rowIndex] ? "inherit" : "gray",
                    filter: compareChecked[rowIndex] ? "none" : "grayscale(1)",
                    transition: "all 0.3s ease",
                    pointerEvents: compareChecked[rowIndex] ? "auto" : "none",
                  }}
                >
                  {boxContentMap[rowIndex].right}
                </Box>
              </Stack>
            </Box>
          )}
        </Box>
      ))}
    </Box>
  );
}

import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  Collapse,
  Checkbox,
  FormControlLabel,
  Stack,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

// Dummy PSCRF data (you can replace with your real data or props)
const pscrfData = [
  { id: "PSCRF001", samVersion: "v1.2", pricingVersion: "p3.4", clientName: "Client A" },
  { id: "PSCRF002", samVersion: "v2.1", pricingVersion: "p2.8", clientName: "Client B" },
];

// PSCRFSection component - sample implementation
function PSCRFSection() {
  return (
    <Box>
      {pscrfData.map((pscrf) => (
        <Box
          key={pscrf.id}
          sx={{
            border: "1px solid #ccc",
            borderRadius: 1,
            p: 1,
            mb: 1,
            backgroundColor: "#e3f2fd",
          }}
        >
          <Typography variant="subtitle2" fontWeight="bold">
            {pscrf.id}
          </Typography>
          <Typography variant="body2">Sam Version: {pscrf.samVersion}</Typography>
          <Typography variant="body2">Pricing Version: {pscrf.pricingVersion}</Typography>
          <Typography variant="body2">Client: {pscrf.clientName}</Typography>
        </Box>
      ))}
    </Box>
  );
}

export default function BoxPairs() {
  const titles = ["Row 1", "Row 2", "Row 3", "Row 4"];
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  const [highlight, setHighlight] = useState(Array(4).fill(null)); // 'left' | 'right' | null
  const [compareChecked, setCompareChecked] = useState(Array(4).fill(true));

  const toggleCollapse = (index) => {
    const updated = [...collapsed];
    updated[index] = !updated[index];
    setCollapsed(updated);
  };

  const handleArrowClick = (index, direction) => {
    const updated = [...highlight];
    updated[index] = direction;
    setHighlight(updated);
  };

  const handleCheckboxChange = (index) => {
    const updated = [...compareChecked];
    updated[index] = !updated[index];
    setCompareChecked(updated);
  };

  return (
    <Box sx={{ maxWidth: "1200px", mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => (
        <Box key={idx} sx={{ mb: 6 }}>
          {/* Title Bar */}
          <Box
            sx={{
              width: "100%",
              bgcolor: "#e0e0e0",
              px: 3,
              py: 1.5,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              borderRadius: 1,
              border: "1px solid #bbb",
              mb: 1,
              cursor: "pointer",
            }}
            onClick={() => toggleCollapse(idx)}
          >
            <Typography variant="h6" fontWeight="bold">
              {title} (Pair {idx + 1})
            </Typography>
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                toggleCollapse(idx);
              }}
              aria-label={collapsed[idx] ? "Expand" : "Collapse"}
            >
              {collapsed[idx] ? <AddIcon /> : <CloseIcon />}
            </IconButton>
          </Box>

          {/* Compare checkbox */}
          <FormControlLabel
            control={
              <Checkbox
                checked={compareChecked[idx]}
                onChange={() => handleCheckboxChange(idx)}
              />
            }
            label="Compare"
            sx={{ mb: 1 }}
          />

          {/* Collapsible content */}
          <Collapse in={!collapsed[idx]}>
            <Stack
              direction="row"
              spacing={3}
              alignItems="center"
              justifyContent="center"
              sx={{ minHeight: 350 }}
            >
              {/* Left Box */}
              <Box
                sx={{
                  width: 550,
                  height: 300,
                  border: "2px solid",
                  borderColor:
                    highlight[idx] === "left"
                      ? "gray"
                      : highlight[idx] === "right"
                      ? "lightgray"
                      : "#ccc",
                  borderRadius: 2,
                  p: 3,
                  overflowY: "auto",
                  bgcolor: compareChecked[idx] ? "white" : "#f0f0f0",
                  color: compareChecked[idx] ? "inherit" : "gray",
                  pointerEvents: compareChecked[idx] ? "auto" : "none",
                  transition: "all 0.3s ease",
                }}
              >
                {/* Render PSCRFSection conditionally */}
                {(idx === 0 || idx === 3) ? (
                  <PSCRFSection />
                ) : (
                  <Typography variant="body1" fontWeight="medium">
                    Left Box Content (Pair {idx + 1})
                  </Typography>
                )}
              </Box>

              {/* Arrows */}
              <Stack spacing={1} alignItems="center">
                <ArrowBackIcon
                  onClick={() => handleArrowClick(idx, "left")}
                  sx={{
                    cursor: "pointer",
                    fontSize: 40,
                    color: highlight[idx] === "left" ? "#424242" : "#bdbdbd",
                    userSelect: "none",
                  }}
                />
                <ArrowForwardIcon
                  onClick={() => handleArrowClick(idx, "right")}
                  sx={{
                    cursor: "pointer",
                    fontSize: 40,
                    color: highlight[idx] === "right" ? "#424242" : "#bdbdbd",
                    userSelect: "none",
                  }}
                />
              </Stack>

              {/* Right Box */}
              <Box
                sx={{
                  width: 550,
                  height: 300,
                  border: "2px solid",
                  borderColor:
                    highlight[idx] === "right"
                      ? "gray"
                      : highlight[idx] === "left"
                      ? "lightgray"
                      : "#ccc",
                  borderRadius: 2,
                  p: 3,
                  overflowY: "auto",
                  bgcolor: compareChecked[idx] ? "white" : "#f0f0f0",
                  color: compareChecked[idx] ? "inherit" : "gray",
                  pointerEvents: compareChecked[idx] ? "auto" : "none",
                  transition: "all 0.3s ease",
                }}
              >
                {/* Render PSCRFSection conditionally */}
                {(idx === 2 || idx === 3) ? (
                  <PSCRFSection />
                ) : (
                  <Typography variant="body1" fontWeight="medium">
                    Right Box Content (Pair {idx + 1})
                  </Typography>
                )}
              </Box>
            </Stack>
          </Collapse>
        </Box>
      ))}
    </Box>
  );
}

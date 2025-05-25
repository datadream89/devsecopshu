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

// Dummy components
const PSCRFSection = () => (
  <Typography>PSCRF Section Content</Typography>
);

const ApprovedContractSection = () => (
  <Typography>Approved Contract Section Content</Typography>
);

const SignedContractSection = () => (
  <Typography>Signed Contract Section Content</Typography>
);

const titles = [
  "Pair 1",
  "Pair 2",
  "Pair 3",
  "Pair 4",
];

// Main component
export default function BoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  // highlight: 'left', 'right', or null for each pair
  const [highlight, setHighlight] = useState(Array(4).fill(null));
  // compare checkbox states for each pair
  const [compareChecked, setCompareChecked] = useState(Array(4).fill(true));

  const toggleCollapse = (index) => {
    const updated = [...collapsed];
    updated[index] = !updated[index];
    setCollapsed(updated);
  };

  const handleArrowClick = (index, direction) => {
    const updated = [...highlight];
    // Toggle if same direction clicked
    updated[index] = updated[index] === direction ? null : direction;
    setHighlight(updated);
  };

  const handleCompareChange = (index, checked) => {
    const updated = [...compareChecked];
    updated[index] = checked;
    setCompareChecked(updated);
  };

  // Helper to get border and arrow color based on highlight and compare
  const getColors = (pairIndex, side) => {
    if (!compareChecked[pairIndex]) {
      return { border: "#ccc", bg: "#f5f5f5", arrow: "#f0f0f0", textOpacity: 0.4 };
    }
    if (highlight[pairIndex] === side) {
      return { border: "#424242", bg: "#fff", arrow: "#424242", textOpacity: 1 };
    }
    if (highlight[pairIndex] === null) {
      return { border: "#ccc", bg: "#fff", arrow: "#bdbdbd", textOpacity: 1 };
    }
    // other side highlighted
    return { border: "#bdbdbd", bg: "#fff", arrow: "#bdbdbd", textOpacity: 1 };
  };

  return (
    <Box sx={{ maxWidth: "1100px", mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => {
        const leftColors = getColors(idx, "left");
        const rightColors = getColors(idx, "right");

        return (
          <Box key={idx} sx={{ mb: 5 }}>
            {/* Title bar */}
            <Box
              sx={{
                width: "100%",
                bgcolor: "#e0e0e0",
                px: 3,
                py: 1.5,
                borderRadius: 1,
                border: "1px solid #ccc",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                cursor: "pointer",
                userSelect: "none",
                mb: 1,
              }}
              onClick={() => toggleCollapse(idx)}
            >
              <Typography variant="h6" fontWeight="bold">
                {title}
              </Typography>
              <IconButton size="small" onClick={(e) => { e.stopPropagation(); toggleCollapse(idx); }}>
                {collapsed[idx] ? <AddIcon /> : <CloseIcon />}
              </IconButton>
            </Box>

            {/* Collapsible content */}
            <Collapse in={!collapsed[idx]}>
              <Stack direction="row" spacing={2} alignItems="center">
                {/* Compare checkbox */}
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={compareChecked[idx]}
                      onChange={(e) => handleCompareChange(idx, e.target.checked)}
                    />
                  }
                  label="Compare"
                  sx={{ whiteSpace: "nowrap", userSelect: "none" }}
                />

                {/* Left Box */}
                <Box
                  sx={{
                    width: 470,
                    height: 220,
                    border: `2px solid ${leftColors.border}`,
                    borderRadius: 2,
                    p: 3,
                    bgcolor: leftColors.bg,
                    opacity: leftColors.textOpacity,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    userSelect: "none",
                  }}
                >
                  {/* Render components based on row and side */}
                  {(idx === 0 || idx === 3) && <PSCRFSection />}
                  {idx === 1 && <ApprovedContractSection />}
                  {idx === 2 && <SignedContractSection />}
                </Box>

                {/* Arrows */}
                <Stack spacing={1} alignItems="center" sx={{ userSelect: "none" }}>
                  <ArrowBackIcon
                    onClick={() => handleArrowClick(idx, "left")}
                    sx={{
                      cursor: "pointer",
                      fontSize: 40,
                      color: leftColors.arrow,
                      userSelect: "none",
                    }}
                  />
                  <ArrowForwardIcon
                    onClick={() => handleArrowClick(idx, "right")}
                    sx={{
                      cursor: "pointer",
                      fontSize: 40,
                      color: rightColors.arrow,
                      userSelect: "none",
                    }}
                  />
                </Stack>

                {/* Right Box */}
                <Box
                  sx={{
                    width: 470,
                    height: 220,
                    border: `2px solid ${rightColors.border}`,
                    borderRadius: 2,
                    p: 3,
                    bgcolor: rightColors.bg,
                    opacity: rightColors.textOpacity,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    userSelect: "none",
                  }}
                >
                  {/* Render components based on row and side */}
                  {idx === 0 && <ApprovedContractSection />}
                  {idx === 1 && <SignedContractSection />}
                  {(idx === 2 || idx === 3) && <PSCRFSection />}
                </Box>
              </Stack>
            </Collapse>
          </Box>
        );
      })}
    </Box>
  );
}

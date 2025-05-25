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

const titles = [
  "Pair 1",
  "Pair 2",
  "Pair 3",
  "Pair 4",
];

export default function BoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(titles.length).fill(false));
  const [highlight, setHighlight] = useState(Array(titles.length).fill(null)); // 'left' | 'right' | null
  const [compareChecked, setCompareChecked] = useState(Array(titles.length).fill(true));

  const toggleCollapse = (index) => {
    const updated = [...collapsed];
    updated[index] = !updated[index];
    setCollapsed(updated);
  };

  const handleArrowClick = (index, direction) => {
    if (!compareChecked[index]) return; // disable if unchecked
    const updated = [...highlight];
    // Toggle arrow selection:
    updated[index] = updated[index] === direction ? null : direction;
    setHighlight(updated);
  };

  const handleCompareChange = (index) => {
    const newChecked = [...compareChecked];
    newChecked[index] = !newChecked[index];
    // If disabling compare, also clear arrow highlights
    if (!newChecked[index]) {
      const newHighlight = [...highlight];
      newHighlight[index] = null;
      setHighlight(newHighlight);
    }
    setCompareChecked(newChecked);
  };

  return (
    <Box sx={{ maxWidth: "1200px", mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => (
        <Box key={idx} sx={{ mb: 4 }}>
          {/* Title Bar */}
          <Box
            sx={{
              width: "100%",
              bgcolor: "#e0e0e0",
              px: 2,
              py: 1.5,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              borderRadius: 1,
              border: "1px solid #ccc",
              cursor: "pointer",
            }}
            onClick={() => toggleCollapse(idx)}
          >
            <Typography variant="h6" fontWeight="bold">
              {title}
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

          <Collapse in={!collapsed[idx]}>
            <Stack
              direction="row"
              spacing={2}
              alignItems="center"
              sx={{ mt: 2 }}
            >
              {/* Compare Checkbox */}
              <FormControlLabel
                control={
                  <Checkbox
                    checked={compareChecked[idx]}
                    onChange={() => handleCompareChange(idx)}
                    color="primary"
                  />
                }
                label="Compare"
                sx={{ whiteSpace: "nowrap", userSelect: "none" }}
              />

              {/* Left Box */}
              <Box
                sx={{
                  width: 500,
                  height: 300,
                  border: "2px solid",
                  borderColor:
                    highlight[idx] === "left"
                      ? "gray"
                      : highlight[idx] === "right"
                      ? "lightgray"
                      : "#ccc",
                  borderRadius: 2,
                  p: 2,
                  overflowY: "auto",
                  bgcolor: compareChecked[idx] ? "white" : "#f0f0f0",
                  color: compareChecked[idx] ? "inherit" : "gray",
                  pointerEvents: compareChecked[idx] ? "auto" : "none",
                  transition: "all 0.3s ease",
                }}
              >
                <Typography variant="body1" fontWeight="medium">
                  Left Box Content (Pair {idx + 1})
                </Typography>
              </Box>

              {/* Arrows */}
              <Stack spacing={2} alignItems="center" sx={{ mx: 1 }}>
                <ArrowBackIcon
                  onClick={() => handleArrowClick(idx, "left")}
                  sx={{
                    cursor: compareChecked[idx] ? "pointer" : "default",
                    fontSize: 36,
                    color:
                      compareChecked[idx] && highlight[idx] === "left"
                        ? "#424242"
                        : "#bdbdbd",
                    userSelect: "none",
                    transition: "color 0.3s ease",
                  }}
                />
                <ArrowForwardIcon
                  onClick={() => handleArrowClick(idx, "right")}
                  sx={{
                    cursor: compareChecked[idx] ? "pointer" : "default",
                    fontSize: 36,
                    color:
                      compareChecked[idx] && highlight[idx] === "right"
                        ? "#424242"
                        : "#bdbdbd",
                    userSelect: "none",
                    transition: "color 0.3s ease",
                  }}
                />
              </Stack>

              {/* Right Box */}
              <Box
                sx={{
                  width: 500,
                  height: 300,
                  border: "2px solid",
                  borderColor:
                    highlight[idx] === "right"
                      ? "gray"
                      : highlight[idx] === "left"
                      ? "lightgray"
                      : "#ccc",
                  borderRadius: 2,
                  p: 2,
                  overflowY: "auto",
                  bgcolor: compareChecked[idx] ? "white" : "#f0f0f0",
                  color: compareChecked[idx] ? "inherit" : "gray",
                  pointerEvents: compareChecked[idx] ? "auto" : "none",
                  transition: "all 0.3s ease",
                }}
              >
                <Typography variant="body1" fontWeight="medium">
                  Right Box Content (Pair {idx + 1})
                </Typography>
              </Box>
            </Stack>
          </Collapse>
        </Box>
      ))}
    </Box>
  );
}

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
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

const pairTitles = [
  "Pair 1",
  "Pair 2",
  "Pair 3",
  "Pair 4",
];

export default function BoxPairs() {
  // Manage collapse state of each pair
  const [collapsed, setCollapsed] = useState(Array(pairTitles.length).fill(false));
  
  // Manage checkbox checked state for each pair
  const [checked, setChecked] = useState(Array(pairTitles.length).fill(true));
  
  // Manage arrow selection: 'left' | 'right' | null for each pair (independent)
  const [leftArrowSelected, setLeftArrowSelected] = useState(Array(pairTitles.length).fill(false));
  const [rightArrowSelected, setRightArrowSelected] = useState(Array(pairTitles.length).fill(false));
  
  const toggleCollapse = (idx) => {
    const updated = [...collapsed];
    updated[idx] = !updated[idx];
    setCollapsed(updated);
  };
  
  const toggleCheckbox = (idx) => {
    const updated = [...checked];
    updated[idx] = !updated[idx];
    setChecked(updated);
  };
  
  // Arrow toggles independently
  const toggleLeftArrow = (idx) => {
    const updated = [...leftArrowSelected];
    updated[idx] = !updated[idx];
    setLeftArrowSelected(updated);
  };
  const toggleRightArrow = (idx) => {
    const updated = [...rightArrowSelected];
    updated[idx] = !updated[idx];
    setRightArrowSelected(updated);
  };
  
  return (
    <Box sx={{ maxWidth: 700, mx: "auto", mt: 4, mb: 4 }}>
      {pairTitles.map((title, idx) => {
        // Determine border colors for boxes based on arrow selection
        const leftBoxBorderColor = leftArrowSelected[idx]
          ? "#424242" // dark gray
          : rightArrowSelected[idx]
          ? "#bdbdbd" // light gray
          : "#ccc"; // default gray
        
        const rightBoxBorderColor = rightArrowSelected[idx]
          ? "#424242"
          : leftArrowSelected[idx]
          ? "#bdbdbd"
          : "#ccc";
        
        // Determine grayscale for boxes when unchecked
        const disabledOpacity = checked[idx] ? 1 : 0.4;
        
        return (
          <Box key={idx} sx={{ mb: 5 }}>
            {/* Title bar with collapse toggle */}
            <Box
              sx={{
                bgcolor: "#f5f5f5",
                px: 2,
                py: 1,
                mb: 1,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                borderRadius: 1,
                cursor: "pointer",
                userSelect: "none",
              }}
              onClick={() => toggleCollapse(idx)}
            >
              <Typography variant="h6" fontWeight="bold">{title}</Typography>
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

            {/* Collapsible content */}
            <Collapse in={!collapsed[idx]}>
              <Stack
                direction="row"
                spacing={2}
                alignItems="center"
                sx={{ width: "100%" }}
              >
                {/* Checkbox left */}
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={checked[idx]}
                      onChange={() => toggleCheckbox(idx)}
                    />
                  }
                  label="Compare"
                  sx={{ mr: 0 }}
                />

                {/* Left box */}
                <Box
                  sx={{
                    flex: 1,
                    height: 150,
                    border: "2px solid",
                    borderColor: leftBoxBorderColor,
                    borderRadius: 2,
                    bgcolor: "#fff",
                    opacity: disabledOpacity,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    userSelect: "none",
                  }}
                >
                  <Typography>Left Box</Typography>
                </Box>

                {/* Arrows in center */}
                <Stack spacing={2} alignItems="center" justifyContent="center">
                  <ArrowBackIcon
                    onClick={() => toggleLeftArrow(idx)}
                    sx={{
                      cursor: "pointer",
                      fontSize: 30,
                      color: leftArrowSelected[idx] ? "#424242" : "#bdbdbd",
                      userSelect: "none",
                    }}
                  />
                  <ArrowForwardIcon
                    onClick={() => toggleRightArrow(idx)}
                    sx={{
                      cursor: "pointer",
                      fontSize: 30,
                      color: rightArrowSelected[idx] ? "#424242" : "#bdbdbd",
                      userSelect: "none",
                    }}
                  />
                </Stack>

                {/* Right box */}
                <Box
                  sx={{
                    flex: 1,
                    height: 150,
                    border: "2px solid",
                    borderColor: rightBoxBorderColor,
                    borderRadius: 2,
                    bgcolor: "#fff",
                    opacity: disabledOpacity,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    userSelect: "none",
                  }}
                >
                  <Typography>Right Box</Typography>
                </Box>
              </Stack>
            </Collapse>
          </Box>
        );
      })}
    </Box>
  );
}

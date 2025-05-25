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
  const [collapsed, setCollapsed] = useState(Array(pairTitles.length).fill(false));
  const [checked, setChecked] = useState(Array(pairTitles.length).fill(true));
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
    <Box sx={{ maxWidth: 1200, mx: "auto", mt: 4, mb: 4 }}>
      {pairTitles.map((title, idx) => {
        const leftBoxBorderColor = leftArrowSelected[idx]
          ? "#424242"
          : rightArrowSelected[idx]
          ? "#bdbdbd"
          : "#ccc";

        const rightBoxBorderColor = rightArrowSelected[idx]
          ? "#424242"
          : leftArrowSelected[idx]
          ? "#bdbdbd"
          : "#ccc";

        const disabledOpacity = checked[idx] ? 1 : 0.4;

        return (
          <Box key={idx} sx={{ mb: 5 }}>
            {/* Title bar */}
            <Box
              sx={{
                width: "100%",
                maxWidth: 1200,
                bgcolor: "#f5f5f5",
                px: 3,
                py: 1.5,
                mb: 1,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                borderRadius: 1,
                cursor: "pointer",
                userSelect: "none",
                border: "1px solid #ccc",
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

            {/* Collapsible content */}
            <Collapse in={!collapsed[idx]}>
              <Stack
                direction="row"
                spacing={3}
                alignItems="center"
                sx={{ width: "100%", maxWidth: 1200 }}
              >
                {/* Checkbox */}
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={checked[idx]}
                      onChange={() => toggleCheckbox(idx)}
                    />
                  }
                  label="Compare"
                  sx={{ mr: 0, minWidth: 110 }}
                />

                {/* Left box */}
                <Box
                  sx={{
                    flex: 1,
                    height: 180,
                    border: "2px solid",
                    borderColor: leftBoxBorderColor,
                    borderRadius: 2,
                    bgcolor: "#fff",
                    opacity: disabledOpacity,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    userSelect: "none",
                    minWidth: 450,
                  }}
                >
                  <Typography>Left Box</Typography>
                </Box>

                {/* Arrows */}
                <Stack spacing={3} alignItems="center" justifyContent="center">
                  <ArrowBackIcon
                    onClick={() => toggleLeftArrow(idx)}
                    sx={{
                      cursor: "pointer",
                      fontSize: 36,
                      color: leftArrowSelected[idx] ? "#424242" : "#bdbdbd",
                      userSelect: "none",
                    }}
                  />
                  <ArrowForwardIcon
                    onClick={() => toggleRightArrow(idx)}
                    sx={{
                      cursor: "pointer",
                      fontSize: 36,
                      color: rightArrowSelected[idx] ? "#424242" : "#bdbdbd",
                      userSelect: "none",
                    }}
                  />
                </Stack>

                {/* Right box */}
                <Box
                  sx={{
                    flex: 1,
                    height: 180,
                    border: "2px solid",
                    borderColor: rightBoxBorderColor,
                    borderRadius: 2,
                    bgcolor: "#fff",
                    opacity: disabledOpacity,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    userSelect: "none",
                    minWidth: 450,
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

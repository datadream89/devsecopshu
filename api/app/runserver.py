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

const titles = ["Section 1", "Section 2", "Section 3", "Section 4"];

export default function BoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  const [highlight, setHighlight] = useState(Array(4).fill(null)); // 'left' | 'right' | null

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

  return (
    <Box sx={{ maxWidth: "1000px", mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => (
        <Box key={idx} sx={{ mb: 4, border: "1px solid #ccc", borderRadius: 1 }}>
          {/* Title Bar - 70% width and centered */}
          <Box
            sx={{
              width: "70%",
              mx: "auto",
              bgcolor: "#e0e0e0",
              px: 2,
              py: 1.5,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              borderBottom: "1px solid #ccc",
              borderRadius: 1,
            }}
            onClick={() => toggleCollapse(idx)}
          >
            <Typography variant="subtitle1" fontWeight="bold">
              {title}
            </Typography>
            <IconButton size="small">
              {collapsed[idx] ? <AddIcon /> : <CloseIcon />}
            </IconButton>
          </Box>

          {/* Collapsible content */}
          <Collapse in={!collapsed[idx]}>
            <Box sx={{ p: 3, bgcolor: "#fff" }}>
              <Stack direction="row" spacing={2} alignItems="center">
                {/* Compare checkbox */}
                <FormControlLabel
                  control={<Checkbox />}
                  label="Compare"
                  sx={{ whiteSpace: "nowrap" }}
                />

                {/* Left box */}
                <Box
                  sx={{
                    width: 300,
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
                  }}
                ></Box>

                {/* Arrows */}
                <Stack spacing={2} alignItems="center">
                  <IconButton
                    onClick={() => handleArrowClick(idx, "left")}
                    sx={{
                      bgcolor:
                        highlight[idx] === "left" ? "#424242" : "#e0e0e0",
                      color: highlight[idx] === "left" ? "#fff" : "#000",
                    }}
                  >
                    <ArrowBackIcon />
                  </IconButton>
                  <IconButton
                    onClick={() => handleArrowClick(idx, "right")}
                    sx={{
                      bgcolor:
                        highlight[idx] === "right" ? "#424242" : "#e0e0e0",
                      color: highlight[idx] === "right" ? "#fff" : "#000",
                    }}
                  >
                    <ArrowForwardIcon />
                  </IconButton>
                </Stack>

                {/* Right box */}
                <Box
                  sx={{
                    width: 300,
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
                  }}
                ></Box>
              </Stack>
            </Box>
          </Collapse>
        </Box>
      ))}
    </Box>
  );
}

import React, { useState } from "react";
import {
  Box,
  Checkbox,
  Collapse,
  IconButton,
  Typography,
  Stack,
  Button,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const titles = ["Project Alpha", "Design Sprint", "Marketing Plan", "User Research"];

export default function FinalBoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  const [highlight, setHighlight] = useState(Array(4).fill(null)); // 'left' | 'right' | null

  const toggleCollapse = (index) => {
    const updated = [...collapsed];
    updated[index] = !updated[index];
    setCollapsed(updated);
  };

  const highlightSide = (index, direction) => {
    const newHighlight = [...highlight];
    newHighlight[index] = direction;
    setHighlight(newHighlight);
  };

  return (
    <Box sx={{ maxWidth: 1000, mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => (
        <Box key={idx} sx={{ mb: 4, border: "1px solid #ccc", borderRadius: 1 }}>
          {/* Title Bar */}
          <Stack
            direction="row"
            alignItems="center"
            justifyContent="space-between"
            sx={{
              backgroundColor: "#424242", // dark gray
              color: "white",
              px: 2,
              py: 1,
            }}
            onClick={() => toggleCollapse(idx)}
          >
            <Typography variant="subtitle1" fontWeight="bold">
              {title}
            </Typography>
            <IconButton size="small" sx={{ color: "white" }}>
              {collapsed[idx] ? <AddIcon /> : <CloseIcon />}
            </IconButton>
          </Stack>

          {/* Collapsible Content */}
          <Collapse in={!collapsed[idx]}>
            <Box sx={{ backgroundColor: "#f0f0f0", px: 2, py: 3 }}>
              <Stack direction="row" spacing={2} alignItems="flex-start">
                {/* Overall checkbox */}
                <Checkbox />

                {/* Left Side */}
                <Box
                  sx={{
                    flex: 1,
                    minHeight: 200,
                    border: "1px solid #666",
                    bgcolor:
                      highlight[idx] === "left"
                        ? "gray"
                        : highlight[idx] === "right"
                        ? "lightgray"
                        : "white",
                    transition: "background-color 0.3s",
                    p: 2,
                    borderRadius: 1,
                  }}
                >
                  {/* Placeholder for dropdown / file upload */}
                  <Typography variant="body1" mb={2}>
                    Drop-down / Upload
                  </Typography>
                  <Button variant="outlined" fullWidth>
                    Upload File
                  </Button>
                </Box>

                {/* Arrows */}
                <Stack spacing={2} alignItems="center" justifyContent="center">
                  <IconButton
                    onClick={() => highlightSide(idx, "left")}
                    sx={{
                      bgcolor:
                        highlight[idx] === "left" ? "#424242" : "#e0e0e0",
                      color: highlight[idx] === "left" ? "white" : "black",
                    }}
                  >
                    <ArrowBackIcon />
                  </IconButton>
                  <IconButton
                    onClick={() => highlightSide(idx, "right")}
                    sx={{
                      bgcolor:
                        highlight[idx] === "right" ? "#424242" : "#e0e0e0",
                      color: highlight[idx] === "right" ? "white" : "black",
                    }}
                  >
                    <ArrowForwardIcon />
                  </IconButton>
                </Stack>

                {/* Right Side */}
                <Box
                  sx={{
                    flex: 1,
                    minHeight: 200,
                    border: "1px solid #666",
                    bgcolor:
                      highlight[idx] === "right"
                        ? "gray"
                        : highlight[idx] === "left"
                        ? "lightgray"
                        : "white",
                    transition: "background-color 0.3s",
                    p: 2,
                    borderRadius: 1,
                  }}
                >
                  <Typography variant="body1" mb={2}>
                    Drop-down / Upload
                  </Typography>
                  <Button variant="outlined" fullWidth>
                    Upload File
                  </Button>
                </Box>
              </Stack>
            </Box>
          </Collapse>
        </Box>
      ))}
    </Box>
  );
}

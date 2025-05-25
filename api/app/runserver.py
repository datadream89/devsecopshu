import React, { useState } from "react";
import {
  Box,
  Checkbox,
  Collapse,
  IconButton,
  Typography,
  Stack,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const titles = ["Project Alpha", "Design Sprint", "Marketing Plan", "User Research"];

export default function EnhancedBoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  const [highlight, setHighlight] = useState(Array(4).fill(null)); // 'left' | 'right' | null

  const toggleCollapse = (index) => {
    const newCollapsed = [...collapsed];
    newCollapsed[index] = !newCollapsed[index];
    setCollapsed(newCollapsed);
  };

  const highlightSide = (index, direction) => {
    const newHighlight = [...highlight];
    newHighlight[index] = direction;
    setHighlight(newHighlight);
  };

  return (
    <Box sx={{ maxWidth: 900, mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => (
        <Box key={idx} sx={{ mb: 4, border: "1px solid #ccc", borderRadius: 1 }}>
          {/* Title Bar */}
          <Stack
            direction="row"
            alignItems="center"
            justifyContent="space-between"
            sx={{
              backgroundColor: "#e0e0e0", // gray
              px: 2,
              py: 1,
              cursor: "pointer",
            }}
            onClick={() => toggleCollapse(idx)}
          >
            <Typography variant="subtitle1" fontWeight="bold">
              {title}
            </Typography>
            <IconButton size="small">
              {collapsed[idx] ? <AddIcon /> : <CloseIcon />}
            </IconButton>
          </Stack>

          {/* Collapsible Content */}
          <Collapse in={!collapsed[idx]}>
            <Stack
              direction="row"
              spacing={2}
              alignItems="center"
              sx={{ px: 2, py: 3, backgroundColor: "#f9f9f9" }}
            >
              {/* Left Side */}
              <Stack direction="row" spacing={1} alignItems="flex-start" sx={{ flex: 1 }}>
                <Checkbox />
                <Box
                  sx={{
                    flex: 1,
                    minHeight: 100,
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
                  {/* Placeholder for dropdown or file upload */}
                  <Typography variant="body2">Drop-down / Upload goes here</Typography>
                </Box>
              </Stack>

              {/* Arrows */}
              <Stack spacing={1} alignItems="center">
                <IconButton
                  onClick={() => highlightSide(idx, "left")}
                  title="Highlight Left"
                  size="small"
                >
                  <ArrowBackIcon />
                </IconButton>
                <IconButton
                  onClick={() => highlightSide(idx, "right")}
                  title="Highlight Right"
                  size="small"
                >
                  <ArrowForwardIcon />
                </IconButton>
              </Stack>

              {/* Right Side */}
              <Stack direction="row" spacing={1} alignItems="flex-start" sx={{ flex: 1 }}>
                <Checkbox />
                <Box
                  sx={{
                    flex: 1,
                    minHeight: 100,
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
                  <Typography variant="body2">Drop-down / Upload goes here</Typography>
                </Box>
              </Stack>
            </Stack>
          </Collapse>
        </Box>
      ))}
    </Box>
  );
}

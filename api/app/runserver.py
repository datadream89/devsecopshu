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

const randomTitles = [
  "Project Alpha",
  "Design Sprint",
  "Marketing Plan",
  "User Research",
];

export default function BoxPairsMUIOnly() {
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  const [highlight, setHighlight] = useState(Array(4).fill(null)); // null | 'left' | 'right'

  const toggleCollapse = (index) => {
    const newCollapsed = [...collapsed];
    newCollapsed[index] = !newCollapsed[index];
    setCollapsed(newCollapsed);
  };

  const toggleHighlight = (index) => {
    const current = highlight[index];
    const newHighlight =
      current === "left" ? "right" : current === "right" ? null : "left";
    const newHighlightArr = [...highlight];
    newHighlightArr[index] = newHighlight;
    setHighlight(newHighlightArr);
  };

  return (
    <Box
      sx={{
        maxWidth: 600,
        mx: "auto",
        mt: 4,
        fontFamily: "Roboto, sans-serif",
        userSelect: "none",
      }}
    >
      {randomTitles.map((title, idx) => (
        <Box
          key={idx}
          sx={{
            mb: 4,
            border: "1px solid #ccc",
            borderRadius: 1,
            overflow: "hidden",
          }}
        >
          {/* Title Bar */}
          <Stack
            direction="row"
            alignItems="center"
            justifyContent="space-between"
            sx={{
              backgroundColor: "#007acc",
              color: "white",
              px: 2,
              py: 1,
              cursor: "pointer",
              fontWeight: "bold",
            }}
            onClick={() => toggleCollapse(idx)}
          >
            <Typography variant="subtitle1">{title}</Typography>
            <IconButton
              size="small"
              sx={{ color: "white" }}
              aria-label={collapsed[idx] ? "expand" : "collapse"}
            >
              {collapsed[idx] ? <AddIcon /> : <CloseIcon />}
            </IconButton>
          </Stack>

          {/* Collapsible content */}
          <Collapse in={!collapsed[idx]}>
            <Stack
              direction="row"
              spacing={2}
              sx={{
                px: 2,
                py: 2,
                borderTop: "1px solid #ccc",
                alignItems: "center",
              }}
            >
              {/* Left box with checkbox */}
              <Stack direction="row" spacing={1} sx={{ flex: 1 }} alignItems="center">
                <Checkbox />
                <Box
                  sx={{
                    flex: 1,
                    height: 40,
                    border: "1px solid #666",
                    bgcolor:
                      highlight[idx] === "left"
                        ? "gray"
                        : highlight[idx] === "right"
                        ? "lightgray"
                        : "white",
                    transition: "background-color 0.3s",
                  }}
                />
              </Stack>

              {/* Bidirectional arrow */}
              <Box
                sx={{
                  cursor: "pointer",
                  fontSize: 28,
                  color: "#007acc",
                  userSelect: "none",
                  px: 1,
                  display: "flex",
                  alignItems: "center",
                }}
                onClick={() => toggleHighlight(idx)}
                title="Click to toggle highlight"
              >
                ↔
              </Box>

              {/* Right box with checkbox */}
              <Stack direction="row" spacing={1} sx={{ flex: 1 }} alignItems="center">
                <Checkbox />
                <Box
                  sx={{
                    flex: 1,
                    height: 40,
                    border: "1px solid #666",
                    bgcolor:
                      highlight[idx] === "right"
                        ? "gray"
                        : highlight[idx] === "left"
                        ? "lightgray"
                        : "white",
                    transition: "background-color 0.3s",
                  }}
                />
              </Stack>
            </Stack>
          </Collapse>
        </Box>
      ))}
    </Box>
  );
}

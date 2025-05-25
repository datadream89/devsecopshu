import React, { useState } from "react";
import { Box, Checkbox, Typography } from "@mui/material";
import { Collapse, ActionIcon, Group } from "@mantine/core";
import { IconPlus, IconX } from "@tabler/icons-react";

const randomTitles = [
  "Project Alpha",
  "Design Sprint",
  "Marketing Plan",
  "User Research",
];

export default function BoxPairsMUI() {
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
        <Box key={idx} sx={{ mb: 4, border: "1px solid #ccc", borderRadius: 1 }}>
          {/* Title Bar */}
          <Group
            position="apart"
            align="center"
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
            <ActionIcon color="white" variant="transparent" size={24} sx={{ color: 'white' }}>
              {collapsed[idx] ? <IconPlus size={18} /> : <IconX size={18} />}
            </ActionIcon>
          </Group>

          {/* Collapsible content */}
          <Collapse in={!collapsed[idx]}>
            <Group
              spacing={3}
              sx={{
                px: 2,
                py: 2,
                borderTop: "1px solid #ccc",
              }}
            >
              {/* Left box with checkbox */}
              <Group spacing={1} sx={{ flex: 1 }}>
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
              </Group>

              {/* Bidirectional arrow */}
              <Box
                sx={{
                  cursor: "pointer",
                  fontSize: 28,
                  color: "#007acc",
                  userSelect: "none",
                  px: 1,
                }}
                onClick={() => toggleHighlight(idx)}
                title="Click to toggle highlight"
              >
                ↔
              </Box>

              {/* Right box with checkbox */}
              <Group spacing={1} sx={{ flex: 1 }}>
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
              </Group>
            </Group>
          </Collapse>
        </Box>
      ))}
    </Box>
  );
}

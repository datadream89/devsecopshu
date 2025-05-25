import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  Collapse,
  Checkbox,
  Stack,
  TextField,
  Autocomplete,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

// Sample PSCRF JSON data - replace with your import or fetch
const pscrfOptions = [
  { id: "PSCRF001", samVersion: "v1.2", pricingVersion: "p3.4", clientName: "Client A" },
  { id: "PSCRF002", samVersion: "v2.1", pricingVersion: "p2.8", clientName: "Client B" },
  { id: "PSCRF003", samVersion: "v3.0", pricingVersion: "p1.5", clientName: "Client C" },
];

// PSCRFSection component with autocomplete and 2 cards per row
function PSCRFSection() {
  const [selectedPSCRF, setSelectedPSCRF] = useState([]);

  return (
    <Box>
      <Autocomplete
        multiple
        options={pscrfOptions}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.clientName}`
        }
        filterSelectedOptions
        value={selectedPSCRF}
        onChange={(event, newValue) => {
          setSelectedPSCRF(newValue);
        }}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Select PSCRF"
            placeholder="Start typing..."
            size="small"
            sx={{ mb: 2 }}
          />
        )}
        sx={{ width: "100%" }}
      />

      {/* Cards container: 2 cards per row */}
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: "repeat(2, 1fr)",
          gap: 1,
          maxHeight: 250,
          overflowY: "auto",
        }}
      >
        {selectedPSCRF.map((pscrf) => (
          <Box
            key={pscrf.id}
            sx={{
              border: "1px solid #90caf9",
              borderRadius: 1,
              p: 1,
              backgroundColor: "#e3f2fd",
            }}
          >
            <Typography variant="subtitle2" fontWeight="bold" noWrap>
              {pscrf.id}
            </Typography>
            <Typography variant="body2" noWrap>
              Sam Version: {pscrf.samVersion}
            </Typography>
            <Typography variant="body2" noWrap>
              Pricing Version: {pscrf.pricingVersion}
            </Typography>
            <Typography variant="body2" noWrap>
              Client: {pscrf.clientName}
            </Typography>
          </Box>
        ))}
      </Box>
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

          {/* Collapsible content */}
          <Collapse in={!collapsed[idx]}>
            <Stack direction="row" spacing={3} alignItems="center" justifyContent="center" sx={{ minHeight: 350 }}>
              {/* Compare Checkbox on left side */}
              <Box sx={{ display: "flex", alignItems: "center" }}>
                <Checkbox
                  checked={compareChecked[idx]}
                  onChange={() => handleCheckboxChange(idx)}
                  sx={{ ml: 0 }}
                />
                <Typography>Compare</Typography>
              </Box>

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
                  p: 3,
                  overflowY: "auto",
                  bgcolor: compareChecked[idx] ? "white" : "#f0f0f0",
                  color: compareChecked[idx] ? "inherit" : "gray",
                  pointerEvents: compareChecked[idx] ? "auto" : "none",
                  transition: "all 0.3s ease",
                }}
              >
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
                  p: 3,
                  overflowY: "auto",
                  bgcolor: compareChecked[idx] ? "white" : "#f0f0f0",
                  color: compareChecked[idx] ? "inherit" : "gray",
                  pointerEvents: compareChecked[idx] ? "auto" : "none",
                  transition: "all 0.3s ease",
                }}
              >
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

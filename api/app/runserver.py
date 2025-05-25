import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  Collapse,
  Checkbox,
  FormControlLabel,
  Stack,
  Card,
  CardContent,
  Autocomplete,
  TextField,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const titles = ["Section 1", "Section 2", "Section 3", "Section 4"];

const pscrfData = [
  { id: "PSCRF001", samVersion: "v1.2", pricingVersion: "p3.4", clientName: "Client A" },
  { id: "PSCRF002", samVersion: "v2.1", pricingVersion: "p2.8", clientName: "Client B" },
  { id: "PSCRF003", samVersion: "v1.5", pricingVersion: "p4.0", clientName: "Client C" },
];

// PSCRFSection component
function PSCRFSection() {
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleRemove = (id) => {
    setSelectedOptions((prev) => prev.filter((option) => option.id !== id));
  };

  return (
    <Box sx={{ height: "100%", display: "flex", flexDirection: "column" }}>
      <Autocomplete
        multiple
        options={pscrfData}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        value={selectedOptions}
        onChange={(event, newValue) => setSelectedOptions(newValue)}
        renderInput={(params) => (
          <TextField {...params} label="Search PSCRF" variant="outlined" size="small" />
        )}
        sx={{ mb: 2 }}
      />

      <Box
        sx={{
          flexGrow: 1,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 1,
        }}
      >
        {selectedOptions.map((option) => (
          <Card key={option.id} variant="outlined" sx={{ position: "relative" }}>
            <CardContent sx={{ pr: 5 }}>
              <Typography variant="subtitle1" fontWeight="bold" color="#212121">
                {option.id}
              </Typography>
              <Typography color="#424242">Sam Version: {option.samVersion}</Typography>
              <Typography color="#424242">Pricing Version: {option.pricingVersion}</Typography>
              <Typography color="#424242">Client: {option.clientName}</Typography>
            </CardContent>

            <IconButton
              size="small"
              onClick={() => handleRemove(option.id)}
              sx={{ position: "absolute", top: 4, right: 4 }}
              aria-label="remove"
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          </Card>
        ))}
      </Box>
    </Box>
  );
}

// Main component
export default function BoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  const [highlight, setHighlight] = useState(Array(4).fill(null)); // 'left' | 'right' | null
  const [compareChecked, setCompareChecked] = useState(Array(4).fill(true)); // whether compare checkbox checked for each pair

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

  const handleCompareChange = (index) => {
    const updated = [...compareChecked];
    updated[index] = !updated[index];
    setCompareChecked(updated);
  };

  return (
    <Box sx={{ maxWidth: "1000px", mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => {
        // To keep code cleaner, save highlight for this idx
        const hl = highlight[idx];
        const isCompare = compareChecked[idx];

        return (
          <Box key={idx} sx={{ mb: 4, border: "1px solid #ccc", borderRadius: 1 }}>
            {/* Title Bar - Full width */}
            <Box
              sx={{
                width: "100%",
                bgcolor: "#e0e0e0",
                px: 2,
                py: 1.5,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                borderBottom: "1px solid #ccc",
                borderRadius: 1,
                cursor: "pointer",
              }}
              onClick={() => toggleCollapse(idx)}
            >
              <Typography variant="subtitle1" fontWeight="bold">
                {title}
              </Typography>
              <IconButton
                size="small"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleCollapse(idx);
                }}
              >
                {collapsed[idx] ? <AddIcon /> : <CloseIcon />}
              </IconButton>
            </Box>

            {/* Collapsible content */}
            <Collapse in={!collapsed[idx]}>
              <Box sx={{ p: 3, bgcolor: "#fff" }}>
                <Stack direction="row" spacing={2} alignItems="center" sx={{ minHeight: 320 }}>
                  {/* Compare checkbox */}
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={isCompare}
                        onChange={() => handleCompareChange(idx)}
                        sx={{ color: "#424242" }}
                      />
                    }
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
                        hl === "left" ? "gray" : hl === "right" ? "lightgray" : "#ccc",
                      borderRadius: 2,
                      p: 2,
                      overflowY: "auto",
                      backgroundColor: "#fafafa",
                      boxShadow: "0 0 8px rgba(0,0,0,0.1)",
                      opacity: isCompare ? 1 : 0.4,
                      transition: "opacity 0.3s",
                      pointerEvents: isCompare ? "auto" : "none",
                    }}
                  >
                    {(idx === 0 || idx === 2) && <PSCRFSection />}
                  </Box>

                  {/* Arrows */}
                  <Stack spacing={2} alignItems="center" sx={{ mx: 1 }}>
                    <ArrowBackIcon
                      onClick={() => handleArrowClick(idx, "left")}
                      sx={{
                        cursor: isCompare ? "pointer" : "default",
                        fontSize: 32,
                        color: hl === "left" ? "#424242" : "#bdbdbd",
                        pointerEvents: isCompare ? "auto" : "none",
                      }}
                    />
                    <ArrowForwardIcon
                      onClick={() => handleArrowClick(idx, "right")}
                      sx={{
                        cursor: isCompare ? "pointer" : "default",
                        fontSize: 32,
                        color: hl === "right" ? "#424242" : "#bdbdbd",
                        pointerEvents: isCompare ? "auto" : "none",
                      }}
                    />
                  </Stack>

                  {/* Right box */}
                  <Box
                    sx={{
                      width: 300,
                      height: 300,
                      border: "2px solid",
                      borderColor:
                        hl === "right" ? "gray" : hl === "left" ? "lightgray" : "#ccc",
                      borderRadius: 2,
                      p: 2,
                      overflowY: "auto",
                      backgroundColor: "#fafafa",
                      boxShadow: "0 0 8px rgba(0,0,0,0.1)",
                      opacity: isCompare ? 1 : 0.4,
                      transition: "opacity 0.3s",
                      pointerEvents: isCompare ? "auto" : "none",
                    }}
                  >
                    {idx === 3 && <PSCRFSection />}
                  </Box>
                </Stack>
              </Box>
            </Collapse>
          </Box>
        );
      })}
    </Box>
  );
}

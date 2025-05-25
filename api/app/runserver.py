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
              <Typography variant="subtitle1" fontWeight="bold">
                {option.id}
              </Typography>
              <Typography>Sam Version: {option.samVersion}</Typography>
              <Typography>Pricing Version: {option.pricingVersion}</Typography>
              <Typography>Client: {option.clientName}</Typography>
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

export default function BoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(4).fill(false));
  // Change highlight to object with left/right booleans
  const [highlight, setHighlight] = useState(
    Array(4).fill(null).map(() => ({ left: false, right: false }))
  );

  const toggleCollapse = (index) => {
    const updated = [...collapsed];
    updated[index] = !updated[index];
    setCollapsed(updated);
  };

  const handleArrowClick = (index, direction) => {
    const updated = [...highlight];
    // toggle the clicked arrow
    updated[index] = {
      ...updated[index],
      [direction]: !updated[index][direction],
    };
    setHighlight(updated);
  };

  return (
    <Box sx={{ maxWidth: "1000px", mx: "auto", mt: 4 }}>
      {titles.map((title, idx) => {
        const hl = highlight[idx];

        return (
          <Box key={idx} sx={{ mb: 4, border: "1px solid #ccc", borderRadius: 1 }}>
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
                      borderColor: hl.left ? "gray" : hl.right ? "lightgray" : "#ccc",
                      borderRadius: 2,
                      p: 2,
                      overflowY: "auto",
                      backgroundColor: "#fff",
                      opacity: hl.left || hl.right ? 1 : 0.5,
                      transition: "opacity 0.3s",
                    }}
                  >
                    {(idx === 0 || idx === 2) && <PSCRFSection />}
                  </Box>

                  {/* Arrows */}
                  <Stack spacing={2} alignItems="center">
                    <ArrowBackIcon
                      onClick={() => handleArrowClick(idx, "left")}
                      sx={{
                        cursor: "pointer",
                        fontSize: 32,
                        color: hl.left ? "#424242" : "#bdbdbd",
                      }}
                    />
                    <ArrowForwardIcon
                      onClick={() => handleArrowClick(idx, "right")}
                      sx={{
                        cursor: "pointer",
                        fontSize: 32,
                        color: hl.right ? "#424242" : "#bdbdbd",
                      }}
                    />
                  </Stack>

                  {/* Right box */}
                  <Box
                    sx={{
                      width: 300,
                      height: 300,
                      border: "2px solid",
                      borderColor: hl.right ? "gray" : hl.left ? "lightgray" : "#ccc",
                      borderRadius: 2,
                      p: 2,
                      overflowY: "auto",
                      backgroundColor: "#fff",
                      opacity: hl.left || hl.right ? 1 : 0.5,
                      transition: "opacity 0.3s",
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

import React, { useState, useEffect } from "react";
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

function PSCRFSection() {
  const [options, setOptions] = useState([]);
  const [selectedOptions, setSelectedOptions] = useState([]);

  useEffect(() => {
    fetch("/data/options.json")
      .then((res) => res.json())
      .then((data) => setOptions(data))
      .catch((e) => console.error("Failed to load options.json", e));
  }, []);

  const handleRemove = (id) => {
    setSelectedOptions((prev) => prev.filter((opt) => opt.id !== id));
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        overflowY: "auto",
        bgcolor: "#fff",
        p: 1,
        borderRadius: 1,
      }}
    >
      <Autocomplete
        multiple
        options={options}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        value={selectedOptions}
        onChange={(e, newVal) => setSelectedOptions(newVal)}
        renderInput={(params) => (
          <TextField {...params} label="Select PSCRF" size="small" variant="outlined" />
        )}
        disableCloseOnSelect
        isOptionEqualToValue={(option, value) => option.id === value.id}
        sx={{ mb: 2 }}
      />

      <Box sx={{ flexGrow: 1, overflowY: "auto" }}>
        {selectedOptions.map((option) => (
          <Card
            key={option.id}
            variant="outlined"
            sx={{ mb: 1, position: "relative" }}
          >
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

function DummySection({ text }) {
  return (
    <Box
      sx={{
        height: "100%",
        bgcolor: "#fff",
        borderRadius: 1,
        p: 2,
        overflowY: "auto",
      }}
    >
      <Typography>{text}</Typography>
    </Box>
  );
}

const PAIRS = 4;

export default function BoxPairs() {
  const [collapsed, setCollapsed] = useState(Array(PAIRS).fill(false));
  const [highlight, setHighlight] = useState(Array(PAIRS).fill(null)); // 'left' | 'right' | null
  const [compareChecked, setCompareChecked] = useState(Array(PAIRS).fill(true));

  const toggleCollapse = (index) => {
    setCollapsed((prev) => {
      const copy = [...prev];
      copy[index] = !copy[index];
      return copy;
    });
  };

  const handleArrowClick = (index, direction) => {
    setHighlight((prev) => {
      const copy = [...prev];
      copy[index] = direction;
      return copy;
    });
  };

  const handleCompareChange = (index, checked) => {
    setCompareChecked((prev) => {
      const copy = [...prev];
      copy[index] = checked;
      return copy;
    });
  };

  // Map of what component goes in each box (leftBox, rightBox) per row index (0-based)
  const boxContentMap = [
    // row 0
    {
      left: <PSCRFSection />,
      right: <DummySection text="Approved Contract Content" />,
    },
    // row 1
    {
      left: <DummySection text="Approved Contract Content" />,
      right: <DummySection text="Dummy Content" />,
    },
    // row 2
    {
      left: <DummySection text="Dummy Content" />,
      right: <PSCRFSection />,
    },
    // row 3
    {
      left: <PSCRFSection />,
      right: <PSCRFSection />,
    },
  ];

  return (
    <Box sx={{ maxWidth: 1200, mx: "auto", mt: 3 }}>
      {[...Array(PAIRS)].map((_, idx) => {
        const isCollapsed = collapsed[idx];
        const highlightDir = highlight[idx];
        const isCompareOn = compareChecked[idx];
        return (
          <Box
            key={idx}
            sx={{
              mb: 4,
            }}
          >
            {/* Title bar */}
            <Box
              sx={{
                width: "100%",
                bgcolor: "#f5f5f5",
                px: 2,
                py: 1.5,
                display: "flex",
                alignItems: "center",
                borderRadius: 1,
                border: "1px solid #ccc",
                cursor: "pointer",
                userSelect: "none",
              }}
              onClick={() => toggleCollapse(idx)}
            >
              <Typography sx={{ flexGrow: 1 }} fontWeight="bold">
                {`Pair ${idx + 1}`}
              </Typography>
              <IconButton size="small" onClick={(e) => { e.stopPropagation(); toggleCollapse(idx); }}>
                {isCollapsed ? <AddIcon /> : <CloseIcon />}
              </IconButton>
            </Box>

            {/* Content */}
            <Collapse in={!isCollapsed}>
              <Stack
                direction="row"
                alignItems="center"
                spacing={2}
                sx={{ mt: 1, width: "100%" }}
              >
                {/* Compare checkbox */}
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={isCompareOn}
                      onChange={(e) => handleCompareChange(idx, e.target.checked)}
                    />
                  }
                  label="Compare"
                  sx={{ whiteSpace: "nowrap" }}
                />

                {/* Left box */}
                <Box
                  sx={{
                    flex: 1,
                    height: 320,
                    borderRadius: 1,
                    border: "2px solid",
                    borderColor:
                      !isCompareOn
                        ? "#ddd"
                        : highlightDir === "left"
                        ? "#424242"
                        : highlightDir === "right"
                        ? "#bdbdbd"
                        : "#ccc",
                    bgcolor: isCompareOn ? "#fff" : "#f0f0f0",
                    overflowY: "auto",
                    p: 1,
                  }}
                >
                  {boxContentMap[idx].left}
                </Box>

                {/* Arrows */}
                <Stack spacing={1} alignItems="center">
                  <ArrowBackIcon
                    onClick={() => handleArrowClick(idx, "left")}
                    sx={{
                      cursor: "pointer",
                      fontSize: 36,
                      color:
                        !isCompareOn
                          ? "#ddd"
                          : highlightDir === "left"
                          ? "#424242"
                          : "#bdbdbd",
                      userSelect: "none",
                    }}
                  />
                  <ArrowForwardIcon
                    onClick={() => handleArrowClick(idx, "right")}
                    sx={{
                      cursor: "pointer",
                      fontSize: 36,
                      color:
                        !isCompareOn
                          ? "#ddd"
                          : highlightDir === "right"
                          ? "#424242"
                          : "#bdbdbd",
                      userSelect: "none",
                    }}
                  />
                </Stack>

                {/* Right box */}
                <Box
                  sx={{
                    flex: 1,
                    height: 320,
                    borderRadius: 1,
                    border: "2px solid",
                    borderColor:
                      !isCompareOn
                        ? "#ddd"
                        : highlightDir === "right"
                        ? "#424242"
                        : highlightDir === "left"
                        ? "#bdbdbd"
                        : "#ccc",
                    bgcolor: isCompareOn ? "#fff" : "#f0f0f0",
                    overflowY: "auto",
                    p: 1,
                  }}
                >
                  {boxContentMap[idx].right}
                </Box>
              </Stack>
            </Collapse>
          </Box>
        );
      })}
    </Box>
 

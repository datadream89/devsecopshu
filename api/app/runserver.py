import React, { useState, useEffect } from "react";
import {
  Box,
  Grid,
  Typography,
  Checkbox,
  FormControlLabel,
  Autocomplete,
  TextField,
  Paper,
  RadioGroup,
  Radio,
  Button,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import CloseIcon from "@mui/icons-material/Close";

import options from "./options.json"; // Your PSCRF options data

function LeftBoxCard({ item, onRemove, disabled }) {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 1,
        borderRadius: 1,
        border: "1px solid #ccc",
        backgroundColor: disabled ? "#e0e0e0" : "#f9f9f9",
        position: "relative",
        opacity: disabled ? 0.6 : 1,
        pointerEvents: disabled ? "none" : "auto",
      }}
      elevation={1}
    >
      <Typography variant="subtitle2" fontWeight="bold">
        {item.id}
      </Typography>
      <Typography variant="body2">Client: {item.clientName}</Typography>
      <Typography variant="body2">SAM Version: {item.samVersion}</Typography>
      <Typography variant="body2">Pricing Version: {item.pricingVersion}</Typography>
      {!disabled && (
        <IconButton
          size="small"
          onClick={() => onRemove(item)}
          sx={{ position: "absolute", top: 4, right: 4 }}
          aria-label="Remove"
        >
          <CloseIcon fontSize="small" />
        </IconButton>
      )}
    </Paper>
  );
}

export default function CompareComponent() {
  // Horizontal bar states
  const [pscrfType, setPscrfType] = useState("");
  const [compareDirection, setCompareDirection] = useState("right");
  const [contractType, setContractType] = useState("Agreement");

  // Compare checkbox & selected options state
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [selectedOptions, setSelectedOptions] = useState([]);

  // Border color based on compare state and direction
  const getBoxBorder = (side) => {
    if (!compareEnabled) return "2px solid lightgray";

    if (compareDirection === "right") {
      return side === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return side === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  const removeOption = (item) => {
    setSelectedOptions(
      selectedOptions.filter(
        (o) =>
          !(
            o.id === item.id &&
            o.samVersion === item.samVersion &&
            o.pricingVersion === item.pricingVersion
          )
      )
    );
  };

  return (
    <Box sx={{ p: 3, maxWidth: 900, mx: "auto" }}>
      {/* Horizontal bar at top */}
      <Paper
        sx={{
          p: 2,
          mb: 4,
          display: "flex",
          alignItems: "center",
          gap: 3,
          flexWrap: "wrap",
          borderRadius: 2,
          boxShadow: "0 0 10px rgba(0,0,0,0.05)",
        }}
        elevation={2}
      >
        <FormControl sx={{ minWidth: 160 }}>
          <InputLabel id="pscrf-type-label">PSCRF Type</InputLabel>
          <Select
            labelId="pscrf-type-label"
            value={pscrfType}
            label="PSCRF Type"
            onChange={(e) => setPscrfType(e.target.value)}
            size="small"
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            <MenuItem value="Type 1">Type 1</MenuItem>
            <MenuItem value="Type 2">Type 2</MenuItem>
            <MenuItem value="Type 3">Type 3</MenuItem>
          </Select>
        </FormControl>

        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <Button
            variant={compareDirection === "left" ? "contained" : "outlined"}
            onClick={() => setCompareDirection("left")}
            size="small"
          >
            <ArrowBackIcon />
          </Button>
          <Button
            variant={compareDirection === "right" ? "contained" : "outlined"}
            onClick={() => setCompareDirection("right")}
            size="small"
          >
            <ArrowForwardIcon />
          </Button>
        </Box>

        <RadioGroup
          row
          value={contractType}
          onChange={(e) => setContractType(e.target.value)}
          sx={{ ml: 2 }}
        >
          <FormControlLabel
            value="Agreement"
            control={<Radio />}
            label="Agreement"
          />
          <FormControlLabel
            value="Supplement"
            control={<Radio />}
            label="Supplement"
          />
          <FormControlLabel
            value="Addendum"
            control={<Radio />}
            label="Addendum"
          />
        </RadioGroup>
      </Paper>

      {/* One pair of boxes */}
      <Grid container spacing={2} alignItems="flex-start" sx={{ minHeight: 400 }}>
        {/* Checkbox on left */}
        <Grid item xs={1}>
          <FormControlLabel
            control={
              <Checkbox
                checked={compareEnabled}
                onChange={(e) => setCompareEnabled(e.target.checked)}
                sx={{
                  color: "darkgrey",
                  "&.Mui-checked": {
                    color: "darkgrey",
                  },
                }}
                inputProps={{ "aria-label": "Compare checkbox" }}
              />
            }
            label="Compare"
          />
        </Grid>

        {/* Left Box */}
        <Grid item xs={11}>
          <Paper
            sx={{
              p: 2,
              border: getBoxBorder("left"),
              minHeight: 380,
              boxSizing: "border-box",
              overflowY: "auto",
              backgroundColor: compareEnabled ? "inherit" : "#f0f0f0",
              opacity: compareEnabled ? 1 : 0.6,
              pointerEvents: compareEnabled ? "auto" : "none",
            }}
            elevation={2}
          >
            <Typography variant="h6" mb={2}>
              Pscerf Data
            </Typography>

            <Autocomplete
              multiple
              options={options}
              filterSelectedOptions
              value={selectedOptions}
              onChange={(e, newValue) => setSelectedOptions(newValue)}
              getOptionLabel={(option) =>
                `${option.id} (Client: ${option.clientName}, SAM: ${option.samVersion}, Pricing: ${option.pricingVersion})`
              }
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Select PSCRF IDs"
                  placeholder="Start typing..."
                  size="small"
                />
              )}
              disabled={!compareEnabled}
              sx={{ mb: 2 }}
            />

            {selectedOptions.length === 0 && (
              <Typography variant="body2" color="text.secondary">
                No selections yet.
              </Typography>
            )}

            {selectedOptions.map((item) => (
              <LeftBoxCard
                key={`${item.id}-${item.samVersion}-${item.pricingVersion}`}
                item={item}
                onRemove={removeOption}
                disabled={!compareEnabled}
              />
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

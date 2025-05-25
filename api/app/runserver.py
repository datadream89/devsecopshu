import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  Checkbox,
  FormControlLabel,
  Stack,
  Card,
  CardContent,
  Autocomplete,
  TextField,
  RadioGroup,
  Radio,
  FormControl,
  Button,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const pscrfData = [
  { id: "PSCRF001", samVersion: "v1.2", pricingVersion: "p3.4", clientName: "Client A" },
  { id: "PSCRF002", samVersion: "v2.1", pricingVersion: "p2.8", clientName: "Client B" },
  { id: "PSCRF003", samVersion: "v1.5", pricingVersion: "p4.0", clientName: "Client C" },
];

// PSCRF Section Component
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
        // Keep autocomplete input single line, no multi-line chips
        sx={{
          mb: 2,
          "& .MuiAutocomplete-inputRoot": {
            flexWrap: "nowrap",
          },
          "& .MuiAutocomplete-tag": {
            maxWidth: 150,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          },
        }}
      />

      {/* Container for cards grows vertically */}
      <Box
        sx={{
          flexGrow: 1,
          maxHeight: 350,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 1,
          bgcolor: "white",
          borderRadius: 1,
          p: 1,
          border: "1px solid #ddd",
        }}
      >
        {selectedOptions.map((option) => (
          <Card key={option.id} variant="outlined" sx={{ position: "relative" }}>
            <CardContent sx={{ pr: 5 }}>
              <Typography variant="subtitle1" fontWeight="bold" noWrap>
                {option.id}
              </Typography>
              <Typography noWrap>Sam Version: {option.samVersion}</Typography>
              <Typography noWrap>Pricing Version: {option.pricingVersion}</Typography>
              <Typography noWrap>Client: {option.clientName}</Typography>
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

// Approved Contract / Signed Contract Section Component
function ContractSection({ title }) {
  const [contracts, setContracts] = useState([
    { id: 1, type: "Agreement", fileName: null },
  ]);

  const handleTypeChange = (id, newType) => {
    setContracts((prev) =>
      prev.map((c) =>
        c.id === id ? { ...c, type: newType, fileName: null } : c
      )
    );
  };

  const handleFileChange = (id, event) => {
    const file = event.target.files[0];
    if (file) {
      setContracts((prev) =>
        prev.map((c) =>
          c.id === id ? { ...c, fileName: file.name } : c
        )
      );
    }
  };

  const addContract = () => {
    setContracts((prev) => [
      ...prev,
      { id: Date.now(), type: "Agreement", fileName: null },
    ]);
  };

  const removeContract = (id) => {
    setContracts((prev) => prev.filter((c) => c.id !== id));
  };

  return (
    <Box
      sx={{
        height: "100%",
        display: "flex",
        flexDirection: "column",
        bgcolor: "white",
        borderRadius: 1,
        border: "1px solid #ddd",
        p: 1,
        overflowY: "auto",
      }}
    >
      {contracts.map((contract, index) => (
        <Box
          key={contract.id}
          sx={{
            display: "flex",
            alignItems: "center",
            gap: 2,
            mb: 1,
          }}
        >
          <Typography sx={{ minWidth: 140, fontWeight: "bold" }}>
            {`${title} ${index + 1}`}
          </Typography>

          <FormControl component="fieldset" sx={{ flexGrow: 1 }}>
            <RadioGroup
              row
              value={contract.type}
              onChange={(e) => handleTypeChange(contract.id, e.target.value)}
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
          </FormControl>

          <Button
            variant="contained"
            component="label"
            startIcon={<CloudUploadIcon />}
            sx={{ bgcolor: "#555", "&:hover": { bgcolor: "#333" }, minWidth: 140 }}
          >
            Upload File
            <input
              hidden
              type="file"
              onChange={(e) => handleFileChange(contract.id, e)}
              accept="*"
            />
          </Button>

          <Typography sx={{ minWidth: 120, fontStyle: "italic", overflowWrap: "break-word" }}>
            {contract.fileName || ""}
          </Typography>

          {index !== 0 && (
            <IconButton
              color="error"
              onClick={() => removeContract(contract.id)}
              aria-label="remove contract"
            >
              <CloseIcon />
            </IconButton>
          )}
        </Box>
      ))}

      <Button
        variant="outlined"
        startIcon={<AddIcon />}
        onClick={addContract}
        sx={{ mt: 1 }}
      >
        Add
      </Button>
    </Box>
  );
}

export default function BoxPairs() {
  // Highlight states for arrow selection
  const [highlight, setHighlight] = useState(Array(4).fill(null)); // 'left' | 'right' | null

  // Checkbox state for each pair
  const [compareChecked, setCompareChecked] = useState(Array(4).fill(true));

  const handleArrowClick = (index, direction) => {
    setHighlight((prev) => {
      const copy = [...prev];
      copy[index] = direction;
      return copy;
    });
  };

  const handleCompareChange = (index) => {
    setCompareChecked((prev) => {
      const copy = [...prev];
      copy[index] = !copy[index];
      return copy;
    });
  };

  // Helper for styling boxes based on arrow and compare checkbox
  const getBoxStyles = (index, side) => {
    const arrow = highlight[index];
    const checked = compareChecked[index];
    const isActive = checked && (arrow === side || arrow === null);

    return {
      width: 300,
      height: 360,
      border: "2px solid",
      borderColor:
        arrow === side ? "gray" : arrow && arrow !== side ? "lightgray" : "#ccc",
      borderRadius: 2,
      p: 1,
      overflowY: "auto",
      bgcolor: "white",
      color: checked ? "inherit" : "gray",
      pointerEvents: checked ? "auto" : "none",
      userSelect: checked ? "auto" : "none",
      transition: "background-color 0.3s ease",
      display: "flex",
      flexDirection: "column",
    };
  };

  // Layout of content per box position (row index + left/right)
  const renderContent = (row, side) => {
    if (row === 0 && side === "left") return <PSCRFSection />;
    if (row === 2 && side === "right") return <PSCRFSection />;
    if (row === 3) return <PSCRFSection />;

    if ((row === 0 && side === "right") || (row === 1 && side === "left"))
      return <ContractSection title="Approved Contract" />;

    if ((row === 1 && side === "right") || (row === 2 && side === "right"))
      return <ContractSection title="Signed Contract" />;

    return null;
  };

  return (
    <Box sx={{ maxWidth: 1100, mx: "auto", mt: 4 }}>
      {[0, 1, 2, 3].map((row) => (
        <Box key={row} sx={{ mb: 5 }}>
          {/* Title bar above each pair */}
          <Box
            sx={{
              mb: 1,
              bgcolor: "#f5f5f5",
              p: 1,
              borderRadius: 1,
              border: "1px solid #ccc",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              userSelect: "none",
            }}
          >
            <Typography variant="subtitle1" fontWeight="bold">
              {`Row ${row + 1} Pair`}
            </Typography>
          </Box>

          {/* Compare checkbox and boxes with arrows */}
          <Stack direction="row" spacing={2} alignItems="center">
            <FormControlLabel
              control={
                <Checkbox
                  checked={compareChecked[row]}
                  onChange={() => handleCompareChange(row)}
                />
              }
              label="Compare"
              sx={{ whiteSpace: "nowrap" }}
            />

            <Box sx={getBoxStyles(row, "left")}>
              {renderContent(row, "left")}
            </Box>

            {/* Arrows */}
            <Stack spacing={2} alignItems="center">
              <ArrowBackIcon
                onClick={() => handleArrowClick(row, "left")}
                sx={{
                  cursor: "pointer",
                  fontSize: 32,
                  color: highlight[row] === "left" ? "#424242" : "#bdbdbd",
                }}
              />
              <ArrowForwardIcon
                onClick={() => handleArrowClick(row, "right")}
                sx={{
                  cursor: "pointer",
                  fontSize: 32,
                  color: highlight[row] === "right" ? "#424242" : "#bdbdbd",
                }}
              />
            </Stack>

            <Box sx={getBoxStyles(row, "right")}>
              {renderContent(row, "right")}
            </Box>
          </Stack>
        </Box>
      ))}
    </Box>
  );
}

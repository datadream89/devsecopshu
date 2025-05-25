import React, { useState } from "react";
import {
  Box,
  Checkbox,
  FormControlLabel,
  Typography,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Button,
  IconButton,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CloseIcon from "@mui/icons-material/Close";
import AddIcon from "@mui/icons-material/Add";

function PsCrfSection({ index, section, handleChange, disabled }) {
  return (
    <Box
      sx={{
        flex: 1,
        border: "1px solid #ccc",
        borderRadius: 1,
        p: 1,
        opacity: disabled ? 0.5 : 1,
        pointerEvents: disabled ? "none" : "auto",
      }}
    >
      <FormControl fullWidth size="small" disabled={disabled}>
        <InputLabel>PSCRF Type</InputLabel>
        <Select
          value={section.pscrfType}
          label="PSCRF Type"
          onChange={(e) => handleChange(index, e.target.value)}
        >
          <MenuItem value="Type A">Type A</MenuItem>
          <MenuItem value="Type B">Type B</MenuItem>
          <MenuItem value="Type C">Type C</MenuItem>
        </Select>
      </FormControl>
    </Box>
  );
}

function ApprovedContractSection({
  index,
  section,
  handleTypeChange,
  handleFileChange,
  addSection,
  removeSection,
  disabled,
}) {
  return (
    <Box
      sx={{
        flex: 1,
        border: "1px solid #ccc",
        borderRadius: 1,
        p: 1,
        ml: 1,
        opacity: disabled ? 0.5 : 1,
        pointerEvents: disabled ? "none" : "auto",
      }}
    >
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          gap: 1,
          mb: 1,
        }}
      >
        <FormControl fullWidth size="small" disabled={disabled}>
          <InputLabel>Contract Type</InputLabel>
          <Select
            value={section.contractType}
            label="Contract Type"
            onChange={(e) => handleTypeChange(index, e.target.value)}
          >
            <MenuItem value="Agreement">Agreement</MenuItem>
            <MenuItem value="Master Agreement">Master Agreement</MenuItem>
            <MenuItem value="Amendment">Amendment</MenuItem>
            <MenuItem value="Pricing Sheet">Pricing Sheet</MenuItem>
            <MenuItem value="SOW">SOW</MenuItem>
          </Select>
        </FormControl>

        <Button
          component="label"
          size="small"
          variant="outlined"
          startIcon={<CloudUploadIcon />}
          disabled={disabled}
          sx={{ whiteSpace: "nowrap" }}
        >
          {section.file ? "Change File" : "Upload File"}
          <input
            hidden
            type="file"
            onChange={(e) => {
              if (e.target.files.length > 0) {
                handleFileChange(index, e.target.files[0]);
              }
            }}
          />
        </Button>

        {index > 0 && (
          <IconButton
            size="small"
            color="error"
            onClick={() => removeSection(index)}
            disabled={disabled}
          >
            <CloseIcon />
          </IconButton>
        )}

        {index === 0 && (
          <IconButton
            size="small"
            color="primary"
            onClick={addSection}
            disabled={disabled}
          >
            <AddIcon />
          </IconButton>
        )}
      </Box>

      {section.file && (
        <Typography
          variant="caption"
          sx={{ fontStyle: "italic", color: disabled ? "gray" : "inherit" }}
        >
          Selected File: {section.file.name}
        </Typography>
      )}
    </Box>
  );
}

export default function ComparePairs() {
  const [pairs, setPairs] = useState([
    {
      checked: true,
      pscrf: { pscrfType: "Type A" },
      contract: { contractType: "Agreement", file: null },
    },
  ]);

  const handleCheckboxChange = (index) => {
    setPairs((prev) =>
      prev.map((pair, i) =>
        i === index ? { ...pair, checked: !pair.checked } : pair
      )
    );
  };

  const handlePsCrfChange = (index, value) => {
    setPairs((prev) =>
      prev.map((pair, i) =>
        i === index ? { ...pair, pscrf: { pscrfType: value } } : pair
      )
    );
  };

  const handleContractTypeChange = (index, value) => {
    setPairs((prev) =>
      prev.map((pair, i) =>
        i === index
          ? { ...pair, contract: { ...pair.contract, contractType: value } }
          : pair
      )
    );
  };

  const handleFileChange = (index, file) => {
    setPairs((prev) =>
      prev.map((pair, i) =>
        i === index ? { ...pair, contract: { ...pair.contract, file } } : pair
      )
    );
  };

  const addContractSection = (index) => {
    setPairs((prev) =>
      prev.map((pair, i) => {
        if (i === index) {
          return {
            ...pair,
            contract: { ...pair.contract }, // no multiple contract sections in this simplified version
          };
        }
        return pair;
      })
    );
  };

  const removeContractSection = (index) => {
    setPairs((prev) =>
      prev.map((pair, i) => {
        if (i === index) {
          return {
            ...pair,
            contract: { contractType: "", file: null },
          };
        }
        return pair;
      })
    );
  };

  // Add new pair (both PsCrf and Contract)
  const addPair = () => {
    setPairs((prev) => [
      ...prev,
      {
        checked: true,
        pscrf: { pscrfType: "" },
        contract: { contractType: "", file: null },
      },
    ]);
  };

  // Remove a pair entirely
  const removePair = (index) => {
    setPairs((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <Box sx={{ p: 2, maxWidth: 900, mx: "auto" }}>
      <Typography
        variant="h6"
        sx={{
          mb: 2,
          borderBottom: "2px solid #1976d2",
          pb: 1,
          fontWeight: "bold",
          textAlign: "center",
        }}
      >
        Compare PsCrf and approved contract
      </Typography>

      {pairs.map((pair, index) => {
        const disabled = !pair.checked;

        return (
          <Box
            key={index}
            sx={{
              display: "flex",
              alignItems: "center",
              mb: 2,
              gap: 1,
            }}
          >
            {/* Checkbox on the left */}
            <FormControlLabel
              control={
                <Checkbox
                  checked={pair.checked}
                  onChange={() => handleCheckboxChange(index)}
                />
              }
              label=""
              sx={{ mr: 1 }}
            />

            {/* PsCrf section */}
            <PsCrfSection
              index={index}
              section={pair.pscrf}
              handleChange={handlePsCrfChange}
              disabled={disabled}
            />

            {/* Approved Contract section */}
            <ApprovedContractSection
              index={index}
              section={pair.contract}
              handleTypeChange={handleContractTypeChange}
              handleFileChange={handleFileChange}
              addSection={() => addContractSection(index)}
              removeSection={() => removeContractSection(index)}
              disabled={disabled}
            />

            {/* Optional: Remove entire pair button */}
            <IconButton
              color="error"
              onClick={() => removePair(index)}
              sx={{ ml: 1 }}
            >
              <CloseIcon />
            </IconButton>
          </Box>
        );
      })}

      <Button variant="contained" onClick={addPair}>
        Add New Pair
      </Button>
    </Box>
  );
}

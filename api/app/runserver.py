import React, { useState } from "react";
import {
  Box,
  Typography,
  Checkbox,
  FormControlLabel,
  Paper,
  RadioGroup,
  Radio,
  Button,
  IconButton,
  TextField,
  Autocomplete,
} from "@mui/material";

import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

import options from "./options.json";

// ... LeftBoxCard and ApprovedContractSection unchanged

export default function Request() {
  // Replace global compareEnabled with per-pair state:
  const [compareEnabledPairs, setCompareEnabledPairs] = useState({
    1: true,
    2: true,
    3: true,
    4: true,
  });

  const [direction, setDirection] = useState("right");
  const [collapsed, setCollapsed] = useState(false);

  // Pair 1 states
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [contractSections, setContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // Pair 2-4 states as before...
  // (for brevity, not changing these unless needed)

  // Handlers for pair 1 contract sections unchanged...

  // Utility: border color based on disabled or not, and direction
  const getBoxBorder = (boxSide, disabled) => {
    if (disabled) return "2px solid lightgray";

    if (direction === "right") {
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  const getArrowColor = (arrowDirection) => {
    if (!Object.values(compareEnabledPairs).some(Boolean)) return "lightgray"; // no pair enabled

    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
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

  // Render left box with disabled style when needed
  const renderLeftBox = (selectedOptions, setSelectedOptions, pairNumber, disabled) => (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        border: getBoxBorder("left", disabled),
        minWidth: 320,
        minHeight: 350,
        display: "flex",
        flexDirection: "column",
        backgroundColor: disabled ? "#f0f0f0" : "inherit",
        pointerEvents: disabled ? "none" : "auto",
        opacity: disabled ? 0.6 : 1,
      }}
    >
      <Autocomplete
        multiple
        options={options}
        getOptionLabel={(option) =>
          `${option.id} (SAM: ${option.samVersion}, Pricing: ${option.pricingVersion})`
        }
        value={selectedOptions}
        onChange={(event, newValue) => {
          setSelectedOptions(newValue);
        }}
        renderInput={(params) => <TextField {...params} label="PSCRF IDs" />}
        disableCloseOnSelect
        sx={{ mb: 1 }}
        disabled={disabled}
      />
      <Box sx={{ flexGrow: 1, overflowY: "auto" }}>
        {selectedOptions.map((item) => (
          <LeftBoxCard
            key={`${item.id}-${item.samVersion}-${item.pricingVersion}`}
            item={item}
            onRemove={(item) => {
              if (pairNumber === 1) removeOption(item);
            }}
          />
        ))}
      </Box>
    </Box>
  );

  const renderRightBoxPair1 = (disabled) => (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        border: getBoxBorder("right", disabled),
        minWidth: 320,
        minHeight: 350,
        display: "flex",
        flexDirection: "column",
        backgroundColor: disabled ? "#f0f0f0" : "inherit",
        pointerEvents: disabled ? "none" : "auto",
        opacity: disabled ? 0.6 : 1,
      }}
    >
      <Typography
        variant="h6"
        fontWeight="bold"
        sx={{ mb: 2, borderBottom: "1px solid #ccc", pb: 1 }}
      >
        Approved Contract
      </Typography>

      <Box sx={{ overflowY: "auto", flexGrow: 1 }}>
        {contractSections.map((section, idx) => (
          <ApprovedContractSection
            key={section.id}
            index={idx}
            section={section}
            handleTypeChange={handleTypeChange}
            handleFileChange={handleFileChange}
            addSection={addSection}
            removeSection={removeSection}
            disabled={disabled}
          />
        ))}
      </Box>
    </Box>
  );

  const renderRightBoxPlaceholder = (disabled) => (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        border: getBoxBorder("right", disabled),
        minWidth: 320,
        minHeight: 350,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: disabled ? "lightgray" : "gray",
        fontStyle: "italic",
        backgroundColor: disabled ? "#f0f0f0" : "inherit",
        pointerEvents: disabled ? "none" : "auto",
        opacity: disabled ? 0.6 : 1,
      }}
    >
      Right Box Placeholder
    </Box>
  );

  // Arrows for each pair
  const renderControls = (pairIndex, disabled) => (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        mx: 1,
      }}
    >
      <IconButton
        onClick={() => setDirection("left")}
        size="small"
        sx={{ color: getArrowColor("left") }}
        aria-label="Compare left"
        disabled={disabled}
      >
        <ArrowBackIcon />
      </IconButton>
      <IconButton
        onClick={() => setDirection("right")}
        size="small"
        sx={{ color: getArrowColor("right") }}
        aria-label="Compare right"
        disabled={disabled}
      >
        <ArrowForwardIcon />
      </IconButton>
    </Box>
  );

  return (
    <Box sx={{ p: 3, maxWidth: 1300, mx: "auto" }}>
      {/* Horizontal title bar for all pairs */}
      <Box
        sx={{
          mb: 2,
          borderBottom: "2px solid #ccc",
          pb: 1,
          userSelect: "none",
          textAlign: "center",
        }}
      >
        <Typography variant="h5" fontWeight="bold">
          Compare PSCRF and Approved Contract
        </Typography>
      </Box>

      <Box sx={{ mb: 3 }}>
        {[1, 2, 3, 4].map((pair) => {
          const disabled = !compareEnabledPairs[pair];

          return (
            <Box
              key={pair}
              sx={{
                display: "flex",
                alignItems: "center",
                mb: 4,
                gap: 1,
              }}
            >
              {/* Checkbox left of boxes */}
              <FormControlLabel
                control={
                  <Checkbox
                    checked={compareEnabledPairs[pair]}
                    onChange={(e) =>
                      setCompareEnabledPairs({
                        ...compareEnabledPairs,
                        [pair]: e.target.checked,
                      })
                    }
                    sx={{
                      color: "darkgrey",
                      "&.Mui-checked": {
                        color: "darkgrey",
                      },
                    }}
                  />
                }
                label=""
                sx={{ mr: 2 }}
              />

              {/* Left box */}
              {pair === 1
                ? renderLeftBox(selectedOptions, setSelectedOptions, 1, disabled)
                : renderLeftBox(
                    pair === 2
                      ? selectedOptions2
                      : pair === 3
                      ? selectedOptions3
                      : selectedOptions4,
                    pair === 2
                      ? setSelectedOptions2
                      : pair === 3
                      ? setSelectedOptions3
                      : setSelectedOptions4,
                    pair,
                    disabled
                  )}

              {/* Controls */}
              {renderControls(pair, disabled)}

              {/* Right box */}
              {pair === 1
                ? renderRightBoxPair1(disabled)
                : renderRightBoxPlaceholder(disabled)}
            </Box>
          );
        })}
      </Box>
    </Box>
  );
}

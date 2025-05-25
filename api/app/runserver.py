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
} from "@mui/material";

import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

import options from "./options.json"; // your options file

function LeftBoxCard({ item, onRemove }) {
  return (
    <Paper
      sx={{
        p: 2,
        mb: 1,
        borderRadius: 1,
        border: "1px solid #ccc",
        backgroundColor: "#f9f9f9",
        position: "relative",
      }}
      elevation={1}
    >
      <Typography variant="subtitle2" fontWeight="bold">
        {item.id}
      </Typography>
      <Typography variant="body2">Client: {item.clientName}</Typography>
      <Typography variant="body2">SAM Version: {item.samVersion}</Typography>
      <Typography variant="body2">Pricing Version: {item.pricingVersion}</Typography>
      <IconButton
        size="small"
        onClick={() => onRemove(item)}
        sx={{ position: "absolute", top: 4, right: 4 }}
        aria-label="Remove"
      >
        <CloseIcon fontSize="small" />
      </IconButton>
    </Paper>
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
    <Paper
      sx={{
        p: 2,
        mb: 2,
        position: "relative",
        borderRadius: 2,
        border: "1px solid #ccc",
        backgroundColor: disabled ? "#f0f0f0" : "inherit",
        pointerEvents: disabled ? "none" : "auto",
        opacity: disabled ? 0.6 : 1,
      }}
      elevation={1}
    >
      <Typography variant="subtitle1" fontWeight="bold" mb={1}>
        Approved Contract {index + 1}
      </Typography>

      <RadioGroup
        row
        value={section.contractType}
        onChange={(e) => {
          handleTypeChange(section.id, e.target.value);
          handleFileChange(section.id, null);
        }}
        sx={{
          "& .Mui-checked": {
            color: "darkgrey",
          },
        }}
      >
        <FormControlLabel
          value="Agreement"
          control={<Radio disabled={disabled} />}
          label="Agreement"
        />
        <FormControlLabel
          value="Supplement"
          control={<Radio disabled={disabled} />}
          label="Supplement"
        />
        <FormControlLabel
          value="Addendum"
          control={<Radio disabled={disabled} />}
          label="Addendum"
        />
      </RadioGroup>

      <input
        id={`file-upload-${section.id}`}
        type="file"
        accept=".pdf,.docx"
        style={{ display: "none" }}
        onChange={(e) => handleFileChange(section.id, e.target.files[0])}
        disabled={disabled}
      />
      <label htmlFor={`file-upload-${section.id}`}>
        <Button
          variant="outlined"
          startIcon={<CloudUploadIcon />}
          component="span"
          sx={{
            mt: 1,
            color: "darkgrey",
            borderColor: "darkgrey",
            "&:hover": {
              borderColor: "black",
              color: "black",
            },
          }}
          disabled={disabled}
        >
          Upload File
        </Button>
      </label>
      {section.file && (
        <Typography variant="body2" mt={1}>
          Selected: {section.file.name}
        </Typography>
      )}

      <Box
        sx={{
          position: "absolute",
          top: 8,
          right: 8,
          display: "flex",
          gap: 1,
          pointerEvents: disabled ? "none" : "auto",
          opacity: disabled ? 0.6 : 1,
        }}
      >
        <IconButton size="small" onClick={addSection} title="Add section" disabled={disabled}>
          <AddIcon fontSize="small" />
        </IconButton>
        {index > 0 && (
          <IconButton
            size="small"
            onClick={() => removeSection(section.id)}
            title="Remove section"
            disabled={disabled}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        )}
      </Box>
    </Paper>
  );
}

export default function Request() {
  const [compareEnabled, setCompareEnabled] = useState(true);
  const [direction, setDirection] = useState("right");
  const [collapsed, setCollapsed] = useState(false);

  // State for pair 1
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [contractSections, setContractSections] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // States placeholders for pairs 2, 3, 4
  const [selectedOptions2, setSelectedOptions2] = useState([]);
  const [contractSections2, setContractSections2] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);
  const [selectedOptions3, setSelectedOptions3] = useState([]);
  const [contractSections3, setContractSections3] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);
  const [selectedOptions4, setSelectedOptions4] = useState([]);
  const [contractSections4, setContractSections4] = useState([
    { id: 0, contractType: "Agreement", file: null },
  ]);

  // Handlers for pair 1 contract sections
  const addSection = () => {
    const newId = contractSections.length
      ? Math.max(...contractSections.map((s) => s.id)) + 1
      : 0;
    setContractSections([
      ...contractSections,
      { id: newId, contractType: "Agreement", file: null },
    ]);
  };

  const removeSection = (id) => {
    setContractSections(contractSections.filter((s) => s.id !== id));
  };

  const handleTypeChange = (id, newType) => {
    setContractSections(
      contractSections.map((s) =>
        s.id === id ? { ...s, contractType: newType, file: null } : s
      )
    );
  };

  const handleFileChange = (id, file) => {
    setContractSections(
      contractSections.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  // Utility for border color based on compareEnabled and direction
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "2px solid lightgray";

    if (direction === "right") {
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  // Utility for arrow color
  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
  };

  // Remove option from left box selections (pair 1)
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

  // Render the pairs with all UI pieces duplicated
  // For brevity, pairs 2-4 left and right boxes will be placeholders,
  // You can expand the state and handlers for those pairs similarly if needed.

  const renderLeftBox = (selectedOptions, setSelectedOptions, pairNumber) => (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        border: getBoxBorder("left"),
        minWidth: 320,
        minHeight: 350,
        display: "flex",
        flexDirection: "column",
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
      />
      <Box sx={{ flexGrow: 1, overflowY: "auto" }}>
        {selectedOptions.map((item) => (
          <LeftBoxCard
            key={`${item.id}-${item.samVersion}-${item.pricingVersion}`}
            item={item}
            onRemove={(item) => {
              if (pairNumber === 1) removeOption(item);
              // Extend for pairs 2-4 if needed
            }}
          />
        ))}
      </Box>
    </Box>
  );

  const renderRightBoxPair1 = () => (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        border: getBoxBorder("right"),
        minWidth: 320,
        minHeight: 350,
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* Parent container titled "Approved Contract" */}
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
            disabled={!compareEnabled}
          />
        ))}
      </Box>
    </Box>
  );

  // Placeholder right boxes for pairs 2, 3, 4 (you can implement like pair 1)
  const renderRightBoxPlaceholder = () => (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        border: getBoxBorder("right"),
        minWidth: 320,
        minHeight: 350,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: "gray",
        fontStyle: "italic",
      }}
    >
      Right Box Placeholder
    </Box>
  );

  // Arrows and checkboxes for each pair (same style)
  const renderControls = (pairIndex) => (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        mx: 1,
      }}
    >
      <Checkbox
        checked={compareEnabled}
        onChange={(e) => setCompareEnabled(e.target.checked)}
        sx={{
          color: "darkgrey",
          "&.Mui-checked": {
            color: "darkgrey",
          },
          mb: 1,
        }}
      />
      <IconButton
        onClick={() => setDirection("left")}
        size="small"
        sx={{ color: getArrowColor("left") }}
        aria-label="Compare left"
      >
        <ArrowBackIcon />
      </IconButton>
      <IconButton
        onClick={() => setDirection("right")}
        size="small"
        sx={{ color: getArrowColor("right") }}
        aria-label="Compare right"
      >
        <ArrowForwardIcon />
      </IconButton>
    </Box>
  );

  return (
    <Box sx={{ p: 3, maxWidth: 1300, mx: "auto" }}>
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          mb: 1,
          userSelect: "none",
          border: "1px solid #ccc",
          borderRadius: 1,
          p: 1,
          backgroundColor: "#f5f5f5",
          cursor: "pointer",
        }}
        onClick={() => setCollapsed(!collapsed)}
      >
        <Typography variant="subtitle1" fontWeight="bold" sx={{ ml: 1 }}>
          Compare PSCRF and Approved Contract
        </Typography>
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            setCollapsed(!collapsed);
          }}
          aria-label={collapsed ? "Expand" : "Collapse"}
        >
          {collapsed ? <AddIcon /> : <CloseIcon />}
        </IconButton>
      </Box>

      {!collapsed && (
        <>
          <Box sx={{ mb: 3 }}>
            {[1, 2, 3, 4].map((pair) => (
              <Box
                key={pair}
                sx={{
                  display: "flex",
                  alignItems: "center",
                  mb: 4,
                  gap: 1,
                }}
              >
                {/* Left box */}
                {pair === 1
                  ? renderLeftBox(selectedOptions, setSelectedOptions, 1)
                  : renderLeftBox(
                      pair === 2 ? selectedOptions2 : pair === 3 ? selectedOptions3 : selectedOptions4,
                      pair === 2 ? setSelectedOptions2 : pair === 3 ? setSelectedOptions3 : setSelectedOptions4,
                      pair
                    )}

                {/* Controls */}
                {renderControls(pair)}

                {/* Right box */}
                {pair === 1
                  ? renderRightBoxPair1()
                  : renderRightBoxPlaceholder()}
              </Box>
            ))}
          </Box>
        </>
      )}
    </Box>
  );
}

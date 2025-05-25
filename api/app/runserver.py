import React, { useState } from "react";
import {
  Box,
  Grid,
  Paper,
  Typography,
  IconButton,
  Checkbox,
  FormControlLabel,
  Collapse,
  Divider,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import ExpandLessIcon from "@mui/icons-material/ExpandLess";

// Dummy contract section input
function ContractSection({
  section,
  handleTypeChange,
  handleFileChange,
  addSection,
  removeSection,
  disabled,
  index,
}) {
  return (
    <Box
      sx={{
        mb: 1,
        p: 1,
        border: "1px solid #ccc",
        borderRadius: 1,
        backgroundColor: disabled ? "#eee" : "white",
        opacity: disabled ? 0.6 : 1,
      }}
    >
      <Typography variant="body2" sx={{ mb: 1 }}>
        Section {index + 1}: {section.title || "Untitled"}
      </Typography>
      <input
        type="text"
        placeholder="Type"
        disabled={disabled}
        value={section.type || ""}
        onChange={(e) => handleTypeChange(index, e.target.value)}
        style={{ width: "100%", marginBottom: 6 }}
      />
      <input
        type="file"
        disabled={disabled}
        onChange={(e) => handleFileChange(index, e.target.files)}
        style={{ width: "100%" }}
      />
      <Box sx={{ mt: 1, display: "flex", justifyContent: "space-between" }}>
        <button disabled={disabled} onClick={() => addSection(index)}>
          +
        </button>
        <button disabled={disabled} onClick={() => removeSection(index)}>
          x
        </button>
      </Box>
    </Box>
  );
}

function CompareBoxes({
  titleLeft,
  titleRight,
  contractSectionsLeft,
  contractSectionsRight,
  handleTypeChangeLeft,
  handleFileChangeLeft,
  addSectionLeft,
  removeSectionLeft,
  handleTypeChangeRight,
  handleFileChangeRight,
  addSectionRight,
  removeSectionRight,
  compareEnabled,
  direction,
  setDirection,
}) {
  const getBoxBorder = (boxSide) => {
    if (!compareEnabled) return "2px solid lightgray";

    if (direction === "right") {
      return boxSide === "left" ? "2px solid darkgrey" : "2px solid lightgrey";
    } else {
      return boxSide === "left" ? "2px solid lightgrey" : "2px solid darkgrey";
    }
  };

  const getArrowColor = (arrowDirection) => {
    if (!compareEnabled) return "lightgray";
    if (direction === arrowDirection) return "darkgray";
    return "lightgray";
  };

  const disabledStyle = {
    backgroundColor: "#f0f0f0",
    opacity: 0.6,
    pointerEvents: "none",
  };

  return (
    <Grid container spacing={2} alignItems="center" sx={{ minHeight: 400, mb: 1 }}>
      {/* Left Box */}
      <Grid item xs={5}>
        <Paper
          sx={{
            p: 2,
            border: getBoxBorder("left"),
            minHeight: 400,
            boxSizing: "border-box",
            overflowY: "auto",
            ...(compareEnabled ? {} : disabledStyle),
          }}
          elevation={2}
        >
          <Typography variant="h6" mb={2}>
            {titleLeft}
          </Typography>

          {contractSectionsLeft.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              No contract sections.
            </Typography>
          ) : (
            contractSectionsLeft.map((section, index) => (
              <ContractSection
                key={section.id}
                index={index}
                section={section}
                handleTypeChange={handleTypeChangeLeft}
                handleFileChange={handleFileChangeLeft}
                addSection={addSectionLeft}
                removeSection={removeSectionLeft}
                disabled={!compareEnabled}
              />
            ))
          )}
        </Paper>
      </Grid>

      {/* Center arrows */}
      <Grid
        item
        xs={2}
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: 400,
          position: "relative",
        }}
      >
        <IconButton
          onClick={() => setDirection("left")}
          sx={{ color: getArrowColor("left") }}
          disabled={!compareEnabled}
          aria-label="Left direction"
        >
          <ArrowBackIcon fontSize="large" />
        </IconButton>
        <IconButton
          onClick={() => setDirection("right")}
          sx={{ color: getArrowColor("right") }}
          disabled={!compareEnabled}
          aria-label="Right direction"
        >
          <ArrowForwardIcon fontSize="large" />
        </IconButton>
      </Grid>

      {/* Right Box */}
      <Grid item xs={5}>
        <Paper
          sx={{
            p: 2,
            border: getBoxBorder("right"),
            minHeight: 400,
            boxSizing: "border-box",
            overflowY: "auto",
            ...(compareEnabled ? {} : disabledStyle),
          }}
          elevation={2}
        >
          <Typography variant="h6" mb={2}>
            {titleRight}
          </Typography>

          {contractSectionsRight.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              No contract sections.
            </Typography>
          ) : (
            contractSectionsRight.map((section, index) => (
              <ContractSection
                key={section.id}
                index={index}
                section={section}
                handleTypeChange={handleTypeChangeRight}
                handleFileChange={handleFileChangeRight}
                addSection={addSectionRight}
                removeSection={removeSectionRight}
                disabled={!compareEnabled}
              />
            ))
          )}
        </Paper>
      </Grid>
    </Grid>
  );
}

export default function ContractComparison() {
  // First pair: PSCRF Data vs Approved Contract
  const [pscrfSections, setPscrfSections] = useState([
    { id: 1, title: "PSCRF Section 1", type: "" },
  ]);
  const [approvedContractSections1, setApprovedContractSections1] = useState([
    { id: 2, title: "Approved Section 1", type: "" },
  ]);
  const [direction1, setDirection1] = useState("right");
  const [compareEnabled1, setCompareEnabled1] = useState(true);

  // Second pair: Approved Contract vs Unsigned Contract
  const [approvedContractSections2, setApprovedContractSections2] = useState([
    { id: 3, title: "Approved Section 2", type: "" },
  ]);
  const [unsignedContractSections, setUnsignedContractSections] = useState([
    { id: 4, title: "Unsigned Section 1", type: "" },
  ]);
  const [direction2, setDirection2] = useState("right");
  const [compareEnabled2, setCompareEnabled2] = useState(true);
  const [collapse2, setCollapse2] = useState(true);

  // Handlers for section changes
  const handleTypeChange = (setter, sections) => (index, value) => {
    const newSections = [...sections];
    newSections[index].type = value;
    setter(newSections);
  };

  const handleFileChange = (index, files) => {
    // Implement file handling if needed
  };

  const addSection = (setter, sections) => (index) => {
    const newSections = [...sections];
    newSections.splice(index + 1, 0, { id: Date.now(), title: "", type: "" });
    setter(newSections);
  };

  const removeSection = (setter, sections) => (index) => {
    const newSections = [...sections];
    if (newSections.length > 1) {
      newSections.splice(index, 1);
      setter(newSections);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* First pair */}
      <Box sx={{ mb: 4 }}>
        <FormControlLabel
          control={
            <Checkbox
              checked={compareEnabled1}
              onChange={(e) => setCompareEnabled1(e.target.checked)}
            />
          }
          label="Compare"
        />
        <CompareBoxes
          titleLeft="PSCRF Data"
          titleRight="Approved Contract"
          contractSectionsLeft={pscrfSections}
          contractSectionsRight={approvedContractSections1}
          handleTypeChangeLeft={handleTypeChange(setPscrfSections, pscrfSections)}
          handleFileChangeLeft={handleFileChange}
          addSectionLeft={addSection(setPscrfSections, pscrfSections)}
          removeSectionLeft={removeSection(setPscrfSections, pscrfSections)}
          handleTypeChangeRight={handleTypeChange(
            setApprovedContractSections1,
            approvedContractSections1
          )}
          handleFileChangeRight={handleFileChange}
          addSectionRight={addSection(setApprovedContractSections1, approvedContractSections1)}
          removeSectionRight={removeSection(setApprovedContractSections1, approvedContractSections1)}
          compareEnabled={compareEnabled1}
          direction={direction1}
          setDirection={setDirection1}
        />
      </Box>

      <Divider />

      {/* Second pair with collapse and compare checkbox */}
      <Box sx={{ mt: 4 }}>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            cursor: "pointer",
            mb: 1,
            userSelect: "none",
          }}
          onClick={() => setCollapse2(!collapse2)}
        >
          <Typography variant="h6">Approved Contract vs Unsigned Contract</Typography>
          {collapse2 ? <ExpandLessIcon /> : <ExpandMoreIcon />}
        </Box>
        <FormControlLabel
          control={
            <Checkbox
              checked={compareEnabled2}
              onChange={(e) => setCompareEnabled2(e.target.checked)}
            />
          }
          label="Compare"
        />
        <Collapse in={collapse2}>
          <CompareBoxes
            titleLeft="Approved Contract"
            titleRight="Unsigned Contract"
            contractSectionsLeft={approvedContractSections2}
            contractSectionsRight={unsignedContractSections}
            handleTypeChangeLeft={handleTypeChange(setApprovedContractSections2, approvedContractSections2)}
            handleFileChangeLeft={handleFileChange}
            addSectionLeft={addSection(setApprovedContractSections2, approvedContractSections2)}
            removeSectionLeft={removeSection(setApprovedContractSections2, approvedContractSections2)}
            handleTypeChangeRight={handleTypeChange(setUnsignedContractSections, unsignedContractSections)}
            handleFileChangeRight={handleFileChange}
            addSectionRight={addSection(setUnsignedContractSections, unsignedContractSections)}
            removeSectionRight={removeSection(setUnsignedContractSections, unsignedContractSections)}
            compareEnabled={compareEnabled2}
            direction={direction2}
            setDirection={setDirection2}
          />
        </Collapse>
      </Box>
    </Box>
  );
}

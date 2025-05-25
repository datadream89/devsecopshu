import React, { useState } from "react";
import {
  Box,
  Typography,
  Checkbox,
  IconButton,
  TextField,
  Autocomplete,
  Card,
  CardContent,
  RadioGroup,
  FormControlLabel,
  Radio,
  Button,
} from "@mui/material";
import {
  Add as AddIcon,
  Close as CloseIcon,
  Upload as UploadIcon,
  ExpandLess as ExpandLessIcon,
  ExpandMore as ExpandMoreIcon,
  ArrowBackIosNew,
  ArrowForwardIos,
} from "@mui/icons-material";

const pscrfOptions = [
  { id: "PS001", samVersion: "v1", pricingVersion: "p1", clientName: "Client A" },
  { id: "PS002", samVersion: "v2", pricingVersion: "p2", clientName: "Client B" },
  { id: "PS003", samVersion: "v3", pricingVersion: "p3", clientName: "Client C" },
];

const FILE_TYPES = [
  "application/pdf",
  "application/msword",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

const PSCRFSection = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);

  const handleRemove = (index) => {
    const updated = [...selectedOptions];
    updated.splice(index, 1);
    setSelectedOptions(updated);
  };

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white" minHeight={220}>
      <Autocomplete
        multiple
        options={pscrfOptions}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        onChange={(event, value) => setSelectedOptions(value)}
        renderInput={(params) => <TextField {...params} label="Select PSCRF" variant="outlined" />}
      />
      <Box display="flex" flexWrap="wrap" mt={2} gap={2} sx={{ maxHeight: 300, overflowY: "auto" }}>
        {selectedOptions.map((option, index) => (
          <Card key={index} sx={{ width: "48%", position: "relative", boxSizing: "border-box" }}>
            <CardContent sx={{ padding: "8px !important" }}>
              <Typography variant="body2" component="div" whiteSpace="normal">
                <strong>ID:</strong> {option.id}
                <br />
                <strong>SAM:</strong> {option.samVersion}
                <br />
                <strong>Pricing:</strong> {option.pricingVersion}
                <br />
                <strong>Client:</strong> {option.clientName}
              </Typography>
              <IconButton
                size="small"
                onClick={() => handleRemove(index)}
                sx={{ position: "absolute", top: 4, right: 4 }}
                aria-label="remove card"
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

const ContractSection = ({ title }) => {
  const [sections, setSections] = useState([
    { id: Date.now(), type: "Agreement", file: null, filename: "" },
  ]);

  const handleAddSection = () => {
    setSections([
      ...sections,
      { id: Date.now() + Math.random(), type: "Agreement", file: null, filename: "" },
    ]);
  };

  const handleRemoveSection = (id) => {
    setSections(sections.filter((section) => section.id !== id));
  };

  const handleRadioChange = (id, type) => {
    setSections(
      sections.map((section) =>
        section.id === id ? { ...section, type, file: null, filename: "" } : section
      )
    );
  };

  const handleFileChange = (id, file) => {
    if (!file) return;
    if (!FILE_TYPES.includes(file.type)) {
      alert("Only PDF and Word files are allowed.");
      return;
    }
    setSections(
      sections.map((section) =>
        section.id === id ? { ...section, file, filename: file.name } : section
      )
    );
  };

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white" minHeight={220} sx={{ overflowY: "auto" }}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      {sections.map((section, idx) => (
        <Box
          key={section.id}
          display="flex"
          alignItems="center"
          gap={1}
          mt={idx === 0 ? 0 : 2}
          flexWrap="wrap"
          position="relative"
          border={1}
          borderColor="grey.200"
          borderRadius={1}
          p={1}
          bgcolor="#fafafa"
        >
          <RadioGroup
            row
            value={section.type}
            onChange={(e) => handleRadioChange(section.id, e.target.value)}
            sx={{ flexGrow: 1, minWidth: 240 }}
          >
            <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
            <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
            <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
          </RadioGroup>
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            style={{ display: "none" }}
            id={`upload-${section.id}`}
            onChange={(e) => handleFileChange(section.id, e.target.files[0])}
          />
          <label htmlFor={`upload-${section.id}`}>
            <IconButton component="span" title="Upload File">
              <UploadIcon />
            </IconButton>
          </label>
          <Typography
            sx={{
              fontSize: 12,
              maxWidth: 180,
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
            title={section.filename}
          >
            {section.filename || "No file chosen"}
          </Typography>
          {sections.length > 1 && (
            <IconButton aria-label="remove section" onClick={() => handleRemoveSection(section.id)} sx={{ ml: 1 }}>
              <CloseIcon />
            </IconButton>
          )}
        </Box>
      ))}
      <Button startIcon={<AddIcon />} onClick={handleAddSection} size="small" sx={{ mt: 2 }}>
        Add Section
      </Button>
    </Box>
  );
};

const BidirectionalArrow = ({ leftSelected, rightSelected, onLeftClick, onRightClick }) => {
  return (
    <Box
      sx={{
        width: 40,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 8,
        userSelect: "none",
      }}
    >
      <ArrowBackIosNew
        sx={{
          cursor: "pointer",
          color: leftSelected ? "grey.800" : "grey.400",
          fontSize: 20,
          transform: "rotate(0deg)",
        }}
        onClick={onLeftClick}
        title="Left arrow"
      />
      <ArrowForwardIos
        sx={{
          cursor: "pointer",
          color: rightSelected ? "grey.800" : "grey.400",
          fontSize: 20,
          transform: "rotate(0deg)",
        }}
        onClick={onRightClick}
        title="Right arrow"
      />
    </Box>
  );
};

const TitleBar = ({ title, expanded, toggleExpanded, checked, onCheckChange }) => (
  <Box
    display="flex"
    alignItems="center"
    bgcolor="#f5f5f5"
    px={2}
    py={1}
    borderTop={1}
    borderBottom={1}
    borderColor="grey.400"
    mb={1}
    sx={{ userSelect: "none" }}
  >
    <Checkbox checked={checked} onChange={onCheckChange} sx={{ mr: 2 }} inputProps={{ "aria-label": `${title} checkbox` }} />
    <Typography variant="subtitle1" flex={1} sx={{ userSelect: "none", fontWeight: 600 }}>
      {title}
    </Typography>
    <IconButton onClick={toggleExpanded} aria-label={expanded ? "Collapse section" : "Expand section"} size="small">
      {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
    </IconButton>
  </Box>
);

const BoxPair = ({ leftComponent, rightComponent, title, checked, onCheckChange }) => {
  const [expanded, setExpanded] = useState(true);
  const [leftArrowSelected, setLeftArrowSelected] = useState(false);
  const [rightArrowSelected, setRightArrowSelected] = useState(false);

  const toggleExpanded = () => setExpanded((v) => !v);
  const toggleLeftArrow = () => setLeftArrowSelected((v) => !v);
  const toggleRightArrow = () => setRightArrowSelected((v) => !v);

  const leftBoxStyle = {
    opacity: checked ? 1 : 0.4,
    borderColor: leftArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };
  const rightBoxStyle = {
    opacity: checked ? 1 : 0.4,
    borderColor: rightArrowSelected ? "grey.800" : "grey.300",
    transition: "opacity 0.3s, border-color 0.3s",
  };

  return (
    <Box mb={3}>
      <TitleBar title={title} expanded={expanded} toggleExpanded={toggleExpanded} checked={checked} onCheckChange={onCheckChange} />
      {expanded && (
        <Box display="flex" alignItems="center" gap={1}>
          <Box flex={1} border={1} borderRadius={2} sx={leftBoxStyle} minHeight={250} bgcolor="white">
            {leftComponent}
          </Box>
          <BidirectionalArrow
            leftSelected={leftArrowSelected}
            rightSelected={rightArrowSelected}
            onLeftClick={toggleLeftArrow}
            onRightClick={toggleRightArrow}
          />
          <Box flex={1} border={1} borderRadius={2} sx={rightBoxStyle} minHeight={250} bgcolor="white">
            {rightComponent}
          </Box>
        </Box>
      )}
    </Box>
  );
};

const ComparisonLayout = () => {
  const [rowChecks, setRowChecks] = useState([true, true, true, true]);

  const toggleRowCheck = (index) => {
    const newChecks = [...rowChecks];
    newChecks[index] = !newChecks[index];
    setRowChecks(newChecks);
  };

  return (<Box
  sx={{
    width: "95vw",
    maxWidth: 1200,
    mx: "auto",
    mt: 3,
    mb: 6,
    px: 1,
    userSelect: "none",
  }}
>
  {/* Row 1 */}
  <BoxPair
    title="Row 1"
    checked={rowChecks[0]}
    onCheckChange={() => toggleRowCheck(0)}
    leftComponent={<PSCRFSection />}
    rightComponent={<ContractSection title="Approved Contract" />}
  />

  {/* Row 2 */}
  <BoxPair
    title="Row 2"
    checked={rowChecks[1]}
    onCheckChange={() => toggleRowCheck(1)}
    leftComponent={<ContractSection title="Approved Contract" />}
    rightComponent={<ContractSection title="Signed Contract" />}
  />

  {/* Row 3 */}
  <BoxPair
    title="Row 3"
    checked={rowChecks[2]}
    onCheckChange={() => toggleRowCheck(2)}
    leftComponent={<ContractSection title="Signed Contract" />}
    rightComponent={<PSCRFSection />}
  />

  {/* Row 4 */}
  <BoxPair
    title="Row 4"
    checked={rowChecks[3]}
    onCheckChange={() => toggleRowCheck(3)}
    leftComponent={<PSCRFSection />}
    rightComponent={<PSCRFSection />}
  />
</Box>);};
export default ComparisonLayout


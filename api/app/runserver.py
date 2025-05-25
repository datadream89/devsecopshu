import React, { useState } from "react";
import {
  Box,
  Typography,
  Checkbox,
  IconButton,
  TextField,
  Chip,
  MenuItem,
  Button,
  RadioGroup,
  FormControlLabel,
  Radio,
} from "@mui/material";
import { ArrowForwardIos, ArrowBackIos, CloudUpload, Close } from "@mui/icons-material";
import Autocomplete from "@mui/material/Autocomplete";
import options from "./data/options.json";

const PSCRFSection = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);

  return (
    <Box>
      <Typography variant="subtitle1" fontWeight="bold" mb={1}>Select PSCRF</Typography>
      <Autocomplete
        multiple
        options={options}
        getOptionLabel={(option) => option}
        value={selectedOptions}
        onChange={(_, newValue) => setSelectedOptions(newValue)}
        renderInput={(params) => (
          <TextField {...params} variant="outlined" placeholder="Select PSCRF" />
        )}
      />
      <Box display="flex" flexWrap="wrap" gap={2} mt={2}>
        {selectedOptions.map((item, index) => (
          <Chip key={index} label={item} sx={{ backgroundColor: "#f0f0f0" }} />
        ))}
      </Box>
    </Box>
  );
};

const ApprovedContractSection = () => {
  const [sections, setSections] = useState([
    { type: "Agreement", file: null }
  ]);

  const handleRadioChange = (index, value) => {
    const newSections = [...sections];
    newSections[index].type = value;
    newSections[index].file = null;
    setSections(newSections);
  };

  const handleFileChange = (index, file) => {
    const newSections = [...sections];
    newSections[index].file = file;
    setSections(newSections);
  };

  const addSection = () => {
    setSections([...sections, { type: "Agreement", file: null }]);
  };

  const removeSection = (index) => {
    const newSections = [...sections];
    newSections.splice(index, 1);
    setSections(newSections);
  };

  return (
    <Box>
      <Typography variant="subtitle1" fontWeight="bold" mb={1}>Approved Contract</Typography>
      {sections.map((section, index) => (
        <Box key={index} mb={2} display="flex" alignItems="center" gap={2}>
          <RadioGroup
            row
            value={section.type}
            onChange={(e) => handleRadioChange(index, e.target.value)}
          >
            {["Agreement", "Supplement", "Addendum"].map((type) => (
              <FormControlLabel key={type} value={type} control={<Radio />} label={type} />
            ))}
          </RadioGroup>
          <input
            accept="*"
            type="file"
            style={{ display: "none" }}
            id={`upload-${index}`}
            onChange={(e) => handleFileChange(index, e.target.files[0])}
          />
          <label htmlFor={`upload-${index}`}>
            <IconButton component="span">
              <CloudUpload />
            </IconButton>
          </label>
          {section.file && <Typography>{section.file.name}</Typography>}
          {sections.length > 1 && (
            <IconButton onClick={() => removeSection(index)}><Close /></IconButton>
          )}
        </Box>
      ))}
      <Button onClick={addSection}>+ Add Section</Button>
    </Box>
  );
};

const BoxPair = ({ title, leftComponent, rightComponent }) => {
  const [compareChecked, setCompareChecked] = useState(true);
  const [leftToRight, setLeftToRight] = useState(false);
  const [rightToLeft, setRightToLeft] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  const handleArrowClick = (dir) => {
    if (dir === "ltr") {
      setLeftToRight(!leftToRight);
      setRightToLeft(false);
    } else {
      setRightToLeft(!rightToLeft);
      setLeftToRight(false);
    }
  };

  return (
    <Box mb={4}>
      <Box display="flex" alignItems="center" gap={1} mb={1}>
        <Checkbox
          checked={compareChecked}
          onChange={(e) => setCompareChecked(e.target.checked)}
        />
        <Typography fontWeight="bold">{title}</Typography>
        <Box flexGrow={1} />
        <IconButton onClick={() => setCollapsed(!collapsed)}>
          {collapsed ? "+" : "×"}
        </IconButton>
      </Box>

      {!collapsed && (
        <Box display="flex" alignItems="center" gap={2}>
          <Box
            flex={1}
            p={2}
            bgcolor="white"
            border={`2px solid ${rightToLeft ? "#888" : "#ccc"}`}
            opacity={compareChecked ? 1 : 0.4}
          >
            {leftComponent}
          </Box>

          <Box display="flex" flexDirection="column" alignItems="center" gap={1}>
            <IconButton
              onClick={() => handleArrowClick("ltr")}
              sx={{ color: leftToRight ? "#666" : "#ccc" }}
            >
              <ArrowForwardIos />
            </IconButton>
            <IconButton
              onClick={() => handleArrowClick("rtl")}
              sx={{ color: rightToLeft ? "#666" : "#ccc" }}
            >
              <ArrowBackIos />
            </IconButton>
          </Box>

          <Box
            flex={1}
            p={2}
            bgcolor="white"
            border={`2px solid ${leftToRight ? "#888" : "#ccc"}`}
            opacity={compareChecked ? 1 : 0.4}
          >
            {rightComponent}
          </Box>
        </Box>
      )}
    </Box>
  );
};

const App = () => {
  return (
    <Box p={4} bgcolor="#f9f9f9">
      <BoxPair
        title="Row 1"
        leftComponent={<PSCRFSection />}
        rightComponent={<ApprovedContractSection />}
      />
      <BoxPair
        title="Row 2"
        leftComponent={<ApprovedContractSection />}
        rightComponent={<PSCRFSection />}
      />
      <BoxPair
        title="Row 3"
        leftComponent={<ApprovedContractSection />}
        rightComponent={<PSCRFSection />}
      />
      <BoxPair
        title="Row 4"
        leftComponent={<PSCRFSection />}
        rightComponent={<PSCRFSection />}
      />
    </Box>
  );
};

export default App;

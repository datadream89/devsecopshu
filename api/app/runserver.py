import React, { useState } from "react";
import {
  Box,
  Grid,
  Typography,
  Checkbox,
  IconButton,
  TextField,
  Chip,
  MenuItem,
  Radio,
  RadioGroup,
  FormControlLabel,
  Button,
  Stack,
} from "@mui/material";
import CompareArrowsIcon from "@mui/icons-material/CompareArrows";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CloseIcon from "@mui/icons-material/Close";

const pscrfOptions = ["PSCRF 101", "PSCRF 102", "PSCRF 103"];

const SectionTitleBar = ({ title }) => (
  <Box
    sx={{
      width: "100%",
      backgroundColor: "#f0f0f0",
      padding: "10px 20px",
      borderRadius: "8px",
      marginBottom: "10px",
    }}
  >
    <Typography variant="h6">{title}</Typography>
  </Box>
);

const PSCRFSection = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [inputValue, setInputValue] = useState("");

  const handleChange = (event) => {
    const value = event.target.value;
    if (!selectedOptions.includes(value)) {
      setSelectedOptions([...selectedOptions, value]);
    }
    setInputValue("");
  };

  const handleDelete = (option) => {
    setSelectedOptions(selectedOptions.filter((item) => item !== option));
  };

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        Select PSCRF
      </Typography>
      <TextField
        select
        fullWidth
        label="PSCRF"
        value={inputValue}
        onChange={handleChange}
      >
        {pscrfOptions.map((option) => (
          <MenuItem key={option} value={option}>
            {option}
          </MenuItem>
        ))}
      </TextField>
      <Grid container spacing={2} mt={2}>
        {selectedOptions.map((option) => (
          <Grid item xs={6} key={option}>
            <Box
              sx={{
                backgroundColor: "#f9f9f9",
                padding: 2,
                borderRadius: 2,
                border: "1px solid #ccc",
              }}
            >
              <Chip label={option} onDelete={() => handleDelete(option)} />
            </Box>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

const ApprovedContractSection = () => {
  const [sections, setSections] = useState([
    { type: "Agreement", file: null },
  ]);

  const handleTypeChange = (index, value) => {
    const updated = [...sections];
    updated[index] = { ...updated[index], type: value, file: null };
    setSections(updated);
  };

  const handleFileChange = (index, event) => {
    const updated = [...sections];
    updated[index] = { ...updated[index], file: event.target.files[0] };
    setSections(updated);
  };

  const addSection = () => {
    setSections([...sections, { type: "Agreement", file: null }]);
  };

  const removeSection = (index) => {
    const updated = sections.filter((_, i) => i !== index);
    setSections(updated);
  };

  return (
    <Box>
      <Typography variant="subtitle1" gutterBottom>
        Approved Contract
      </Typography>
      {sections.map((section, index) => (
        <Box key={index} sx={{ mb: 2, borderBottom: "1px solid #eee", pb: 2, position: 'relative' }}>
          {sections.length > 1 && (
            <IconButton
              size="small"
              sx={{ position: 'absolute', top: 0, right: 0 }}
              onClick={() => removeSection(index)}
            >
              <CloseIcon fontSize="small" />
            </IconButton>
          )}
          <RadioGroup
            row
            value={section.type}
            onChange={(e) => handleTypeChange(index, e.target.value)}
          >
            <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
            <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
            <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
          </RadioGroup>
          <Stack direction="row" alignItems="center" spacing={2}>
            <Button
              variant="outlined"
              component="label"
              startIcon={<CloudUploadIcon />}
            >
              Upload File
              <input
                type="file"
                hidden
                onChange={(e) => handleFileChange(index, e)}
              />
            </Button>
            <Typography variant="body2">
              {section.file ? section.file.name : "No file selected"}
            </Typography>
          </Stack>
        </Box>
      ))}
      <Button onClick={addSection}>+ Add Section</Button>
    </Box>
  );
};

const BoxPair = ({ leftContent, rightContent, rowIndex }) => {
  const [leftToRight, setLeftToRight] = useState(false);
  const [rightToLeft, setRightToLeft] = useState(false);
  const [checked, setChecked] = useState(true);

  const getBorderStyle = (direction) =>
    direction ? "2px solid gray" : "1px solid lightgray";

  const getOpacity = () => (checked ? 1 : 0.4);

  return (
    <Box mb={6}>
      <SectionTitleBar title={`Section ${rowIndex + 1}`} />
      <Box display="flex" alignItems="flex-start">
        <Box mt={4} mr={1}>
          <Checkbox checked={checked} onChange={(e) => setChecked(e.target.checked)} />
        </Box>
        <Grid container spacing={2} alignItems="flex-start" sx={{ opacity: getOpacity() }}>
          <Grid
            item
            xs={5.5}
            sx={{
              border: getBorderStyle(rightToLeft),
              borderRadius: "8px",
              backgroundColor: "white",
              padding: 2,
              minHeight: 200,
            }}
          >
            {leftContent}
          </Grid>
          <Grid item xs={1} textAlign="center">
            <Box>
              <IconButton onClick={() => setLeftToRight(!leftToRight)}>
                <CompareArrowsIcon
                  sx={{
                    transform: "rotate(0deg)",
                    color: leftToRight ? "gray" : "lightgray",
                  }}
                />
              </IconButton>
              <IconButton onClick={() => setRightToLeft(!rightToLeft)}>
                <CompareArrowsIcon
                  sx={{
                    transform: "rotate(180deg)",
                    color: rightToLeft ? "gray" : "lightgray",
                  }}
                />
              </IconButton>
            </Box>
          </Grid>
          <Grid
            item
            xs={5.5}
            sx={{
              border: getBorderStyle(leftToRight),
              borderRadius: "8px",
              backgroundColor: "white",
              padding: 2,
              minHeight: 200,
            }}
          >
            {rightContent}
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

const MainComponent = () => {
  return (
    <Box p={4}>
      <BoxPair
        rowIndex={0}
        leftContent={<PSCRFSection />}
        rightContent={<ApprovedContractSection />}
      />
      <BoxPair
        rowIndex={1}
        leftContent={<ApprovedContractSection />}
        rightContent={<ApprovedContractSection />}
      />
      <BoxPair
        rowIndex={2}
        leftContent={<ApprovedContractSection />}
        rightContent={<PSCRFSection />}
      />
      <BoxPair
        rowIndex={3}
        leftContent={<PSCRFSection />}
        rightContent={<PSCRFSection />}
      />
    </Box>
  );
};

export default MainComponent;

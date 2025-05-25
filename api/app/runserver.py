import React, { useState, useRef, forwardRef, useImperativeHandle, useEffect } from "react";
import {
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  Typography,
  Alert,
  IconButton,
  Collapse,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";

// PSCRFSection component with ref and validation method
const PSCRFSection = forwardRef((props, ref) => {
  const [selectedOptions, setSelectedOptions] = useState([]);

  useImperativeHandle(ref, () => ({
    hasSelectedOptions: () => selectedOptions.length > 0,
  }));

  // Simulated selection UI
  return (
    <Box
      sx={{
        p: 2,
        bgcolor: "#fff",
        border: "1px solid #ccc",
        borderRadius: 1,
        height: 250,
        overflowY: "auto",
      }}
    >
      <Typography variant="subtitle1" gutterBottom>
        PSCRF Section
      </Typography>
      <FormControlLabel
        control={
          <Checkbox
            checked={selectedOptions.includes("option1")}
            onChange={(e) => {
              if (e.target.checked) {
                setSelectedOptions((prev) => [...prev, "option1"]);
              } else {
                setSelectedOptions((prev) => prev.filter((o) => o !== "option1"));
              }
            }}
          />
        }
        label="Option 1"
      />
      <FormControlLabel
        control={
          <Checkbox
            checked={selectedOptions.includes("option2")}
            onChange={(e) => {
              if (e.target.checked) {
                setSelectedOptions((prev) => [...prev, "option2"]);
              } else {
                setSelectedOptions((prev) => prev.filter((o) => o !== "option2"));
              }
            }}
          />
        }
        label="Option 2"
      />
    </Box>
  );
});

// ContractSection component with ref and validation method
const ContractSection = forwardRef(({ title }, ref) => {
  const [files, setFiles] = useState([]);

  useImperativeHandle(ref, () => ({
    hasFileUploaded: () => files.length > 0,
  }));

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  return (
    <Box
      sx={{
        p: 2,
        bgcolor: "#fff",
        border: "1px solid #ccc",
        borderRadius: 1,
        height: 250,
        overflowY: "auto",
      }}
    >
      <Typography variant="subtitle1" gutterBottom>
        {title}
      </Typography>
      <input type="file" multiple onChange={handleFileChange} />
      {files.length > 0 && (
        <Box mt={1}>
          <Typography variant="body2">
            Uploaded files:
            <ul>
              {files.map((f, i) => (
                <li key={i}>{f.name}</li>
              ))}
            </ul>
          </Typography>
        </Box>
      )}
    </Box>
  );
});

// BoxPair component for each row
const BoxPair = ({
  title,
  checked,
  onCheckChange,
  validationMessage,
  leftComponent,
  rightComponent,
}) => {
  const [showValidation, setShowValidation] = useState(true);

  useEffect(() => {
    if (!validationMessage) setShowValidation(false);
    else setShowValidation(true);
  }, [validationMessage]);

  return (
    <Box mb={3} p={2} bgcolor="#fafafa" borderRadius={2} boxShadow={1}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
        <FormControlLabel
          control={<Checkbox checked={checked} onChange={onCheckChange} />}
          label={<Typography variant="h6">{title}</Typography>}
        />
        {validationMessage && (
          <Collapse in={showValidation} timeout="auto" unmountOnExit>
            <Alert
              severity="error"
              action={
                <IconButton
                  aria-label="close"
                  color="inherit"
                  size="small"
                  onClick={() => setShowValidation(false)}
                >
                  <CloseIcon fontSize="inherit" />
                </IconButton>
              }
              sx={{ ml: 2, maxWidth: 400 }}
            >
              {validationMessage}
            </Alert>
          </Collapse>
        )}
      </Box>
      <Box display="flex" gap={2}>
        <Box flex={1}>{leftComponent}</Box>
        <Box flex={1}>{rightComponent}</Box>
      </Box>
    </Box>
  );
};

// Main layout component
const ComparisonLayout = () => {
  // Checkbox checked state for 4 rows
  const [rowChecks, setRowChecks] = useState([false, false, false, false]);

  // Refs for PSCRF and Contract sections per row and side
  const pscrfLeftRefs = [useRef(), useRef(), useRef(), useRef()];
  const pscrfRightRefs = [useRef(), useRef(), useRef(), useRef()];
  const contractLeftRefs = [useRef(), useRef(), useRef(), useRef()];
  const contractRightRefs = [useRef(), useRef(), useRef(), useRef()];

  // Validation messages per row
  const [validationMessages, setValidationMessages] = useState(["", "", "", ""]);

  // Helper to check if a section is present on a side
  const isPSCRFPresent = (rowIndex, side) => {
    if (rowIndex === 0 && side === "left") return true;
    if (rowIndex === 2 && side === "right") return true;
    if (rowIndex === 3) return true;
    return false;
  };
  const isContractPresent = (rowIndex, side) => {
    if (rowIndex === 0 && side === "right") return true;
    if (rowIndex === 1 && side === "left") return true;
    if (rowIndex === 2 && side === "left") return true;
    return false;
  };

  const validateRow = (rowIndex) => {
    if (!rowChecks[rowIndex]) return ""; // Not checked => no validation error

    // Validate PSCRF if present on left and/or right
    let pscrfValid = true;
    if (isPSCRFPresent(rowIndex, "left")) {
      const hasSelected = pscrfLeftRefs[rowIndex].current?.hasSelectedOptions() || false;
      if (!hasSelected) pscrfValid = false;
    }
    if (isPSCRFPresent(rowIndex, "right")) {
      const hasSelected = pscrfRightRefs[rowIndex].current?.hasSelectedOptions() || false;
      if (!hasSelected) pscrfValid = false;
    }

    // Validate Contract if present on left and/or right
    let contractValid = true;
    if (isContractPresent(rowIndex, "left")) {
      const hasFile = contractLeftRefs[rowIndex].current?.hasFileUploaded() || false;
      if (!hasFile) contractValid = false;
    }
    if (isContractPresent(rowIndex, "right")) {
      const hasFile = contractRightRefs[rowIndex].current?.hasFileUploaded() || false;
      if (!hasFile) contractValid = false;
    }

    if (!pscrfValid && !contractValid)
      return "Please select at least one PSCRF and upload at least one contract file.";

    if (!pscrfValid) return "Please select at least one PSCRF.";

    if (!contractValid) return "Please upload at least one contract file.";

    return "";
  };

  // Validate all rows and update messages on checkbox change
  useEffect(() => {
    const msgs = [];
    for (let i = 0; i < 4; i++) {
      msgs.push(validateRow(i));
    }
    setValidationMessages(msgs);
  }, [rowChecks]);

  // Force re-validation state for internal triggers
  const [forceValidate, setForceValidate] = useState(0);

  // Re-validate on forceValidate changes
  useEffect(() => {
    const msgs = [];
    for (let i = 0; i < 4; i++) {
      msgs.push(validateRow(i));
    }
    setValidationMessages(msgs);
  }, [forceValidate]);

  const handleCheckboxChange = (index) => {
    const updatedChecks = [...rowChecks];
    updatedChecks[index] = !updatedChecks[index];
    setRowChecks(updatedChecks);
    setForceValidate((f) => f + 1); // force re-validate on toggle
  };

  // Submit enabled only if all checked rows have no validation errors
  const submitEnabled = rowChecks.every(
    (checked, i) => !checked || (validationMessages[i] === "")
  );

  return (
    <Box p={3} maxWidth={1200} mx="auto" bgcolor="#e0e0e0" borderRadius={2} my={4}>
      <BoxPair
        title="Row 1"
        checked={rowChecks[0]}
        onCheckChange={() => handleCheckboxChange(0)}
        validationMessage={validationMessages[0]}
        leftComponent={<PSCRFSection ref={pscrfLeftRefs[0]} />}
        rightComponent={<ContractSection ref={contractRightRefs[0]} title="Contract Section (Right)" />}
      />
      <BoxPair
        title="Row 2"
        checked={rowChecks[1]}
        onCheckChange={() => handleCheckboxChange(1)}
        validationMessage={validationMessages[1]}
        leftComponent={<ContractSection ref={contractLeftRefs[1]} title="Contract Section (Left)" />}
        rightComponent={<Box sx={{ height: 250, bgcolor: "#f0f0f0" }} />}
      />
      <BoxPair
        title="Row 3"
        checked={rowChecks[2]}
        onCheckChange={() => handleCheckboxChange(2)}
        validationMessage={validationMessages[2]}
        leftComponent={<ContractSection ref={contractLeftRefs[2]} title="Contract Section (Left)" />}
        rightComponent={<PSCRFSection ref={pscrfRightRefs[2]} />}
      />
      <BoxPair
        title="Row 4"
        checked={rowChecks[3]}
        onCheckChange={() => handleCheckboxChange(3)}
        validationMessage={validationMessages[3]}
        leftComponent={<PSCRFSection ref={pscrfLeftRefs[3]} />}
        rightComponent={<PSCRFSection ref={pscrfRightRefs[3]} />}
      />

      <Box mt={4} textAlign="center">
        <Button
          variant="contained"
          color="primary"
          disabled={!submitEnabled}
          onClick={() => alert("Submit successful!")}
          sx={{ minWidth: 140, fontWeight: 600, fontSize: 16 }}
        >
          Submit
        </Button>
        {!submitEnabled && (
          <Typography
            variant="body2"
            color="error"
            mt={1}
            sx={{ userSelect: "none", fontWeight: 500 }}
          >
            Please fix validation errors above before submitting.
          </Typography>
        )}
      </Box>
    </Box>
  );
};

export default ComparisonLayout;

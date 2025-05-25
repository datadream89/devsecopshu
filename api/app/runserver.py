import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Checkbox,
  Button,
  FormControlLabel,
  FormControl,
  FormLabel,
  RadioGroup,
  Radio,
} from "@mui/material";

const FILE_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  "application/msword",
];

const ContractSection = ({ title, sections: initialSections, onSectionsChange }) => {
  const [sections, setSections] = useState(
    initialSections && initialSections.length > 0
      ? initialSections
      : [{ id: Date.now(), type: "Agreement", file: null, filename: "" }]
  );

  useEffect(() => {
    if (initialSections) setSections(initialSections);
  }, [initialSections]);

  const updateSections = (updatedSections) => {
    setSections(updatedSections);
    if (onSectionsChange) onSectionsChange(updatedSections);
  };

  const handleAddSection = () => {
    updateSections([
      ...sections,
      { id: Date.now() + Math.random(), type: "Agreement", file: null, filename: "" },
    ]);
  };

  const handleRemoveSection = (id) => {
    updateSections(sections.filter((section) => section.id !== id));
  };

  const handleRadioChange = (id, type) => {
    updateSections(
      sections.map((section) =>
        section.id === id ? { ...section, type, file: null, filename: "" } : section
      )
    );
  };

  const handleFileChange = (id, event) => {
    const file = event.target.files[0];
    if (!file) return;
    if (!FILE_TYPES.includes(file.type)) {
      alert("Only PDF and Word files are allowed.");
      return;
    }
    updateSections(
      sections.map((section) =>
        section.id === id ? { ...section, file, filename: file.name } : section
      )
    );
  };

  return (
    <Box
      sx={{
        border: "1px solid #ccc",
        borderRadius: 1,
        p: 2,
        mt: 1,
        position: "relative",
      }}
    >
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>

      {sections.map((section, idx) => (
        <Box
          key={section.id}
          sx={{
            mb: 2,
            p: 1,
            border: "1px dashed #999",
            borderRadius: 1,
            position: "relative",
          }}
        >
          <FormControl component="fieldset">
            <FormLabel component="legend">Type</FormLabel>
            <RadioGroup
              row
              value={section.type}
              onChange={(e) => handleRadioChange(section.id, e.target.value)}
            >
              <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
              <FormControlLabel value="PO" control={<Radio />} label="PO" />
              <FormControlLabel value="Invoice" control={<Radio />} label="Invoice" />
            </RadioGroup>
          </FormControl>

          <Box mt={1}>
            <Button variant="outlined" component="label" size="small">
              Upload File
              <input
                type="file"
                accept=".pdf,.doc,.docx"
                hidden
                onChange={(e) => handleFileChange(section.id, e)}
              />
            </Button>
            {section.filename && (
              <Typography variant="body2" component="span" sx={{ ml: 2 }}>
                {section.filename}
              </Typography>
            )}
          </Box>

          {sections.length > 1 && (
            <Button
              variant="text"
              color="error"
              size="small"
              sx={{ position: "absolute", top: 8, right: 8 }}
              onClick={() => handleRemoveSection(section.id)}
            >
              ×
            </Button>
          )}
        </Box>
      ))}

      <Button variant="text" size="small" onClick={handleAddSection}>
        + Add Section
      </Button>
    </Box>
  );
};

const PSCRFSection = () => {
  return (
    <Box
      sx={{
        border: "1px solid #ccc",
        borderRadius: 1,
        p: 2,
        mt: 1,
        height: 150,
        textAlign: "center",
        color: "#666",
      }}
    >
      <Typography>PSCRF Section (placeholder)</Typography>
    </Box>
  );
};

const BoxPair = ({ title, checked, onCheckChange, leftComponent, rightComponent }) => {
  return (
    <Box sx={{ display: "flex", gap: 2, mb: 3, alignItems: "center" }}>
      <FormControlLabel
        control={<Checkbox checked={checked} onChange={onCheckChange} />}
        label={title}
        sx={{ width: 100 }}
      />
      <Box sx={{ flex: 1 }}>{leftComponent}</Box>
      <Box sx={{ flex: 1 }}>{rightComponent}</Box>
    </Box>
  );
};

const ComparisonLayout = () => {
  const [rowChecks, setRowChecks] = useState([true, true, true, true]);

  // Lifted ContractSection states
  const [contractData, setContractData] = useState({
    approved1: [{ id: Date.now(), type: "Agreement", file: null, filename: "" }],
    approved2: [{ id: Date.now() + 1, type: "Agreement", file: null, filename: "" }],
    signed1: [{ id: Date.now() + 2, type: "Agreement", file: null, filename: "" }],
  });

  const updateContractSection = (key, sections) => {
    setContractData((prev) => ({ ...prev, [key]: sections }));
  };

  const toggleRowCheck = (index) => {
    const newChecks = [...rowChecks];
    newChecks[index] = !newChecks[index];
    setRowChecks(newChecks);
  };

  const handleSubmit = () => {
    for (const [sectionName, sections] of Object.entries(contractData)) {
      const hasValidSection = sections.some(
        (sec) => sec.type && sec.file != null
      );
      if (!hasValidSection) {
        alert(
          `Please upload at least one file and select type in ${sectionName
            .replace(/([A-Z])/g, " $1")
            .trim()}`
        );
        return;
      }
    }
    alert("Validation passed! Submitting form...");
    // Add your submit logic here
  };

  return (
    <Box
      sx={{ width: "95vw", maxWidth: 1200, mx: "auto", mt: 3, mb: 6, px: 1, userSelect: "none" }}
    >
      {/* Row 1 */}
      <BoxPair
        title="Row 1"
        checked={rowChecks[0]}
        onCheckChange={() => toggleRowCheck(0)}
        leftComponent={<PSCRFSection />}
        rightComponent={
          <ContractSection
            title="Approved Contract"
            sections={contractData.approved1}
            onSectionsChange={(sections) => updateContractSection("approved1", sections)}
          />
        }
      />

      {/* Row 2 */}
      <BoxPair
        title="Row 2"
        checked={rowChecks[1]}
        onCheckChange={() => toggleRowCheck(1)}
        leftComponent={
          <ContractSection
            title="Approved Contract"
            sections={contractData.approved2}
            onSectionsChange={(sections) => updateContractSection("approved2", sections)}
          />
        }
        rightComponent={
          <ContractSection
            title="Signed Contract"
            sections={contractData.signed1}
            onSectionsChange={(sections) => updateContractSection("signed1", sections)}
          />
        }
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

      <Box mt={4} textAlign="center">
        <Button variant="contained" color="primary" onClick={handleSubmit}>
          Submit
        </Button>
      </Box>
    </Box>
  );
};

export default ComparisonLayout;

import React, { useState, forwardRef, useImperativeHandle } from "react";
import { Box, Typography, Button, Input } from "@mui/material";

const ContractSection = forwardRef(({ title }, ref) => {
  const [sections, setSections] = useState([
    { id: Date.now(), file: null, filename: "", error: false },
  ]);

  // Expose a validate method to parent
  useImperativeHandle(ref, () => ({
    validate: () => {
      let isValid = true;
      const updated = sections.map((section) => {
        const valid = !!section.file;
        if (!valid) isValid = false;
        return { ...section, error: !valid };
      });
      setSections(updated);
      return isValid;
    },
  }));

  const handleFileChange = (id, event) => {
    const file = event.target.files[0];
    setSections((prev) =>
      prev.map((section) => {
        if (section.id === id) {
          return {
            ...section,
            file,
            filename: file ? file.name : "",
            error: !file ? true : false, // <-- reset error when file is valid
          };
        }
        return section;
      })
    );
  };

  const handleAddSection = () => {
    setSections((prev) => [
      ...prev,
      { id: Date.now(), file: null, filename: "", error: false },
    ]);
  };

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white" minHeight={220}>
      <Typography variant="h6" mb={2}>
        {title}
      </Typography>
      {sections.map(({ id, filename, error }) => (
        <Box key={id} mb={2}>
          <Input
            type="file"
            onChange={(e) => handleFileChange(id, e)}
            error={error}
            sx={{ display: "block", mb: 1 }}
          />
          <Typography color={filename ? "text.secondary" : error ? "error" : "text.secondary"} variant="body2">
            {filename || "No file chosen"}
          </Typography>
          {error && !filename && (
            <Typography color="error" variant="caption">
              Please upload a file.
            </Typography>
          )}
        </Box>
      ))}
      <Button variant="outlined" onClick={handleAddSection}>
        Add Section
      </Button>
    </Box>
  );
});

export default ContractSection;

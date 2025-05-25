import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  Collapse,
  TextField,
  Autocomplete,
  Card,
  CardContent,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel as MuiFormControlLabel,
  Stack,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

// Sample PSCRF data
const pscrfData = [
  { id: 101, samVersion: "v1.0", pricingVersion: "p1.0", clientName: "Client A" },
  { id: 102, samVersion: "v1.1", pricingVersion: "p1.1", clientName: "Client B" },
  { id: 103, samVersion: "v2.0", pricingVersion: "p2.0", clientName: "Client C" },
];

// PSCRF Section with autocomplete and closeable cards
function PSCRFSection() {
  const [selected, setSelected] = useState([]);

  const handleSelect = (event, value) => {
    if (!value) return;
    if (selected.find((item) => item.id === value.id)) return;
    setSelected((prev) => [...prev, value]);
  };

  const handleRemove = (id) => {
    setSelected((prev) => prev.filter((item) => item.id !== id));
  };

  return (
    <Box>
      <Autocomplete
        options={pscrfData}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        onChange={handleSelect}
        renderInput={(params) => (
          <TextField {...params} label="Select PSCRF" variant="outlined" size="small" />
        )}
        clearOnBlur
        clearOnEscape
        disableClearable={false}
        sx={{ mb: 2 }}
      />

      {selected.map((item) => (
        <Card key={item.id} sx={{ mb: 1, position: "relative" }}>
          <IconButton
            size="small"
            sx={{ position: "absolute", top: 4, right: 4 }}
            onClick={() => handleRemove(item.id)}
            aria-label="Remove PSCRF"
          >
            <CloseIcon fontSize="small" />
          </IconButton>
          <CardContent>
            <Typography>
              ID: {item.id}, SAM: {item.samVersion}, Pricing: {item.pricingVersion}, Client:{" "}
              {item.clientName}
            </Typography>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
}

// Approved Contract Box with radios and file upload
function ContractBox({ id, data, onChange, onRemove, removable, title }) {
  const handleRadioChange = (event) => {
    onChange(id, { type: event.target.value, fileName: null });
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      onChange(id, { ...data, fileName: file.name });
    }
  };

  return (
    <Box
      sx={{
        border: "1px solid #ccc",
        borderRadius: 1,
        p: 2,
        mb: 2,
        position: "relative",
      }}
    >
      {removable && (
        <IconButton
          size="small"
          sx={{ position: "absolute", top: 4, right: 4 }}
          onClick={() => onRemove(id)}
          aria-label="Remove contract"
        >
          <CloseIcon />
        </IconButton>
      )}

      <Typography variant="subtitle1" fontWeight="bold" mb={1}>
        {title}
      </Typography>

      <RadioGroup
        row
        value={data.type}
        onChange={handleRadioChange}
        aria-label="contract type"
        name={`contract-type-${id}`}
      >
        <MuiFormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
        <MuiFormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
        <MuiFormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
      </RadioGroup>

      <Stack direction="row" alignItems="center" spacing={1} sx={{ mt: 1 }}>
        <Button
          variant="contained"
          component="label"
          startIcon={<CloudUploadIcon />}
          sx={{ bgcolor: "#424242", "&:hover": { bgcolor: "#333" } }}
        >
          Upload File
          <input
            type="file"
            hidden
            onChange={handleFileUpload}
            aria-label="upload contract file"
          />
        </Button>

        {data.fileName && (
          <Typography variant="body2" sx={{ ml: 1 }}>
            {data.fileName}
          </Typography>
        )}
      </Stack>
    </Box>
  );
}

// Approved Contract Section managing multiple ContractBoxes
function ApprovedContractSection() {
  const [contracts, setContracts] = useState([{ id: 1, type: "Agreement", fileName: null }]);

  const addContract = () => {
    const newId = contracts.length ? contracts[contracts.length - 1].id + 1 : 1;
    setContracts([...contracts, { id: newId, type: "Agreement", fileName: null }]);
  };

  const updateContract = (id, newData) => {
    setContracts((prev) =>
      prev.map((contract) => (contract.id === id ? { ...contract, ...newData } : contract))
    );
  };

  const removeContract = (id) => {
    setContracts((prev) => prev.filter((contract) => contract.id !== id));
  };

  return (
    <Box>
      {contracts.map((contract, index) => (
        <ContractBox
          key={contract.id}
          id={contract.id}
          data={contract}
          onChange={updateContract}
          onRemove={removeContract}
          removable={index !== 0}
          title={`Approved contract ${index + 1}`}
        />
      ))}

      <Button variant="outlined" startIcon={<AddIcon />} onClick={addContract} sx={{ mt: 1 }}>
        Add Contract
      </Button>
    </Box>
  );
}

// Main component with layout and all 4 sections
export default function MainComponent() {
  /*
    Layout:
    Row 1: Section 1 top left box | Section 2 right box
    Row 2: Section 3 left box
    Row 3: Section 4 left and right boxes
  */

  return (
    <Box sx={{ maxWidth: 1200, mx: "auto", mt: 4, px: 2 }}>
      {/* Row 1 */}
      <Box sx={{ display: "flex", gap: 4, mb: 4 }}>
        {/* Section 1 top left box */}
        <Box sx={{ flex: 1, border: "1px solid #ccc", p: 2, borderRadius: 1 }}>
          <Typography variant="h6" mb={2}>
            PSCRF Section (Section 1 - Top Left Box)
          </Typography>
          <PSCRFSection />
        </Box>

        {/* Section 2 right box */}
        <Box sx={{ flex: 1, border: "1px solid #ccc", p: 2, borderRadius: 1 }}>
          <Typography variant="h6" mb={2}>
            Approved Contract Section (Section 2 - Right Box)
          </Typography>
          <ApprovedContractSection />
        </Box>
      </Box>

      {/* Row 2 */}
      <Box sx={{ display: "flex", gap: 4, mb: 4 }}>
        {/* Section 3 left box */}
        <Box sx={{ flex: 1, border: "1px solid #ccc", p: 2, borderRadius: 1 }}>
          <Typography variant="h6" mb={2}>
            Approved Contract Section (Section 3 - Left Box)
          </Typography>
          <ApprovedContractSection />
        </Box>

        {/* empty space */}
        <Box sx={{ flex: 1 }} />
      </Box>

      {/* Row 3 */}
      <Box sx={{ display: "flex", gap: 4, mb: 4 }}>
        {/* Section 4 left box */}
        <Box sx={{ flex: 1, border: "1px solid #ccc", p: 2, borderRadius: 1 }}>
          <Typography variant="h6" mb={2}>
            PSCRF Section (Section 4 - Left Box)
          </Typography>
          <PSCRFSection />
        </Box>

        {/* Section 4 right box */}
        <Box sx={{ flex: 1, border: "1px solid #ccc", p: 2, borderRadius: 1 }}>
          <Typography variant="h6" mb={2}>
            PSCRF Section (Section 4 - Right Box)
          </Typography>
          <PSCRFSection />
        </Box>
      </Box>
    </Box>
  );
}

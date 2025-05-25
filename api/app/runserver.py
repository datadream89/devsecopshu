import React, { useState } from "react";
import {
  Box,
  Typography,
  IconButton,
  TextField,
  Autocomplete,
  Card,
  CardContent,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel as MuiFormControlLabel,
  Stack,
  Checkbox,
  Divider,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CompareArrowsIcon from "@mui/icons-material/CompareArrows";

// Sample PSCRF data
const pscrfData = [
  { id: 101, samVersion: "v1.0", pricingVersion: "p1.0", clientName: "Client A" },
  { id: 102, samVersion: "v1.1", pricingVersion: "p1.1", clientName: "Client B" },
  { id: 103, samVersion: "v2.0", pricingVersion: "p2.0", clientName: "Client C" },
];

// PSCRF Section component
function PSCRFSection() {
  const [selected, setSelected] = useState([]);

  const handleSelect = (event, value) => {
    if (!value) return;
    if (selected.find((item) => item.id === value.id)) return; // prevent duplicates
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

// ContractBox component
function ContractBox({ id, data, onChange, onRemove, removable, title }) {
  const handleRadioChange = (event) => {
    onChange(id, { type: event.target.value, fileName: null }); // Reset fileName on radio change
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

// Approved Contract Section component
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

// Empty Box placeholder component
function EmptyBox() {
  return (
    <Box
      sx={{
        border: "1px solid #ccc",
        borderRadius: 1,
        minHeight: 350,
        p: 2,
      }}
    >
      {/* Empty box, can add content if needed */}
    </Box>
  );
}

// Left panel with arrows and compare checkbox
function LeftPanel({ compareChecked, onCompareChange }) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        pr: 1,
        minWidth: 80,
        justifyContent: "center",
        borderRight: "1px solid #ccc",
      }}
    >
      <CompareArrowsIcon fontSize="large" sx={{ mb: 1 }} />
      <MuiFormControlLabel
        control={<Checkbox checked={compareChecked} onChange={onCompareChange} />}
        label="Compare"
        sx={{ mt: 1 }}
      />
    </Box>
  );
}

// Row component with left panel and two boxes
function Row({
  leftContent,
  rightContent,
  compareChecked,
  onCompareChange,
  leftTitle,
  rightTitle,
  leftKey,
  rightKey,
}) {
  return (
    <Box sx={{ width: "100%" }}>
      <Divider sx={{ mb: 2, borderBottomWidth: 2 }} />

      <Box sx={{ display: "flex", alignItems: "stretch", gap: 2 }}>
        <LeftPanel compareChecked={compareChecked} onCompareChange={onCompareChange} />

        {/* Left box */}
        <Box sx={{ flex: 1 }}>
          <Typography variant="h6" mb={2} fontWeight="bold">
            {leftTitle}
          </Typography>
          <Box sx={{ border: "1px solid #ccc", borderRadius: 1, p: 2, minHeight: 350 }}>
            {leftContent}
          </Box>
        </Box>

        {/* Right box */}
        <Box sx={{ flex: 1 }}>
          <Typography variant="h6" mb={2} fontWeight="bold">
            {rightTitle}
          </Typography>
          <Box sx={{ border: "1px solid #ccc", borderRadius: 1, p: 2, minHeight: 350 }}>
            {rightContent}
          </Box>
        </Box>
      </Box>
    </Box>
  );
}

// Main component with 4 rows × 2 boxes layout with left panels and dividers
export default function MainComponent() {
  // Track compare checkbox states for each row (4 rows)
  const [compareStates, setCompareStates] = useState([false, false, false, false]);

  const handleCompareChange = (index) => (event) => {
    const newStates = [...compareStates];
    newStates[index] = event.target.checked;
    setCompareStates(newStates);
  };

  return (
    <Box
      sx={{
        maxWidth: 1200,
        mx: "auto",
        mt: 4,
        px: 2,
        display: "flex",
        flexDirection: "column",
        gap: 4,
      }}
    >
      {/* Row 1 */}
      <Row
        compareChecked={compareStates[0]}
        onCompareChange={handleCompareChange(0)}
        leftTitle="PSCRF Section (Row 1 Left)"
        rightTitle="Approved Contract Section (Row 1 Right)"
        leftContent={<PSCRFSection />}
        rightContent={<ApprovedContractSection />}
      />

      {/* Row 2 */}
      <Row
        compareChecked={compareStates[1]}
        onCompareChange={handleCompareChange(1)}
        leftTitle="Approved Contract Section (Row 2 Left)"
        rightTitle="Empty Box (Row 2 Right)"
        leftContent={<ApprovedContractSection />}
        rightContent={<EmptyBox />}
      />

      {/* Row 3 */}
      <Row
        compareChecked={compareStates[2]}
        onCompareChange={handleCompareChange(2)}
        leftTitle="Empty Box (Row 3 Left)"
        rightTitle="PSCRF Section (Row 3 Right)"
        leftContent={<EmptyBox />}
        rightContent={<PSCRFSection />}
      />

      {/* Row 4 */}
      <Row
        compareChecked={compareStates[3]}
        onCompareChange={handleCompareChange(3)}
        leftTitle="PSCRF Section (Row 4 Left)"
        rightTitle="PSCRF Section (Row 4 Right)"
        leftContent={<PSCRFSection />}
        rightContent={<PSCRFSection />}
      />
    </Box>
  );
}

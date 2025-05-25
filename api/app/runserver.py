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
import ArrowBackIosNewIcon from "@mui/icons-material/ArrowBackIosNew";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

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
        <Card
          key={item.id}
          sx={{
            mb: 1,
            position: "relative",
            borderColor: "#1976d2",
            borderWidth: 1,
            borderStyle: "solid",
          }}
        >
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
function ContractBox({ id, data, onChange, onRemove, removable, title, borderColor, opacity }) {
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
        border: `2px solid ${borderColor}`,
        borderRadius: 1,
        p: 2,
        mb: 2,
        position: "relative",
        opacity: opacity,
        transition: "opacity 0.3s",
        minHeight: 350,
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
function ApprovedContractSection({ borderColor, opacity }) {
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
          borderColor={borderColor}
          opacity={opacity}
        />
      ))}

      <Button variant="outlined" startIcon={<AddIcon />} onClick={addContract} sx={{ mt: 1 }}>
        Add Contract
      </Button>
    </Box>
  );
}

// Empty Box placeholder component
function EmptyBox({ borderColor, opacity }) {
  return (
    <Box
      sx={{
        border: `2px solid ${borderColor}`,
        borderRadius: 1,
        minHeight: 350,
        p: 2,
        opacity: opacity,
        transition: "opacity 0.3s",
      }}
    />
  );
}

// Arrow and border colors
const lightGray = "#b0b0b0";
const darkGray = "#424242";

// Compare arrows between boxes with highlight
function CompareArrows({ direction, onChange }) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        px: 1,
        userSelect: "none",
      }}
    >
      <ArrowBackIosNewIcon
        sx={{
          cursor: "pointer",
          color: direction === "left" ? darkGray : lightGray,
          mb: 1,
        }}
        onClick={() => onChange("left")}
        fontSize="small"
        aria-label="Arrow left"
      />
      <ArrowForwardIosIcon
        sx={{
          cursor: "pointer",
          color: direction === "right" ? darkGray : lightGray,
        }}
        onClick={() => onChange("right")}
        fontSize="small"
        aria-label="Arrow right"
      />
    </Box>
  );
}

// Left Compare checkbox
function CompareCheckbox({ checked, onChange }) {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        px: 1,
        userSelect: "none",
        mb: 1,
        justifyContent: "flex-start",
      }}
    >
      <Checkbox checked={checked} onChange={onChange} />
      <Typography>Compare</Typography>
    </Box>
  );
}

// Row component with divider, compare checkbox, arrows, and two boxes
function Row({ index, leftContent, rightContent, leftTitle, rightTitle }) {
  // State for compare checkbox and arrow direction for this row
  const [compareChecked, setCompareChecked] = useState(false);
  const [arrowDirection, setArrowDirection] = useState("left"); // "left" or "right"

  // Handle compare checkbox toggle
  const handleCompareChange = (e) => {
    setCompareChecked(e.target.checked);
  };

  // Handle arrow click
  const handleArrowChange = (dir) => {
    setArrowDirection(dir);
  };

  // Determine box border and opacity based on compare and arrowDirection
  const leftBoxBorder = arrowDirection === "left" ? darkGray : lightGray;
  const rightBoxBorder = arrowDirection === "right" ? darkGray : lightGray;
  const opacity = compareChecked ? 1 : 0.4;

  return (
    <Box sx={{ width: "100%" }}>
      <Divider sx={{ mb: 2, borderBottomWidth: 2 }} />

      {/* Compare checkbox above arrow */}
      <CompareCheckbox checked={compareChecked} onChange={handleCompareChange} />

      <Box sx={{ display: "flex", alignItems: "stretch", gap: 1 }}>
        {/* Left box */}
        <Box
          sx={{
            flex: 1,
            border: 2,
            borderColor: leftBoxBorder,
            borderRadius: 1,
            p: 2,
            minHeight: 350,
            opacity: opacity,
            transition: "opacity 0.3s",
          }}
        >
          <Typography variant="h6" mb={2} fontWeight="bold">
            {leftTitle}
          </Typography>
          {leftContent}
        </Box>

        {/* Arrows between boxes */}
        <CompareArrows direction={arrowDirection} onChange={handleArrowChange} />

        {/* Right box */}
        <Box
          sx={{
            flex: 1,
            border: 2,
            borderColor: rightBoxBorder,
            borderRadius: 1,
            p: 2,
            minHeight: 350,
            opacity: opacity,
            transition: "opacity 0.3s",
          }}
        >
          <Typography variant="h6" mb={2} fontWeight="bold">
            {rightTitle}
          </Typography>
          {rightContent}
        </Box>
      </Box>
    </Box>
  );
}

// Main component with 4 rows and correct content
export default function MainComponent() {
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
        index={1}
        leftTitle="PSCRF Section (Row 1 Left)"
        rightTitle="Approved Contract Section (Row 1 Right)"
        leftContent={<PSCRFSection />}
        rightContent={<ApprovedContractSection />}
      />

      {/* Row 2 */}
      <Row
        index={2}
        leftTitle="Empty Box (Row 2 Left)"
        rightTitle="Empty Box (Row 2 Right)"
        leftContent={<EmptyBox />}
        rightContent={<EmptyBox />}
      />

      {/* Row 3 */}
      <Row
        index={3}
        leftTitle="Empty Box (Row 3 Left)"
        rightTitle="Empty Box (Row 3 Right)"
        leftContent={<EmptyBox />}
        rightContent={<EmptyBox />}
      />

      {/* Row 4 */}
      <Row
        index={4}
        leftTitle="Empty Box (Row 4 Left)"
        rightTitle="Empty Box (Row 4 Right)"
        leftContent={<EmptyBox />}
        rightContent={<EmptyBox />}
      />
    </Box>
  );
}

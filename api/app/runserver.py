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
  FormControlLabel,
  Stack,
  Checkbox,
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

// PSCRF Section with Autocomplete + removable cards
function PSCRFSection() {
  const [selected, setSelected] = useState([]);

  const handleSelect = (event, value) => {
    if (!value) return;
    if (selected.find((item) => item.id === value.id)) return; // no duplicates
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

// Approved Contract Box
function ContractBox({ id, data, onChange, onRemove, removable, borderColor, opacity }) {
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
        border: `2px solid ${borderColor}`,
        borderRadius: 1,
        p: 2,
        mb: 2,
        position: "relative",
        opacity: opacity,
        transition: "opacity 0.3s",
        minHeight: 160,
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
        Approved contract {id}
      </Typography>

      <RadioGroup
        row
        value={data.type}
        onChange={handleRadioChange}
        aria-label="contract type"
        name={`contract-type-${id}`}
      >
        <FormControlLabel value="Agreement" control={<Radio />} label="Agreement" />
        <FormControlLabel value="Supplement" control={<Radio />} label="Supplement" />
        <FormControlLabel value="Addendum" control={<Radio />} label="Addendum" />
      </RadioGroup>

      <Stack direction="row" alignItems="center" spacing={1} sx={{ mt: 1 }}>
        <Button
          variant="contained"
          component="label"
          startIcon={<CloudUploadIcon />}
          sx={{ bgcolor: "#424242", "&:hover": { bgcolor: "#333" } }}
          disabled={opacity < 1}
        >
          Upload File
          <input type="file" hidden onChange={handleFileUpload} aria-label="upload contract file" />
        </Button>

        {data.fileName && <Typography variant="body2">{data.fileName}</Typography>}
      </Stack>
    </Box>
  );
}

// Approved Contract Section with add/remove
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
      {contracts.map((contract, idx) => (
        <ContractBox
          key={contract.id}
          id={contract.id}
          data={contract}
          onChange={updateContract}
          onRemove={removeContract}
          removable={idx !== 0}
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

// Empty Box placeholder
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

const lightGray = "#b0b0b0";
const darkGray = "#424242";

function CompareArrows({ direction, onChange, disabled }) {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        px: 1,
        userSelect: "none",
        justifyContent: "center",
        height: "100%",
        opacity: disabled ? 0.5 : 1,
      }}
    >
      <ArrowBackIosNewIcon
        sx={{
          cursor: disabled ? "default" : "pointer",
          color: direction === "left" ? darkGray : lightGray,
          mb: 1,
        }}
        onClick={() => !disabled && onChange("left")}
        fontSize="small"
        aria-label="Arrow left"
      />
      <ArrowForwardIosIcon
        sx={{
          cursor: disabled ? "default" : "pointer",
          color: direction === "right" ? darkGray : lightGray,
        }}
        onClick={() => !disabled && onChange("right")}
        fontSize="small"
        aria-label="Arrow right"
      />
    </Box>
  );
}

function CompareCheckbox({ checked, onChange }) {
  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        userSelect: "none",
        mr: 2,
        minWidth: 120,
      }}
    >
      <Checkbox checked={checked} onChange={onChange} />
      <Typography>Compare</Typography>
    </Box>
  );
}

function PairTitle({ title }) {
  return (
    <Box
      sx={{
        bgcolor: "#e0e0e0",
        py: 1,
        mb: 1,
        borderRadius: 1,
        textAlign: "center",
        fontWeight: "bold",
        fontSize: 16,
        userSelect: "none",
      }}
    >
      {title}
    </Box>
  );
}

// Main Component
export default function App() {
  // state for 4 pairs: each has compare checked, arrow direction: "left", "right" or null
  const [pairs, setPairs] = useState([
    { compare: true, arrow: null },
    { compare: true, arrow: null },
    { compare: true, arrow: null },
    { compare: true, arrow: null },
  ]);

  const handleCompareChange = (index) => (e) => {
    setPairs((prev) =>
      prev.map((p, i) => (i === index ? { ...p, compare: e.target.checked, arrow: null } : p))
    );
  };

  const handleArrowChange = (index, direction) => {
    setPairs((prev) =>
      prev.map((p, i) =>
        i === index ? { ...p, arrow: p.arrow === direction ? null : direction } : p
      )
    );
  };

  // Helper to determine border color and opacity per box
  const getBoxStyles = (pairIndex, side) => {
    const pair = pairs[pairIndex];
    if (!pair.compare) return { borderColor: lightGray, opacity: 0.6 };
    // highlight border if arrow matches this side
    if (pair.arrow === side) return { borderColor: darkGray, opacity: 1 };
    return { borderColor: lightGray, opacity: 1 };
  };

  return (
    <Box sx={{ maxWidth: 1300, mx: "auto", p: 3, fontFamily: "Arial, sans-serif" }}>
      {/* Four pairs */}

      {[0, 1, 2, 3].map((pairIndex) => (
        <Box key={pairIndex} sx={{ mb: 6 }}>
          <PairTitle title={`Pair ${pairIndex + 1} Title`} />

          <Box sx={{ display: "flex", alignItems: "stretch" }}>
            {/* Compare checkbox left */}
            <CompareCheckbox
              checked={pairs[pairIndex].compare}
              onChange={handleCompareChange(pairIndex)}
            />

            {/* Left box */}
            <Box
              sx={{
                flex: 1,
                borderRadius: 1,
                border: `2px solid ${getBoxStyles(pairIndex, "left").borderColor}`,
                opacity: getBoxStyles(pairIndex, "left").opacity,
                p: 2,
                mr: 1,
                minHeight: 350,
                transition: "opacity 0.3s, border-color 0.3s",
                backgroundColor: "#fff",
              }}
            >
              {pairIndex === 0 && <PSCRFSection />}
              {pairIndex === 1 && (
                <ApprovedContractSection
                  borderColor={getBoxStyles(pairIndex, "left").borderColor}
                  opacity={getBoxStyles(pairIndex, "left").opacity}
                />
              )}
              {(pairIndex === 2 || pairIndex === 3) && (
                <EmptyBox
                  borderColor={getBoxStyles(pairIndex, "left").borderColor}
                  opacity={getBoxStyles(pairIndex, "left").opacity}
                />
              )}
            </Box>

            {/* Arrows */}
            <CompareArrows
              direction={pairs[pairIndex].arrow}
              onChange={(dir) => handleArrowChange(pairIndex, dir)}
              disabled={!pairs[pairIndex].compare}
            />

            {/* Right box */}
            <Box
              sx={{
                flex: 1,
                borderRadius: 1,
                border: `2px solid ${getBoxStyles(pairIndex, "right").borderColor}`,
                opacity: getBoxStyles(pairIndex, "right").opacity,
                p: 2,
                ml: 1,
                minHeight: 350,
                transition: "opacity 0.3s, border-color 0.3s",
                backgroundColor: "#fff",
              }}
            >
              {(pairIndex === 0 || pairIndex === 1) && (
                <EmptyBox
                  borderColor={getBoxStyles(pairIndex, "right").borderColor}
                  opacity={getBoxStyles(pairIndex, "right").opacity}
                />
              )}
              {(pairIndex === 2 || pairIndex === 3) && (
                <EmptyBox
                  borderColor={getBoxStyles(pairIndex, "right").borderColor}
                  opacity={getBoxStyles(pairIndex, "right").opacity}
                />
              )}
            </Box>
          </Box>
        </Box>
      ))}
    </Box>
  );
}

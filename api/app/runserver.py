import React, { useState } from 'react';
import { Card, Typography } from "@/components/ui/card";
import { TextField, Autocomplete } from "@mui/material";
import LeftBoxCard from "./LeftBoxCard"; // Update path as needed

const options = [
  { id: 'PS001', samVersion: 'v1', pricingVersion: 'p1', clientName: 'Client A' },
  { id: 'PS002', samVersion: 'v2', pricingVersion: 'p2', clientName: 'Client B' },
  { id: 'PS003', samVersion: 'v3', pricingVersion: 'p3', clientName: 'Client C' }
];

const PSCRFComparison = () => {
  const [compareEnabled, setCompareEnabled] = useState(true);

  const [selectedPSCRF, setSelectedPSCRF] = useState([]);
  const [selectedContract, setSelectedContract] = useState([]);
  const [selectedOptionsLeft, setSelectedOptionsLeft] = useState([]);
  const [selectedOptionsRight, setSelectedOptionsRight] = useState([]);
  const [selectedOptionsLeft2, setSelectedOptionsLeft2] = useState([]);
  const [selectedOptionsRight2, setSelectedOptionsRight2] = useState([]);

  const removeOption = (setFn, currentList, itemToRemove) => {
    setFn(currentList.filter(item => item !== itemToRemove));
  };

  return (
    <div className="p-8">
      {/* === FIRST ROW: PSCRF vs Approved Contract === */}
      <Typography variant="h5" className="mt-8 mb-4">
        Compare PSCRF Data and Approved Contract
      </Typography>
      <div className="grid grid-cols-2 gap-4">
        <Card className="p-4">
          <Typography variant="h6" mb={2}>PSCRF Data</Typography>
          <Autocomplete
            multiple
            options={options}
            filterSelectedOptions
            value={selectedPSCRF}
            onChange={(e, newValue) => setSelectedPSCRF(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select PSCRF IDs" placeholder="Start typing..." size="small" />
            )}
            disabled={!compareEnabled}
            sx={{ mb: 2 }}
          />
          {selectedPSCRF.map((item) => (
            <LeftBoxCard
              key={`pscrf-${item.id}-${item.samVersion}-${item.pricingVersion}`}
              item={item}
              onRemove={() => removeOption(setSelectedPSCRF, selectedPSCRF, item)}
            />
          ))}
        </Card>

        <Card className="p-4">
          <Typography variant="h6" mb={2}>Approved Contract</Typography>
          <Autocomplete
            multiple
            options={options}
            filterSelectedOptions
            value={selectedContract}
            onChange={(e, newValue) => setSelectedContract(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select Contract IDs" placeholder="Start typing..." size="small" />
            )}
            disabled={!compareEnabled}
            sx={{ mb: 2 }}
          />
          {selectedContract.map((item) => (
            <LeftBoxCard
              key={`contract-${item.id}-${item.samVersion}-${item.pricingVersion}`}
              item={item}
              onRemove={() => removeOption(setSelectedContract, selectedContract, item)}
            />
          ))}
        </Card>
      </div>

      {/* === SECOND ROW: PSCRF vs PSCRF === */}
      <Typography variant="h5" className="mt-12 mb-4">
        Compare PSCRF Data and PSCRF Data
      </Typography>
      <div className="grid grid-cols-2 gap-4">
        <Card className="p-4">
          <Typography variant="h6" mb={2}>PSCRF Data (Left)</Typography>
          <Autocomplete
            multiple
            options={options}
            filterSelectedOptions
            value={selectedOptionsLeft}
            onChange={(e, newValue) => setSelectedOptionsLeft(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select PSCRF IDs" placeholder="Start typing..." size="small" />
            )}
            disabled={!compareEnabled}
            sx={{ mb: 2 }}
          />
          {selectedOptionsLeft.map((item) => (
            <LeftBoxCard
              key={`left-${item.id}-${item.samVersion}-${item.pricingVersion}`}
              item={item}
              onRemove={() => removeOption(setSelectedOptionsLeft, selectedOptionsLeft, item)}
            />
          ))}
        </Card>

        <Card className="p-4">
          <Typography variant="h6" mb={2}>PSCRF Data (Right)</Typography>
          <Autocomplete
            multiple
            options={options}
            filterSelectedOptions
            value={selectedOptionsRight}
            onChange={(e, newValue) => setSelectedOptionsRight(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select PSCRF IDs" placeholder="Start typing..." size="small" />
            )}
            disabled={!compareEnabled}
            sx={{ mb: 2 }}
          />
          {selectedOptionsRight.map((item) => (
            <LeftBoxCard
              key={`right-${item.id}-${item.samVersion}-${item.pricingVersion}`}
              item={item}
              onRemove={() => removeOption(setSelectedOptionsRight, selectedOptionsRight, item)}
            />
          ))}
        </Card>
      </div>

      {/* === THIRD ROW: PSCRF vs PSCRF (2) === */}
      <Typography variant="h5" className="mt-12 mb-4">
        Compare PSCRF Data and PSCRF Data (Second Pair)
      </Typography>
      <div className="grid grid-cols-2 gap-4">
        <Card className="p-4">
          <Typography variant="h6" mb={2}>PSCRF Data (Left 2)</Typography>
          <Autocomplete
            multiple
            options={options}
            filterSelectedOptions
            value={selectedOptionsLeft2}
            onChange={(e, newValue) => setSelectedOptionsLeft2(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select PSCRF IDs" placeholder="Start typing..." size="small" />
            )}
            disabled={!compareEnabled}
            sx={{ mb: 2 }}
          />
          {selectedOptionsLeft2.map((item) => (
            <LeftBoxCard
              key={`left2-${item.id}-${item.samVersion}-${item.pricingVersion}`}
              item={item}
              onRemove={() => removeOption(setSelectedOptionsLeft2, selectedOptionsLeft2, item)}
            />
          ))}
        </Card>

        <Card className="p-4">
          <Typography variant="h6" mb={2}>PSCRF Data (Right 2)</Typography>
          <Autocomplete
            multiple
            options={options}
            filterSelectedOptions
            value={selectedOptionsRight2}
            onChange={(e, newValue) => setSelectedOptionsRight2(newValue)}
            renderInput={(params) => (
              <TextField {...params} label="Select PSCRF IDs" placeholder="Start typing..." size="small" />
            )}
            disabled={!compareEnabled}
            sx={{ mb: 2 }}
          />
          {selectedOptionsRight2.map((item) => (
            <LeftBoxCard
              key={`right2-${item.id}-${item.samVersion}-${item.pricingVersion}`}
              item={item}
              onRemove={() => removeOption(setSelectedOptionsRight2, selectedOptionsRight2, item)}
            />
          ))}
        </Card>
      </div>
    </div>
  );
};

export default PSCRFComparison;

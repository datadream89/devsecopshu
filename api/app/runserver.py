
import React, { useState, forwardRef, useImperativeHandle } from "react";
// ...

const PSCRFSection = forwardRef((props, ref) => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [error, setError] = useState(false);

  useImperativeHandle(ref, () => ({
    validate: () => {
      const isValid = selectedOptions.length > 0;
      setError(!isValid);
      return isValid;
    },
  }));

  const handleRemove = (index) => {
    const updated = [...selectedOptions];
    updated.splice(index, 1);
    setSelectedOptions(updated);
  };

  return (
    <Box p={2} border={1} borderColor={error ? "red" : "grey.300"} borderRadius={2} bgcolor="white" minHeight={220}>
      <Autocomplete
        multiple
        options={pscrfOptions}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        onChange={(event, value) => {
          setSelectedOptions(value);
          setError(false);
        }}
        renderInput={(params) => <TextField {...params} label="Select PSCRF" variant="outlined" error={error} />}
      />
      {/* Cards... */}
    </Box>
  );
});

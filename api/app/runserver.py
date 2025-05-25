<Autocomplete
  multiple
  options={pscrfOptions}
  value={selectedPSCRFs}
  onChange={(event, newValue) => {
    setSelectedPSCRFs(newValue);
    setPscrfError(false); // clear error on change
  }}
  renderInput={(params) => (
    <TextField
      {...params}
      label="Select PSCRFs"
      error={pscrfError}
      helperText={pscrfError ? "Please select at least one PSCRF ID" : ""}
    />
  )}
/>

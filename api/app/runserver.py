const PSCRFSection = ({ selectedOptions, onChange }) => {
  const handleRemove = (index) => {
    const updated = [...selectedOptions];
    updated.splice(index, 1);
    onChange(updated);
  };

  return (
    <Box p={2} border={1} borderColor="grey.300" borderRadius={2} bgcolor="white" minHeight={220}>
      <Autocomplete
        multiple
        options={pscrfOptions}
        getOptionLabel={(option) =>
          `${option.id}, ${option.samVersion}, ${option.pricingVersion}, ${option.clientName}`
        }
        value={selectedOptions}
        onChange={(event, value) => onChange(value)}
        renderInput={(params) => <TextField {...params} label="Select PSCRF" variant="outlined" />}
      />
      <Box display="flex" flexWrap="wrap" mt={2} gap={2} sx={{ maxHeight: 300, overflowY: "auto" }}>
        {selectedOptions.map((option, index) => (
          <Card key={index} sx={{ width: "48%", position: "relative", boxSizing: "border-box" }}>
            <CardContent sx={{ padding: "8px !important" }}>
              <Typography variant="body2" component="div" whiteSpace="normal">
                <strong>ID:</strong> {option.id}
                <br />
                <strong>SAM:</strong> {option.samVersion}
                <br />
                <strong>Pricing:</strong> {option.pricingVersion}
                <br />
                <strong>Client:</strong> {option.clientName}
              </Typography>
              <IconButton
                size="small"
                onClick={() => handleRemove(index)}
                sx={{ position: "absolute", top: 4, right: 4 }}
                aria-label="remove card"
              >
                <CloseIcon fontSize="small" />
              </IconButton>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
};

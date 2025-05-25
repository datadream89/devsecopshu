<Box sx={{ display: "flex", justifyContent: "space-between", mb: 2 }}>
  <FormControlLabel
    control={
      <Checkbox
        checked={compareEnabled}
        onChange={(e) => setCompareEnabled(e.target.checked)}
        size="small"
      />
    }
    label="Compare"
  />
  <Box sx={{ flexGrow: 1, textAlign: "center" }}>
    <Typography variant="h6" fontWeight="bold" sx={{ userSelect: "none" }}>
      {`Comparison Unit ${unitNumber}`}
    </Typography>
  </Box>
  <Button
    variant="outlined"
    size="small"
    onClick={() => setCollapsed(!collapsed)}
  >
    {collapsed ? "Expand" : "Collapse"}
  </Button>
</Box>

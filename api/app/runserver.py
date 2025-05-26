const ComparisonLayout = () => {
  const [visibleRows, setVisibleRows] = useState([false, false, false, false]);

  const toggleRowVisibility = (index) => {
    setVisibleRows((prev) => prev.map((v, i) => (i === index ? !v : v)));
  };

  const rowTitles = ["Row 1", "Row 2", "Row 3", "Row 4"];

  return (
    // Outer full-screen dark brown background
    <Box
      sx={{
        minHeight: "100vh",
        width: "100%",
        bgcolor: "#4B2E2E", // Dark brown background
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        py: 4,
        px: 2,
      }}
    >
      {/* Inner white container box */}
      <Box
        sx={{
          width: "95vw",
          maxWidth: 1200,
          bgcolor: "white",
          borderRadius: 4,
          boxShadow: 4,
          px: 2,
          py: 4,
        }}
      >
        {/* Buttons */}
        <Box
          mb={2}
          display="flex"
          justifyContent="center"
          gap={2}
        >
          {rowTitles.map((title, i) => (
            <Button
              key={title}
              variant="contained"
              onClick={() => toggleRowVisibility(i)}
              sx={{
                bgcolor: visibleRows[i] ? "grey.600" : "grey.300",
                color: "white",
                "&:hover": {
                  bgcolor: visibleRows[i] ? "grey.700" : "grey.400",
                },
                textTransform: "none",
                fontWeight: 600,
                minWidth: 80,
              }}
            >
              {title}
            </Button>
          ))}
        </Box>

        {/* Row Sections */}
        {visibleRows[0] && (
          <BoxPair
            title="Row 1"
            visible={visibleRows[0]}
            leftComponent={<PSCRFSection />}
            rightComponent={<ContractSection title="Approved Contract" />}
          />
        )}
        {visibleRows[1] && (
          <BoxPair
            title="Row 2"
            visible={visibleRows[1]}
            leftComponent={<ContractSection title="Approved Contract" />}
            rightComponent={<ContractSection title="Signed Contract" />}
          />
        )}
        {visibleRows[2] && (
          <BoxPair
            title="Row 3"
            visible={visibleRows[2]}
            leftComponent={<ContractSection title="Signed Contract" />}
            rightComponent={<PSCRFSection />}
          />
        )}
        {visibleRows[3] && (
          <BoxPair
            title="Row 4"
            visible={visibleRows[3]}
            leftComponent={<PSCRFSection />}
            rightComponent={<PSCRFSection />}
          />
        )}
      </Box>
    </Box>
  );
};

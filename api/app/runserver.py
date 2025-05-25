// Main component with two comparison units
export default function ComparisonPage() {
  return (
    <Box
      sx={{
        p: 4,
        display: "flex",
        flexDirection: "column",
        alignItems: "center", // centers children horizontally
        gap: 5, // spacing between units
      }}
    >
      <ComparisonUnit title="Comparison Unit 1" />
      <ComparisonUnit title="Comparison Unit 2" />
    </Box>
  );
}

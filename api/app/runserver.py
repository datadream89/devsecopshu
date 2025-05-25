{/* Left box */}
<Box
  sx={{
    width: 300,
    height: 300,
    border: "2px solid",
    borderColor:
      highlight[idx] === "left"
        ? "gray"
        : highlight[idx] === "right"
        ? "lightgray"
        : "#ccc",
    borderRadius: 2,
    p: 2,
    overflowY: "auto",
    backgroundColor: "#fff",
  }}
>
  {(idx === 0 || idx === 2 || idx === 3) && <PSCRFSection />}
</Box>

{/* Right box */}
<Box
  sx={{
    width: 300,
    height: 300,
    border: "2px solid",
    borderColor:
      highlight[idx] === "right"
        ? "gray"
        : highlight[idx] === "left"
        ? "lightgray"
        : "#ccc",
    borderRadius: 2,
    p: 2,
    overflowY: "auto",
    backgroundColor: "#fff",
  }}
>
  {idx === 3 && <PSCRFSection />}
</Box>

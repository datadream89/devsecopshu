const ContractSection = forwardRef(({ title }, ref) => {
  const [sections, setSections] = useState([
    { id: Date.now(), type: "Agreement", file: null, filename: "", error: false },
  ]);

  useImperativeHandle(ref, () => ({
    validate: () => {
      let isValid = true;
      const updated = sections.map((s) => {
        const sectionValid = !!s.file;
        if (!sectionValid) isValid = false;
        return { ...s, error: !sectionValid };
      });
      setSections(updated);
      return isValid;
    },
  }));

  const handleFileChange = (id, file) => {
    // unchanged logic
  };

  return (
    <Box /* style unchanged */>
      <Typography>{title}</Typography>
      {sections.map((section) => (
        <Box /* props unchanged */>
          {/* Radio + Upload */}
          <Typography
            sx={{
              color: section.error ? "red" : "inherit",
              // other styles...
            }}
          >
            {section.filename || "No file chosen"}
          </Typography>
        </Box>
      ))}
      <Button onClick={handleAddSection}>Add Section</Button>
    </Box>
  );
});

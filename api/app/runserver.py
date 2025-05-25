const handleValidate = () => {
  const results = [
    row1LeftRef.current?.validate?.(),
    row1RightRef.current?.validate?.(),
    row2LeftRef.current?.validate?.(),
    row2RightRef.current?.validate?.(),
    row3LeftRef.current?.validate?.(),
    row3RightRef.current?.validate?.(),
    row4LeftRef.current?.validate?.(),
    row4RightRef.current?.validate?.(),
  ];
  const allValid = results.every((v) => v !== false);
  if (allValid) alert("Validation Passed ✅");
  else alert("Some sections are missing inputs ❌");
};

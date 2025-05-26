const handleFileChange = (id, event) => {
  const file = event.target.files[0];

  setSections((prev) =>
    prev.map((section) =>
      section.id === id
        ? {
            ...section,
            file,
            filename: file?.name || "", // More robust filename handling
            error: false, // Clear error if a file is selected
          }
        : section
    )
  );
};

export default function ComparisonLayout() {
  const [activeSections, setActiveSections] = useState<string[]>([]);
  const [selectedPscrfs, setSelectedPscrfs] = useState<{ [key: string]: string[] }>({});
  const [uploadedFiles, setUploadedFiles] = useState<{ [key: string]: File }>({});

  // ...button rendering, section rendering, etc.

  const handleSubmit = () => {
    const missingFields: string[] = [];

    activeSections.forEach((section) => {
      if (section.includes('PSCRF')) {
        const hasData = selectedPscrfs[section]?.length > 0;
        if (!hasData) {
          missingFields.push(`${section} (PSCRF)`);
        }
      } else {
        const hasFile = !!uploadedFiles[section];
        if (!hasFile) {
          missingFields.push(`${section} (Contract)`);
        }
      }
    });

    if (missingFields.length > 0) {
      alert(`Please complete the following:\n${missingFields.join('\n')}`);
      return;
    }

    // All good – go to next page
    navigate('/next-page'); // or use router.push in Next.js
  };

  return (
    <div className="comparison-container">
      {/* buttons, layout, etc. */}
      <Button onClick={handleSubmit}>Submit</Button>
    </div>
  );
}

import React, { useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Autocomplete, TextField, Chip } from "@mui/material";
import { ArrowLeftRight } from "lucide-react";

type PSCRF = {
  pscrfId: string;
  samVersion: string;
  pricingVersion: string;
  clientName: string;
};

type ContractSection = {
  id: number;
  contractType: string;
  file: File | null;
  checked: boolean;
};

const defaultPSCRFList: PSCRF[] = [
  {
    pscrfId: "PSCRF-101",
    samVersion: "1.0",
    pricingVersion: "2.0",
    clientName: "Client A",
  },
  {
    pscrfId: "PSCRF-102",
    samVersion: "1.1",
    pricingVersion: "2.2",
    clientName: "Client B",
  },
];

const ComparisonLayout: React.FC = () => {
  const [selectedPSCRFs, setSelectedPSCRFs] = useState<PSCRF[]>([]);
  const [sections, setSections] = useState<ContractSection[]>([
    { id: 1, contractType: "", file: null, checked: false },
  ]);

  const handleAddSection = () => {
    setSections((prev) => [
      ...prev,
      { id: Date.now(), contractType: "", file: null, checked: false },
    ]);
  };

  const handleRemoveSection = (id: number) => {
    setSections((prev) => prev.filter((s) => s.id !== id));
  };

  const handleCheckboxChange = (id: number, checked: boolean) => {
    setSections((prev) =>
      prev.map((s) => (s.id === id ? { ...s, checked } : s))
    );
  };

  const handleFileChange = (id: number, file: File | null) => {
    setSections((prev) =>
      prev.map((s) => (s.id === id ? { ...s, file } : s))
    );
  };

  const handleContractTypeChange = (id: number, contractType: string) => {
    setSections((prev) =>
      prev.map((s) => (s.id === id ? { ...s, contractType } : s))
    );
  };

  const handleSubmit = () => {
    const errors = sections.filter(
      (s) => s.checked && (!s.contractType.trim() || !s.file)
    );
    if (errors.length > 0) {
      alert("Please fill in all required fields for checked sections.");
      return;
    }
    const output = {
      selectedPSCRFs,
      enabledSections: sections.filter((s) => s.checked),
    };
    console.log("Submitting:", output);
    alert("Submitted successfully! Check console.");
  };

  const getBoxContent = (row: number, side: "left" | "right") => {
    if (row === 1) return side === "left" ? "PSCRF" : "Approved Contract";
    if (row === 2) return side === "left" ? "Approved Contract" : "PSCRF";
    if (row === 3) return side === "left" ? "Approved Contract" : "PSCRF";
    return "PSCRF"; // Row 4 both
  };

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold">PSCRF Comparison</h2>

      {/* PSCRF Dropdown */}
      <Autocomplete
        multiple
        options={defaultPSCRFList}
        getOptionLabel={(option) => option.pscrfId}
        value={selectedPSCRFs}
        onChange={(event, newValue) => setSelectedPSCRFs(newValue)}
        renderInput={(params) => (
          <TextField {...params} label="Select PSCRF IDs" />
        )}
        renderTags={(value: readonly PSCRF[], getTagProps) =>
          value.map((option: PSCRF, index: number) => (
            <Chip
              label={option.pscrfId}
              {...getTagProps({ index })}
              key={option.pscrfId}
            />
          ))
        }
      />

      {/* Modal Cards for Each PSCRF */}
      {selectedPSCRFs.map((pscrf) => (
        <Card key={pscrf.pscrfId} className="mt-4">
          <CardHeader>
            <CardTitle>{pscrf.pscrfId}</CardTitle>
          </CardHeader>
          <CardContent>
            <p>SAM Version: {pscrf.samVersion}</p>
            <p>Pricing Version: {pscrf.pricingVersion}</p>
            <p>Client: {pscrf.clientName}</p>
          </CardContent>
        </Card>
      ))}

      {/* Contract Sections */}
      <div>
        <h3 className="text-xl font-semibold mt-6 mb-2">Contract Sections</h3>
        {sections.map((section) => (
          <Card key={section.id} className="p-4 mb-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Checkbox
                  checked={section.checked}
                  onCheckedChange={(checked) =>
                    handleCheckboxChange(section.id, Boolean(checked))
                  }
                />
                <span>Enable Section</span>
              </div>
              <Button
                size="sm"
                variant="destructive"
                onClick={() => handleRemoveSection(section.id)}
              >
                x
              </Button>
            </div>

            <div className="mt-4 space-y-4">
              <div>
                <label className="font-medium">Contract Type</label>
                <Input
                  value={section.contractType}
                  onChange={(e) =>
                    handleContractTypeChange(section.id, e.target.value)
                  }
                  placeholder="Enter contract type"
                  disabled={!section.checked}
                />
              </div>

              <div>
                <label className="font-medium">Upload File</label>
                <Input
                  type="file"
                  onChange={(e) =>
                    handleFileChange(
                      section.id,
                      e.target.files?.[0] || null
                    )
                  }
                  disabled={!section.checked}
                />
              </div>
            </div>
          </Card>
        ))}

        <div className="flex gap-4">
          <Button onClick={handleAddSection}>+ Add Section</Button>
          <Button onClick={handleSubmit} className="bg-green-600 hover:bg-green-700">
            Submit
          </Button>
        </div>
      </div>

      {/* 4-row layout */}
      <div className="grid grid-cols-2 gap-6 mt-10">
        {[1, 2, 3, 4].map((row) => (
          <>
            {["left", "right"].map((side) => (
              <div
                key={`${row}-${side}`}
                className="border p-4 rounded-xl shadow"
              >
                <h4 className="font-semibold mb-2">
                  {getBoxContent(row, side as "left" | "right")}
                </h4>
                {row === 1 && side === "left" && (
                  <div className="flex items-center justify-center text-gray-400">
                    <ArrowLeftRight />
                  </div>
                )}
              </div>
            ))}
          </>
        ))}
      </div>
    </div>
  );
};

export default ComparisonLayout;

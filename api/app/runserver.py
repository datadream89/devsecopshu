import json
from collections import defaultdict

# Step 1: Load original data from file
with open("input_data.json", "r") as infile:
    data = json.load(infile)

# Step 2: Group entries by (pid, sid, qid, filename, questionDesc)
grouped = defaultdict(list)

for entry in data["results"]:
    key = (
        entry["pid"],
        entry["sid"],
        entry["qid"],
        entry["filename"],
        entry["questionDesc"]
    )
    grouped[key].append({
        "page": entry["page"],
        "excerpt": entry["excerpt"],
        "answer": entry["answer"],
        "statement": entry["statement"]
    })

# Step 3: Format the grouped data and calculate the aggregated answer
output = {
    "results": []
}

for (pid, sid, qid, filename, questionDesc), results in grouped.items():
    # Count Ys and Ns
    y_count = sum(1 for result in results if result["answer"] == "Y")
    n_count = len(results) - y_count  # Total count minus Ys gives Ns

    # Determine majority answer
    aggregated_answer = "Y" if y_count > n_count else "N"

    output["results"].append({
        "pid": pid,
        "sid": sid,
        "qid": qid,
        "filename": filename,
        "questionDesc": questionDesc,
        "aggregated_answer": aggregated_answer,
        "results": results
    })

# Step 4: Write to output file
with open("output_data.json", "w") as outfile:
    json.dump(output, outfile, indent=2)

# Output message to indicate success
print("Data has been successfully grouped and saved with the aggregated_answer field in 'output_data.json'.")

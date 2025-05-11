if st.session_state.get("submitted") and st.session_state.get("selected_pscrf_id"):
    pscrf_id = st.session_state["selected_pscrf_id"]

    # Match files using PSCRF ID
    matched_pdf = next((f for f in os.listdir("pdfs") if f.endswith(f"{pscrf_id}.pdf")), None)
    matched_reference = next((f for f in os.listdir("references") if f.endswith(f"{pscrf_id}.json")), None)

    if matched_pdf and matched_reference:
        pdf_path = os.path.join("pdfs", matched_pdf)
        reference_path = os.path.join("references", matched_reference)
        prompt_path = os.path.join("prompts", st.session_state["prompt_filename"])

        with open(reference_path, "r") as ref_file:
            reference_data = json.load(ref_file)

        with open(prompt_path, "r") as prompt_file:
            prompt_data = json.load(prompt_file)

        from ai_logic.ai_backend import process_pdf_with_questions

        results = process_pdf_with_questions(
            pdf_path,
            prompt_data,
            reference_data,
            reference_name=matched_reference
        )

        # Write to output JSON
        output_data = {"results": results}
        output_path = os.path.join("outputs", f"{matched_reference.split('.')[0]}_outcome.json")
        with open(output_path, "w") as out_file:
            json.dump(output_data, out_file, indent=2)

        # Save results in session state for later rendering
        st.session_state["results"] = results
        st.session_state["current_index"] = 0

from collections import Counter
import fitz  # PyMuPDF
import json
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = Ollama(model="llama3")

template = """
You are a helpful assistant. Answer the question based on the text below.

Text:
{context}

Question:
{question}

Only answer 'Yes' or 'No' as your final output.
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])
chain = LLMChain(llm=llm, prompt=prompt)

def get_pdf_text_with_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({"page_number": i + 1, "text": text})
    return pages

def majority_vote(answers):
    count = Counter(answers)
    return count.most_common(1)[0]

def generate_output(pdf_path, ref_path, prompt_path, output_path, n_votes=3):
    with open(ref_path) as ref_file:
        ref_data = json.load(ref_file)
    with open(prompt_path) as prompt_file:
        prompt_data = json.load(prompt_file)

    pscrf_id = ref_data["pscrfId"]
    scenarios = ref_data["scenarios"]
    prompts = prompt_data["prompts"]

    page_texts = get_pdf_text_with_pages(pdf_path)
    results = []

    question_lookup = {
        item["questionRefId"]: item["prompt"]
        for item in prompts
    }

    for scenario in scenarios:
        scenario_id = scenario["scenarioId"]
        for question in scenario["questions"]:
            question_id = question["questionId"]
            question_ref_id = question["questionRefId"]
            answer_data_type = question["answerDataType"]
            question_text = question_lookup[question_ref_id]

            votes = []
            for page in page_texts:
                page_num = page["page_number"]
                context = page["text"]

                answers = []
                for _ in range(n_votes):
                    result = chain.run({"context": context, "question": question_text}).strip().lower()
                    if "yes" in result:
                        answers.append("Yes")
                    elif "no" in result:
                        answers.append("No")

                if answers:
                    voted_answer, count = majority_vote(answers)
                    accuracy = round(count / n_votes, 2)
                    is_valid = "Yes" if accuracy >= 0.66 else "No"

                    if any(voted_answer in s for s in context.lower().split(".")):
                        snippet = next((s for s in context.split(".") if voted_answer.lower() in s.lower()), "")
                    else:
                        snippet = ""

                    results.append({
                        "pscrfId": pscrf_id,
                        "scenarioId": scenario_id,
                        "questionId": question_id,
                        "questionRefId": question_ref_id,
                        "question": question_text.split("?")[0] + "?",
                        "filename": pdf_path.split("/")[-1],
                        "pageNumber": page_num,
                        "answer": voted_answer,
                        "accuracy": accuracy,
                        "isValid": is_valid,
                        "snippet": snippet.strip()
                    })
                    break  # Stop on first relevant page

    with open(output_path, "w") as out_file:
        json.dump(results, out_file, indent=2)

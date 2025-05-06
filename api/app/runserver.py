import subprocess
from pathlib import Path

def convert_docx_to_pdf(input_path):
    input_path = Path(input_path)
    output_dir = input_path.parent
    subprocess.run([
        "libreoffice", "--headless", "--convert-to", "pdf", str(input_path),
        "--outdir", str(output_dir)
    ], check=True)
    return str(output_dir / input_path.with_suffix(".pdf").name)

pdf_path = convert_docx_to_pdf("your_file.docx")              
from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader(pdf_path)
docs = loader.load()

# Each doc has: doc.page_content and doc.metadata["page"]
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
paged_chunks = []

for doc in docs:
    page_number = doc.metadata.get("page", "unknown")
    stamped_text = f"[Page {page_number}] {doc.page_content}"
    chunks = splitter.create_documents([stamped_text])
    paged_chunks.extend(chunks)
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(paged_chunks, embedding=embeddings)
retriever = vectorstore.as_retriever()
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

llm = Ollama(model="mistral")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

query = "What does the document say about deadlines?"
answer = qa.run(query)

print("Answer:", answer)

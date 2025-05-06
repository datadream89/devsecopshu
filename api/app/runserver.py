import fitz  # PyMuPDF
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_pages_with_numbers(pdf_path):
    doc = fitz.open(pdf_path)
    docs = []

    for i, page in enumerate(doc):
        text = page.get_text()
        metadata = {"page": i + 1}
        docs.append(Document(page_content=text, metadata=metadata))

    return docs

# Load and verify
docs = extract_pages_with_numbers("your_file.pdf")

# Chunk with page stamps
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
stamped_chunks = []

for doc in docs:
    page_number = doc.metadata["page"]
    stamped = f"[Page {page_number}] {doc.page_content}"
    chunks = splitter.create_documents([stamped])
    stamped_chunks.extend(chunks)
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# Embed
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(stamped_chunks, embedding=embeddings)
retriever = vectorstore.as_retriever()

# Question answering
llm = Ollama(model="mistral")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

response = qa.run("What does the document say about project deadlines?")
print("Answer:", response)

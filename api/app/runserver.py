from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import re

# Step 1: Load Word Document
loader = UnstructuredWordDocumentLoader("your_file.docx")
raw_docs = loader.load()

# Step 2: Simulate Page Number Stamping
# Assume 3000 characters ≈ 1 page (you can tune this per document)
page_size = 3000
updated_docs = []
for i, doc in enumerate(raw_docs):
    text = doc.page_content
    chunks = [text[j:j+page_size] for j in range(0, len(text), page_size)]
    for idx, chunk in enumerate(chunks):
        page_number = idx + 1
        updated_docs.append(f"[Page {page_number}] {chunk}")

# Step 3: Split Text for Embedding
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.create_documents(updated_docs)

# Step 4: Embed and Store in Chroma
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(split_docs, embedding=embeddings)

# Step 5: Create Retriever and QA Chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = Ollama(model="mistral")

qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Step 6: Ask Question
query = "What does the document say about project deadlines?"
response = qa.run(query)

print("Answer:", response)

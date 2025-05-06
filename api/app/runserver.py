from langchain.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import Ollama

# Step 1: Load Word document
loader = Docx2txtLoader("your_file.docx")
documents = loader.load()

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Step 3: Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 4: Store vectors in Chroma (in-memory)
vectorstore = Chroma.from_documents(documents=texts, embedding=embeddings)

# Step 5: Setup retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Step 6: Initialize Ollama model
llm = Ollama(model="mistral")

# Step 7: Create RAG chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Step 8: Ask a question
query = "What are the main points discussed in the document?"
answer = qa.run(query)

print("Answer:", answer)

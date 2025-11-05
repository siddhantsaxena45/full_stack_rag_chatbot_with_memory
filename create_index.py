# read files
# break in chunks
# embeddings
# store in vector store -> Chroma (cloud-friendly alternative to FAISS)

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

DATA_PATH = "knowledge_base"
CHROMA_PATH = "chroma_index"

print("📂 Loading documents...")

# Load text files
txt_loader = DirectoryLoader(
    DATA_PATH,
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
txt_docs = txt_loader.load()

# Load PDFs
pdf_loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader)
pdf_docs = pdf_loader.load()

# Combine all documents
docs = txt_docs + pdf_docs

# Split into chunks
print("✂️ Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
docs = text_splitter.split_documents(docs)

# Create embeddings
print("🧠 Creating embeddings (this may take a moment)...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store in Chroma vector store
print("💾 Building Chroma vector store...")
db = Chroma.from_documents(docs, embeddings, persist_directory=CHROMA_PATH)
db.persist()

print("✅ Embeddings created and saved successfully at:", CHROMA_PATH)

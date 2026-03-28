from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.embeddings import Embeddings
import tempfile
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import os
import hashlib

os.environ["HF_HOME"] = "./hf_cache"

class SimpleEmbeddings(Embeddings):
    """Simple pure-Python embeddings using hash-based vectors"""
    
    def embed_documents(self, texts):
        """Embed search docs - uses hash of text"""
        embeddings = []
        for text in texts:
            if not text or not text.strip():
                # Return zero vector for empty text
                embeddings.append([0.0] * 384)
            else:
                # Create a simple 384-dimensional embedding from text hash
                # Use multiple hash rounds to get enough bytes
                embedding = []
                hash_input = text.encode()
                for i in range(384):
                    # Create unique hash for each dimension
                    hash_obj = hashlib.sha256(hash_input + str(i).encode())
                    hash_bytes = hash_obj.digest()
                    byte_val = hash_bytes[0]  # Get first byte
                    embedding.append((byte_val - 128) / 128.0)
                embeddings.append(embedding)
        return embeddings
    
    def embed_query(self, text):
        """Embed query text"""
        return self.embed_documents([text])[0]

class PDFIngestor:
    def __init__(self, pdfs, api_key):
        self.pdfs = pdfs
        self.api_key = api_key
        self.docs_list = self.get_docs()

        # Try to use tiktoken encoder, fallback to character splitter
        try:
            self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=200, chunk_overlap=0
            )
        except Exception:
            # Fallback if tiktoken not available
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=200, chunk_overlap=0, separators=["\n\n", "\n", " ", ""]
            )
        
        self.doc_splits = self.text_splitter.split_documents(self.docs_list)

        self.embeddings = SimpleEmbeddings()

        self.vectorstore = FAISS.from_documents(
            documents=self.doc_splits,
            docstore=InMemoryDocstore(),
            embedding=self.embeddings
        )

    def get_docs(self):
        docs_list = []
        for pdf_file in self.pdfs:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(pdf_file.getvalue())
                temp_pdf.flush()
                docs_list.append(PyPDFLoader(temp_pdf.name).load())
        docs_list = [item for sublist in docs_list for item in sublist]
        return docs_list

    def get_retriever(self):
        return self.vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": 3})

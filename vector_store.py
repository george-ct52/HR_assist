from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer

POLICY_DIR = Path(__file__).parent / "data" / "policies"
PERSIST_DIR = Path(__file__).parent / "data" / "chroma_db"




def build():

    loader = DirectoryLoader(
        str(POLICY_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
    )
    raw_documents = loader.load()

    splitter=RecursiveCharacterTextSplitter(
        chunk_size=500,chunk_overlap=50, length_function=len,separators=["\n\n", "\n", " ", ""]
    )

    documents = splitter.split_documents(raw_documents)

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(
        documents, embeddings, persist_directory=str(PERSIST_DIR)
    )

    print(f"Indexed {len(documents)} chunks from {len(raw_documents)} policy docs \n into {PERSIST_DIR}")

    if __name__=="__main__":
        build()
          
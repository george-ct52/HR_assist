from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path


PERSIST_DIR = Path(__file__).parent / "data" / "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)   

def query_policy_docs(question: str, k: int = 4) -> str:
    """Returns the top-k relevant policy chunks, concatenated with their source."""
    try:
        store = Chroma(
            collection_name="hr_policies",
            embedding_function=embeddings,
            persist_directory=str(PERSIST_DIR),
        )
        docs = store.similarity_search(question, k=k)
    except Exception as e:
        print(f"[vector_tool] Retrieval failed: {e}")
        return "Policy documents are currently unavailable."

    if not docs:
        return "No relevant policy information was found."

    context = []

    
    context = "\n\n".join(d.page_content for d in docs)
    return context


if __name__ == "__main__":
    print(query_policy_docs("Can unused leave be carried forward?"))

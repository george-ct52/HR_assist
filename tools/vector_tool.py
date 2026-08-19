from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


PERSIST_DIR = Path(__file__).parent.parent / "data" / "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def query_policy_docs(question: str, k: int = 4) -> str:

    store = Chroma(
        collection_name="hr_policies",
        embedding_function=embeddings,
        persist_directory=str(PERSIST_DIR),
    )

    docs = store.similarity_search(question, k=k)

    if not docs:
        return "No relevant policy information was found."

    return "\n\n".join(doc.page_content for doc in docs)


if __name__ == "__main__":
   print(query_policy_docs("What is the company's maternity leave policy?"))
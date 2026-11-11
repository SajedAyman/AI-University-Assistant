from functools import lru_cache
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# Project root folder and the vector database folder
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FOLDER = BASE_DIR / "data" / "chroma_db"

# Must be the same embedding model that ingest.py used
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_vector_db():
    """Open the existing vector database (without rebuilding it).

    The result is cached, so the embedding model is loaded only once.
    """
    # Ingestion already downloaded this model. Avoid Hub checks on startup.
    if not (DB_FOLDER / "chroma.sqlite3").exists():
        raise FileNotFoundError("Run python src/ingest.py before starting the app.")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"local_files_only": True},
    )

    return Chroma(
        persist_directory=str(DB_FOLDER),
        embedding_function=embeddings,
    )


def retrieve_chunks(question, k=4):
    """Return the k closest chunks to the question, each with its distance score.

    A smaller distance means the chunk is closer in meaning to the question.
    """
    db = get_vector_db()
    return db.similarity_search_with_score(question, k=k)


def main():
    """Simple command-line test for the retrieval step (no LLM involved)."""
    question = input("Ask a question: ")

    results = retrieve_chunks(question)

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\n--- Result {i} (distance: {score:.3f}) ---")
        print("Document:", doc.metadata.get("document_name"))
        print("Page:", doc.metadata.get("page", 0) + 1)  # PyPDF pages start at 0
        print(doc.page_content[:500])


if __name__ == "__main__":
    main()
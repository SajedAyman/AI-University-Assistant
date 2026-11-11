from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from functools import lru_cache


# مكان المشروع الرئيسي ومكان قاعدة البيانات
BASE_DIR = Path(__file__).resolve().parent.parent
DB_FOLDER = BASE_DIR / "data" / "chroma_db"

# لازم يكون نفس الموديل اللي استخدمه ingest.py
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_vector_db():
    """يفتح قاعدة البيانات الموجودة (من غير ما يعيد بناءها)."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    return Chroma(
        persist_directory=str(DB_FOLDER),
        embedding_function=embeddings,
    )


def retrieve_chunks(question, k=4):
    """يرجّع أقرب k chunks للسؤال مع درجة المسافة لكل واحد."""
    db = get_vector_db()
    return db.similarity_search_with_score(question, k=k)


def main():
    question = input("Ask a question: ")

    results = retrieve_chunks(question)

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\n--- Result {i} (distance: {score:.3f}) ---")
        print("Document:", doc.metadata.get("document_name"))
        print("Page:", doc.metadata.get("page", 0) + 1)
        print(doc.page_content[:500])


if __name__ == "__main__":
    main()
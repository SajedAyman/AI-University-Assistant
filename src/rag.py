import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from retrieve import retrieve_chunks

load_dotenv()

NOT_FOUND_MESSAGE = "I could not find this in the course materials."

# chunks أقصر من كده غالباً عناوين slides من غير شرح
MIN_CHUNK_CHARS = 80

PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an Operating Systems study assistant. "
        "Answer the student's question using ONLY the context below. "
        "If the context does not contain the answer, reply exactly: "
        + NOT_FOUND_MESSAGE
        + " Do not use outside knowledge. Explain clearly and concisely.\n\n"
        "Context:\n{context}",
    ),
    ("human", "{question}"),
])


@lru_cache(maxsize=1)
def get_llm():
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,
    )


def message_to_text(message):
    """يطلّع النص الصافي من رد الموديل (ممكن يكون string أو قايمة blocks)."""
    content = message.content

    if isinstance(content, str):
        return content.strip()

    parts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
        elif isinstance(block, str):
            parts.append(block)

    return "".join(parts).strip()


def get_relevant_chunks(question, k=4):
    """يجيب أقرب chunks للسؤال، ويستبعد العناوين القصيرة."""
    results = retrieve_chunks(question, k=k + 4)

    chunks = [
        doc
        for doc, _score in results
        if len(doc.page_content.strip()) >= MIN_CHUNK_CHARS
    ]

    return chunks[:k]


def format_context(chunks):
    parts = []

    for doc in chunks:
        name = doc.metadata.get("document_name", "unknown")
        page = doc.metadata.get("page", 0) + 1
        parts.append(f"[Source: {name}, page {page}]\n{doc.page_content}")

    return "\n\n".join(parts)


def collect_sources(chunks):
    sources = []
    seen = set()

    for doc in chunks:
        name = doc.metadata.get("document_name", "unknown")
        page = doc.metadata.get("page", 0) + 1

        if (name, page) not in seen:
            seen.add((name, page))
            sources.append({"document": name, "page": page})

    return sources


def answer_question(question):
    """الدالة الرئيسية: بترجّع {"answer": ..., "sources": [...]}"""
    chunks = get_relevant_chunks(question)

    if not chunks:
        return {"answer": NOT_FOUND_MESSAGE, "sources": []}

    prompt_value = PROMPT.invoke({
        "context": format_context(chunks),
        "question": question,
    })

    response = get_llm().invoke(prompt_value)
    answer = message_to_text(response)

    # لو الموديل قال إنه ملقاش الإجابة، منعرضش مصادر
    if answer == NOT_FOUND_MESSAGE:
        return {"answer": answer, "sources": []}

    return {"answer": answer, "sources": collect_sources(chunks)}


def main():
    print("OS Study Assistant (type 'exit' to quit)")

    while True:
        question = input("\nQuestion: ").strip()

        if not question:
            continue
        if question.lower() in ("exit", "quit"):
            break

        try:
            result = answer_question(question)
        except Exception as error:
            print(f"\nError: {error}")
            continue

        print("\nAnswer:\n" + result["answer"])

        if result["sources"]:
            print("\nSources:")
            for source in result["sources"]:
                print(f"- {source['document']} (page {source['page']})")


if __name__ == "__main__":
    main()
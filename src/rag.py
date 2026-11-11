import os
from functools import lru_cache
from time import perf_counter

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from retrieve import retrieve_chunks

# Load GROQ_API_KEY and GROQ_MODEL from the .env file
load_dotenv()

# Fixed reply used when the answer is not in the course materials
NOT_FOUND_MESSAGE = "I could not find this in the course materials."

# Chunks shorter than this are usually slide titles with no explanation
MIN_CHUNK_CHARS = 80

# Prompt template: forces the model to answer only from the retrieved context
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
    """Create the Groq client once and reuse it."""
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        reasoning_effort="low",
        timeout=45,
        max_retries=0,
    )


def message_to_text(message):
    """Extract plain text from the model reply (it can be a string or a list of blocks)."""
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
    """Fetch the closest chunks to the question and drop short title-only chunks."""
    # Ask for extra chunks so that k remain after filtering
    results = retrieve_chunks(question, k=k + 4)

    chunks = [
        doc
        for doc, _score in results
        if len(doc.page_content.strip()) >= MIN_CHUNK_CHARS
    ]

    return chunks[:k]


def format_context(chunks):
    """Join the chunks into one context string, each labeled with its source."""
    parts = []

    for doc in chunks:
        name = doc.metadata.get("document_name", "unknown")
        page = doc.metadata.get("page", 0) + 1  # PyPDF pages start at 0
        parts.append(f"[Source: {name}, page {page}]\n{doc.page_content}")

    return "\n\n".join(parts)


def collect_sources(chunks):
    """Build a list of unique (document, page) sources from the chunks."""
    sources = []
    seen = set()

    for doc in chunks:
        name = doc.metadata.get("document_name", "unknown")
        page = doc.metadata.get("page", 0) + 1

        if (name, page) not in seen:
            seen.add((name, page))
            sources.append({"document": name, "page": page})

    return sources


def answer_question(question, on_progress=None):
    """Return answer and sources; optionally report the current stage to the UI."""
    if on_progress:
        on_progress("Searching the course PDFs...")
    started = perf_counter()
    chunks = get_relevant_chunks(question)
    print(f"[RAG] Retrieval: {perf_counter() - started:.2f}s", flush=True)

    # Nothing useful was retrieved
    if not chunks:
        return {"answer": NOT_FOUND_MESSAGE, "sources": []}

    # Augmentation: combine the retrieved context and the question into one prompt
    prompt_value = PROMPT.invoke({
        "context": format_context(chunks),
        "question": question,
    })

    # Generation: send the prompt to the LLM.
    if on_progress:
        on_progress("Generating an answer from the retrieved passages...")
    started = perf_counter()
    try:
        response = get_llm().invoke(prompt_value)
    finally:
        print(f"[RAG] LLM request: {perf_counter() - started:.2f}s", flush=True)
    answer = message_to_text(response)

    # If the model could not find the answer, do not show sources
    if answer == NOT_FOUND_MESSAGE:
        return {"answer": answer, "sources": []}

    return {"answer": answer, "sources": collect_sources(chunks)}


def main():
    """Simple command-line chat loop."""
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
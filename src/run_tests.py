import csv
import time
from pathlib import Path

from rag import answer_question

BASE_DIR = Path(__file__).resolve().parent.parent
QUESTIONS_FILE = BASE_DIR / "data" / "test_questions.csv"
RESULTS_FILE = BASE_DIR / "data" / "test_results.csv"

# الـ free tier بيحدد عدد الطلبات في الدقيقة، فبنستنى بين كل سؤال
DELAY_SECONDS = 15
MAX_RETRIES = 3

FIELDS = ["id", "category", "question", "answer", "sources"]


def ask_with_retry(question):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return answer_question(question)
        except Exception as error:
            print(f"   attempt {attempt} failed: {error}")
            if attempt < MAX_RETRIES:
                time.sleep(30)

    return {"answer": "ERROR: request failed", "sources": []}

def load_questions():
    with open(QUESTIONS_FILE, newline="", encoding="utf-8-sig") as f:
        lines = [line for line in f if line.strip()]

    reader = csv.DictReader(lines)
    reader.fieldnames = [name.strip().lower() for name in reader.fieldnames]

    return list(reader)

def main():
    questions = load_questions()

    print(f"Loaded {len(questions)} questions.\n")

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8-sig") as out:
        writer = csv.DictWriter(out, fieldnames=FIELDS)
        writer.writeheader()

        for i, row in enumerate(questions, start=1):
            question = row["question"].strip()
            print(f"[{i}/{len(questions)}] {question}")

            result = ask_with_retry(question)

            sources = "; ".join(
                f"{s['document']} p.{s['page']}" for s in result["sources"]
            )

            writer.writerow({
                "id": row.get("id", i),
                "category": row.get("category", ""),
                "question": question,
                "answer": result["answer"],
                "sources": sources,
            })
            out.flush()

            if i < len(questions):
                time.sleep(DELAY_SECONDS)

    print(f"\nDone. Results saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
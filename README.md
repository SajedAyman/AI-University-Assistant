# OS Study Assistant

A Retrieval-Augmented Generation (RAG) chatbot for university students studying Operating Systems. It searches the project's course PDFs and asks Gemini to answer using the retrieved passages.

The Streamlit interface accepts a question, displays the answer, and lists retrieved source documents with PDF page numbers. If the retrieved context cannot answer a question, the prompt instructs the model to reply:

> I could not find this in the course materials.

## Technology stack

- Python 3.12
- LangChain for document processing and RAG orchestration
- ChromaDB for local vector storage
- Sentence Transformers: `sentence-transformers/all-MiniLM-L6-v2`
- Gemini API for answer generation
- Streamlit for the web interface

## How it works

1. Load the 24 PDFs from `data/documents/`.
2. Split their text into chunks of 800 characters with 150 characters of overlap.
3. Generate embeddings and store them in `data/chroma_db/`.
4. For each question, retrieve relevant chunks and filter out short, title-only passages.
5. Send up to four remaining chunks and the question to Gemini.
6. Display the answer and unique document/page sources, or the fallback response.

Source page numbers are PDF page positions starting at 1. They may differ from printed page or slide labels. Listed sources identify the retrieved passages; they are not a guarantee that every statement is correct.

## Project files

| Path | Purpose |
| --- | --- |
| `data/documents/` | Operating Systems source PDFs |
| `data/dataset_inventory.csv` | Dataset inventory |
| `data/test_questions.csv` | 20 evaluation questions |
| `data/test_results.csv` | Test runner output |
| `data/chroma_db/` | Generated local vector database; ignored by Git |
| `src/ingest.py` | PDF loading, chunking, embedding, and indexing |
| `src/retrieve.py` | Similarity search against ChromaDB |
| `src/rag.py` | Prompt construction, Gemini generation, and source collection |
| `src/app.py` | Streamlit question-and-answer interface |
| `src/run_tests.py` | Batch evaluation runner |
| `.env.example` | API configuration template |
| `requirements.txt` | Python dependencies |

## Setup on Windows

Use Python 3.12, the version used by the team. Keep the project outside OneDrive, for example at `C:\Projects\AI-University-Assistant`, to avoid syncing the virtual environment and database.

### 1. Clone the repository

You need access to this private repository. Sign in with an authorized GitHub account if prompted.

```powershell
git clone https://github.com/SajedAyman/AI-University-Assistant.git
cd AI-University-Assistant
```

If you already cloned the project, pull the latest changes instead.

Run all subsequent commands from the project root, where `requirements.txt` is located.

### 2. Create a virtual environment and install dependencies

```powershell
py -3.12 --version
py -3.12 -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

These commands use the virtual environment directly; PowerShell activation is optional.

### 3. Configure Gemini

Create or view an API key in [Google AI Studio](https://aistudio.google.com/apikey).

Copy the template once:

```powershell
Copy-Item .env.example .env
```

Open `.env`, replace the API key placeholder, and save:

```dotenv
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Keep the configured model consistent with the backend. Model access and API quotas depend on your account.

Never commit `.env` or put a real key in `.env.example`. The repository ignores `.env`, `venv/`, and `data/chroma_db/`. Each teammate supplies their own API key and builds their own database.

### 4. Build the local database

```powershell
.\venv\Scripts\python.exe src/ingest.py
```

The first run downloads the embedding model and may take time. Keep sufficient disk space available for Python dependencies, the model cache, and the database.

Successful completion prints `Ingestion completed successfully!`.

Run ingestion when setting up a new machine or after changing documents or indexing settings. It deletes and rebuilds the existing local ChromaDB folder, so stop the app before rebuilding. Ingestion is not required every time you start the app.

## Run the web interface

```powershell
.\venv\Scripts\python.exe -m streamlit run src/app.py
```

Open the Local URL printed in the terminal, normally [http://localhost:8501](http://localhost:8501).

Enter an OS question and click **Ask**. The app shows a loading indicator, the answer, and sources when available. Empty input displays a warning; failed requests display a helpful error message. Press `Ctrl+C` in the terminal to stop the server.

Example questions:

- What is virtual memory?
- What is a deadlock?
- What is the difference between a process and a thread?

## Test the command-line backend

```powershell
.\venv\Scripts\python.exe src/rag.py
```

Enter a question at the prompt. Type `exit` or `quit` to stop.

## Evaluation and report handoff

Run the question set with:

```powershell
.\venv\Scripts\python.exe src/run_tests.py
```

This overwrites `data/test_results.csv`. The runner includes delays and retries, so completion takes several minutes and may take longer under rate limiting.

For each response, evaluate:

- **Relevance:** whether the retrieved sources address the question.
- **Faithfulness:** whether the response is supported by the retrieved passages.
- **Answer correctness:** whether it correctly answers the question.

Before handoff, check an in-scope OS question, an unrelated question, and empty input. Capture screenshots of the app and sources for the technical report. Human evaluation and screenshots should accompany the generated CSV; the script does not automatically grade correctness.

## Troubleshooting

- **No suitable Python runtime:** install Python 3.12, restart VS Code, and retry `py -3.12 --version`.
- **No space left on device:** free disk space, then rerun the dependency installation command. Pip retains successfully installed packages.
- **Slow first question:** the app needs to load the embedding model into its process. Later requests reuse the cached model, but network latency, memory pressure, API retries, and quotas can still affect response time.
- **Hugging Face unauthenticated warning:** the model can be downloaded without a token; this warning alone does not mean the request failed.
- **No documents or useful results:** confirm the PDFs exist in `data/documents/` and ingestion completed successfully.
- **Answer generation fails:** check your internet connection, `GOOGLE_API_KEY`, model access, and API quota. The interface deliberately shows a general error message.
- **Unexpected answer or fallback:** inspect the retrieved pages and record the case for evaluation. A grounding prompt reduces unsupported answers but does not eliminate them.

## License

See [LICENSE](LICENSE).

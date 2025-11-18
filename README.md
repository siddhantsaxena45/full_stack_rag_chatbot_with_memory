# Full-Stack RAG Chatbot with Memory

This repository contains a small Retrieval-Augmented Generation (RAG) demo: a FastAPI backend that loads a FAISS vector index and serves a simple RAG endpoint, plus a Streamlit frontend to chat with the documents. The project also includes utilities to create the PostgreSQL tables and to build the FAISS index from the `knowledge_base`.

## Project Structure

- `backend/` : FastAPI app and helper scripts
  - `main.py` : FastAPI application that loads the FAISS index and exposes endpoints (`/query`, `/get_or_create_user`, `/get_history`)
  - `create_index.py` : builds FAISS index from files in `knowledge_base/`
  - `create_tables.py` : creates PostgreSQL tables `users` and `chat_history`
  - `requirements.txt` : Python dependencies used by the backend
- `frontend/` : Streamlit chat UI
  - `app.py` : Streamlit frontend that talks to the FastAPI backend
- `faiss_index/` : stores the serialized FAISS index (`index.faiss`)
- `knowledge_base/` : source documents used to build the FAISS index (e.g. `webscraping.txt`)
- `pip_installs.txt` : (informational)

## Prerequisites

- Python 3.10+ recommended
- PostgreSQL database for chat memory
- A Google API key (used by the configured LLM in `backend/main.py`)
- On Windows, installing `faiss-cpu` may require either a compatible wheel or using Conda; see troubleshooting below.

## Setup (Windows - `cmd.exe` examples)

1. Create and activate a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

2. Install backend dependencies

```
pip install -r backend\requirements.txt
```

3. Create a `.env` file at the project root with at least the following variables:

```
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<db>
GOOGLE_API_KEY=<your-google-api-key>
```

4. Create PostgreSQL tables

```
python backend\create_tables.py
```

5. (Re)build the FAISS index from files in `knowledge_base/`

```
python backend\create_index.py
```

The script writes the index to `faiss_index/` (default path used by `backend/main.py`). If `faiss_index/index.faiss` already exists, running `create_index.py` will overwrite it.

6. Run the backend (FastAPI)

```
uvicorn backend.main:app --reload --port 8000
```

7. Run the frontend (Streamlit)

```
streamlit run frontend\app.py
```

Open the Streamlit UI in the browser (Streamlit prints the local URL), or call the backend at `http://127.0.0.1:8000` (the FastAPI docs UI is available at `/docs`).

## Notes

- The FAISS index is created from text and PDF files in `knowledge_base/` using `sentence-transformers/all-MiniLM-L6-v2` embeddings (see `backend/create_index.py`).
- The backend loads the FAISS index from `../faiss_index/` relative to `backend/` (this is set in `backend/main.py` via `FAISS_PATH = "../faiss_index/"`). Ensure that `faiss_index/index.faiss` exists or run `create_index.py` to (re)create it.
- `backend/main.py` expects `DATABASE_URL` and `GOOGLE_API_KEY` to be set in the environment (via `.env`).

## Troubleshooting

- If `faiss-cpu` fails to install on Windows via `pip`, consider using Conda:

```
conda create -n rag python=3.10 -y
conda activate rag
conda install -c pytorch faiss-cpu -y
pip install -r backend\requirements.txt
```

- If you see issues loading the sentence-transformers model, ensure you have network access and sufficient disk space to cache the model.

## Next steps / Improvements

- Add authentication and better user management
- Persist LLM responses and metadata for debugging
- Add tests and CI for reproducibility

---

If you'd like, I can also:
- add a sample `.env.example` file,
- add a short `run-dev.bat` script to start both backend and frontend,
- or commit these changes and run simple sanity checks.

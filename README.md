
# 🧠 Full Stack RAG Chatbot with Memory

An end-to-end **Retrieval-Augmented Generation (RAG)** chatbot built using **FastAPI**, **LangChain**, **Hugging Face embeddings**, and **Streamlit** — with persistent **PostgreSQL** memory for chat history and **ChromaDB** for document retrieval.

---

## 🚀 Tech Stack

| Layer | Technology |
|--------|-------------|
| Backend | FastAPI (Python) |
| Frontend | Streamlit |
| Vector DB | Chroma |
| LLM | Groq (Llama 3.3 - 70B Versatile) |
| Embeddings | sentence-transformers / all-MiniLM-L6-v2 |
| Database | PostgreSQL |
| Deployment | Render (Backend) |
| Env Management | python-dotenv |

---

## 🧩 Project Structure

```

full_stack_rag_chatbot_with_memory/
├── backend/
│   ├── main.py               # FastAPI backend (RAG + memory logic)
│   ├── requirements.txt      # Backend dependencies
│   ├── .env                  # Env vars (DATABASE_URL, GROQ_API_KEY)
│   ├── chroma_index/         # Persisted Chroma embeddings
│   └── ...
│
├── frontend/
│   ├── app.py                # Streamlit UI for chat interface
│   ├── requirements.txt      # Frontend dependencies
│   └── ...
│
├── knowledge_base/           # Your documents for RAG
│   ├── webscraping.txt
│   └── oops_java.pdf
│
├── create_index.py           # Builds and saves document embeddings
├── create_tables.py          # Initializes database tables
└── README.md

````

---

## ⚙️ Setup (Local Development)

### 1️⃣ Clone the repo
```bash
git clone https://github.com/siddhantsaxena45/full_stack_rag_chatbot_with_memory.git
cd full_stack_rag_chatbot_with_memory
````

### 2️⃣ Set up backend

```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ Add environment variables

Create a `.env` file inside `/backend`:

```bash
DATABASE_URL=your_postgres_connection_string
GROQ_API_KEY=your_groq_api_key
```

### 4️⃣ Build the vector index

```bash
python create_index.py
```

This will:

* Load PDFs and text files from `knowledge_base/`
* Split them into chunks
* Create embeddings using HuggingFace
* Save them in `backend/chroma_index/`

### 5️⃣ Initialize the database

```bash
python create_tables.py
```

### 6️⃣ Run the backend (FastAPI)

```bash
uvicorn main:app --reload
```

Visit:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)
Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 💬 Streamlit Frontend

### 1️⃣ Install dependencies

```bash
cd ../frontend
pip install -r requirements.txt
```

### 2️⃣ Run the app

```bash
streamlit run app.py
```

This connects to the backend (by default: `https://full-stack-rag-chatbot-with-memory.onrender.com`).

---

## 🌐 Deploying on Render

### Backend (FastAPI)

* **Root Directory:** `backend`
* **Build Command:**

  ```bash
  pip install -r requirements.txt
  ```
* **Start Command:**

  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
* **Environment Variables:**

  | Key              | Value               |
  | ---------------- | ------------------- |
  | DATABASE_URL     | your PostgreSQL URL |
  | GROQ_API_KEY     | your Groq API Key   |
  | PYTHONUNBUFFERED | 1                   |

### Frontend (Streamlit)
 - https://gen-ai-rag-chatbot.streamlit.app/
---

## 💾 Database Schema

| Table          | Columns                                                                  | Description                 |
| -------------- | ------------------------------------------------------------------------ | --------------------------- |
| `users`        | `id SERIAL PRIMARY KEY`, `username TEXT UNIQUE`                          | Stores unique users         |
| `chat_history` | `id SERIAL PRIMARY KEY`, `user_id INTEGER`, `prompt TEXT`, `answer TEXT` | Stores conversation context |

---

## ⚙️ How It Works

1. **User login/signup**

   * User provides a username.
   * FastAPI checks or creates a record in the `users` table.

2. **Chat with memory**

   * Each question and answer is stored in the `chat_history` table.
   * On each new query, the app retrieves full conversation history for context.

3. **Retrieval-Augmented Generation (RAG)**

   * User query → embedded via `HuggingFaceEmbeddings`
   * Similar chunks retrieved from Chroma
   * Context + query passed to Groq LLM (`llama-3.3-70b-versatile`)
   * Response returned and stored in the database.

---

## 🧠 Example Workflow

```text
User: "What is web scraping?"
→ Retrieved context from knowledge_base/webscraping.txt
→ Groq LLM generates 3-line summary using context
→ Saved to chat_history
→ Displayed in Streamlit frontend
```

---

## 🛠️ Key Features

✅ Retrieval-Augmented Generation (RAG)
✅ Persistent chat history (PostgreSQL)
✅ Document indexing and search (ChromaDB)
✅ Secure .env configuration
✅ Fully deployable on Render
✅ Streamlit-powered frontend chat UI

---

## 🧰 Requirements

* Python ≥ 3.10
* PostgreSQL Database
* Groq API Key (get from [https://console.groq.com/keys](https://console.groq.com/keys))

---

## 📚 Future Enhancements

* ✅ Add multiple document upload support in frontend
* ✅ Stream responses for faster feedback
* 🚀 Fine-tune embeddings for specific domain knowledge
* 🔐 Add authentication and user sessions

---

## 👨‍💻 Author

**Siddhant Saxena**
🎓 B.Tech CSE | AI & ML Enthusiast | EdTech Learner
📧 [siddhant.saxena.2004@gmail.com](mailto:siddhant.saxena.2004@gmail.com)
🌐 [LinkedIn](https://www.linkedin.com) | [GitHub](https://github.com/siddhantsaxena45)

---


import os
import psycopg2
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# LangChain + RAG imports
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# ---- GLOBALS ----
rag_chain = None
retriever = None
db = None


# ✅ NEW lifespan handler (replaces deprecated @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources at startup and clean up on shutdown."""
    global rag_chain, retriever, db
    try:
        print("🚀 Initializing RAG components...")

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        CHROMA_PATH = "chroma_index"
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
        retriever = db.as_retriever(search_kwargs={"k": 3})

        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
        print("🤖 LLM initialized successfully!")

        SYSTEM_PROMPT = '''
        You are a helpful assistant.
        Use the context to answer the question in max three sentences.
        If you don't know, just say you don't know.
        Context: {context}
        Chat History: {chat_history}
        '''

        prompt = ChatPromptTemplate.from_messages(
            [("system", SYSTEM_PROMPT), ("human", "{input}")]
        )

        qa_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, qa_chain)

        print("✅ RAG chain initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")

    # Yield control to FastAPI while keeping resources alive
    yield

    # Shutdown cleanup
    print("🧹 Cleaning up resources...")


# ✅ Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# ---- DATABASE ----
def get_db_conn():
    return psycopg2.connect(DB_URL)


# ---- MODELS ----
class QueryRequest(BaseModel):
    user_id: int
    text: str


class HistoryRequest(BaseModel):
    user_id: int


class UserRequest(BaseModel):
    username: str


# ---- ROUTES ----
@app.post("/get_or_create_user")
def get_or_create_user(req: UserRequest):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (req.username,))
    user_row = cur.fetchone()

    if user_row:
        user_id = user_row[0]
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (req.username,))
        user_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return {"user_id": user_id, "username": req.username}


@app.post("/get_history")
def get_history(req: HistoryRequest):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT prompt, answer FROM chat_history WHERE user_id = %s ORDER BY id ASC", (req.user_id,))
    history = cur.fetchall()
    cur.close()
    conn.close()

    formatted_history = []
    for p, a in history:
        formatted_history.append({"role": "human", "content": p})
        formatted_history.append({"role": "ai", "content": a})
    return {"history": formatted_history}


@app.post("/query")
def query_rag(req: QueryRequest):
    global rag_chain
    if rag_chain is None:
        return {"answer": "RAG system not initialized yet. Please wait a few seconds and retry."}

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT prompt, answer FROM chat_history WHERE user_id = %s ORDER BY id ASC", (req.user_id,))
    db_history = cur.fetchall()

    chat_history_messages = []
    for prompt, answer in db_history:
        chat_history_messages.append(HumanMessage(content=prompt))
        chat_history_messages.append(AIMessage(content=answer))

    try:
        response = rag_chain.invoke({"input": req.text, "chat_history": chat_history_messages})
        answer = response.get("answer", "No answer found.")
    except Exception as e:
        answer = f"Error during retrieval: {str(e)}"

    cur.execute(
        "INSERT INTO chat_history (user_id, prompt, answer) VALUES (%s, %s, %s)",
        (req.user_id, req.text, answer)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"answer": answer}


@app.get("/")
def read_root():
    return {"message": "✅ FastAPI running! Go to /docs to test endpoints."}

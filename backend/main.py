import os
import requests
import pytesseract
import io
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from pdfminer.high_level import extract_text
from PIL import Image
from starlette.middleware.sessions import SessionMiddleware
from nlu_infer import predict_intent
from nlu_entities import extract_age, extract_yes_no, extract_memory_freq
from consent_utils import check_consent
from langdetect import DetectorFactory
from rag import query_index, add_to_index, call_llm
from memory_utils import init_memory_db, save_memory, retrieve_memories
import time

DB_PATH = "app.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            user_id INTEGER PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            memory_issues TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            user_id INTEGER,
            chat_history TEXT
        )
    """)
    conn.commit()
    conn.close()


# -------------------- Load Environment --------------------
load_dotenv()
DetectorFactory.seed = 0

# -------------------- FastAPI Setup --------------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="a8f5f167f44f4964e6c998dee827110c")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
sessions = {}  # in-memory sessions


def get_user_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = {
            "user_id": user_id,
            "slots": {"age": None, "family_history": None, "memory_freq": None, "yes_no": None},
            "last_question": None,
            "memory": []
        }
    return sessions[user_id]


class Message(BaseModel):
    text: str


# -------------------- Main Chat Endpoint --------------------
@app.post("/message")
def process_message(message: Message):
    print("\n🧠 New message received!")
    start_total = time.time()

    user_id = 1
    session = get_user_session(user_id)
    user_text = message.text.strip()

    # Emergency filter
    if any(word in user_text.lower() for word in ["severe", "urgent", "danger", "sudden"]):
        return {"response": "🚨 Please seek immediate medical attention if symptoms are severe or sudden."}

    # Save message to memory
    save_memory(user_id, user_text, role="user")
    similar_context = retrieve_memories(user_id, user_text)
    session["memory"].append({"text": user_text, "timestamp": datetime.now().isoformat()})

    memory_summary = ""
    if similar_context:
        memory_summary = "Earlier, you or I mentioned:\n" + "\n".join(similar_context[:3]) + "\n"

    chat_history = "\n".join([f"User: {m['text']}" for m in session["memory"][-4:]])

    combined_input = f"""
You are a compassionate Alzheimer’s care companion. Be natural, kind, and brief (max 3 sentences).
If greeted, respond once politely, no repetition.
Relevant past info:
{memory_summary}
Recent chat:
{chat_history}
User says: "{user_text}"
"""

    try:
        start_time = time.time()
        reply = call_llm(combined_input, stream=False).strip()
        print(f"✅ LLM response time: {time.time() - start_time:.2f}s")
    except Exception as e:
        print("❌ LLM error:", e)
        reply = "Sorry 💜, I'm having trouble connecting right now."

    save_memory(user_id, reply, role="bot")
    print(f"💡 Total handled in {time.time() - start_total:.2f}s")

    return {
        "response": reply,
        "slots_filled": session["slots"],
        "disclaimer": "⚠️ This is not medical advice. Consult a professional if symptoms worsen."
    }


# -------------------- File Upload --------------------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    user_id = 1
    try:
        content = await file.read()
        if file.content_type == "application/pdf":
            with open("temp.pdf", "wb") as f:
                f.write(content)
            text = extract_text("temp.pdf")
            os.remove("temp.pdf")
        else:
            img = Image.open(io.BytesIO(content))
            text = pytesseract.image_to_string(img)
        add_to_index(text, user_id=user_id, filename=file.filename)
        return {"ok": True, "excerpt": text[:400]}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# -------------------- Startup --------------------
@app.on_event("startup")
def startup_event():
    print("✅ App starting...")
    init_db()
    init_memory_db()
    print("✅ DB ready and memory initialized.")


@app.get("/ping")
def ping():
    return {"status": "ok"}

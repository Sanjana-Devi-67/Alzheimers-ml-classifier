import os
import json
import faiss
import time
import numpy as np
from sentence_transformers import SentenceTransformer
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------- Load or initialize model and index --------------------
MODEL_PATH = "all-MiniLM-L6-v2"
INDEX_PATH = os.path.join(BASE_DIR, "faiss.index")
DOCS_PATH = os.path.join(BASE_DIR, "faiss_docs.json")

# Load model once at startup (avoid reloading on each request)
print("⚙️ Loading embedding model once...")
model = SentenceTransformer(MODEL_PATH)

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH)
else:
    index = faiss.IndexFlatL2(384)  # 384 dims for MiniLM
    faiss.write_index(index, INDEX_PATH)

if os.path.exists(DOCS_PATH):
    with open(DOCS_PATH, "r", encoding="utf8") as f:
        docs = json.load(f)
else:
    docs = []

# -------------------- Persistent session for LLM --------------------
session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "HTTP-Referer": "http://localhost:5173",
    "X-Title": "AlzChatbot",
    "Content-Type": "application/json",
})

# -------------------- LLM CALL (Optimized & Fast) --------------------
def call_llm(prompt, stream=False):
    """
    Calls OpenRouter API using mistral-7b-instruct.
    Clean, fast, and avoids repetitive greetings.
    """
    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": (
                "You are a calm, empathetic Alzheimer’s support companion. "
                "Respond in a short, kind, and human-like way (1–3 sentences). "
                "Avoid repeating greetings like 'hi' or 'hello'. "
                "If the user greets you, respond briefly and move on naturally."
            )},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 150,
        "temperature": 0.7,
    }

    try:
        start_time = time.time()
        response = session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=data,
            timeout=7,  # shorter timeout for speed
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"].strip()

        # Clean unwanted prefixes and tags
        reply = reply.replace("<s>", "").replace("[OUT]", "").replace("</s>", "").strip()
        # Remove repeated greetings like "Hi Hi" or "Hello Hello"
        for g in ["hi", "hello", "hey"]:
            reply = reply.replace(f"{g} {g}", g).replace(f"{g.capitalize()} {g.capitalize()}", g.capitalize())

        print(f"✅ LLM response time: {round(time.time() - start_time, 2)}s")
        return reply
    except Exception as e:
        print("❌ Error calling LLM:", str(e))
        return "Sorry 💜, I’m having trouble connecting right now. Please try again."


# -------------------- Add content to index --------------------
def add_to_index(text, user_id=0, filename=""):
    """Add text to FAISS index and save doc info."""
    global index, docs
    embedding = model.encode([text], convert_to_numpy=True)
    index.add(embedding)
    docs.append({
        "user_id": user_id,
        "filename": filename,
        "text": text
    })
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "w", encoding="utf8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)


# -------------------- Query index --------------------
def query_index(user_id, query, k=5, min_score=0.35):
    """Return relevant text chunks for given query."""
    if len(docs) == 0:
        return ""

    q_emb = model.encode([query], convert_to_numpy=True)
    D, I = index.search(q_emb, k)

    results = []
    for dist, idx in zip(D[0], I[0]):
        if idx < len(docs):
            doc = docs[idx]
            if user_id and doc.get("user_id") != user_id:
                continue
            sim = float(np.exp(-dist / 10.0))
            if sim >= min_score:
                results.append((sim, doc["text"]))

    results.sort(reverse=True, key=lambda x: x[0])
    if not results:
        return ""

    top_texts = [text for _, text in results[:3]]
    return "\n\n".join(top_texts)

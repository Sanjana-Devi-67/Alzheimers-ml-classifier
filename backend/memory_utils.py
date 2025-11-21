# # memory_utils.py
# import sqlite3
# import os
# import numpy as np
# import requests
# from sklearn.metrics.pairwise import cosine_similarity

# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# DB_PATH = "app.db"

# # --- Create memory table if not exists ---
# def init_memory_db():
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS memory (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             message TEXT,
#             embedding TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# # --- Create embedding using OpenRouter ---
# def get_embedding(text):
#     url = "https://openrouter.ai/api/v1/embeddings"
#     headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
#     data = {"model": "text-embedding-3-small", "input": text}
#     response = requests.post(url, headers=headers, json=data)
#     emb = response.json()["data"][0]["embedding"]
#     return emb

# # --- Save message + embedding ---
# def save_memory(user_id, message):
#     emb = get_embedding(message)
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO memory (user_id, message, embedding) VALUES (?, ?, ?)",
#         (user_id, message, str(emb))
#     )
#     conn.commit()
#     conn.close()

# # --- Retrieve top 3 similar memories ---
# def retrieve_memories(user_id, new_message, top_k=3):
#     new_emb = np.array(get_embedding(new_message)).reshape(1, -1)
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()
#     cur.execute("SELECT message, embedding FROM memory WHERE user_id=?", (user_id,))
#     rows = cur.fetchall()
#     conn.close()

#     if not rows:
#         return []

#     messages, embeddings = [], []
#     for msg, emb_str in rows:
#         emb = np.array(eval(emb_str))  # Convert string back to list
#         messages.append(msg)
#         embeddings.append(emb)

#     sims = cosine_similarity(new_emb, embeddings)[0]
#     top_indices = np.argsort(sims)[-top_k:][::-1]
#     return [messages[i] for i in top_indices]
# memory_utils.py
import sqlite3
import os
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DB_PATH = "app.db"

# --- Create memory table if not exists ---
def init_memory_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,         -- 'user' or 'bot'
            message TEXT,
            embedding TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Create embedding using OpenRouter ---
def get_embedding(text):
    url = "https://openrouter.ai/api/v1/embeddings"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    data = {"model": "text-embedding-3-small", "input": text}
    response = requests.post(url, headers=headers, json=data)
    emb = response.json()["data"][0]["embedding"]
    return emb

# --- Save message + embedding ---
def save_memory(user_id, message, role="user"):
    """Save a message + embedding. role can be 'user' or 'bot'."""
    emb = get_embedding(message)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO memory (user_id, role, message, embedding) VALUES (?, ?, ?, ?)",
        (user_id, role, message, str(emb))
    )
    conn.commit()
    conn.close()

# --- Retrieve similar memories (user + bot) ---
def retrieve_memories(user_id, new_message, top_k=3):
    """Retrieve top similar messages from both user and bot history."""
    new_emb = np.array(get_embedding(new_message)).reshape(1, -1)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT role, message, embedding FROM memory WHERE user_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return []

    messages, embeddings, roles = [], [], []
    for role, msg, emb_str in rows:
        try:
            emb = np.array(eval(emb_str))
            messages.append(msg)
            embeddings.append(emb)
            roles.append(role)
        except Exception:
            continue

    if not embeddings:
        return []

    sims = cosine_similarity(new_emb, embeddings)[0]
    top_indices = np.argsort(sims)[-top_k:][::-1]
    return [f"[{roles[i]}] {messages[i]}" for i in top_indices]

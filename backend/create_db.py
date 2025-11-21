import sqlite3
from datetime import datetime

DB_PATH = "app.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 1️⃣ Create tables if they don't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    name TEXT,
    role TEXT,
    preferred_language TEXT,
    created_at TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS preferences (
    user_id INTEGER PRIMARY KEY,
    music BOOLEAN DEFAULT 1,
    reminders BOOLEAN DEFAULT 1,
    tone TEXT DEFAULT 'friendly',
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# 2️⃣ Insert a test user if not exists
cur.execute("SELECT * FROM users WHERE email=?", ("test@example.com",))
if not cur.fetchone():
    cur.execute("""
        INSERT INTO users (email, name, role, preferred_language, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("test@example.com", "Test User", "user", "en", datetime.now().isoformat()))
    conn.commit()
    print("✅ Test user created")
else:
    print("ℹ️ Test user already exists")

conn.close()

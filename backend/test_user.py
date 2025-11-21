import sqlite3
from datetime import datetime

conn = sqlite3.connect("app.db")
cur = conn.cursor()

# Check if test user exists
cur.execute("SELECT * FROM users WHERE email=?", ("test@example.com",))
if not cur.fetchone():
    cur.execute("""
        INSERT INTO users (email, name, role, preferred_language, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("test@example.com", "Test User", "user", "en", datetime.now().isoformat()))
    conn.commit()
    print("Test user created")
else:
    print("Test user already exists")

conn.close()

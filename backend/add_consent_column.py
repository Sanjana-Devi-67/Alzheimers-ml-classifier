import sqlite3

conn = sqlite3.connect("app.db")
cur = conn.cursor()
cur.execute("ALTER TABLE users ADD COLUMN consent BOOLEAN DEFAULT 0")
conn.commit()
conn.close()

print("✅ 'consent' column added successfully!")

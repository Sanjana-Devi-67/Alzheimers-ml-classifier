import sqlite3

conn = sqlite3.connect("app.db")
cur = conn.cursor()

# Check if preferences exist for user 1
cur.execute("SELECT * FROM preferences WHERE user_id = 1")
prefs = cur.fetchone()

if not prefs:
    cur.execute("""
        INSERT INTO preferences (user_id, music, reminders, tone)
        VALUES (?, ?, ?, ?)
    """, (1, 1, 1, 'friendly'))
    conn.commit()
    print("✅ Default preferences created for user 1")
else:
    print("ℹ️ Preferences already exist for user 1")

conn.close()

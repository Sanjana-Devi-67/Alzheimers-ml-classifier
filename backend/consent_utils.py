
from db import get_connection

def check_consent(session, user_id, user_text):
    """
    Enforces consent before collecting medical info.
    Returns (bool, str|None):
      - (False, reply) if consent not given yet
      - (True, None) if consent already given
    """
    # Check session first
    if session.get("consent", False):
        return True, None

    # Check DB for existing consent
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT consent FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if row and row["consent"]:
        session["consent"] = True
        conn.close()
        return True, None

    # User agrees in text
    if "consent" in user_text.lower():
        session["consent"] = True
        if row:
            cur.execute("UPDATE users SET consent = 1 WHERE id = ?", (user_id,))
        else:
            # if user does not exist yet, create a placeholder
            cur.execute(
                "INSERT INTO users (id, consent) VALUES (?, ?)",
                (user_id, 1)
            )
        conn.commit()
        conn.close()
        return True, "✅ Thank you. Your consent is saved. You can request deletion anytime."

    # Show consent prompt
    consent_text = (
        "⚠️ Before we continue, I need your consent.\n\n"
        "Please reply:\n\n"
        "'I consent to storing my answers and uploaded reports "
        "for care guidance and research. I can request deletion anytime.'"
    )
    conn.close()
    return False, consent_text

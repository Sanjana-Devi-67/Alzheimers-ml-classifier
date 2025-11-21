# slot_manager.py
INTENT_SLOTS = {
    "ask_medication": ["age", "yes_no"],
    "report_symptom": ["age", "family_history", "memory_freq"],
}

sessions = {}  # key: user_id, value: slot dict

def get_user_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = {}
    return sessions[user_id]

def fill_slot(user_id, slot, value):
    session = get_user_session(user_id)
    session[slot] = value
    return session

def slots_remaining(user_id, intent):
    session = get_user_session(user_id)
    required = INTENT_SLOTS.get(intent, [])
    return [s for s in required if s not in session]

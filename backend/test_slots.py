from slot_manager import get_user_session, fill_slot, slots_remaining

user_id = "test_user"

print("Initial session:", get_user_session(user_id))

# Fill one slot
fill_slot(user_id, "age", 28)
print("After filling age:", get_user_session(user_id))

# Check what is missing for intent = ask_medication
print("Slots remaining:", slots_remaining(user_id, "ask_medication"))

# Fill yes_no
fill_slot(user_id, "yes_no", True)
print("After filling yes_no:", get_user_session(user_id))

# Check again
print("Slots remaining:", slots_remaining(user_id, "ask_medication"))

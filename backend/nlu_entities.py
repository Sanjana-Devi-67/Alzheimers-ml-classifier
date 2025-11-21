import re

# Extract 2-digit age
def extract_age(text):
    m = re.search(r'\b(\d{2})\b', text)
    return int(m.group(1)) if m else None

# Extract yes/no answers
def extract_yes_no(text):
    text = text.lower()
    if "yes" in text:
        return True
    elif "no" in text:
        return False
    else:
        return None
def extract_memory_freq(text: str):
    """
    Very simple extractor for memory frequency.
    Returns the text if it contains keywords like 'sometimes', 'often', 'rarely', etc.
    """
    keywords = ["never", "rarely", "sometimes", "often", "frequently", "always"]
    text_lower = text.lower()
    for word in keywords:
        if word in text_lower:
            return word
    return text.strip()  # fallback

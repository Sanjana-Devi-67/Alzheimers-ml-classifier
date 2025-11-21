# generate_responses.py
import random
from rag import query_index, add_to_index, call_llm
import os





def generate_response(user_text, session, lang="en"):
    """
    Generates a deeply empathetic, supportive response
    to any message — now RAG-aware (uses uploaded file content) and memory-aware.
    """

    user_text_lower = user_text.lower()

    # --- Step 1: Retrieve relevant uploaded file content (RAG) ---
    rag_context = ""
    if session.get("user_id"):
        try:
            rag_context = query_index(user_id=session["user_id"], query=user_text)
        except Exception as e:
            print("RAG retrieval failed:", e)
            rag_context = ""
    if not rag_context:
        ai_reply = call_llm(
            f"You are a professional Alzheimer's caregiver assistant. "
            f"Give a short, precise, empathetic answer for caregivers. "
            f"Question: {user_text}"
        )
        if ai_reply:
            return ai_reply       
     # --- ✅ Step 1a: Use caregiver knowledge if relevant ---
    if rag_context and len(rag_context.strip()) > 50:
        # Make sure the response is focused and precise for caregivers
        return (
            f"Here’s what I found from your caregiver resources 📘:\n\n"
            f"{rag_context[:600].strip()}...\n\n"
            f"Would you like me to summarize this or explain how it applies to your situation?"
        )
    # --- Step 2: Memory recall if requested ---
    recall_phrases = ["remind me", "what did i say", "last time", "do you remember"]
    if any(phrase in user_text_lower for phrase in recall_phrases) and session.get("memory"):
        recent_memories = session.get("memory", [])[-3:]
        if recent_memories:
            memory_texts = " | ".join([m["text"] for m in recent_memories])
            return f"Of course 💜! Here's a quick recap: {memory_texts}"

    # --- Step 3: Keyword-based caring replies ---
    medication_keywords = ["medication", "medicine", "pill", "tablet", "dose", "meds"]
    memory_keywords = ["memory", "forget", "remember", "recall"]
    feeling_keywords = ["sad", "anxious", "tired", "worried", "overwhelmed", "lonely"]
    caregiver_keywords = ["caregiver", "taking care", "support", "help them"]
    greeting_keywords = ["hello", "hi", "hey", "good morning", "good evening"]
    upload_keywords = ["upload", "file", "pdf", "image"]

    if any(k in user_text_lower for k in medication_keywords):
        replies = [
            "I’m really glad you’re thinking carefully about medication 💊. It’s always best to check with a doctor before starting or changing anything.",
            "It’s thoughtful of you to ask 💜. Medication decisions depend on individual needs — your doctor is the best person to guide you.",
            "I’m here for you 💖. While I can’t prescribe, I can help you track symptoms and prepare questions for your doctor."
        ]
    elif any(k in user_text_lower for k in memory_keywords):
        replies = [
            "I hear you 💛. Memory changes can feel worrying, but you’re doing the right thing by paying attention to them.",
            "It’s okay — noticing memory lapses early is an important step. 💜 Let’s track them together and see how things evolve.",
            "Thank you for sharing this 💖. You’re not alone — memory shifts happen, and support is always available."
        ]
    elif any(k in user_text_lower for k in feeling_keywords):
        replies = [
            "I’m here with you 💜. It’s completely okay to feel this way — your emotions are valid.",
            "Thank you for trusting me with how you feel 💖. You’re not alone, and we can go through this one step at a time.",
            "It’s brave of you to share this 🌷. Let’s focus on small, gentle steps that make things feel lighter."
        ]
    elif any(k in user_text_lower for k in caregiver_keywords):
        replies = [
            "You’re doing such an important job 💜. Being a caregiver can be tough, but your support truly matters.",
            "It’s okay to feel tired or unsure 💖 — caregiving is a journey, and I’m here to help you navigate it.",
            "Remember, taking care of yourself is part of caring for them 🌷. You’re doing better than you think."
        ]
    elif any(k in user_text_lower for k in greeting_keywords):
        replies = [
            "Hello 💜! It’s wonderful to see you here. How are you feeling today?",
            "Hi 🌷! I’m here and ready to support you — what’s on your mind?",
            "Hey there 💖! I hope today has been gentle on you so far. Want to talk about anything specific?"
        ]
    elif any(k in user_text_lower for k in upload_keywords):
        replies = [
            "Sure 💜! Just upload your PDF or image, and I’ll read and summarize it for you.",
            "No worries 🌷 — upload your file, and I’ll help you extract the important information.",
            "I’m ready 💖! Once you upload the file, I’ll handle the rest and share what I find."
        ]
    else:
        replies = [
            "I’m here to listen 💜. Tell me more — every detail you share helps me understand and support you better.",
            "Thank you for opening up 💖. Whatever’s on your mind, we’ll figure it out together.",
            "It means a lot that you’re sharing this 🌷. I’m right here beside you — would you like some tips or just someone to talk to?"
        ]

    # --- Step 4: Pick a reply ---
    response_text = random.choice(replies)

    # --- Step 5: Occasionally add memory reminder ---
    if random.random() < 0.1 and session.get("memory"):
        last_action = session.get("memory")[-1]["text"]
        response_text += f" 🌷 Just a gentle reminder: last time you mentioned '{last_action}'."

    # --- Step 6: Append RAG context if available ---
    if rag_context:
        response_text += f"\n\n📄 Based on your uploaded content: {rag_context[:400]}..."
        # --- Step 7: LLM fallback for more empathetic, context-aware replies ---
    # --- Step 7: LLM fallback using OpenRouter ---
    if random.random() < 0.5 or not replies:
        try:
            context_text = (
                f"User said: {user_text}\n\n"
                f"Recent memory: {session.get('memory', [])[-3:]}\n\n"
                f"Relevant caregiver notes: {rag_context}"
            )
            prompt = (
                "You are an empathetic AI wellness companion that supports Alzheimer’s caregivers. "
                "Be warm, precise, emotionally supportive, and always give advice tailored to caregivers. "
                "Avoid repeating earlier responses.\n\n"
                f"{context_text}\n\n"
                "Your response:"
            )
            ai_reply = call_llm(prompt)
            if ai_reply:
                response_text = ai_reply
        except Exception as e:
            print("LLM generation via OpenRouter failed:", e)


    return response_text

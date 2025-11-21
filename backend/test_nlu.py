from nlu_infer import predict_intent
from nlu_entities import extract_age, extract_yes_no

inputs = [
    "I am 28 years old and yes, I have taken the medicine",
    "I want to upload a pdf",
    "My memory is failing",
    "Which medications are needed?"
]

for text in inputs:
    intent = predict_intent(text)
    age = extract_age(text)
    yes_no = extract_yes_no(text)
    print(f"Input: {text}")
    print(f"Intent: {intent}, Age: {age}, Yes/No: {yes_no}")
    print("-"*40)

import pickle

# Load the trained classifier and embedding model
with open('intent_model.pkl', 'rb') as f:
    clf, emb_model = pickle.load(f)

# Function to predict intent
def predict_intent(text):
    v = emb_model.encode([text])  # convert input text to embedding
    return clf.predict(v)[0]      # predict the intent label

# Example usage
user_input = "I want to upload a pdf"
intent = predict_intent(user_input)
print("Predicted intent:", intent)

from sentence_transformers import SentenceTransformer

# Step 1: Define your training sentences and their intents
sentences = [
    "I have memory issues",
    "My memory is failing",
    "I am forgetting things",
    "How do I upload my report?",
    "I want to upload a pdf",
    "Where can I submit my report?",
    "What medicines should I take?",
    "Which medications are needed?",
    "Tell me about my medicines"
]

labels = [
    "report_symptom",
    "report_symptom",
    "report_symptom",
    "upload_help",
    "upload_help",
    "upload_help",
    "ask_medication",
    "ask_medication",
    "ask_medication"
]


from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import pickle

# Step 1: Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Convert sentences to embeddings
X = model.encode(sentences)

# Step 3: Train Logistic Regression classifier
clf = LogisticRegression(max_iter=1000)
clf.fit(X, labels)

# Step 4: Save both the classifier and embedding model
with open('intent_model.pkl', 'wb') as f:
    pickle.dump((clf, model), f)

print("NLU model trained and saved as intent_model.pkl")

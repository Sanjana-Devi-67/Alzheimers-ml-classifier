import os
from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
docs = []

# Walk through kb folder and all subfolders
for root, _, files in os.walk('kb'):
    for fn in files:
        path = os.path.join(root, fn)
        with open(path, encoding='utf8') as f:
            text = f.read().strip()
        docs.append({"id": os.path.relpath(path, 'kb'), "text": text})

# Create embeddings
corpus = [d['text'] for d in docs]
emb = model.encode(corpus, convert_to_numpy=True, show_progress_bar=True)

# Build FAISS index
d = emb.shape[1]
index = faiss.IndexFlatL2(d)
index.add(emb)

# Save index + docs metadata
faiss.write_index(index, 'faiss.index')
with open('faiss_docs.json','w', encoding='utf8') as f:
    json.dump(docs, f, ensure_ascii=False)

print(f"Indexed {len(docs)} files.")

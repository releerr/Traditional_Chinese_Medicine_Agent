import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

embed_model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

def retrieve(user_input, k=3):
    with open("faiss_index/TCM_docs.pkl", "rb") as f:
        docs = pickle.load(f)

    query_vector = embed_model.encode([user_input],convert_to_numpy=True, normalize_embeddings=True) #user input to vector

    index = faiss.read_index("faiss_index/TCM_index.faiss")

    D, I = index.search(query_vector, k)
    results = [docs[i] for i in I[0]]
    return results


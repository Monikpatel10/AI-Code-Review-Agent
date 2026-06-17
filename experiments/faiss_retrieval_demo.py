import faiss
import numpy as np

dimension = 384
num_vectors = 5000
top_k = 5

vectors = np.random.random((num_vectors, dimension)).astype("float32")

index = faiss.IndexFlatL2(dimension)
index.add(vectors)

query = np.random.random((1, dimension)).astype("float32")

distances, indices = index.search(query, top_k)

print("FAISS Retrieval Demo")
print(f"Vectors Indexed: {num_vectors}")
print(f"Dimension: {dimension}")
print(f"Top-K: {top_k}")
print("Nearest Neighbors:", indices[0])
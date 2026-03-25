import faiss
import numpy as np
import sys

# model embedding file
embedding_file = sys.argv[1]

print("Loading embeddings:", embedding_file)

embeddings = np.load(f"../models/{embedding_file}")
embeddings = embeddings.astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

index_name = embedding_file.replace("_embeddings.npy", "_index.index")

faiss.write_index(index, index_name)

print("Index created:", index_name)
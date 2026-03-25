import numpy as np
import faiss

# Load embeddings
embeddings = np.load("../models/embeddings.npy")

# Convert to float32 (FAISS requirement)
embeddings = embeddings.astype("float32")

# Get dimension
dimension = embeddings.shape[1]

# Create FAISS index
index = faiss.IndexFlatL2(dimension)

# Add embeddings to index
index.add(embeddings)

# Save index
faiss.write_index(index, "faiss_index.index")

print("FAISS index created and saved successfully!")
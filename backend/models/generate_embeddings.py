import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

# Load dataset
df = pd.read_csv("../data/medquad.csv")

# Check column names
print("Columns:", df.columns)

# Combine question + answer
texts = df["question"] + " " + df["answer"]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(texts.tolist(), show_progress_bar=True)

# Save embeddings
np.save("embeddings.npy", embeddings)

print("Embeddings generated and saved successfully!")

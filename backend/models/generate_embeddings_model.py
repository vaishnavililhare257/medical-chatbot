import pandas as pd
import numpy as np
import sys
from sentence_transformers import SentenceTransformer

# ---- TAKE MODEL NAME FROM TERMINAL ----
model_name = sys.argv[1]

print(f"Loading model: {model_name}")

# Load dataset
df = pd.read_csv("../data/medquad.csv")

# Combine question + answer
texts = df["question"] + " " + df["answer"]

# Load model
model = SentenceTransformer(model_name)

# Generate embeddings
embeddings = model.encode(texts.tolist(), show_progress_bar=True)

# Save embeddings with model name
save_path = f"{model_name.replace('/', '_')}_embeddings.npy"
np.save(save_path, embeddings)

print(f"Embeddings saved as {save_path}")
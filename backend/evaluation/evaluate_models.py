import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from retrieval.search_engine import load_models, encode, indexes

df = pd.read_csv("../data/medquad.csv")

load_models()

models = ["sbert", "biobert", "clinicalbert", "pubmedbert"]

results = {}

TOP_K = 5
TEST_SIZE = 50

for model in models:

    correct = 0

    print("\nTesting model:", model)

    for i in range(TEST_SIZE):

        query = df.iloc[i]["question"]

        # encode query
        query_vector = encode(query, model)

        # search FAISS
        distances, indices = indexes[model].search(query_vector, TOP_K)

        # check if correct index appears in top K
        if i in indices[0]:
            correct += 1

    accuracy = correct / TEST_SIZE
    results[model] = accuracy

print("\nModel Comparison Results (Recall@5):")

for model, score in results.items():
    print(model, ":", score)
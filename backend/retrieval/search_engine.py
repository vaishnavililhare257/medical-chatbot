import faiss
import numpy as np
import pandas as pd
import torch
import os
from transformers import AutoTokenizer, AutoModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "../data/medquad.csv")

df = pd.read_csv(data_path)

MODEL_CONFIG = {

    "sbert": {
        "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        "index": os.path.join(BASE_DIR, "all-MiniLM-L6-v2_index.index")
    },

    "biobert": {
        "model_name": "dmis-lab/biobert-base-cased-v1.1",
        "index": os.path.join(BASE_DIR, "dmis-lab_biobert-base-cased-v1.1_index.index")
    },

    "clinicalbert": {
        "model_name": "emilyalsentzer/Bio_ClinicalBERT",
        "index": os.path.join(BASE_DIR, "emilyalsentzer_Bio_ClinicalBERT_index.index")
    },

    "pubmedbert": {
        "model_name": "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract",
        "index": os.path.join(BASE_DIR, "microsoft_BiomedNLP-PubMedBERT-base-uncased-abstract_index.index")
    }

}

models = {}
tokenizers = {}
indexes = {}


def load_models():
    for key, config in MODEL_CONFIG.items():
        print("Loading:", key)

        tokenizers[key] = AutoTokenizer.from_pretrained(config["model_name"])
        models[key] = AutoModel.from_pretrained(config["model_name"])
        indexes[key] = faiss.read_index(config["index"])


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]
    mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * mask, 1) / torch.clamp(mask.sum(1), min=1e-9)


def encode(query, model_key):

    tokenizer = tokenizers[model_key]
    model = models[model_key]

    encoded = tokenizer(query, return_tensors="pt", truncation=True, padding=True)

    with torch.no_grad():
        output = model(**encoded)

    embedding = mean_pooling(output, encoded["attention_mask"])

    return embedding.numpy().astype("float32")


def search(query, model_key):

    query_vector = encode(query, model_key)

    distances, indices = indexes[model_key].search(query_vector, 5)

    # Confidence threshold check
   # if distances[0][0] > 1.5:
    #    return [{
     #       "question": query,
      #      "answer": "I'm not confident about the answer. Please consult a doctor."
      #  }]

    results = []

    for idx in indices[0]:
        results.append({
            "question": df.iloc[idx]["question"],
            "answer": df.iloc[idx]["answer"]
        })

    return results
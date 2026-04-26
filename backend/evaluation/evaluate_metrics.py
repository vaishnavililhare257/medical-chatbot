import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from retrieval.search_engine import load_models, encode, indexes
from rouge_score import rouge_scorer
import nltk
from nltk.translate.bleu_score import sentence_bleu

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("../data/medquad.csv")

load_models()

models = ["sbert", "biobert", "clinicalbert", "pubmedbert"]

results = {m: {"Recall@5": 0, "ROUGE-1": 0, "ROUGE-L": 0, "BLEU-1": 0, "BLEU-2": 0} for m in models}

TOP_K = 5
TEST_SIZE = 50

scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

for model in models:
    
    correct = 0
    rouge1_total = 0
    rougel_total = 0
    bleu1_total = 0
    bleu2_total = 0
    
    print("\nTesting model:", model)
    
    for i in range(TEST_SIZE):
        
        query = df.iloc[i]["question"]
        actual_answer = str(df.iloc[i]["answer"])
        
        # encode query
        query_vector = encode(query, model)
        
        # search FAISS
        distances, indices = indexes[model].search(query_vector, TOP_K)
        
        # check if correct index appears in top K
        if i in indices[0]:
            correct += 1
            
        # Use top 1 retrieved index for textual similarity metrics
        top1_idx = indices[0][0]
        retrieved_answer = str(df.iloc[top1_idx]["answer"])
        
        # Calculate ROUGE
        scores = scorer.score(actual_answer, retrieved_answer)
        rouge1_total += scores['rouge1'].fmeasure
        rougel_total += scores['rougeL'].fmeasure
        
        # Calculate BLEU
        ref_tokens = actual_answer.split()
        cand_tokens = retrieved_answer.split()
        
        # weight vectors for BLEU-1 and BLEU-2
        bleu1 = sentence_bleu([ref_tokens], cand_tokens, weights=(1, 0, 0, 0))
        bleu2 = sentence_bleu([ref_tokens], cand_tokens, weights=(0.5, 0.5, 0, 0))
        
        bleu1_total += bleu1
        bleu2_total += bleu2

    results[model]["Recall@5"] = correct / TEST_SIZE
    results[model]["ROUGE-1"] = rouge1_total / TEST_SIZE
    results[model]["ROUGE-L"] = rougel_total / TEST_SIZE
    results[model]["BLEU-1"] = bleu1_total / TEST_SIZE
    results[model]["BLEU-2"] = bleu2_total / TEST_SIZE

print("\nModel Comparison Results:")
for model in models:
    print(f"{model}: {results[model]}")

# Plotting the results
plot_df = pd.DataFrame(results).T
plot_df.reset_index(inplace=True)
plot_df.rename(columns={'index': 'Model'}, inplace=True)

metrics_to_plot = ['ROUGE-1', 'ROUGE-L', 'BLEU-1', 'BLEU-2', 'Recall@5']
filenames = []

for metric in metrics_to_plot:
    plt.figure(figsize=(8, 6))
    sns.barplot(data=plot_df, x='Model', y=metric, palette='Set2')
    plt.title(f'Comparison of Models: {metric}')
    plt.ylabel('Score')
    plt.xlabel('Model')
    plt.ylim(0, 1.0)
    plt.tight_layout()
    
    filename = f"{metric.lower().replace('@', '_')}_comparison.png"
    plt.savefig(filename, dpi=300)
    plt.close()
    filenames.append(filename)

print(f"\nGraphs saved separately as:\n" + "\n".join(filenames))

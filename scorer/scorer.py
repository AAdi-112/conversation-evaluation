import pandas as pd
import numpy as np
import re
from functools import lru_cache

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load facet dataset ONCE
FACET_PATH = "data/Facets Assignment.csv"
facets_df = pd.read_csv(FACET_PATH)

#  Text Cleaning 
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

facets_df["facet_clean"] = facets_df["Facets"].apply(clean_text)

#  Facet Grouping 
def assign_facet_group(text):
    if re.search(r"safety|harm|abuse|violence", text):
        return "safety"
    elif re.search(r"emotion|sentiment|feeling", text):
        return "emotion"
    elif re.search(r"clarity|grammar|fluency", text):
        return "linguistic"
    elif re.search(r"intent|context|relevance", text):
        return "pragmatic"
    else:
        return "general"

facets_df["facet_group"] = facets_df["facet_clean"].apply(assign_facet_group)

#  Embedding Model (CPU)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
facet_embeddings = embedding_model.encode(
    facets_df["facet_clean"].tolist(), show_progress_bar=False
)

#  Conversation Preprocessing 
def preprocess_conversation(text):
    text_clean = clean_text(text)
    return {
        "text": text,
        "clean": text_clean,
        "token_count": len(text_clean.split()),
        "question_present": "?" in text,
        "emotion_words": len(re.findall(r"happy|sad|angry|fear|love", text_clean))
    }

#  Rule-Based Scoring 
def rule_score(conv, facet):
    score = 3

    if "clarity" in facet and conv["token_count"] < 5:
        score = 2
    if "question" in facet and conv["question_present"]:
        score = 4
    if "emotion" in facet and conv["emotion_words"] > 0:
        score = 4
    
    if facet["facet_group"] == "safety":
      if re.search(r"threat|unsafe|violence|kill|harm", conv["clean"]):
        return 1, 0.9


    return score, 0.65

# Embedding-Based Scoring 
def embedding_score(conv_text, facet_idx):
    conv_emb = embedding_model.encode([conv_text], show_progress_bar=False)
    sim = cosine_similarity(conv_emb, [facet_embeddings[facet_idx]])[0][0]

    if sim < 0.15:
      score = 3   # neutral
    elif sim < 0.30:
        score = 2
    elif sim < 0.50:
        score = 4
    else:
      score = 5

    return score, float(sim)

#Unified Scorer
@lru_cache(maxsize=2048)
def score_facet(conversation, facet_idx):
    facet = facets_df.iloc[facet_idx]
    conv = preprocess_conversation(conversation)

    if facet["facet_group"] in ["linguistic", "safety"]:
        return rule_score(conv, facet["facet_clean"])

    return embedding_score(conv["clean"], facet_idx)

# Public API 
def score_conversation(conversation, max_facets=30):
    results = []

    for i in range(min(max_facets, len(facets_df))):
        score, conf = score_facet(conversation, i)
        results.append({
            "facet": facets_df.iloc[i]["Facets"],
            "score": score,
            "confidence": round(conf, 2)
        })

    return pd.DataFrame(results)

def summarize_scores(df):
    return {
        "avg_score": round(df["score"].mean(), 2),
        "avg_confidence": round(df["confidence"].mean(), 2),
        "high_risk_facets": df[df["score"] <= 2]["facet"].tolist()
    }

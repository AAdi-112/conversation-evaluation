# Conversation Evaluation Benchmark  
**Ahoum – AI/ML Assignment**

## Overview

This project implements a **production-ready conversation evaluation benchmark** that scores
individual conversation turns across **hundreds of distinct facets** spanning:

- Linguistic quality
- Pragmatics
- Safety
- Emotion

The system is designed with **scalability, cost-efficiency, and reproducibility** in mind and
supports **300+ facets today** with the ability to scale to **5000+ facets without architectural changes**.

---

## Problem Statement

Given a single conversation turn, the system must assign:

- A **score** (five ordered integers)  
- A **confidence value**  

for each evaluation facet defined in the provided dataset (`Facets Assignment.csv`).

---

## Key Design Goals

-  **Scalable to thousands of facets**
-  **Avoid one-shot prompting**
-  **Production-oriented (latency & cost aware)**
-  **Open-weight model compatibility**
-  **Transparent and explainable scoring**

---

## Architecture Overview

The system uses a **hybrid, tiered evaluation pipeline**:

              Conversation Turn
                     ↓
         Preprocessing & Feature Extraction
                     ↓
        Facet Routing (by category)
                     ↓
        ┌─────────────────┬──────────────────┐
        │ Rule-Based │ Embedding-Based │
        │ Evaluation │ Similarity │
        │ (Cheap & Fast) │ (Scalable ML) │
        └─────────────────┴──────────────────┘
                     ↓
        (Optional) LLM Fallback for Low-Confidence Pragmatic Facets
                     ↓
            Final Score + Confidence

### Why Hybrid?

Scoring hundreds or thousands of facets using an LLM for every evaluation is **not scalable**.
Instead, the system relies on:

- **Deterministic rules** for safety and linguistic facets
- **Sentence embeddings** for semantic relevance
- **Optional LLM fallback** only for ambiguous, low-confidence pragmatic cases

This mirrors how real production evaluation systems are built.

---

## Facet Processing & Scalability

- Facets are **data-driven**, not hard-coded
- Adding new facets requires **only updating the CSV**
- No redesign is needed to scale from 300 → 5000 facets
- Facets are grouped dynamically (safety, emotion, linguistic, pragmatic, general)

---

## Data Cleaning & Feature Engineering

The facet dataset is cleaned and enriched with additional metadata, including:

- Normalized facet text
- Token length
- Category assignment (safety / emotion / linguistic / pragmatic)
- Safety indicators

Conversation turns are preprocessed to extract:

- Token counts
- Question presence
- Emotion indicators
- Cleaned text representation

These features reduce unnecessary model inference and improve interpretability.

---

## Scoring & Confidence

Each facet produces:

- **Score:** one of five ordered integers
- **Confidence:** derived from rule certainty or embedding similarity

A **neutral prior** is applied when a facet is weakly expressed, ensuring that
unrelated facets are not unfairly penalized.

Low confidence explicitly signals **evaluation uncertainty**, which is an intended and
important property of the benchmark.

---

## LLM Usage Strategy

The system does **not rely on LLM inference for every facet**.

Reasoning:
- Thousands of facets × LLM calls is not production-viable
- One-shot prompt evaluation is explicitly disallowed

Instead:
- Open-weight LLMs (e.g., Qwen2-7B, Llama-3-8B) are **architecturally supported**
- LLMs can be used as an **optional fallback** for low-confidence pragmatic facets
- This avoids one-shot prompting and excessive inference cost

This design prioritizes scalability and real-world feasibility.

---

## Sample UI

A lightweight **Gradio UI** is provided to demonstrate:

- Single conversation turn input
- Facet-wise scores and confidence
- Aggregate summary statistics

For demo stability, the UI limits evaluation to a subset of facets, while the backend
supports full-scale evaluation.

---

## Dockerised Baseline

A **CPU-only Dockerfile** is included for reproducibility.

- No GPU or CUDA dependency
- Uses open-weight libraries only
- Suitable for local, server, or CI environments

Docker was not executed inside Google Colab due to environment limitations,
but the Dockerfile follows standard conventions and can be built as:

    docker build -t ahoum-eval .
    docker run ahoum-eval

## Evaluation Samples

The submission includes a ZIP file containing 50 diverse conversation turns covering:

- Safety and threat scenarios

- Strong and subtle emotional expressions

- Pragmatic failures and irrelevance

- Polite, sarcastic, neutral, and low-quality inputs

- Leadership, risk, and ethical reasoning cases

Each conversation is scored using the same evaluation pipeline as the main system.

 ## Repository Structure
    .
    ├── scorer/
    │   ├── __init__.py
    │   └── scorer.py
    ├── ui/
    │   └── app.py
    ├── data/
    │   └── Facets Assignment.csv
    ├── submission_data/
    │   ├── conversations.csv
    │   └── conversation_scores.csv
    ├── Dockerfile
    ├── main.py
    └── README.md

## How to Run

Local / Colab:

         python ui/app.py
Docker

    docker build -t ahoum-eval .
    docker run -p 7860:7860 ahoum-eval

## Summary

This project focuses on robust system design rather than brute-force LLM usage.
The resulting benchmark is:

 - Scalable

 - Cost-aware

 - Transparent

 - Production-ready

The architecture intentionally balances deterministic logic, lightweight ML, and optional LLM usage to meet real-world constraints.

### UI Preview

[Gradio UI – Overview](https://github.com/AAdi-112/conversation-evaluation/blob/624cc91a516a5d3716f43297df6765648e9aeecc/assets/conversation%20evaluation%20UI%20home.png)

[Gradio UI – Facet Scores 1]([assets/ui_scores.png](https://github.com/AAdi-112/conversation-evaluation/blob/624cc91a516a5d3716f43297df6765648e9aeecc/assets/conversation%20evaluation%20UI%20results%201.png))

[Gradio UI – Facet Scores 2]([[assets/ui_scores.png](https://github.com/AAdi-112/conversation-evaluation/blob/624cc91a516a5d3716f43297df6765648e9aeecc/assets/conversation%20evaluation%20UI%20results%201.png)](https://github.com/AAdi-112/conversation-evaluation/blob/624cc91a516a5d3716f43297df6765648e9aeecc/assets/conversation%20evaluation%20UI%20results%202.png))


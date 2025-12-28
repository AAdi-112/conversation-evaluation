import sys
import os
import gradio as gr
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# Importing scorer 
from scorer.scorer import score_conversation, summarize_scores

def evaluate_conversation(text):
    if not text or not text.strip():
        return "Please enter a conversation.", pd.DataFrame()

    # Limiting the facets for demo (for making it safe for Colab)
    df = score_conversation(text, max_facets=30)

    summary = summarize_scores(df)

    summary_text = (
        f"Average Score: {summary['avg_score']}\n"
        f"Average Confidence: {summary['avg_confidence']}\n"
        f"Low-Scoring Facets: {', '.join(summary['high_risk_facets'][:5])}"
    )

    return summary_text, df


with gr.Blocks(title="Conversation Evaluation – Ahoum") as demo:
    gr.Markdown(
        """
        #  Conversation Evaluation System  
        Scores a conversation turn across linguistic, safety, emotion and pragmatic facets.
        """
    )

    input_text = gr.Textbox(
        label="Conversation Turn",
        placeholder="Enter a single conversation turn here...",
        lines=4
    )

    submit_btn = gr.Button("Evaluate")

    summary_output = gr.Textbox(
        label="Summary",
        lines=4
    )

    table_output = gr.Dataframe(
        headers=["facet", "score", "confidence"],
        label="Facet-wise Scores"
    )

    submit_btn.click(
        fn=evaluate_conversation,
        inputs=input_text,
        outputs=[summary_output, table_output]
    )

if __name__ == "__main__":
    demo.launch(share=True)

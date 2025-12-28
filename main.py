import os

if __name__ == "__main__":
    mode = os.environ.get("MODE", "ui")

    if mode == "ui":
        from ui.app import demo
        demo.launch()
    else:
        from scorer.scorer import score_conversation
        text = "I am unhappy with the service. Can you help me?"
        df = score_conversation(text, max_facets=20)
        print(df.head())

# sentiment_engine.py
from transformers import pipeline
import logging

# Suppress warnings to keep output clean
logging.getLogger("transformers").setLevel(logging.ERROR)

print(">> Loading AI Model (FinBERT)...")
pipe = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze(comments):
    """
    Input: List of strings
    Output: List of dictionaries [{'label': 'positive', 'score': 0.9}, ...]
    """
    if not comments: return []
    
    # Analyze all comments in one go
    results = pipe(comments, truncation=True, max_length=512)
    return results
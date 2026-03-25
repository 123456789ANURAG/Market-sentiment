# generate_scenarios.py
import csv
import random
import os

# --- TEMPLATES ---
TICKERS = ["NVDA", "TSLA", "AAPL", "AMD", "PLTR"]

TEMPLATES = {
    "bullish": [
        "Buying more {t}!, massive potential.", "{t} is going to the moon! 🚀", 
        "Great earnings, {t} is a strong buy.", "Long term hold on {t}.", 
        "Fundamentals for {t} are solid."
    ],
    "bearish": [
        "Selling {t}, chart looks weak.", "{t} is a bubble waiting to pop.", 
        "Shorting {t} now.", "Management of {t} is terrible.", 
        "Revenue missed, {t} is done."
    ],
    "neutral": [
        "Watching {t} closely.", "When is the earnings call?", 
        "Just analyzing the chart.", "First view!", "Thanks for the video."
    ],
    "spam": [
        "Whatsapp +12345 for crypto tips!", "Earn $5k weekly with Mr. James.", 
        "Check my bio for signals.", "Invest in Bitcoin now! 💰", 
        "Click here for free money."
    ],
    "tricky": [
        "Great job losing my money {t}.", "Buy high sell low strategy for {t}!",
        "Yeah sure, {t} always goes up... right?", "Wow, another drop. Amazing.",
        "I love seeing red in my portfolio."
    ]
}

def create_dataset(filename, count, ratios):
    """
    ratios: dict with keys 'bullish', 'bearish', 'neutral', 'spam', 'tricky'
    Sum of values must roughly equal 1.0
    """
    data = []
    print(f"Generating {filename} ({count} rows)...")
    
    for i in range(count):
        # Determine category based on weighted random choice
        categories = list(ratios.keys())
        weights = list(ratios.values())
        category = random.choices(categories, weights=weights, k=1)[0]
        
        ticker = random.choice(TICKERS)
        text_template = random.choice(TEMPLATES[category])
        text = text_template.format(t=ticker)
        
        # Determine the "Expected Sentiment" (Ground Truth)
        # Note: Spam and Tricky are hard. We assume specific truths for testing.
        if category == 'bullish': ground_truth = 'positive'
        elif category == 'bearish': ground_truth = 'negative'
        elif category == 'neutral': ground_truth = 'neutral'
        elif category == 'spam': ground_truth = 'spam' # AI should ideally mark this Neutral or Filter it
        elif category == 'tricky': ground_truth = 'negative' # Sarcasm is usually negative sentiment
        
        data.append([i+1, category, ground_truth, text])

    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "category", "ground_truth", "comment_text"])
        writer.writerows(data)

def run_generation():
    if not os.path.exists("test_data"):
        os.makedirs("test_data")

    # --- SCENARIO 1: THE UTOPIA (Clean Data) ---
    # 0% Spam, 0% Sarcasm. Pure sentiment. Best case scenario.
    create_dataset("test_data/1_clean.csv", 100, {
        'bullish': 0.4, 'bearish': 0.4, 'neutral': 0.2, 'spam': 0.0, 'tricky': 0.0
    })

    # --- SCENARIO 2: THE REAL WORLD (Standard) ---
    # 10% Spam, 5% Tricky. Typical YouTube comment section.
    create_dataset("test_data/2_realistic.csv", 100, {
        'bullish': 0.35, 'bearish': 0.35, 'neutral': 0.15, 'spam': 0.1, 'tricky': 0.05
    })

    # --- SCENARIO 3: THE BOT ATTACK (High Noise) ---
    # 50% Spam. Simulates a video hit by crypto bots.
    create_dataset("test_data/3_spam_attack.csv", 100, {
        'bullish': 0.2, 'bearish': 0.2, 'neutral': 0.1, 'spam': 0.5, 'tricky': 0.0
    })

    # --- SCENARIO 4: THE TROLLS (High Complexity) ---
    # 30% Sarcasm/Tricky. Hardest for NLP models to understand.
    create_dataset("test_data/4_complexity_test.csv", 100, {
        'bullish': 0.25, 'bearish': 0.25, 'neutral': 0.2, 'spam': 0.0, 'tricky': 0.3
    })

    print("\n✅ All 4 datasets generated in '/test_data' folder.")

if __name__ == "__main__":
    run_generation()
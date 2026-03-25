# dummy_data.py

def get_dummy_comments():
    """
    Returns a list of fake YouTube comments to test the NLP pipeline.
    """
    return [
        # --- CLEARLY BULLISH (Positive) ---
        "NVDA is unstoppable, buying more at this dip!",
        "Earnings were incredible, revenue up 20% year over year.",
        "Target price $150 by next month. LETS GOOO 🚀",
        "The fundamentals are solid, long term hold for sure.",

        # --- CLEARLY BEARISH (Negative) ---
        "This is a bubble, getting out before it pops.",
        "CEO sold shares, that is a huge red flag.",
        "Revenue missed expectations, I am shorting this.",
        "Garbage stock, down 50% from all time high.",

        # --- NEUTRAL / IRRELEVANT ---
        "First view!",
        "Can you analyze TSLA next week?",
        "I have been watching this channel for 2 years.",

        # --- SPAM (Common on YouTube - FinBERT might be confused by these) ---
        "Great video! For crypto signals WhatsApp me +1 234 567 890",
        "Invest with Mr. James to earn $5000 weekly.",
        
        # --- TRICKY (Sarcasm/Mixed) ---
        "Great earnings report and the stock drops 10%. Classic manipulation.",
        "I love losing money on this stock every week."
    ]
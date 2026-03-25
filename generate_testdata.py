import csv
import random

def generate_dataset(filename="stock_comments_dataset.csv", total_count=500):
    print(f"Generating {total_count} synthetic comments...")

    # --- 1. DATA TEMPLATES (The DNA of your data) ---
    tickers = ["NVDA", "TSLA", "AAPL", "AMD", "MSFT", "GOOGL", "PLTR", "COIN"]
    
    # [Positive/Bullish]
    bull_templates = [
        "Buying more {t} at this price, it's a steal!",
        "{t} to the moon! 🚀🚀",
        "Fundamentals for {t} are incredible, revenue up {n}% year over year.",
        "Just bought 100 shares of {t}, holding for 5 years.",
        "Everyone doubting {t} is going to regret it.",
        "Long term bullish on {t}.",
        "The AI revolution is just starting, {t} is the leader.",
        "Solid earnings, great guidance. Easy hold.",
        "My portfolio is 50% {t} and I sleep like a baby.",
        "Ignore the FUD, {t} is going to $1000."
    ]

    # [Negative/Bearish]
    bear_templates = [
        "Selling my {t} position, the chart looks weak.",
        "{t} is a bubble waiting to burst.",
        "Shorting {t} with everything I have.",
        "Management is selling shares, get out of {t} now!",
        "Revenue missed expectations. {t} is done.",
        "This stock is overhyped garbage.",
        "Dead cat bounce. {t} is going to crash.",
        "Puts on {t} printed today! 📉",
        "I lost so much money on {t}, never again.",
        "The valuation makes no sense. {t} is overvalued."
    ]

    # [Neutral / Questions]
    neutral_templates = [
        "What do you think is a good entry price for {t}?",
        "Watching {t} closely this week.",
        "Does anyone know when the next earnings call is?",
        "Just analyzing the chart for {t}.",
        "First view!",
        "Interesting video, thanks for the analysis.",
        "Holding cash for now, waiting for a dip.",
        "Can you cover {t} in the next video?",
        "Market is choppy today.",
        "Volume is low on {t} today."
    ]

    # [Spam / Scrap Data] - The LLM should filter or ignore these
    spam_templates = [
        "Whatsapp me at +1 234 567 for crypto signals!",
        "Start earning $5000 weekly with Mr. James.",
        "Check my bio for the best trading bot.",
        "Invest in Bitcoin now! 💰",
        "Lose weight fast with this one trick.",
        "Great video! msg me 📞 +44 7890 123",
        "CLICK HERE FOR FREE MONEY",
        "Are you tired of losing? Join my telegram.",
        "Ignore the video, read my profile.",
        "Promoting my new music channel, check it out."
    ]

    # [Tricky / Sarcasm] - Hard for AI to detect
    tricky_templates = [
        "Great job losing my money, thanks for the tip.",
        "Buy high sell low, that's my strategy for {t}!",
        "Yeah sure, because {t} always goes up... right?",
        "Wow, another 'groundbreaking' announcement. Yawn.",
        "I love how this stock drops every time good news comes out."
    ]

    # --- 2. SCENARIO DISTRIBUTION ---
    # We want a messy, realistic mix:
    # 35% Bullish, 35% Bearish, 15% Neutral, 10% Spam, 5% Tricky
    data = []
    
    for i in range(total_count):
        roll = random.random()
        ticker = random.choice(tickers)
        num = random.randint(10, 200) # Random number for percentages
        
        if roll < 0.35:
            category = "bullish"
            text = random.choice(bull_templates).format(t=ticker, n=num)
        elif roll < 0.70:
            category = "bearish"
            text = random.choice(bear_templates).format(t=ticker, n=num)
        elif roll < 0.85:
            category = "neutral"
            text = random.choice(neutral_templates).format(t=ticker, n=num)
        elif roll < 0.95:
            category = "spam"
            text = random.choice(spam_templates).format(t=ticker, n=num)
        else:
            category = "tricky"
            text = random.choice(tricky_templates).format(t=ticker, n=num)
            
        # We append a tuple: (ID, Ticker, Category, Comment)
        data.append([i+1, ticker, category, text])

    # --- 3. SAVE TO CSV ---
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "ticker", "true_label", "comment_text"]) # Header
        writer.writerows(data)
        
    print(f"Success! Saved {filename} with 500 rows.")

if __name__ == "__main__":
    generate_dataset()
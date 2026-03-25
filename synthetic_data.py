# synthetic_data.py
import random

def generate_comments(num_comments=15):
    """
    Generates a list of random synthetic stock market comments.
    Every time you run this, the mix and wording will be different.
    """
    
    # --- Building Blocks ---
    tickers = ["NVDA", "TSLA", "AAPL", "AMD", "The stock", "This company"]
    
    bullish_templates = [
        "{t} is going to the moon! 🚀",
        "Buying more {t} at this dip, easy money.",
        "{t} fundamentals are looking stronger than ever.",
        "Just loaded up on more {t} calls.",
        "I predict {t} will double by Q4.",
        "Everyone selling {t} is going to regret it."
    ]
    
    bearish_templates = [
        "{t} is a total scam, get out while you can.",
        "Selling all my {t}, the chart looks awful.",
        "{t} is overvalued garbage.",
        "Shorting {t} with everything I have.",
        "The CEO of {t} has no idea what he is doing.",
        "Huge crash coming for {t} soon."
    ]
    
    spam_templates = [
        "Whatsapp me at +1-202-555 for crypto tips!",
        "I made $50k last week thanks to Mr. Smith.",
        "Click my profile to see how I trade {t}.",
        "Don't trust the banks! Buy Bitcoin now."
    ]
    
    neutral_templates = [
        "Does anyone know when the earnings call is?",
        "Watching {t} closely this week.",
        "First view!",
        "Good analysis video, thanks."
    ]

    comments = []
    
    # Randomly decide the "market mood" for this run to make it realistic
    # (e.g., 50% chance it's a Bull market run, 30% Bear, 20% Mixed)
    mood = random.choice(['bull_run', 'bear_crash', 'mixed'])
    
    for _ in range(num_comments):
        roll = random.random() # Number between 0.0 and 1.0
        
        if mood == 'bull_run':
            # High chance of bullish comments
            if roll < 0.6: template = random.choice(bullish_templates)
            elif roll < 0.8: template = random.choice(neutral_templates)
            elif roll < 0.9: template = random.choice(bearish_templates)
            else: template = random.choice(spam_templates)
            
        elif mood == 'bear_crash':
            # High chance of bearish comments
            if roll < 0.6: template = random.choice(bearish_templates)
            elif roll < 0.8: template = random.choice(neutral_templates)
            elif roll < 0.9: template = random.choice(bullish_templates)
            else: template = random.choice(spam_templates)
            
        else: # Mixed market
            template = random.choice(bullish_templates + bearish_templates + neutral_templates)

        # Fill in the ticker placeholder
        filled_comment = template.format(t=random.choice(tickers))
        comments.append(filled_comment)
        
    return comments
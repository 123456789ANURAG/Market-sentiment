# main.py
import pandas as pd
import sentiment_engine as se
import spam_filter as sf  # <--- IMPORT THE NEW FILTER

def run_analysis():
    print("--- LOADING DATA ---")
    try:
        df = pd.read_csv("stock_comments_dataset.csv")
    except FileNotFoundError:
        print("Error: Run 'generate_test_data.py' first!")
        return

    total_comments = len(df)
    print(f"Loaded {total_comments} raw comments.")

    # --- STEP 1: SPAM FILTERING ---
    print("\n--- 1. FLAGGING SPAM ---")
    
    clean_comments = []
    spam_comments = []

    for index, row in df.iterrows():
        text = row['comment_text']
        
        if sf.is_spam(text):
            spam_comments.append(text)
        else:
            clean_comments.append(text)

    # Calculate Stats
    spam_count = len(spam_comments)
    clean_count = len(clean_comments)
    spam_percent = (spam_count / total_comments) * 100

    print(f"Found {spam_count} SPAM messages ({spam_percent:.1f}% of data).")
    print(f"Remaining {clean_count} clean comments for analysis.")
    
    # Show examples of what we caught (to verify it works)
    if spam_count > 0:
        print("\n[Spam Examples Caught]:")
        for s in spam_comments[:3]: # Show first 3
            print(f"  ❌ {s}")

    # --- STEP 2: SENTIMENT ANALYSIS (On Clean Data Only) ---
    print(f"\n--- 2. ANALYZING SENTIMENT (FinBERT) ---")
    
    if clean_count == 0:
        print("No clean data left to analyze!")
        return

    # We only send 'clean_comments' to the AI now
    results = se.analyze(clean_comments)

    # --- STEP 3: REPORTING ---
    bullish = 0
    bearish = 0
    neutral = 0

    for res in results:
        if res['label'] == 'positive': bullish += 1
        elif res['label'] == 'negative': bearish += 1
        else: neutral += 1

    print("\n--- FINAL REPORT ---")
    print(f"Total Analyzed: {clean_count}")
    print(f"✅ Bullish: {bullish}")
    print(f"🔻 Bearish: {bearish}")
    print(f"😐 Neutral: {neutral}")

    # Calculate Signal (ignoring neutral)
    if bullish + bearish > 0:
        ratio = bullish / (bullish + bearish)
        print(f"\nBullish Sentiment Score: {ratio:.2%} (Clean Data Only)")
        
        if ratio > 0.65: print(">> SIGNAL: BUY 🟢")
        elif ratio < 0.35: print(">> SIGNAL: SELL 🔴")
        else: print(">> SIGNAL: HOLD 🟡")
    else:
        print(">> SIGNAL: NO CLEAR TREND")

if __name__ == "__main__":
    run_analysis()
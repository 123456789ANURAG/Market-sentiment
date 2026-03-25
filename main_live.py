# main_live.py
import youtube_fetcher as yt
import sentiment_engine as se
import spam_filter as sf
import sys

def run_live_analysis():
    # 1. GET USER INPUT
    ticker = input("Enter Stock Ticker (e.g., NVDA, TSLA): ").upper().strip()
    if not ticker:
        print("Please enter a valid ticker.")
        sys.exit()

    # 2. FETCH VIDEOS
    print("-" * 50)
    videos = yt.search_videos(ticker, max_results=3) # Limit to 3 videos to save quota
    
    if not videos:
        print("No videos found. Check your API Key or Quota.")
        sys.exit()

    # 3. HARVEST COMMENTS
    all_comments = []
    print(f"\n📥 Extracting comments from {len(videos)} videos...")
    
    for v in videos:
        print(f"   > Parsing: {v['title'][:40]}...") # Print truncated title
        comm = yt.fetch_comments(v['id'], max_comments=15)
        all_comments.extend(comm)

    total_raw = len(all_comments)
    print(f"\n📊 Total Raw Comments Fetched: {total_raw}")
    
    if total_raw == 0:
        print("No comments found. Try a more popular stock.")
        sys.exit()

    # 4. FILTER SPAM (The Robust Pipeline)
    print("🧹 Running Spam Filter...")
    clean_comments = [c for c in all_comments if not sf.is_spam(c)]
    spam_count = total_raw - len(clean_comments)
    
    print(f"   - Removed {spam_count} spam bots.")
    print(f"   - {len(clean_comments)} valid comments remaining.")

    # 5. ANALYZE SENTIMENT
    print("\n🧠 Running FinBERT AI...")
    results = se.analyze(clean_comments)

    # 6. REPORT
    bullish = 0
    bearish = 0
    neutral = 0
    
    # Let's print a few examples to see what people are actually saying
    print("\n--- VOICE OF THE CROWD (Samples) ---")
    for i, (txt, res) in enumerate(zip(clean_comments, results)):
        if i < 3: # Show first 3 only
            label = res['label']
            print(f"[{label.upper()}] {txt[:60]}...")

        # Tally scores
        if res['label'] == 'positive': bullish += 1
        elif res['label'] == 'negative': bearish += 1
        else: neutral += 1

    # 7. FINAL VERDICT
    total_valid = bullish + bearish + neutral
    if total_valid > 0:
        bull_ratio = bullish / total_valid
        
        print("\n" + "="*30)
        print(f"📢 LIVE REPORT FOR ${ticker}")
        print("="*30)
        print(f"✅ Bullish: {bullish} ({bullish/total_valid:.1%})")
        print(f"🔻 Bearish: {bearish} ({bearish/total_valid:.1%})")
        print(f"😐 Neutral: {neutral}")
        
        # Simple signal logic
        if bullish > bearish * 1.5:
            print("\n>> SIGNAL: 🟢 BUY (Strong Sentiment)")
        elif bearish > bullish * 1.5:
            print("\n>> SIGNAL: 🔴 SELL (Negative Sentiment)")
        else:
            print("\n>> SIGNAL: 🟡 HOLD (Mixed/Uncertain)")
            
    else:
        print("Not enough data.")

if __name__ == "__main__":
    run_live_analysis()
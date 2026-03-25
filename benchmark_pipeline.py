# benchmark_pipeline.py
import pandas as pd
import sentiment_engine as se
import spam_filter as sf  # <--- NEW: We test the filter now
import glob
import os

def benchmark_model():
    # Find all CSV files in the 'test_data' folder
    files = sorted(glob.glob("test_data/*.csv"))
    
    if not files:
        print("❌ No data found! Please run 'generate_scenarios.py' first.")
        return

    print(f"{'SCENARIO':<20} | {'FILTER CAUGHT':<15} | {'AI ACCURACY':<12} | {'STATUS'}")
    print("-" * 75)

    for filepath in files:
        filename = os.path.basename(filepath)
        df = pd.read_csv(filepath)
        
        total_rows = len(df)
        spam_rows_indices = df[df['ground_truth'] == 'spam'].index
        
        # --- TEST 1: SPAM FILTER PERFORMANCE ---
        # How many rows did the filter correctly mark as spam?
        caught_count = 0
        false_positives = 0 # Real comments mistakenly deleted
        
        # We also need to keep track of rows to send to AI
        clean_comments = []
        clean_ground_truths = []
        
        for index, row in df.iterrows():
            text = row['comment_text']
            is_spam = sf.is_spam(text)
            
            if is_spam:
                if row['ground_truth'] == 'spam':
                    caught_count += 1
                else:
                    false_positives += 1 # Bad! We deleted a real comment
            else:
                # If not spam, we send it to AI
                clean_comments.append(text)
                clean_ground_truths.append(row['ground_truth'])

        # Calculate Filter Effectiveness
        total_spam_in_file = len(spam_rows_indices)
        if total_spam_in_file > 0:
            catch_rate = (caught_count / total_spam_in_file) * 100
        else:
            catch_rate = 100.0 # No spam to catch
            
        # --- TEST 2: AI ACCURACY (On Clean Data Only) ---
        if clean_comments:
            ai_results = se.analyze(clean_comments)
            
            # Check matches
            correct_predictions = 0
            valid_comparison_count = 0
            
            for i, res in enumerate(ai_results):
                prediction = res['label']
                truth = clean_ground_truths[i]
                
                # We only care about accuracy on Bullish/Bearish/Neutral
                if truth in ['positive', 'negative', 'neutral']:
                    valid_comparison_count += 1
                    if prediction == truth:
                        correct_predictions += 1
            
            if valid_comparison_count > 0:
                ai_accuracy = (correct_predictions / valid_comparison_count) * 100
            else:
                ai_accuracy = 0.0
        else:
            ai_accuracy = 0.0

        # --- REPORTING ---
        status = "✅ PASS"
        if catch_rate < 80 and total_spam_in_file > 0: status = "⚠️ FILTER WEAK"
        if ai_accuracy < 70: status = "⚠️ AI WEAK"
        
        print(f"{filename:<20} | {catch_rate:5.1f}% Caught    | {ai_accuracy:5.1f}%      | {status}")
        
        # Special Warning for False Positives (Deleting real users)
        if false_positives > 0:
            print(f"   [!] WARNING: Filter deleted {false_positives} REAL comments in {filename}!")

if __name__ == "__main__":
    benchmark_model()
# spam_filter.py
import re

def is_spam(text):
    """
    Returns True if the comment looks like a bot/scam.
    Returns False if it looks like a real human.
    """
    # Convert to lowercase for easier matching
    text = text.lower()

    # --- RULE 1: CONTACT INFO (The #1 sign of a bot) ---
    # Matches patterns like: "+1 234", "WhatsApp", "Telegram", "msg me"
    if re.search(r'(whatsapp|telegram|viber|skype)', text):
        return True
    
    # Matches phone numbers (e.g., +1, +44, or long digit strings)
    if re.search(r'\+\d{1,3}', text) or re.search(r'\d{8,}', text):
        return True

    # --- RULE 2: "GURU" SCAMS ---
    # Matches: "Thanks to Mr. James", "Mrs. Linda helped me"
    if "mr." in text or "mrs." in text or "manager" in text:
        # Check if they are talking about "trading" or "profit"
        if re.search(r'(trade|profit|invest|earnings|payout)', text):
            return True

    # --- RULE 3: CALLS TO ACTION ---
    # Matches: "Check my bio", "Inbox me", "Click the link"
    if re.search(r'(check my bio|inbox me|message me|click here|link in)', text):
        return True

    # --- RULE 4: SUSPICIOUS MONEY PROMISES ---
    # Matches: "$5,000 weekly", "crypto signals"
    if re.search(r'(weekly|daily) profit', text):
        return True
    if "crypto signals" in text or "forex signals" in text:
        return True

    # If none of the above, it's likely a human
    return False
# MarketPulse — Stock Sentiment Frontend

A clean, terminal-dark dashboard for your FinBERT + YouTube sentiment tool.

---

## Project Structure

```
your-existing-project/
├── api.py                  ← NEW: Drop this in your project root
├── main.py
├── main_live.py
├── sentiment_engine.py
├── youtube_fetcher.py
├── spam_filter.py
├── ...
frontend/
└── index.html              ← NEW: Open this in your browser
```

---

## Setup (2 steps)

### Step 1 — Backend (FastAPI)

Drop `api.py` into your existing project directory, then:

```bash
# Install FastAPI & Uvicorn (one-time)
pip install fastapi uvicorn

# Start the API server
uvicorn api:app --reload --port 8000
```

The API will be live at: **http://localhost:8000**

You can verify it's running by visiting: http://localhost:8000/health
→ Should return `{"status": "ok"}`

> **Note**: The FinBERT model will load on first request (~30 seconds). Subsequent requests are fast.

---

### Step 2 — Frontend

Just open `frontend/index.html` directly in your browser:

```
File → Open File → index.html
```

Or with a simple server (optional):
```bash
cd frontend
python -m http.server 5500
# Open http://localhost:5500
```

---

## How It Works

```
Browser (index.html)
    ↓  POST /analyze  { ticker: "NVDA" }
FastAPI (api.py)
    ↓
youtube_fetcher.py   → Fetch latest YouTube videos + comments
    ↓
spam_filter.py       → Remove bot/scam comments
    ↓
sentiment_engine.py  → FinBERT classifies each comment
    ↓
JSON response        → { signal, bullish, bearish, neutral, samples, ... }
    ↓
Dashboard renders BUY / SELL / HOLD + breakdown
```

---

## API Endpoint

### `POST /analyze`

**Request:**
```json
{
  "ticker": "NVDA",
  "max_videos": 3,
  "max_comments_per_video": 15
}
```

**Response:**
```json
{
  "ticker": "NVDA",
  "signal": "BUY",
  "signal_strength": "Strong",
  "bullish": 28,
  "bearish": 6,
  "neutral": 11,
  "total_analyzed": 45,
  "total_raw": 52,
  "spam_removed": 7,
  "bull_ratio": 0.6222,
  "bear_ratio": 0.1333,
  "neutral_ratio": 0.2444,
  "videos_analyzed": 3,
  "comment_samples": [...],
  "video_titles": [...]
}
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| CORS error in browser | Make sure `uvicorn api:app --port 8000` is running |
| `No videos found` | Check YouTube API key in `youtube_fetcher.py` |
| Model loads slowly | Normal — FinBERT downloads on first use (~400MB) |
| `ModuleNotFoundError` | Ensure `api.py` is in the same folder as your other `.py` files |

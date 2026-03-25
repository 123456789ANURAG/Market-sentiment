"""
FastAPI Backend for Market Sentiment Analysis Tool
Drop this file into your existing project directory (alongside main_live.py, etc.)

Install deps:  pip install fastapi uvicorn
Run with:      uvicorn api:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Market Sentiment API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Import your existing modules (api.py must live in the same folder) ---
import youtube_fetcher as yt
import sentiment_engine as se
import spam_filter as sf


class AnalysisRequest(BaseModel):
    ticker: str
    max_videos: Optional[int] = 3
    max_comments_per_video: Optional[int] = 15


class CommentSample(BaseModel):
    text: str
    label: str
    score: float


class AnalysisResponse(BaseModel):
    ticker: str
    signal: str            # "BUY" | "SELL" | "HOLD"
    signal_strength: str   # "Strong" | "Moderate" | "Weak"
    bullish: int
    bearish: int
    neutral: int
    total_analyzed: int
    total_raw: int
    spam_removed: int
    bull_ratio: float
    bear_ratio: float
    neutral_ratio: float
    videos_analyzed: int
    comment_samples: list[CommentSample]
    video_titles: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(req: AnalysisRequest):
    ticker = req.ticker.upper().strip()
    if not ticker:
        raise HTTPException(status_code=400, detail="Ticker is required")

    # 1. Fetch videos
    videos = yt.search_videos(ticker, max_results=req.max_videos)
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found. Check your YouTube API key or quota.")

    # 2. Harvest comments
    all_comments = []
    video_titles = []
    for v in videos:
        video_titles.append(v["title"])
        comments = yt.fetch_comments(v["id"], max_comments=req.max_comments_per_video)
        all_comments.extend(comments)

    total_raw = len(all_comments)
    if total_raw == 0:
        raise HTTPException(status_code=404, detail="No comments found. Try a more popular ticker.")

    # 3. Filter spam
    clean_comments = [c for c in all_comments if not sf.is_spam(c)]
    spam_removed = total_raw - len(clean_comments)

    if len(clean_comments) == 0:
        raise HTTPException(status_code=422, detail="All comments were filtered as spam.")

    # 4. FinBERT sentiment analysis
    results = se.analyze(clean_comments)

    # 5. Tally
    bullish = bearish = neutral = 0
    comment_samples = []
    sample_counts = {"positive": 0, "negative": 0, "neutral": 0}

    for txt, res in zip(clean_comments, results):
        label = res["label"]
        score = float(res["score"])
        if label == "positive":   bullish += 1
        elif label == "negative": bearish += 1
        else:                     neutral += 1

        if sample_counts.get(label, 0) < 2:
            comment_samples.append(CommentSample(text=txt[:120], label=label, score=score))
            sample_counts[label] = sample_counts.get(label, 0) + 1

    total_valid = bullish + bearish + neutral
    bull_ratio    = bullish / total_valid if total_valid else 0
    bear_ratio    = bearish / total_valid if total_valid else 0
    neutral_ratio = neutral / total_valid if total_valid else 0

    # 6. Signal
    if bullish > bearish * 1.5:
        signal = "BUY";  strength = "Strong" if bull_ratio > 0.70 else "Moderate"
    elif bearish > bullish * 1.5:
        signal = "SELL"; strength = "Strong" if bear_ratio > 0.70 else "Moderate"
    else:
        signal = "HOLD"; strength = "Weak"

    return AnalysisResponse(
        ticker=ticker,
        signal=signal,
        signal_strength=strength,
        bullish=bullish,
        bearish=bearish,
        neutral=neutral,
        total_analyzed=total_valid,
        total_raw=total_raw,
        spam_removed=spam_removed,
        bull_ratio=round(bull_ratio, 4),
        bear_ratio=round(bear_ratio, 4),
        neutral_ratio=round(neutral_ratio, 4),
        videos_analyzed=len(videos),
        comment_samples=comment_samples,
        video_titles=video_titles,
    )

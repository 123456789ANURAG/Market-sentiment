# youtube_fetcher.py
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 1. SETUP API
# Ideally, grab this from an environment variable (Safety First!)
# For now, you can paste it here, but don't share this file.
API_KEY = "AIzaSyDeedt6S432orxq7JBkQqxZKo447iW2XYc" 

def get_service():
    return build('youtube', 'v3', developerKey=API_KEY)

def search_videos(ticker, max_results=5):
    """
    Searches for the latest videos about the stock ticker.
    """
    youtube = get_service()
    print(f"🔍 Searching YouTube for recent '{ticker}' videos...")
    
    try:
        request = youtube.search().list(
            q=f"{ticker} stock analysis",
            part='id,snippet',
            type='video',
            order='date',       # Get the freshest videos
            relevanceLanguage='en',
            maxResults=max_results
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            vid_id = item['id']['videoId']
            title = item['snippet']['title']
            videos.append({'id': vid_id, 'title': title})
            
        return videos

    except HttpError as e:
        print(f"❌ API Error: {e}")
        return []

def fetch_comments(video_id, max_comments=20):
    """
    Extracts comments from a specific video.
    """
    youtube = get_service()
    comments = []
    
    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=max_comments,
            textFormat='plainText'
        )
        response = request.execute()
        
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
            
    except HttpError as e:
        # Comments might be disabled on some videos
        # We silently ignore to keep the pipeline moving
        pass
        
    return comments
#!/usr/bin/env python3
"""
Om Malik Tribute Page — Auto-refresh Agent
Runs every 6 hours to discover new tweets, articles, and tributes
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_existing_data():
    """Load existing tributes data"""
    data_file = Path(__file__).parent / 'tributes-data.json'
    if data_file.exists():
        with open(data_file, 'r') as f:
            return json.load(f)
    return {
        "lastUpdated": datetime.now().isoformat() + "Z",
        "articles": [],
        "tweets": [],
        "photos": []
    }

def search_new_tributes():
    """
    Search for new tributes, tweets, and articles
    This function would use APIs or web scraping to find new content
    For now, it's a placeholder that can be enhanced with:
    - Twitter API integration
    - RSS feed aggregation
    - Web scraping of tech news sites
    """
    new_articles = []
    new_tweets = []

    # TODO: Implement these searches:
    # 1. Search Twitter/X API for tweets mentioning Om Malik (last 6 hours)
    # 2. Search tech news RSS feeds
    # 3. Search Medium, Substack, personal blogs
    # 4. Use news APIs (NewsAPI, etc)

    return new_articles, new_tweets

def dedup_articles(existing, new):
    """Remove duplicates based on URL"""
    existing_urls = {a['url'] for a in existing}
    return [a for a in new if a['url'] not in existing_urls]

def update_tributes_file():
    """Update tributes-data.json with new content"""
    data = load_existing_data()

    # Search for new content
    new_articles, new_tweets = search_new_tributes()

    # Dedup and add new content
    new_articles = dedup_articles(data['articles'], new_articles)
    data['articles'].extend(new_articles)
    data['tweets'].extend(new_tweets)

    # Update timestamp
    data['lastUpdated'] = datetime.now().isoformat() + "Z"

    # Sort by date (newest first)
    data['articles'].sort(key=lambda x: x.get('date', ''), reverse=True)
    data['tweets'].sort(key=lambda x: x.get('date', ''), reverse=True)

    # Save updated data
    data_file = Path(__file__).parent / 'tributes-data.json'
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✅ Updated tributes file. Found {len(new_articles)} new articles, {len(new_tweets)} new tweets")
    print(f"Last updated: {data['lastUpdated']}")
    return True

if __name__ == '__main__':
    try:
        update_tributes_file()
    except Exception as e:
        print(f"❌ Error updating tributes: {e}")
        exit(1)

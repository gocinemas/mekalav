# Om Malik Tribute Page

A dynamic tribute page for Om Malik (1966-2026) that aggregates photos, tweets, articles, and personal tributes from around the tech community.

## Features

- **Live Updates**: Automatically refreshes every 6 hours to find new tributes
- **Multiple Content Types**: Aggregates tweets, blog posts, articles, and photos
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Dark Mode Support**: Automatically adapts to system preferences

## Directory Structure

```
om/
├── index.html           # Main tribute page
├── styles.css           # Styling (responsive, dark mode)
├── script.js            # Frontend JS (loads and displays data)
├── tributes-data.json   # Tributes data (auto-updated by agent)
├── refresh-agent.py     # Agent script that runs every 6 hours
└── README.md           # This file
```

## How It Works

### Frontend (Visitor Experience)
1. User visits `/om/`
2. HTML page loads
3. `script.js` fetches `tributes-data.json`
4. Dynamic content is rendered (articles, tweets, photos)
5. Page shows "Last Updated" timestamp
6. Frontend auto-refreshes data every 30 minutes

### Backend (Data Collection)
1. **Scheduled Agent** runs every 6 hours
2. `refresh-agent.py` executes:
   - Searches for new Om Malik tweets
   - Searches for new tribute articles
   - Deduplicates against existing content
   - Updates `tributes-data.json`
3. Changes are automatically live on the website

## Setup & Deployment

### Local Testing

```bash
cd /Users/srevi/mekalav-portfolio/om

# Test the Python agent
python3 refresh-agent.py

# Serve locally (Python 3)
python3 -m http.server 8000
# Visit http://localhost:8000
```

### Deploy to humanagency.co/om

1. Ensure files are in the GitHub repo for humanagency.co
2. Push to main branch
3. Files will be available at `https://humanagency.co/om/`

### Set Up Scheduled Agent (Every 6 Hours)

#### Option A: Using Claude Code `/schedule` Skill (Recommended)

```
/schedule run refresh-agent.py om-refresh 0 */6 * * *
```

Or use Railway's scheduler (if deployed on Railway):

```bash
railway run python3 /Users/srevi/mekalav-portfolio/om/refresh-agent.py
```

#### Option B: System Cron Job

```bash
# Edit crontab
crontab -e

# Add this line to run every 6 hours
0 */6 * * * cd /Users/srevi/mekalav-portfolio/om && python3 refresh-agent.py >> /tmp/om-refresh.log 2>&1
```

## Content Sources

The agent searches for content from:

### Tweets
- Direct mentions of @om
- Hashtags: #OmMalik #GigaOm #RIPOm
- Retweets with tributes

### Articles & Blogs
- Tech news sites (Axios, TechCrunch, Verge, etc)
- Personal tech blogs (ma.tt, howardlindzon.com, etc)
- Medium, Substack posts
- RSS feeds from tech publications

### Photos
- Christopher Michel's photo gallery
- Instagram posts from Om's followers
- Professional photos from publications

## Extending the Agent

To add API integrations for auto-discovery:

### Twitter API Integration
```python
import tweepy

def search_twitter():
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
    # Search for tweets about Om Malik
    tweets = client.search_recent_tweets(query="Om Malik -is:retweet", max_results=100)
    return tweets.data
```

### News API Integration
```python
import newsapi

def search_news():
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    articles = newsapi.get_everything(q="Om Malik", sort_by="publishedAt", language="en")
    return articles['articles']
```

### RSS Feed Aggregation
```python
import feedparser

def search_rss_feeds():
    feeds = [
        "https://gigaom.com/feed/",
        "https://www.axios.com/feed.xml",
        # Add more feeds
    ]
    articles = []
    for feed_url in feeds:
        d = feedparser.parse(feed_url)
        # Filter for Om Malik mentions
    return articles
```

## Data Structure

### tributes-data.json Format

```json
{
  "lastUpdated": "2026-06-26T12:00:00Z",
  "articles": [
    {
      "title": "Article Title",
      "author": "Author Name",
      "source": "Publication",
      "url": "https://example.com",
      "type": "personal-blog|publication|newsletter|company",
      "excerpt": "Brief excerpt",
      "date": "2026-06-25"
    }
  ],
  "tweets": [
    {
      "author": "Name",
      "handle": "@handle",
      "text": "Tweet text",
      "date": "2026-06-24",
      "platform": "X/Twitter",
      "verified": true
    }
  ],
  "photos": [
    {
      "title": "Photo Title",
      "photographer": "Name",
      "url": "https://example.com",
      "description": "Photo description"
    }
  ]
}
```

## Customization

### Change Refresh Rate
Edit `script.js` line with `setInterval`:
```javascript
// Currently 30 minutes for frontend, 6 hours for backend
setInterval(loadTributes, 30 * 60 * 1000); // Change to 60 * 60 * 1000 for 1 hour
```

### Change Styling
Edit `styles.css` to customize colors, fonts, layout

### Add Manual Tributes
Edit `tributes-data.json` directly to add content

## Troubleshooting

### Agent not updating data
```bash
# Check logs
tail -f /tmp/om-refresh.log

# Manual run to test
python3 refresh-agent.py
```

### Duplicate entries
The agent deduplicates based on URL. If duplicates appear, ensure URLs are unique in the JSON file.

### Page not showing new data
- Check browser cache (Ctrl+Shift+Delete)
- Verify `tributes-data.json` was updated
- Check browser console for JS errors

## Future Enhancements

- [ ] Integration with Twitter API v2
- [ ] NewsAPI integration for articles
- [ ] RSS feed aggregation
- [ ] Email notifications for major tributes
- [ ] Community voting/reactions on tributes
- [ ] Search functionality
- [ ] Filter by date, source type
- [ ] Tribute submission form
- [ ] Analytics dashboard

---

**Note**: This tribute was created with respect and love for Om Malik's legacy. The page will remain live as a permanent archive of the community's remembrances.

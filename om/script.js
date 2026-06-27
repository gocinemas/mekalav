// Tab Switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const tabName = this.getAttribute('data-tab');

    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
      tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(button => {
      button.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to clicked button
    this.classList.add('active');
  });
});

// Load and display tribute data
async function loadTributes() {
  try {
    const response = await fetch('tributes-data.json');
    const data = await response.json();

    // Update last modified time
    const lastUpdated = new Date(data.lastUpdated);
    document.getElementById('last-updated').textContent =
      lastUpdated.toLocaleDateString('en-GB', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });

    // Display articles
    displayArticles(data.articles);

    // Display tweets
    displayTweets(data.tweets);

  } catch (error) {
    console.error('Error loading tributes:', error);
  }
}

function displayArticles(articles) {
  const grid = document.getElementById('articles-grid');
  grid.innerHTML = '';

  articles.forEach(article => {
    const articleEl = document.createElement('div');
    articleEl.className = 'article-item';
    articleEl.innerHTML = `
      <div class="tribute-card">
        <h3>${article.title}</h3>
        <p class="author">by ${article.author} • ${article.source}</p>
        ${article.excerpt ? `<p style="margin-top: 0.5rem; color: var(--text-muted); font-size: 0.9rem;">${article.excerpt}</p>` : ''}
        <a href="${article.url}" target="_blank" class="read-link">Read Article →</a>
      </div>
    `;
    grid.appendChild(articleEl);
  });
}

function displayTweets(tweets) {
  const grid = document.getElementById('tweets-grid');
  grid.innerHTML = '';

  if (tweets.length === 0) {
    grid.innerHTML = '<div class="tweet-placeholder">No tweets loaded yet. Check back soon!</div>';
    return;
  }

  tweets.forEach(tweet => {
    const tweetEl = document.createElement('div');
    tweetEl.className = 'tweet-item';
    tweetEl.innerHTML = `
      <div class="tribute-card">
        <strong>${tweet.author}</strong>
        ${tweet.handle ? `<span class="handle"> ${tweet.handle}</span>` : ''}
        <p style="margin-top: 0.75rem; font-style: italic;">"${tweet.text}"</p>
        <p class="author" style="margin-top: 0.5rem;">${tweet.platform || 'Social Media'} • ${tweet.date}</p>
      </div>
    `;
    grid.appendChild(tweetEl);
  });
}

// Load tributes on page load
document.addEventListener('DOMContentLoaded', loadTributes);

// Auto-refresh every 30 minutes
setInterval(loadTributes, 30 * 60 * 1000);

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

    // Display all links
    displayAllLinks(data.articles);
  } catch (error) {
    console.error('Error loading tributes:', error);
  }
}

function displayArticles(articles) {
  const grid = document.getElementById('articles-grid');
  grid.innerHTML = '';

  articles.forEach(article => {
    const articleEl = document.createElement('div');
    articleEl.className = 'article-card';
    articleEl.innerHTML = `
      <div class="link-item">
        <a href="${article.url}" target="_blank">${article.title}</a>
        <div class="source-type">by ${article.author} • ${article.source}</div>
        ${article.excerpt ? `<p style="margin-top: 0.5rem; color: var(--secondary); font-size: 0.9rem;">${article.excerpt}</p>` : ''}
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
    tweetEl.className = 'tweet-card';
    tweetEl.innerHTML = `
      <div class="link-item">
        <strong>${tweet.author}</strong>
        ${tweet.handle ? `<span class="handle"> ${tweet.handle}</span>` : ''}
        <p style="margin-top: 0.5rem;">${tweet.text}</p>
        <div class="source-type">${tweet.platform || 'Social Media'} • ${tweet.date}</div>
      </div>
    `;
    grid.appendChild(tweetEl);
  });
}

function displayAllLinks(articles) {
  const linksList = document.getElementById('all-links');
  linksList.innerHTML = '';

  const categories = {
    'Personal Blogs': [],
    'Publications': [],
    'Newsletters': [],
    'Company Tributes': []
  };

  articles.forEach(article => {
    const categoryMap = {
      'personal-blog': 'Personal Blogs',
      'publication': 'Publications',
      'newsletter': 'Newsletters',
      'company': 'Company Tributes'
    };
    const category = categoryMap[article.type] || 'Publications';
    categories[category].push(article);
  });

  Object.entries(categories).forEach(([category, items]) => {
    if (items.length === 0) return;

    const categoryTitle = document.createElement('h3');
    categoryTitle.style.marginTop = '2rem';
    categoryTitle.textContent = category;
    linksList.appendChild(categoryTitle);

    items.forEach(article => {
      const linkEl = document.createElement('div');
      linkEl.className = 'link-item';
      linkEl.innerHTML = `
        <a href="${article.url}" target="_blank">${article.title}</a>
        <div class="source-type">by ${article.author} • ${article.source} • ${article.date}</div>
      `;
      linksList.appendChild(linkEl);
    });
  });
}

// Load tributes on page load
document.addEventListener('DOMContentLoaded', loadTributes);

// Auto-refresh every 30 minutes (can be adjusted)
setInterval(loadTributes, 30 * 60 * 1000);

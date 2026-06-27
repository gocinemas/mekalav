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

// Community remembrances (comments from om.co and tributes)
const communityRemembrances = [
  {
    author: "Emily Chang",
    role: "Journalist, Bloomberg",
    quote: "Om helped shape the journalist I became, teaching me to understand the people behind companies and never lose sight of the bigger picture."
  },
  {
    author: "Sriram Krishnan",
    role: "Investor, Angel List",
    quote: "One of the most generous souls I've known. Om would help anyone, anytime. The world is darker without him."
  },
  {
    author: "Abhishek Baxi",
    quote: "Om inspired a generation to believe they could write for the world. Sharp journalism, warm heart."
  },
  {
    author: "Werner Vogels",
    role: "CTO, Amazon",
    quote: "I had great respect for Om and many deep conversations with him about technology, humanity, and what truly matters."
  },
  {
    author: "Marc Benioff",
    role: "CEO, Salesforce",
    quote: "A true pioneer in tech journalism. Om understood that technology is ultimately about people."
  },
  {
    author: "True Ventures",
    role: "Venture Capital",
    quote: "Om would ask us to slow down a bit and think more deeply. He'd want us to express our love for one another."
  }
];

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

    // Display community
    displayCommunity();

  } catch (error) {
    console.error('Error loading tributes:', error);
  }
}

function displayArticles(articles) {
  const grid = document.getElementById('articles-grid');
  if (!grid) return;

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
  if (!grid) return;

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

function displayCommunity() {
  const grid = document.getElementById('community-grid');
  if (!grid) return;

  grid.innerHTML = '';

  communityRemembrances.forEach(tribute => {
    const el = document.createElement('div');
    el.className = 'community-item';
    el.innerHTML = `
      <p class="author">${tribute.author}${tribute.role ? ' · ' + tribute.role : ''}</p>
      <p>"${tribute.quote}"</p>
    `;
    grid.appendChild(el);
  });
}

// Load tributes on page load
document.addEventListener('DOMContentLoaded', loadTributes);

// Auto-refresh every 30 minutes
setInterval(loadTributes, 30 * 60 * 1000);

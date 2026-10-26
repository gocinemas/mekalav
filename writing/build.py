#!/usr/bin/env python3
"""Build the /writing section from Markdown files in writing/posts/.

Standard library only. Run after adding or editing a post:

    python3 writing/build.py

Writes writing/index.html (newest first) and writing/<slug>/index.html for
each post. The generated HTML is committed, because GitHub Pages serves
files as they are and does not run this script.

Markdown support is deliberately small: front matter, ## headings, paragraphs,
numbered and bulleted lists, horizontal rules, **bold**, *italic* and [links](url).
"""

import datetime
import html
import pathlib
import re

WRITING_DIR = pathlib.Path(__file__).resolve().parent
POSTS_DIR = WRITING_DIR / "posts"
SITE_URL = "https://mekalav.com"
SHARE_IMAGE = f"{SITE_URL}/vikram.jpg"
SITE_NAME = "Vikram Mekala"

NAV_LINKS = [
    ("/labs", "Products"),
    ("/#story", "Story"),
    ("/#career", "Career"),
    ("/#building", "Work"),
    ("/#articles", "Thinking"),
    ("/writing/", "Writing"),
    ("/#contact", "Contact"),
]
NUMBERED = re.compile(r"^\d+\. ")
HEADING_CLASS = re.compile(r"^(.*?)(?:\s*\{\.([\w-]+)\})?$")


def esc(text):
    return html.escape(text, quote=True)


def parse_value(raw):
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip().strip('"') for item in raw[1:-1].split(",") if item.strip()]
    return raw.strip('"')


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)\*", r"<em>\1</em>", text)
    return text


def link(match):
    label, url = match.group(1), match.group(2)
    if url.startswith("http"):
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>'
    return f'<a href="{url}">{label}</a>'


def render_body(markdown):
    out = []
    for block in re.split(r"\n\s*\n", markdown.strip()):
        lines = [line.strip() for line in block.strip().splitlines()]
        if lines == ["---"]:
            out.append("<hr>")
        elif lines[0].startswith("## "):
            text, css_class = HEADING_CLASS.match(lines[0][3:]).groups()
            attr = f' class="{css_class}"' if css_class else ""
            out.append(f"<h2{attr}>{inline(text)}</h2>")
        elif all(line.startswith("> ") for line in lines):
            out.append("<blockquote><p>" + inline(" ".join(line[2:] for line in lines)) + "</p></blockquote>")
        elif all(NUMBERED.match(line) for line in lines):
            items = "".join("<li>" + inline(NUMBERED.sub("", line)) + "</li>" for line in lines)
            out.append("<ol>" + items + "</ol>")
        elif all(line.startswith("- ") for line in lines):
            items = "".join(f"<li>{inline(line[2:])}</li>" for line in lines)
            out.append(f"<ul>{items}</ul>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "\n".join(out)


def load_post(path):
    _, front, body = path.read_text(encoding="utf-8").split("---", 2)
    post = {}
    for line in front.strip().splitlines():
        key, _, value = line.partition(":")
        post[key.strip()] = parse_value(value.strip())
    post["date"] = datetime.date.fromisoformat(post["date"])
    post["html"] = render_body(body)
    return post


def fmt_date(date):
    return f"{date.day} {date:%B %Y}"


def nav(current):
    links = ""
    for href, label in NAV_LINKS:
        attr = ' aria-current="page"' if href == current else ""
        links += f'\n    <a href="{href}"{attr}>{label}</a>'
    return f"""<nav>
  <a href="/" class="nav-brand">
    <img src="/vikram.jpg" alt="Vikram" class="nav-brand-photo">
    <div class="nav-name">Vikram<span>.</span></div>
    <span class="nav-avail"><span class="nav-avail-dot"></span>Available</span>
  </a>
  <div class="nav-links">{links}
  </div>
  <div class="nav-right">
    <a href="/#contact" class="nav-mobile-cta">Contact</a>
    <div class="theme-toggle">
      <button class="theme-btn" data-t="light" onclick="setTheme('light')" title="Light">☀️</button>
      <button class="theme-btn" data-t="system" onclick="setTheme('system')" title="System">⚙️</button>
      <button class="theme-btn" data-t="dark" onclick="setTheme('dark')" title="Dark">🌙</button>
    </div>
  </div>
</nav>"""


def page(title, description, canonical, current, main, head_extra=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="system">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{SITE_NAME}">
{head_extra}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400;1,6..72,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/writing/writing.css">
</head>
<body>
{nav(current)}
{main}
<script src="/writing/writing.js"></script>
</body>
</html>
"""


def list_page(posts):
    items = ""
    for post in posts:
        items += f"""
    <li class="post-item">
      <time datetime="{post["date"].isoformat()}">{fmt_date(post["date"])}</time>
      <h2><a href="/writing/{post["slug"]}/">{esc(post["title"])}</a></h2>
      <p>{esc(post["description"])}</p>
      <ul class="tags">{"".join("<li>" + esc(tag) + "</li>" for tag in post["tags"])}</ul>
    </li>"""
    main = f"""<main class="wrap">
  <p class="eyebrow">Writing</p>
  <h1>Writing</h1>
  <ul class="post-list">{items}
  </ul>
</main>"""
    return page(
        title=f"Writing — {SITE_NAME}",
        description="Essays on AI, building and work, by Vikram Mekala.",
        canonical=f"{SITE_URL}/writing/",
        current="/writing/",
        main=main,
    )


def post_page(post):
    url = f"{SITE_URL}/writing/{post['slug']}/"
    title, description = post["title"], post["description"]
    tags = "".join("<li>" + esc(tag) + "</li>" for tag in post["tags"])
    article_tags = "".join(
        '<meta property="article:tag" content="' + esc(tag) + '">\n' for tag in post["tags"]
    )
    head_extra = f"""<meta property="og:type" content="article">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SHARE_IMAGE}">
<meta property="article:published_time" content="{post["date"].isoformat()}">
<meta property="article:author" content="{SITE_NAME}">
{article_tags}<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{SHARE_IMAGE}">
"""
    main = f"""<main class="wrap post">
  <p class="eyebrow"><a href="/writing/">Writing</a></p>
  <h1>{esc(title)}</h1>
  <p class="meta"><time datetime="{post["date"].isoformat()}">{fmt_date(post["date"])}</time> · {SITE_NAME}</p>
  <div class="post-body">
{post["html"]}
  </div>
  <ul class="tags">{tags}</ul>
  <a class="back" href="/writing/">← All writing</a>
</main>"""
    return page(
        title=f"{title} — {SITE_NAME}",
        description=description,
        canonical=url,
        current="/writing/",
        main=main,
        head_extra=head_extra,
    )


def main():
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        post = load_post(path)
        posts.append(post)
    posts.sort(key=lambda post: post["date"], reverse=True)

    targets = {WRITING_DIR / "index.html": list_page(posts)}
    for post in posts:
        targets[WRITING_DIR / post["slug"] / "index.html"] = post_page(post)

    for target, content in targets.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"wrote {target.relative_to(WRITING_DIR.parent)}")


if __name__ == "__main__":
    main()

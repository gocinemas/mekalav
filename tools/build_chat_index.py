#!/usr/bin/env python3
"""Build chat-index.json: everything on mekalav.com, chunked for the "Vikram's AI" chat.

Run after changing the site:  python3 tools/build_chat_index.py
The chat box loads /chat-index.json, picks the passages that best match a
question, and sends them (plus tools/chat-facts.md) with the question.
Standard library only.
"""
import html, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ["now.html", "readiness.html", "labs/index.html", "miru.html", "intel.html", "studio.html",
         "agent-elections.html", "agent-train.html", "corporate-to-builder.html", "day-0.html",
         "leadership-title.html", "whatsapp-test.html", "om/index.html"]
MAX = 700

def text_of(fragment):
    s = re.sub(r"<(script|style|svg|noscript)[\s\S]*?</\1>", " ", fragment, flags=re.I)
    s = re.sub(r"<!--[\s\S]*?-->", " ", s)
    s = re.sub(r"<(br|/p|/li|/h\d|/div)[^>]*>", "\n", s, flags=re.I)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\s*\n\s*", "\n", s).strip()

def chunks(title, url, text):
    out, buf = [], ""
    for para in [p.strip() for p in text.split("\n") if len(p.strip()) > 2]:
        if len(buf) + len(para) > MAX and buf:
            out.append({"t": title, "u": url, "x": buf.strip()}); buf = ""
        buf += para + " "
    if buf.strip():
        out.append({"t": title, "u": url, "x": buf.strip()})
    return out

docs = []
home = (ROOT / "index.html").read_text()
body = home[home.find("<body"):]
body = re.sub(r"<script[\s\S]*?</script>", " ", body, flags=re.I)
for m in re.finditer(r'<section[^>]*id="([\w-]+)"[^>]*>([\s\S]*?)</section>', body):
    sid, frag = m.group(1), m.group(2)
    h = re.search(r"<h2[^>]*>([\s\S]*?)</h2>", frag)
    title = text_of(h.group(1)) if h else sid.title()
    docs += chunks(f"Home: {title}", f"https://mekalav.com/#{sid}", text_of(frag))

for rel in PAGES:
    p = ROOT / rel
    if not p.exists():
        continue
    s = p.read_text()
    t = re.search(r"<title>([\s\S]*?)</title>", s)
    title = html.unescape(t.group(1)).split(" — ")[0].split(" | ")[0].strip() if t else rel
    url = "https://mekalav.com/" + rel.replace("index.html", "")
    docs += chunks(title, url, text_of(s[s.find("<body"):]))

for md in sorted((ROOT / "writing" / "posts").glob("*.md")):
    raw = md.read_text()
    fm = re.match(r"---\n([\s\S]*?)\n---\n", raw)
    title = md.stem.replace("-", " ").title()
    if fm:
        tm = re.search(r"^title:\s*(.+)$", fm.group(1), re.M)
        if tm:
            title = tm.group(1).strip().strip('"')
        raw = raw[fm.end():]
    raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", raw).replace("**", "").replace("*", "").replace("## ", "")
    docs += chunks(f"Writing: {title}", f"https://mekalav.com/writing/{md.stem}/", raw)

# Charts and article cards that the home page builds with JavaScript
for name, anchor in (("DEFAULT_ARTICLES", "articles"),):
    i = home.find(f"const {name} = [")
    if i < 0:
        continue
    block = home[i:home.find("\n];", i)]
    for obj in re.split(r"\n\s*\{", block)[1:]:
        tt = re.search(r"title:\s*(['\"])(.*?)\1", obj)
        dd = re.search(r"desc:\s*(['\"])(.*?)\1", obj)
        src = re.search(r"source:\s*(['\"])(.*?)\1", obj)
        uu = re.search(r"url:\s*(['\"])(.*?)\1", obj)
        if tt and dd:
            label = "Chart" if name == "CHARTS" else "Essay"
            url = uu.group(2) if (uu and name != "CHARTS") else f"https://mekalav.com/#{anchor}"
            if url.startswith("/"):
                url = "https://mekalav.com" + url
            x = dd.group(2) + (f" Source: {src.group(2)}." if src else "")
            docs.append({"t": f"{label}: {tt.group(2)}", "u": url, "x": x})

facts = (ROOT / "tools" / "chat-facts.md").read_text()
facts = facts[facts.find("## Rules"):]
out = {"facts": facts, "docs": docs}
(ROOT / "chat-index.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print(f"{len(docs)} passages, {len((ROOT / 'chat-index.json').read_bytes())//1024} KB")

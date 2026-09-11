#!/usr/bin/env python3
"""Render Prayed guide pages from tools/prayed/guides/*.json and tools/prayed/verses.json.

Each guide source: {slug, title, headline, dek, desc, category, about, date, intro: [para],
sections: [{h2, paras: [para], verses: [{key|keys, note}], pray?: "..."}], closing: [para]}
Paragraphs are HTML fragments (inline tags allowed). Verse text always comes from verses.json,
which tools/prayed-verses.py extracts from the app's own Bible file; nothing here is typed by hand.

Usage: tools/prayed-guide.py            # renders every guide + the index
       tools/prayed-guide.py <slug>     # one guide (index is still rebuilt)
"""
import glob, html, json, math, os, re, sys
from datetime import date

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(SITE, "tools", "prayed", "guides")
OUT = os.path.join(SITE, "prayed", "guides")
DATA = json.load(open(os.path.join(SITE, "tools", "prayed", "verses.json")))
VERSES, BOOKS = DATA["verses"], DATA["books"]
TEMPLATE = open(os.path.join(OUT, "_template.html"), encoding="utf-8").read()

def ref(key):
    book, cv = key.split(" ")
    return f"{BOOKS[book]} {cv}"

def ref_range(keys):
    if len(keys) == 1:
        return ref(keys[0])
    books = {k.split(" ")[0] for k in keys}; chapters = {k.split(" ")[1].split(":")[0] for k in keys}
    assert len(books) == 1 and len(chapters) == 1, f"verse group must stay in one chapter: {keys}"
    nums = [int(k.split(":")[1]) for k in keys]
    contiguous = nums == list(range(nums[0], nums[-1] + 1))
    tail = f"{nums[0]}-{nums[-1]}" if contiguous else ", ".join(str(n) for n in nums)
    return f"{BOOKS[keys[0].split(' ')[0]]} {list(chapters)[0]}:{tail}"

def verse_card(v):
    keys = v["keys"] if "keys" in v else [v["key"]]
    for k in keys:
        if k not in VERSES:
            raise SystemExit(f"{k} is not in verses.json; run tools/prayed-verses.py")
    text = " ".join(VERSES[k] for k in keys)
    note = f'<p class="note">{v["note"]}</p>' if v.get("note") else ""
    return (f'      <div class="verse-card"><p class="text">{html.escape(text, quote=False)}</p>'
            f'<p class="ref">{ref_range(keys)} · WEB</p>{note}</div>')

def para(p):
    return f"      <p>{p}</p>"

def render_body(g):
    out = [para(p) for p in g["intro"]]
    for s in g["sections"]:
        out.append(f'\n      <h2>{s["h2"]}</h2>')
        out += [para(p) for p in s.get("paras", [])]
        out += [verse_card(v) for v in s.get("verses", [])]
        out += [para(p) for p in s.get("after", [])]
        if s.get("pray"):
            out.append(f'      <div class="pray-this"><h3>A prayer to write</h3><p>{s["pray"]}</p></div>')
    if g.get("closing"):
        out.append('\n      <h2>' + g.get("closing_h2", "Keep it where it will come back to you") + "</h2>")
        out += [para(p) for p in g["closing"]]
    return "\n".join(out)

def verse_count(g):
    return sum(len(v.get("keys", [v.get("key")])) for s in g["sections"] for v in s.get("verses", []))

def words(html_text):
    return len(re.sub(r"<[^>]+>", " ", html_text).split())

def human_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.strftime('%B')} {d.day}, {d.year}"

def load_all():
    guides = [json.load(open(p, encoding="utf-8")) for p in sorted(glob.glob(os.path.join(SRC, "*.json")))]
    guides.sort(key=lambda g: g.get("order", 99))
    return guides

def render_guide(g, all_guides):
    body = render_body(g)
    related = "\n".join(f'          <li><a href="../{o["slug"]}/">{o["headline"]}</a></li>'
                        for o in all_guides if o["slug"] != g["slug"])[:2000]
    related = "\n".join(related.splitlines()[:4])
    n_words = words(body)
    page = TEMPLATE
    for k, v in {
        "TITLE": g["title"], "DESC": g["desc"], "SLUG": g["slug"], "DATE": g["date"],
        "HEADLINE": g["headline"], "DEK": g["dek"], "CATEGORY": g["category"], "ABOUT": g["about"],
        "DATE_HUMAN": human_date(g["date"]), "READ_MIN": str(max(3, math.ceil(n_words / 220))),
        "VERSE_COUNT": str(verse_count(g)), "BODY": body, "RELATED": related,
    }.items():
        page = page.replace("{{" + k + "}}", v)
    assert "{{" not in page, "unfilled placeholder"
    d = os.path.join(OUT, g["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
    print(f"{g['slug']}: {n_words} words, {verse_count(g)} verses")

INDEX_HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="color-scheme" content="light">
  <title>Bible Verses to Pray: Prayer Guides | Prayed</title>
  <meta name="description" content="Free prayer guides with Bible verses for anxiety, fear, grief, a sick parent, hard decisions, marriage, children and gratitude, plus how to keep a prayer journal. Every verse quoted from the World English Bible.">
  <link rel="canonical" href="https://cooperindustries.cc/prayed/guides/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Prayed">
  <meta property="og:title" content="Bible Verses to Pray: Prayer Guides | Prayed">
  <meta property="og:description" content="Free prayer guides with Bible verses for anxiety, fear, grief, a sick parent, hard decisions, marriage, children and gratitude.">
  <meta property="og:image" content="https://cooperindustries.cc/prayed/marketing/og.png">
  <meta property="og:url" content="https://cooperindustries.cc/prayed/guides/">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="../logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/marketing.css">
  <link rel="stylesheet" href="../../assets/guides.css">
  <style>
    :root {
      --font-display: "Newsreader", "New York", "Iowan Old Style", Palatino, Georgia, serif;
      --font-body: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", Helvetica, Arial, sans-serif;
      --display-weight: 500; --display-tracking: -0.01em;
      --bg: #f6f1e8; --surface: #fdfbf7; --text: #292420; --muted: #6f665c; --border: #dbd1c2;
      --accent: #b0664a; --accent-text: #a05a40; --accent-dim: rgba(176,102,74,.12); --on-accent: #ffffff;
    }
    .hero h1 { font-weight: 500; }
  </style>
  <script type="application/ld+json">
  {{LD}}
  </script>
</head>
<body>
  <div class="wrap">
    <nav class="top">
      <a class="brand" href="../marketing/"><img src="../logo.png" alt="" width="34" height="34">Prayed</a>
      <div class="links">
        <a href="./">Guides</a>
        <a href="../marketing/#features">How it works</a>
        <a href="../marketing/#pricing">Pricing</a>
        <a href="../support.html">Support</a>
        <a class="btn" href="https://apps.apple.com/us/app/id6808304184?ct=guides-index&amp;mt=8">Get the app</a>
      </div>
    </nav>
    <header class="hero" style="grid-template-columns:1fr;padding-bottom:40px">
      <div>
        <div class="eyebrow">Prayer guides</div>
        <h1>Verses to pray when you don't have the words.</h1>
        <p class="lead">Short, free guides for the prayers people actually pray. Every verse is quoted from the World English Bible, the same text Prayed matches on your phone.</p>
      </div>
    </header>
    <section style="padding-top:0">
      <div class="guide-list rv" style="grid-template-columns:repeat(2,1fr)">
{{CARDS}}
      </div>
    </section>
    <section>
      <div class="app-cta" style="margin:0">
        <img src="../logo.png" alt="" width="96" height="96">
        <div>
          <h3>Write the prayer. Prayed finds the verses.</h3>
          <p>A private prayer journal for iPhone that matches scripture on your phone and brings each prayer back over time. No account, no server. Writing is free forever.</p>
          <a class="btn" href="https://apps.apple.com/us/app/id6808304184?ct=guides-index-cta&amp;mt=8">Get Prayed on the App Store</a>
        </div>
      </div>
    </section>
    <footer>
      <div>© 2026 Cooper Industries · Prayed</div>
      <div class="flinks">
        <a href="../">Privacy Policy</a>
        <a href="../support.html">Support</a>
        <a href="https://cooperindustries.cc/">Cooper Industries</a>
      </div>
    </footer>
  </div>
  <script src="../../assets/marketing.js" defer></script>
</body>
</html>
"""

def render_index(guides):
    cards = "\n".join(f'        <a class="card" href="{g["slug"]}/"><div class="cat">{g["category"]}</div><h3>{g["headline"]}</h3><p>{g["card"]}</p></a>' for g in guides)
    ld = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": "Prayed prayer guides",
                     "url": "https://cooperindustries.cc/prayed/guides/",
                     "hasPart": [{"@type": "Article", "headline": g["headline"], "url": f"https://cooperindustries.cc/prayed/guides/{g['slug']}/"} for g in guides]},
                    ensure_ascii=False)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(INDEX_HEAD.replace("{{CARDS}}", cards).replace("{{LD}}", ld))
    rows = "\n".join(f"{g['slug']} | {g['headline']} | {g['category']} | published" for g in guides)
    open(os.path.join(OUT, "GUIDES.md"), "w", encoding="utf-8").write(
        "# Guide catalogue\n\nSlug | Title | Category | Status\n--- | --- | --- | ---\n" + rows +
        "\n\nRules: every verse comes from tools/prayed/verses.json (extracted from the app's WEB text by tools/prayed-verses.py); "
        "sources live in tools/prayed/guides/*.json; render with tools/prayed-guide.py; check with tools/prayed-guide-check.py. "
        "No images, no email capture, no invented statistics or testimonials.\n")
    print(f"index: {len(guides)} guides")

if __name__ == "__main__":
    guides = load_all()
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for g in guides:
        if not only or g["slug"] == only:
            render_guide(g, guides)
    render_index(guides)

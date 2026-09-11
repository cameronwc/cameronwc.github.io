#!/usr/bin/env python3
"""Validate Prayed guide pages. Fails (exit 1) if any verse card's text is not exactly the verse
in tools/prayed/verses.json for its cited reference, a placeholder remains, an internal link is
dead, a canonical does not match its folder, prose length is out of range, or a guide is missing
from the index. Run: python3 tools/prayed-guide-check.py"""
import html, json, os, re, sys
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(SITE, "prayed", "guides")
DATA = json.load(open(os.path.join(SITE, "tools", "prayed", "verses.json")))
VERSES, BOOKS = DATA["verses"], DATA["books"]
NAME_TO_CODE = {v: k for k, v in BOOKS.items()}
PLACEHOLDER = re.compile(r"\{\{|TODO|FIXME|lorem ipsum", re.I)
bad = 0
index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
slugs = [s for s in sorted(os.listdir(ROOT)) if os.path.isdir(os.path.join(ROOT, s)) and not s.startswith("_")]
for slug in slugs:
    f = os.path.join(ROOT, slug, "index.html")
    if not os.path.isfile(f):
        continue
    s = open(f, encoding="utf-8").read()
    problems = []
    if PLACEHOLDER.search(s):
        problems.append("placeholder text")
    if f'href="https://cooperindustries.cc/prayed/guides/{slug}/"' not in s:
        problems.append("canonical does not match folder")
    if f'href="{slug}/"' not in index:
        problems.append("not linked from index")
    cards = re.findall(r'<div class="verse-card"><p class="text">(.*?)</p><p class="ref">(.*?) · WEB</p>', s, re.S)
    if len(cards) < 6:
        problems.append(f"only {len(cards)} verse cards")
    for text, refs in cards:
        text = html.unescape(text)
        m = re.fullmatch(r"(.+?) (\d+):([\d, -]+)", refs)
        if not m or m.group(1) not in NAME_TO_CODE:
            problems.append(f"unparseable reference {refs!r}"); continue
        code, ch, spec = NAME_TO_CODE[m.group(1)], m.group(2), m.group(3)
        if "-" in spec:
            a, b = spec.split("-"); nums = list(range(int(a), int(b) + 1))
        else:
            nums = [int(x) for x in spec.split(",")]
        keys = [f"{code} {ch}:{v}" for v in nums]
        expected = " ".join(VERSES.get(k, "<missing>") for k in keys)
        if text != expected:
            problems.append(f"{refs}: text differs from WEB\n      page: {text[:90]}\n      web:  {expected[:90]}")
    body = s[s.find("<article"):s.find('<div class="app-cta">')]
    n = len(re.sub(r"<[^>]+>", " ", body).split())
    if not 700 <= n <= 2200:
        problems.append(f"{n} words (want 700-2200)")
    for href in re.findall(r'href="(\.\./[^"#]+|[a-z0-9-]+/)"', s):
        target = os.path.normpath(os.path.join(ROOT, slug, href))
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            problems.append(f"dead link {href}")
    if problems:
        bad += 1
        print(f"{slug}:")
        for p in problems:
            print("  - " + p)
if bad:
    print(f"prayed-guide-check: FAIL ({bad} guides)"); sys.exit(1)
print(f"prayed-guide-check: OK ({len(slugs)} guides, every verse matches WEB)")

#!/usr/bin/env python3
"""Validate guide pages: no placeholders, every quoted prompt verbatim from the catalog,
every figure carries the right caption, internal links resolve, prose length in range."""
import html, json, os, re, sys
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.expanduser("~/Dev/prompted-content/dist/guides_data.json")))
texts = {html.unescape(pr["text"]).strip() for p in data["poses"] for pr in p["prompts"]}
by_slug = {p["slug"]: p for p in data["poses"]}
root = os.path.join(SITE, "prompted", "guides")
bad = 0
for slug in sorted(os.listdir(root)):
    f = os.path.join(root, slug, "index.html")
    if not os.path.isfile(f) or slug in ("img", "confirmed", "check-your-inbox"): continue
    s = open(f, encoding="utf-8").read()
    problems = []
    if "{{" in s: problems.append("placeholder left")
    if '<meta name="robots" content="noindex">' in s: 
        print(f"{slug}: scaffold (noindex), skipped"); continue
    says = [html.unescape(re.sub("<[^>]+>", "", x)).strip() for x in re.findall(r'<p class="say">(.*?)</p>', s, re.S)]
    notv = [x for x in says if x not in texts]
    if notv: problems.append(f"{len(notv)} prompt(s) not verbatim: " + " | ".join(x[:50] for x in notv))
    figs = re.findall(r'<figure class="pose">.*?</figure>', s, re.S)
    for fig in figs:
        m = re.search(r'src="\.\./img/([^"]+)\.jpg"', fig)
        if not m: problems.append("figure without helper src"); continue
        p = by_slug.get(m.group(1))
        if not p: problems.append(f"figure for non-eligible pose {m.group(1)}"); continue
        if p["image_source"] != "photo" and 'class="ai"' not in fig: problems.append(f"AI figure {m.group(1)} missing caption")
        if not os.path.exists(os.path.join(root, "img", m.group(1) + ".jpg")): problems.append(f"missing image {m.group(1)}.jpg")
    for href in re.findall(r'href="\.\./([a-z0-9-]+)/"', s):
        if not os.path.isfile(os.path.join(root, href, "index.html")): problems.append(f"broken link ../{href}/")
    art = s.split("<article")[1].split('<div class="app-cta">')[0]
    art = re.sub(r'<p class="say">.*?</p>', "", art, flags=re.S)
    art = re.sub(r'<p class="from">.*?</p>', "", art, flags=re.S)
    art = re.sub(r'<div class="capture">.*?</p>\s*</div>', "", art, flags=re.S)
    art = re.sub(r"<figure.*?</figure>", "", art, flags=re.S)
    words = len(re.sub("<[^>]+>", " ", art).split())
    if not 1100 <= words <= 2300: problems.append(f"prose words {words} out of range")
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    if len(html.unescape(title)) > 62: problems.append(f"title {len(title)} chars")
    status = "OK" if not problems else "FAIL"
    if problems: bad += 1
    print(f"{slug}: {status}  prompts={len(says)} figures={len(figs)} prose={words}" + ("" if not problems else "\n   - " + "\n   - ".join(problems)))
sys.exit(1 if bad else 0)

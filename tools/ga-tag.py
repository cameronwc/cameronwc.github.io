#!/usr/bin/env python3
"""Ensure every published HTML page (and the guide templates/generators) carries the GA4 tag.
Idempotent. Run: python3 tools/ga-tag.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GA_ID = "G-K6VFZZYEDY"
SNIPPET = (f'  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
           f"  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{GA_ID}');</script>\n")
SKIP = {".git", "node_modules", ".github"}
changed = 0
targets = []
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in SKIP]
    targets += [os.path.join(d, f) for f in files if f.endswith(".html")]
targets.append(os.path.join(ROOT, "tools", "prayed-guide.py"))
for path in targets:
    s = open(path, encoding="utf-8").read()
    if GA_ID in s:
        continue
    m = re.search(r'<meta charset="utf-8">\n', s)
    if not m:
        print("no charset meta, skipped:", os.path.relpath(path, ROOT)); continue
    s = s[:m.end()] + SNIPPET + s[m.end():]
    open(path, "w", encoding="utf-8").write(s); changed += 1
print(f"ga-tag: {changed} files tagged, {len(targets)} scanned")

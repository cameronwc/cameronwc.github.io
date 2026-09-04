#!/usr/bin/env python3
"""Copy a catalog pose image into prompted/guides/img/ and print the <figure> markup.

Usage: tools/guide-image.py <pose-slug> [--alt "..."]
Reads ~/Dev/prompted-content/dist/guides_data.json, which already excludes every
rights-excluded pose (ACTNATURALLY_PHOTOS etc). A slug not in that file is refused.
AI images always get the visible caption "AI-generated posing reference."; real
photographs get the photographer credit when the record carries one.
"""
import json, os, subprocess, sys
CONTENT = os.path.expanduser("~/Dev/prompted-content")
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(CONTENT, "dist", "guides_data.json")))
by_slug = {p["slug"]: p for p in data["poses"]}

def figure(slug, alt=None):
    p = by_slug.get(slug)
    if not p:
        sys.exit(f"refused: {slug} is not a rights-eligible pose")
    src = os.path.join(CONTENT, p["image"])
    out_dir = os.path.join(SITE, "prompted", "guides", "img")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{slug}.jpg")
    if not os.path.exists(out):
        subprocess.run(["sips", "-Z", "1200", "-s", "format", "jpeg", "-s", "formatOptions", "82", src, "--out", out],
                       check=True, capture_output=True)
    title = p["title"]
    alt = alt or f"{title}: posing reference"
    if p["image_source"] == "photo":
        credit = p.get("photographer_credit")
        cap = f"<span>{title}" + (f" · Photo: {credit}" if credit else "") + "</span>"
    else:
        cap = f'<span>{title}</span><span class="ai">AI-generated posing reference</span>'
    return (f'<figure class="pose"><img src="../img/{slug}.jpg" alt="{alt}" width="1200" height="1500" loading="lazy">'
            f'<figcaption>{cap}</figcaption></figure>')

if __name__ == "__main__":
    args = sys.argv[1:]
    alt = None
    if "--alt" in args:
        i = args.index("--alt"); alt = args[i + 1]; del args[i:i + 2]
    print(figure(args[0], alt))

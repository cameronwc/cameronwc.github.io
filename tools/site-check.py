#!/usr/bin/env python3
"""Pre-publish checks for cooperindustries.cc.

Fails (exit 1) if:
  * any placeholder token appears in a publishable file
  * two apps in config/apps.json share an App Store ID
  * an apps.apple.com link under /<slug>/ uses an ID other than the one
    configured for that slug in config/apps.json
  * a support/contact address still points at a personal mailbox
Run: python3 tools/site-check.py
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDERS = re.compile(r"APP_STORE_ID|CHANGEME|YOUR_[A-Z]|<insert|\bXXX\b|\bTODO\b|\bFIXME\b")
BANNED_TEXT = re.compile(r"cameron\.w\.cooper@gmail\.com")
APPLE_LINK = re.compile(r"https://apps\.apple\.com/[^\"'\s)]*?id(\d+)")
PUBLISH_EXT = {".html", ".txt", ".xml", ".svg", ".json", ".md"}
SKIP_DIRS = {".git", "tools", "config", ".github", "node_modules"}

def publishable_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if os.path.splitext(f)[1] in PUBLISH_EXT:
                yield os.path.join(dirpath, f)

def main():
    with open(os.path.join(ROOT, "config", "apps.json")) as fh:
        apps = json.load(fh)["apps"]
    errors = []

    ids = {}
    for slug, app in apps.items():
        aid = app["appStoreId"]
        if not re.fullmatch(r"\d{9,11}", aid):
            errors.append(f"config/apps.json: {slug} has a non-numeric App Store ID {aid!r}")
        if aid in ids:
            errors.append(f"config/apps.json: {slug} and {ids[aid]} share App Store ID {aid}")
        ids[aid] = slug

    for path in publishable_files():
        rel = os.path.relpath(path, ROOT)
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        for m in PLACEHOLDERS.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            errors.append(f"{rel}:{line}: placeholder token {m.group(0)!r}")
        for m in BANNED_TEXT.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            errors.append(f"{rel}:{line}: personal email address; use support@cooperindustries.cc")
        slug = rel.split(os.sep)[0]
        if slug in apps:
            expected = apps[slug]["appStoreId"]
            for m in APPLE_LINK.finditer(text):
                if m.group(1) != expected:
                    line = text.count("\n", 0, m.start()) + 1
                    errors.append(f"{rel}:{line}: App Store link uses id{m.group(1)}, expected id{expected} for {slug}")

    if errors:
        print("site-check: FAIL")
        for e in errors:
            print("  " + e)
        sys.exit(1)
    print(f"site-check: OK ({len(apps)} apps, no placeholders, IDs consistent)")

if __name__ == "__main__":
    main()

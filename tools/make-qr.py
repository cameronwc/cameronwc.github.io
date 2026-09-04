#!/usr/bin/env python3
"""Regenerate <slug>/marketing/qr.svg from config/apps.json. Requires: pip install segno"""
import json, os, segno
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = {"preplate": "#1c1c1e", "prompted": "#1c1915", "prayed": "#292420"}
apps = json.load(open(os.path.join(ROOT, "config", "apps.json")))["apps"]
for slug, app in apps.items():
    url = f"https://apps.apple.com/us/app/id{app['appStoreId']}?ct=marketing-site-qr&mt=8"
    out = os.path.join(ROOT, slug, "marketing", "qr.svg")
    segno.make(url, error="m").save(out, scale=6, dark=INK.get(slug, "#000"), light=None, border=1)
    print(f"{slug}: {url} -> {os.path.relpath(out, ROOT)}")

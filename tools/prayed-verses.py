#!/usr/bin/env python3
"""Extract the verses the Prayed guides quote, verbatim, from the app's bundled World English Bible.

Reads ~/Dev/Kept/Prayed/Resources/Bible/web.txt and topics.json (the same files the app ships) and
writes tools/prayed/verses.json: {"translation": "WEB", "books": {code: name}, "verses": {"PSA 23:4": text}}
for every verse referenced by tools/prayed/guides/*.json plus every verse in every app topic.
Guides are rendered from verses.json, so the site never carries a hand-typed verse.

Usage: tools/prayed-verses.py [--kept ~/Dev/Kept]
"""
import argparse, glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "prayed", "verses.json")
BOOKS = [("GEN","Genesis"),("EXO","Exodus"),("LEV","Leviticus"),("NUM","Numbers"),("DEU","Deuteronomy"),("JOS","Joshua"),("JDG","Judges"),("RUT","Ruth"),("1SA","1 Samuel"),("2SA","2 Samuel"),("1KI","1 Kings"),("2KI","2 Kings"),("1CH","1 Chronicles"),("2CH","2 Chronicles"),("EZR","Ezra"),("NEH","Nehemiah"),("EST","Esther"),("JOB","Job"),("PSA","Psalm"),("PRO","Proverbs"),("ECC","Ecclesiastes"),("SOL","Song of Solomon"),("ISA","Isaiah"),("JER","Jeremiah"),("LAM","Lamentations"),("EZE","Ezekiel"),("DAN","Daniel"),("HOS","Hosea"),("JOE","Joel"),("AMO","Amos"),("OBA","Obadiah"),("JON","Jonah"),("MIC","Micah"),("NAH","Nahum"),("HAB","Habakkuk"),("ZEP","Zephaniah"),("HAG","Haggai"),("ZEC","Zechariah"),("MAL","Malachi"),("MAT","Matthew"),("MAR","Mark"),("LUK","Luke"),("JOH","John"),("ACT","Acts"),("ROM","Romans"),("1CO","1 Corinthians"),("2CO","2 Corinthians"),("GAL","Galatians"),("EPH","Ephesians"),("PHI","Philippians"),("COL","Colossians"),("1TH","1 Thessalonians"),("2TH","2 Thessalonians"),("1TI","1 Timothy"),("2TI","2 Timothy"),("TIT","Titus"),("PHM","Philemon"),("HEB","Hebrews"),("JAM","James"),("1PE","1 Peter"),("2PE","2 Peter"),("1JO","1 John"),("2JO","2 John"),("3JO","3 John"),("JUD","Jude"),("REV","Revelation")]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kept", default=os.path.expanduser("~/Dev/Kept"))
    a = ap.parse_args()
    bible = os.path.join(a.kept, "Prayed", "Resources", "Bible")
    text = {}
    with open(os.path.join(bible, "web.txt"), encoding="utf-8") as fh:
        for line in fh:
            key, _, body = line.rstrip("\n").partition("\t")
            text[key] = body.strip()
    topics = json.load(open(os.path.join(bible, "topics.json")))
    wanted = set()
    for t in topics:
        wanted.update(t["verseKeys"])
    for path in glob.glob(os.path.join(HERE, "prayed", "guides", "*.json")):
        g = json.load(open(path))
        for s in g.get("sections", []):
            for v in s.get("verses", []):
                for k in v["keys"] if "keys" in v else [v["key"]]:
                    wanted.add(k)
    missing = sorted(k for k in wanted if k not in text)
    if missing:
        raise SystemExit(f"verses not in web.txt: {missing}")
    # Strip the WEB's inline psalm headings ("A Psalm by David.") from the verse body: they are
    # editorial, not verse text, and the app shows them the same way.
    out = {}
    for k in sorted(wanted):
        body = text[k]
        if re.match(r"PSA \d+:1$", k):
            # WEB puts the psalm superscription inside verse 1. Strip it; the app does the same.
            body = re.sub(r"^(?:(?:For the Chief Musician|By David|By Asaph|By Solomon|By Moses|By the sons of Korah|Of the sons of Korah|A Psalm|A Song|A song|A Contemplation|A contemplation|A Prayer|A prayer|A Poem|A poem|Set to|To Jeduthun|On |With stringed|For the|A Song of Ascents|A Psalm of praise)[^.]*\.[”]?\s*)+", "", body)
        out[k] = body
    json.dump({"translation": "WEB", "books": dict(BOOKS), "verses": out}, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {OUT}: {len(out)} verses")

if __name__ == "__main__":
    main()

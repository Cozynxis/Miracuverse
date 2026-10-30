#!/usr/bin/env python3
"""Populate MiracuVerse character/kwami portraits from Miraculous Wiki's MediaWiki API.
Never changes episodes, endcards, or hand-curated nonempty image fields.
"""
import json
import re
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog.js"
OUTPUT = ROOT / "api" / "characters.json"
API = "https://miraculousladybug.fandom.com/api.php"
HEADERS = {"User-Agent": "MiracuVerseFanCatalog/1.0 (fan catalog image metadata; GitHub Actions)", "Accept": "application/json"}

class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.candidates = []
        self.in_aside = 0
        self.in_infobox = 0
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "aside":
            self.in_aside += 1
        if tag == "div" and "portable-infobox" in d.get("class", ""):
            self.in_infobox += 1
        if tag == "img":
            url = d.get("data-src") or d.get("src") or ""
            alt = d.get("alt", "")
            if not url.startswith("https://") or "static.wikia.nocookie.net" not in url:
                return
            score = (8 if self.in_aside or self.in_infobox else 0)
            if "portrait" in (alt + " " + url).lower(): score += 5
            if any(word in (alt + " " + url).lower() for word in ("icon", "logo", "gallery", "navigation", "badge")): score -= 8
            self.candidates.append((score, url))
    def handle_endtag(self, tag):
        if tag == "aside" and self.in_aside: self.in_aside -= 1
        if tag == "div" and self.in_infobox: self.in_infobox -= 1

def request(params):
    url = API + "?" + urlencode(params)
    with urlopen(Request(url, headers=HEADERS), timeout=22) as response:
        return json.load(response)

def parse_names():
    text = CATALOG.read_text(encoding="utf-8")
    result = {}
    for kind in ("CHARACTERS", "KWAMIS"):
        start = text.index("window.MV_" + kind + "=[")
        body = text[start:].split("].map(", 1)[0] if kind == "KWAMIS" else text[start:].split("].filter(", 1)[0]
        names = re.findall(r'\[\s*"([^"]+)"\s*,\s*"[^"]*"\s*,\s*"[^"]*"\s*\]', body)
        if not names:
            raise RuntimeError("No names for " + kind)
        result["characters" if kind == "CHARACTERS" else "kwamis"] = list(dict.fromkeys(names))
    return result

def image_for(name):
    aliases = {"Cat Noir": "Adrien Agreste", "Ladybug": "Marinette Dupain-Cheng"}
    page = aliases.get(name, name).replace(" ", "_")
    try:
        parsed = request({"action": "parse", "page": page, "prop": "text", "format": "json", "formatversion": "2"})
        html = parsed.get("parse", {}).get("text", "")
        parser = ImageParser()
        parser.feed(html)
        if parser.candidates:
            parser.candidates.sort(key=lambda x: x[0], reverse=True)
            if parser.candidates[0][0] >= 5:
                return parser.candidates[0][1]
    except Exception as error:
        print("Could not load", name, ":", error)
    return ""

def main():
    original = json.loads(OUTPUT.read_text(encoding="utf-8"))
    names = parse_names()
    total = 0
    for kind, all_names in names.items():
        items = {entry["name"]: entry for entry in original.get(kind, []) if isinstance(entry, dict) and entry.get("name")}
        for name in all_names:
            entry = items.setdefault(name, {"name": name, "image": ""})
            if entry.get("image"): continue
            url = image_for(name)
            if url:
                entry["image"] = url
                total += 1
            time.sleep(0.25)
        original[kind] = [items[name] for name in all_names]
    OUTPUT.write_text(json.dumps(original, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Found", total, "new portraits; catalog entries:", {key: len(original[key]) for key in names})

if __name__ == "__main__":
    main()

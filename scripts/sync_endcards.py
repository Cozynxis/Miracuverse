#!/usr/bin/env python3
"""Collect episode end-card image URLs from the public Miraculous Wiki season galleries.
Run by GitHub Actions. Failed requests preserve the previous JSON.
"""
import json, re, time, pathlib, requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "endcards.json"
BASE = "https://miraculousladybug.fandom.com"
HEADERS = {"User-Agent": "MiracuVerseFanSite/1.0 (public wiki image metadata; contact via GitHub Cozynxis/Miracuverse)"}
SEASONS = range(1, 7)
ALIASES = {
    "the evilustrator": "the evillustrator", "copy cat": "copycat",
    "the gamer": "gamer", "puppeteer": "the puppeteer",
    "the origins - part 1": "ladybug & cat noir",
    "the origins - part 2": "stoneheart",
    "dark owl": "the dark owl", "a christmas special": "santa claws",
    "chris master": "christmaster", "kwami buster": "kwamibuster",
    "onichan": "oni-chan", "soul crusher": "sole crusher",
    "guilt trip": "guiltrip", "optygami": "optigami",
    "strike back": "strikeback", "recreation": "re-creation",
    "felix": "félix", "mister agreste": "mister agreste", "mr. agreste": "mister agreste",
    "grandiaper": "grendiaper", "the origins part 1": "ladybug & cat noir",
    "the origins part 2": "stoneheart",
}
def norm(s):
    s = re.sub(r"\([^)]*\)", "", s or "")
    s = re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()
    return s
def canonical(s):
    s = norm(s)
    return norm(ALIASES.get(s, s))
def full_image(img):
    for key in ("data-src", "data-original", "data-image-src", "src"):
        val = img.get(key, "")
        if ("static.wikia.nocookie.net/" in val or "vignette.wikia.nocookie.net/" in val):
            val = val.split("/revision/")[0]
            return val if val.startswith("https://") else ""
    return ""

def read_season(session, season):
    # Use Fandom's public MediaWiki Action API rather than its blocked /wiki HTML pages.
    response = session.get(BASE + "/api.php", params={
        "action": "parse", "page": f"Season_{season}/Gallery",
        "prop": "text", "format": "json", "formatversion": "2"
    }, headers=HEADERS, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if "error" in payload:
        raise RuntimeError(str(payload["error"]))
    html = payload.get("parse", {}).get("text", "")
    if isinstance(html, dict):
        html = html.get("*", "")
    if not html:
        raise RuntimeError("Wiki API returned no gallery HTML")
    soup = BeautifulSoup(html, "html.parser")
    heading = next((h for h in soup.find_all(re.compile("^h[2-4]$"))
                    if re.search(r"end\s*cards?", h.get_text(" ", strip=True), re.I)), None)
    if not heading:
        heading = soup.find(id=re.compile("end[_ -]?cards?", re.I))
    if not heading:
        raise RuntimeError("No End cards section found in API response")
    images = {}
    scanned = 0
    for element in heading.next_elements:
        if getattr(element, "name", None) in ("h2", "h3") and element is not heading:
            break
        if getattr(element, "name", None) != "img":
            continue
        image = full_image(element)
        if not image:
            continue
        scanned += 1
        parent = element.find_parent(class_=re.compile("wikia-gallery-item|gallerybox|gallery-item|lightbox-caption|thumb|gallery"))
        captions = [element.get("alt", ""), element.get("data-image-name", ""), element.get("title", "")]
        if parent:
            captions += [parent.get_text(" ", strip=True), parent.get("data-image-name", "")]
        for caption in captions:
            caption = re.sub(r"\.(png|jpg|jpeg|webp)$", "", caption, flags=re.I)
            caption = re.sub(r"\b(end\s*cards?|endcards?|ending)\b", "", caption, flags=re.I)
            key = canonical(caption)
            if len(key) > 2:
                images.setdefault(key, image)
    print(f"Season {season}: {scanned} end-card images, {len(images)} labels via API", flush=True)
    return images

def read_episode_endcard(session, title):
    # Fallback for episodes omitted from the season-wide end-card gallery.
    pages = [title + "/Gallery"]
    aliases = {
        "The Origins - Part 1": "Ladybug & Cat Noir (Origins - Part 1)",
        "The Origins - Part 2": "Stoneheart (Origins - Part 2)",
        "A Christmas Special": "Santa Claws",
        "Chris Master": "Christmaster",
        "Kwami Buster": "Kwamibuster",
        "Strike Back": "Strikeback (Shadow Moth's Final Attack - Part 2)",
        "Re-Creation": "Re-creation (The Final Day - Part 2)",
        "Felix": "Félix", "Mister Agreste": "Mister Agreste",
        "Mr. Agreste": "Mister Agreste", "Grandiaper": "Grendiaper",
    }
    if title in aliases:
        pages.insert(0, aliases[title] + "/Gallery")
    for page in pages:
        try:
            r = session.get(BASE + "/api.php", params={
                "action": "parse", "page": page, "prop": "text",
                "format": "json", "formatversion": "2"
            }, headers=HEADERS, timeout=25)
            r.raise_for_status()
            data = r.json()
            html = data.get("parse", {}).get("text", "")
            if isinstance(html, dict): html = html.get("*", "")
            soup = BeautifulSoup(html, "html.parser")
            for h in soup.find_all(re.compile("^h[2-5]$")):
                if not re.search(r"end\s*cards?", h.get_text(" ", strip=True), re.I):
                    continue
                for el in h.next_elements:
                    if getattr(el, "name", None) in ("h2", "h3", "h4", "h5") and el is not h:
                        break
                    if getattr(el, "name", None) == "img":
                        url = full_image(el)
                        if url: return url
        except (requests.RequestException, ValueError, KeyError):
            pass
    return None

SPECIAL_GALLERIES = {
    1: "Miraculous New York/Gallery",
    2: "Miraculous Shanghai/Gallery",
    3: "Ladybug & Cat Noir: The Movie/Gallery",
    4: "Miraculous Paris/Gallery",
    5: "Miraculous London/Gallery",
    6: "Miraculous Tokyo/Gallery",
}

def read_special_image(session, page):
    """Prefer an explicitly labeled end card; otherwise use an actual gallery image."""
    r = session.get(BASE + "/api.php", params={
        "action": "parse", "page": page, "prop": "text",
        "format": "json", "formatversion": "2"
    }, headers=HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(str(data["error"]))
    html = data.get("parse", {}).get("text", "")
    if isinstance(html, dict): html = html.get("*", "")
    soup = BeautifulSoup(html, "html.parser")
    for heading in soup.find_all(re.compile("^h[2-5]$")):
        if re.search(r"end\s*cards?", heading.get_text(" ", strip=True), re.I):
            for el in heading.next_elements:
                if getattr(el, "name", None) in ("h2", "h3", "h4", "h5") and el is not heading:
                    break
                if getattr(el, "name", None) == "img":
                    image = full_image(el)
                    if image: return image, "endcard"
    # Specials and movies frequently have no end-card section.
    # Only accept a screenshot/poster from a gallery section, not UI/navigation images.
    for heading in soup.find_all(re.compile("^h[2-5]$")):
        if re.search(r"screenshots?|posters?|credits", heading.get_text(" ", strip=True), re.I):
            for el in heading.next_elements:
                if getattr(el, "name", None) in ("h2", "h3", "h4", "h5") and el is not heading:
                    break
                if getattr(el, "name", None) == "img":
                    image = full_image(el)
                    if image: return image, "gallery"
    return None, None

def main():
    existing = {}
    if OUTPUT.exists():
        try:
            existing = json.loads(OUTPUT.read_text("utf-8"))
        except Exception:
            pass
    result = dict(existing)
    # Episode order/title is generated by data.js, read its JS arrays as literal JSON.
    text = (ROOT / "data.js").read_text("utf-8")
    groups = re.findall(r'\.\.\.\[(.*?)\]\.map\(\(title,i\)=>\(\{season:(\d+),episode:i\+1,title\}\)\)', text, re.S)
    episodes = {}
    for raw, season in groups:
        if season == "0":
            continue
        try:
            titles = json.loads("[" + raw + "]")
            episodes[int(season)] = titles
        except json.JSONDecodeError:
            print(f"Could not parse season {season}", flush=True)
    order_path = ROOT / "episode-order.json"
    if order_path.exists():
        production = json.loads(order_path.read_text("utf-8"))
        for season, titles in production.items():
            episodes[int(season)] = titles
    with requests.Session() as session:
        for season in SEASONS:
            if season not in episodes:
                continue
            try:
                matches = read_season(session, season)
                for i, title in enumerate(episodes[season], 1):
                    key = f"{season}-{i}"
                    n = canonical(title)
                    img = matches.get(n)
                    if not img:
                        img = next((url for caption, url in matches.items()
                                    if caption == n or (len(n) > 5 and (caption.startswith(n + " ") or n.startswith(caption + " ")))), None)
                    if not img and key not in result:
                        img = read_episode_endcard(session, title)
                        if img:
                            print(f"Season {season} episode {i}: recovered from episode gallery", flush=True)
                    if img:
                        result[key] = img
                time.sleep(1)
            except Exception as exc:
                print(f"Season {season}: {exc}", flush=True)
    with requests.Session() as session:
        for number, page in SPECIAL_GALLERIES.items():
            key = f"0-{number}"
            if key in result:
                continue
            try:
                image, kind = read_special_image(session, page)
                if image:
                    result[key] = image
                    print(f"Special {number}: {kind} image found", flush=True)
                else:
                    print(f"Special {number}: no suitable gallery image", flush=True)
            except Exception as exc:
                print(f"Special {number}: {exc}", flush=True)
    if not result:
        raise RuntimeError("No end cards found. Keeping existing JSON; check Fandom response and gallery markup.")
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", "utf-8")
    print(f"Saved {len(result)} end-card URLs", flush=True)
if __name__ == "__main__":
    main()

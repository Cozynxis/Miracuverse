#!/usr/bin/env python3
"""Sync production-code episode ordering from Fandom's MediaWiki API.
Preserves image-to-title association when episode numbers change.
"""
import json, pathlib, re, requests
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE="https://miraculousladybug.fandom.com/api.php"
HEADERS={"User-Agent":"MiracuVerseFanSite/1.0"}
def norm(value):
    value=re.sub(r"\([^)]*\)","",value).lower()
    return re.sub(r"[^a-z0-9]+","",value)
ALIASES={"theevillustrator":"theevilustrator","copycat":"copycat","thepuppeteer":"puppeteer","ladybugcatnoir":"theoriginspart1","stoneheart":"theoriginspart2","christmaster":"chrismaster","kwamibuster":"kwamibuster","onichan":"onichan","misteragreste":"mragreste","grendiaper":"grandiaper","recreation":"recreation"}
def canon(s):
    n=norm(s)
    return ALIASES.get(n,n)
def groups():
    source=(ROOT/"data.js").read_text("utf8")
    parts=re.findall(r'\.\.\.\[(.*?)\]\.map\(\(title,i\)=>\(\{season:(\d+),episode:i\+1,title\}\)\)',source,re.S)
    return {int(season):json.loads("["+titles+"]") for titles,season in parts}
def get_order(session,season,titles):
    r=session.get(BASE,params={"action":"parse","page":f"Season_{season}","prop":"text","format":"json","formatversion":"2"},headers=HEADERS,timeout=40)
    r.raise_for_status()
    data=r.json()
    if "error" in data: raise RuntimeError(str(data["error"]))
    html=data.get("parse",{}).get("text","")
    if isinstance(html,dict):html=html.get("*","")
    soup=BeautifulSoup(html,"html.parser")
    mapping={}
    for table in soup.select("table"):
        heads=" ".join(th.get_text(" ",strip=True).lower() for th in table.select("tr th")[:20])
        if "prod" not in heads or ("episode" not in heads and "title" not in heads):continue
        for tr in table.select("tr"):
            cells=tr.find_all(["td","th"],recursive=False)
            if len(cells)<4:continue
            values=[c.get_text(" ",strip=True) for c in cells]
            codes=[int(x) for v in values for x in re.findall(r"\b"+str(season)+r"\d{2}\b",v)]
            if not codes:continue
            code=codes[-1]
            if code//100!=season or code%100<1 or code%100>len(titles):continue
            # Match the full title, not arbitrary cell text.
            for title in titles:
                if any(canon(title)==canon(v.strip('“”" ')) or
                       (len(canon(title))>5 and canon(title) in canon(v) and len(canon(v))<len(canon(title))+25)
                       for v in values):
                    mapping[code%100]=title
                    break
        if len(mapping)>=len(titles)-2:break
    if len(mapping)<len(titles)-3:
        raise RuntimeError(f"Season {season}: only {len(mapping)}/{len(titles)} production titles matched")
    # Keep unknown titles in their previous positions instead of losing episodes.
    remaining=[t for t in titles if t not in mapping.values()]
    result=[]
    for n in range(1,len(titles)+1):
        result.append(mapping.get(n) or (remaining.pop(0) if remaining else titles[n-1]))
    print(f"Season {season}: {len(mapping)}/{len(titles)} production codes matched",flush=True)
    return result
def main():
    seasons=groups()
    old_images=json.loads((ROOT/"endcards.json").read_text("utf8"))
    order_file=ROOT/"episode-order.json"
    previous={}
    if order_file.exists():
        previous=json.loads(order_file.read_text("utf8"))
    # Image keys may already use a previously generated production order.
    old_titles={season:previous.get(str(season),titles) for season,titles in seasons.items()}
    new={}
    with requests.Session() as session:
        for season,titles in seasons.items():
            if season==0:continue
            try:new[str(season)]=get_order(session,season,titles)
            except Exception as e:
                print(f"Season {season}: {e}; retaining existing order",flush=True)
                new[str(season)]=old_titles[season]
    by_title={}
    for season,titles in old_titles.items():
        for i,title in enumerate(titles,1):
            url=old_images.get(f"{season}-{i}")
            if url:by_title[(season,canon(title))]=url
    updated={}
    for season,titles in new.items():
        for i,title in enumerate(titles,1):
            url=by_title.get((int(season),canon(title)))
            if url:updated[f"{season}-{i}"]=url
    # Preserve original metadata for specials.
    for key,url in old_images.items():
        if key.startswith("0-"):updated[key]=url
    order_file.write_text(json.dumps(new,ensure_ascii=False,indent=2)+"\n","utf8")
    (ROOT/"endcards.json").write_text(json.dumps(updated,ensure_ascii=False,indent=2,sort_keys=True)+"\n","utf8")
    print(f"Saved production order for {len(new)} seasons, {len(updated)} mapped images",flush=True)
if __name__=="__main__":main()

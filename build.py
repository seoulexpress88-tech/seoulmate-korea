"""Seoulmate static site builder.

  py build.py             build public/ from content/posts and static/
  py build.py --import    first copy new English posts from the overseas-blog folder, then build
  py build.py --publish   import + build + git commit + git push (Vercel deploys on push)

Standard library only. Output goes to public/, which Vercel serves as-is.
"""
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content" / "posts"
OUT = ROOT / "public"
LOG = ROOT / "logs" / "publish.log"
CFG = json.loads((ROOT / "site.json").read_text(encoding="utf-8"))
BASE = CFG["base_url"].rstrip("/")

# Destination data (city info, festivals, seasons) and the projected Korea outline for the map.
DEST = json.loads((ROOT / "data" / "cities.json").read_text(encoding="utf-8"))
KMAP = json.loads((ROOT / "data" / "korea_map.json").read_text(encoding="utf-8"))
DESTS = {c["id"]: c for c in DEST["cities"]}
PLANNER_CITIES = list(DESTS)
# Cities we recognise in post labels/titles: every destination plus a few without a destination page yet.
CITIES = {c["id"]: (c["name"], c["ko"]) for c in DEST["cities"]}
CITIES["pohang"] = ("Pohang", "포항")
CITIES["damyang"] = ("Damyang", "담양")
CITIES["daejeon"] = ("Daejeon", "대전")
CITIES["suncheon"] = ("Suncheon", "순천")
CAT_NAMES = {"food": "Food", "local": "Local life", "culture": "Culture", "history": "History",
             "kpop": "K-pop", "sports": "Sports", "nature": "Nature", "night": "Nightlife"}
# Cache-busting version for /static files, so browsers pick up CSS/JS changes after each deploy.
ASSET_V = hashlib.sha1(b"".join(f.read_bytes() for f in sorted((ROOT / "static").glob("*")))).hexdigest()[:8]
# Guide topics, matched against each guide's title, labels and description.
# A guide can override them with a "topics" list in its meta header.
TOPICS = [
    ("food", "Food", r"\bfood|\beat\b|restaurant|market|bibimbap|tteokgalbi|tofu|chicken|seafood|bakery|cockle|yellowtail|dinner|lunch|chimaek"),
    ("local", "Local life", r"\blocal\b|market|caf[eé]|neighbo|alley|walking route"),
    ("culture", "Culture", r"museum|hanok|\bart\b|mural|hanbok|culture|performance|\bfilm\b|village"),
    ("history", "History", r"palace|temple|fortress|shrine|heritage|unesco|royal|historic|silla|joseon"),
    ("kpop", "K-pop", r"k-pop|kpop|\bbts\b|idol|hallyu|k-drama"),
    ("sports", "Sports", r"baseball|\bkbo\b|\bski|\bsurf|football|soccer|volleyball|esports|taekwondo|marathon|\bgolf|\bsports?\b"),
    ("nature", "Nature", r"foliage|autumn leaves|fall leaves|forest|beach|mountain|\bhik|reed|garden|bamboo|island|wetland|\btrail|camellia|oreum|ginkgo|nature|tangerine"),
    ("night", "Nightlife", r"\bnight|drone show|fireworks|\bbars?\b|pocha|after dark"),
    ("family", "With kids", r"\bkids?\b|family|children"),
    ("couples", "Couples", r"\bdate\b|couple|romantic"),
    ("festivals", "Festivals", r"festival|fireworks|\bexpo\b"),
]
TOPIC_NAMES = dict((t[0], t[1]) for t in TOPICS)


def detect_topics(p):
    text = " ".join([p["title"], p.get("description", ""), " ".join(p.get("tags", []))]).lower()
    return [tid for tid, _, rx in TOPICS if re.search(rx, text)]


MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def city_url(cid):
    return f"/destinations/{cid}/" if cid in DESTS else f"/guides/?city={cid}"


def log(msg):
    LOG.parent.mkdir(exist_ok=True)
    line = f"[{dt.datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode("ascii", "replace").decode())


def esc(s):
    return html.escape(str(s), quote=True)


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


# ---------------------------------------------------------------- import

def clean_body(body):
    """Turn a Blogger draft body into publishable HTML.

    Removes the title, photo/personal-note placeholders and [CHECK] markers.
    [AFFILIATE: ...] paragraphs are kept and resolved at build time, so links added
    to site.json later still reach older posts.
    """
    had_checks = "[CHECK" in body
    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    body = re.sub(r'<p class="(?:photo|note)"[^>]*>.*?</p>', "", body, flags=re.S)
    body = re.sub(r'\s*<span class="check"[^>]*>.*?</span>', "", body, flags=re.S)
    body = re.sub(r"\[(?:PHOTO|YOUR NOTE|CHECK)[^\]]*\]", "", body)
    body = re.sub(r"<p>\s*</p>", "", body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip(), had_checks


def detect_cities(*texts):
    """Cities a post is about, most prominent first. "from Seoul"/"from Busan" are departure points, not topics."""
    blob = re.sub(r"\bfrom (\w+)", " ", " ".join(texts).lower())
    found = [(blob.find(en.lower()), cid) for cid, (en, _) in CITIES.items() if en.lower() in blob]
    return [cid for _, cid in sorted(found)]


def import_posts():
    src = (ROOT / CFG["source_posts_dir"]).resolve()
    if not src.exists():
        log(f"원본 폴더 없음, 가져오기 건너뜀: {src}")
        return 0
    CONTENT.mkdir(parents=True, exist_ok=True)
    count = 0
    for day_dir in sorted(p for p in src.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name)):
        for f in sorted(day_dir.glob("*.html")):
            if f.name.startswith("00_"):
                continue
            slug = re.sub(r"^\d+_", "", f.stem).lower()
            slug = re.sub(r"[^a-z0-9-]+", "-", slug).strip("-")
            target = CONTENT / f"{day_dir.name}-{slug}.html"
            if target.exists() or list(CONTENT.glob(f"*-{slug}.html")):
                continue
            raw = f.read_text(encoding="utf-8")
            m = re.search(r"<!--POST-START-->(.*?)<!--POST-END-->", raw, re.S)
            if not m:
                log(f"건너뜀(POST-START/END 없음): {f.name}")
                continue
            body = m.group(1)
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
            title = strip_tags(h1.group(1)) if h1 else strip_tags(re.search(r"<title>(.*?)</title>", raw, re.S).group(1))
            lm = re.search(r'<meta name="labels" content="([^"]*)"', raw)
            labels = [x.strip() for x in html.unescape(lm.group(1)).split(",") if x.strip()] if lm else []
            dm = re.search(r'<meta name="search-description" content="([^"]*)"', raw)
            desc = html.unescape(dm.group(1)) if dm else ""
            body, had_checks = clean_body(body)
            meta = {
                "title": title, "slug": slug, "date": day_dir.name, "description": desc,
                "tags": labels, "cities": detect_cities(" ".join(labels), title),
                "facts_checked": day_dir.name if had_checks else None,
                "source": f"{day_dir.name}/{f.name}", "draft": False,
            }
            target.write_text("<!--meta\n" + json.dumps(meta, ensure_ascii=False, indent=2) + "\n-->\n" + body + "\n", encoding="utf-8")
            log(f"새 글 가져옴: {target.name}")
            count += 1
    return count


# ---------------------------------------------------------------- load

def load_posts():
    posts = []
    for f in sorted(CONTENT.glob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"<!--meta\n(.*?)\n-->\n", raw, re.S)
        if not m:
            continue
        meta = json.loads(m.group(1))
        if meta.get("draft"):
            continue
        meta["body"] = raw[m.end():]
        meta["url"] = f"/guides/{meta['slug']}/"
        words = len(strip_tags(meta["body"]).split())
        meta["minutes"] = max(1, round(words / 220))
        meta["topics"] = meta.get("topics") or detect_topics(meta)
        posts.append(meta)
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def resolve_affiliates(body):
    links = {k: v for k, v in CFG.get("affiliate_links", {}).items() if not k.startswith("_")}
    used = False

    def repl(m):
        nonlocal used
        key = m.group(1).strip()
        url = links.get(key)
        if not url:
            return ""
        used = True
        partner, _, what = key.partition("—")
        text = f"Check {what.strip()} on {partner.strip()}" if what else f"Check prices on {key}"
        return f'<p class="aff"><a class="btn ghost" href="{esc(url)}" target="_blank" rel="sponsored noopener">{esc(text)} ↗</a></p>'

    body = re.sub(r"<p>\s*\[AFFILIATE:\s*(.*?)\]\s*</p>", repl, body, flags=re.S)
    body = re.sub(r"\[AFFILIATE[^\]]*\]", "", body)
    return body, used


def add_heading_ids(body):
    toc, seen = [], set()

    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        text = strip_tags(inner)
        hid = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "section"
        while hid in seen:
            hid += "-2"
        seen.add(hid)
        toc.append((hid, text))
        return f'<h2 id="{hid}"{attrs}>{inner}</h2>'

    body = re.sub(r"<h2(?![^>]*\bid=)([^>]*)>(.*?)</h2>", repl, body, flags=re.S)
    return body, toc


# ---------------------------------------------------------------- templates

def fmt_date(d):
    return dt.date.fromisoformat(d).strftime("%b %-d, %Y") if sys.platform != "win32" else dt.date.fromisoformat(d).strftime("%b %#d, %Y")


def layout(title, desc, path, body, active="", head_extra="", page_title=None):
    full = page_title or (f"{title} | {CFG['name']}" if title != CFG["name"] else f"{CFG['name']} · {CFG['tagline']}")
    nav = [("/planner/", "Plan a trip", "planner"), ("/destinations/", "Destinations", "destinations"), ("/guides/", "Travel guides", "guides"), ("/about/", "About", "about")]
    nav_html = "".join(f'<a href="{u}"{" aria-current=\"page\"" if k == active else ""}>{t}</a>' for u, t, k in nav)
    year = dt.date.today().year
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="{'article' if path.startswith('/guides/') and path.count('/') == 3 else 'website'}">
<meta property="og:site_name" content="{esc(CFG['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{BASE}{path}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="{esc(CFG['name'])} guides" href="{BASE}/feed.xml">
{f'<meta name="google-site-verification" content="{esc(CFG["google_site_verification"])}">' if CFG.get("google_site_verification") and path == "/" else ""}
<link rel="icon" href="/static/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+KR:wght@400;600&display=swap">
<link rel="stylesheet" href="/static/style.css?v={ASSET_V}">
{head_extra}
</head>
<body>
<header class="site-head"><div class="wrap">
<a class="logo" href="/">Seoul<span>mate</span></a>
<nav class="nav" aria-label="Main">{nav_html}</nav>
</div></header>
<main class="wrap">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<span>© {year} {esc(CFG['name'])} · Made in Seoul for travelers to Korea</span>
<nav aria-label="Footer"><a href="/guides/">Guides</a><a href="/about/">About</a><a href="/privacy/">Privacy</a><a href="/disclosure/">Affiliate disclosure</a><a href="/feed.xml">RSS</a></nav>
</div></footer>
</body>
</html>
"""


def card(p):
    city = CITIES[p["cities"][0]][0] if p["cities"] else "Korea"
    shown = sorted(p["topics"], key=lambda t: t not in ("family", "couples"))[:3]  # audience first
    topics = "".join(f"<span>{TOPIC_NAMES[t]}</span>" for t in shown)
    text = esc(" ".join([p["title"], p["description"], " ".join(p["tags"])]).lower())
    return f"""<a class="card" href="{p['url']}" data-cities="{' '.join(p['cities'])}" data-topics="{' '.join(p['topics'])}" data-text="{text}">
<span class="eyebrow">{esc(city)}</span>
<h3>{esc(p['title'])}</h3>
<p>{esc(p['description'])}</p>
<span class="card-topics">{topics}</span>
<span class="meta">{fmt_date(p['date'])} · {p['minutes']} min read</span>
</a>"""


def cards(posts):
    if not posts:
        return '<div class="empty">New guides are published every morning. Check back soon.</div>'
    return '<div class="cards">' + "".join(card(p) for p in posts) + "</div>"


def proj(lon, lat):
    return ((lon - KMAP["lon0"]) * KMAP["c"] * KMAP["k"], (KMAP["lat1"] - lat) * KMAP["k"])


def korea_map(active=None, interactive=True):
    """Inline SVG map of South Korea with a pin for every destination."""
    pins = []
    for c in DEST["cities"]:
        x, y = proj(c["lon"], c["lat"])
        pos = c.get("label", "right")
        tx, ty, anchor = {"right": (x + 10, y + 5, "start"), "left": (x - 10, y + 5, "end"),
                          "top": (x, y - 12, "middle"), "bottom": (x, y + 20, "middle")}[pos]
        cls = "pin is-active" if c["id"] == active else "pin"
        label = f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{esc(c.get("short", c["name"]))}</text>'
        dot = f'<circle class="halo" cx="{x:.1f}" cy="{y:.1f}" r="13"/><circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="6.5"/>'
        if interactive:
            pins.append(f'<a class="{cls}" href="{city_url(c["id"])}" data-city="{c["id"]}" aria-label="{esc(c["name"])}">{dot}{label}</a>')
        else:
            pins.append(f'<g class="{cls}">{dot}{label}</g>')
    return (f'<svg class="kmap" viewBox="0 0 {KMAP["width"]} {KMAP["height"]}" role="img" aria-label="Map of South Korea with destinations">'
            f'<rect class="sea" width="{KMAP["width"]}" height="{KMAP["height"]}"/>'
            f'<path class="land-other" d="{KMAP["neighbours"]}"/><path class="land" d="{KMAP["korea"]}"/>'
            f'<text class="sea-label" x="{KMAP["width"] * 0.80:.0f}" y="{KMAP["height"] * 0.42:.0f}">East Sea</text>'
            f'<text class="sea-label" x="{KMAP["width"] * 0.08:.0f}" y="{KMAP["height"] * 0.62:.0f}">Yellow Sea</text>'
            + "".join(pins) + "</svg>")


def festival_items(festivals, city=None):
    out = []
    for f in festivals:
        where = f'<a href="{city_url(city["id"])}">{esc(city["name"])}</a> · ' if city else ""
        out.append(f'<li class="fest" data-months="{",".join(map(str, f["months"]))}"><span class="fest-when">{esc(f["when"])}</span>'
                   f'<b>{esc(f["name"])}</b> <span class="ko">{esc(f["ko"])}</span><p>{where}{esc(f["about"])}</p></li>')
    return "".join(out)


def city_panel(c, posts):
    n = sum(c["id"] in p["cities"] for p in posts)
    cats = " ".join(f"<span>{CAT_NAMES[k]}</span>" for k in c["best_for"])
    fest = "".join(f'<li><b>{esc(f["when"])}</b> {esc(f["name"])}</li>' for f in c["festivals"][:3])
    guides = f'<a href="{city_url(c["id"])}#guides">{n} guide{"s" if n != 1 else ""}</a>' if n else "Guides coming soon"
    return f"""<div class="cpanel" data-panel="{c['id']}"{'' if c['id'] == 'seoul' else ' hidden'}>
  <div class="cpanel-h"><h3>{esc(c['name'])}</h3><span class="ko">{esc(c['ko'])}</span></div>
  <p class="cpanel-tag">{esc(c['tagline'])}</p>
  <dl class="facts"><div><dt>From Seoul</dt><dd>{esc(c['from_seoul'])}</dd></div><div><dt>Stay</dt><dd>{esc(c['stay'])}</dd></div></dl>
  <div class="bestfor">{cats}</div>
  <p class="cpanel-hl"><span class="lbl">Don't miss</span> {esc(" · ".join(c['highlights']))}</p>
  <div><span class="lbl">Festivals &amp; seasons</span><ul class="mini-fest">{fest}</ul></div>
  <div class="cpanel-actions"><a class="btn" href="/planner/?city={c['id']}">Plan days here</a><a class="btn ghost" href="{city_url(c['id'])}">About {esc(c['name'])}</a></div>
  <p class="hint">{guides}</p>
</div>"""


def map_section(posts, heading="Where to go in Korea", intro=True):
    chips = "".join(f'<button type="button" class="city-chip" data-city="{c["id"]}"{" aria-pressed=\"true\"" if c["id"] == "seoul" else " aria-pressed=\"false\""}>{esc(c["name"])}</button>' for c in DEST["cities"])
    lead = '<p class="hint" style="margin:-8px 0 14px">Tap a city on the map to see what it\'s like, how far it is from Seoul and when its festivals happen.</p>' if intro else ""
    return f"""<section class="section" id="map">
  <div class="section-h"><h2>{heading}</h2><a href="/destinations/">All destinations →</a></div>
  {lead}
  <div class="mapwrap">
    <div class="mapcol">{korea_map()}<div class="city-chips" aria-label="Choose a city">{chips}</div></div>
    <div class="panelcol">{"".join(city_panel(c, posts) for c in DEST["cities"])}</div>
  </div>
</section>"""


def whats_on_section():
    month = dt.date.today().month
    chips = "".join(f'<button type="button" class="month" data-month="{i + 1}" aria-pressed="{"true" if i + 1 == month else "false"}">{m}</button>' for i, m in enumerate(MONTHS))
    items = "".join(festival_items(c["festivals"], c) for c in DEST["cities"])
    seasons = "".join(f'<p class="season" data-months="{",".join(map(str, s["months"]))}"><b>{s["name"]} · {s["temp"]}</b> {esc(s["tip"])}</p>' for s in DEST["seasons"])
    return f"""<section class="section" id="whats-on">
  <div class="section-h"><h2>What's on when you visit</h2></div>
  <div class="months" role="group" aria-label="Travel month">{chips}</div>
  {seasons}
  <ul class="fest-list">{items}</ul>
  <p class="hint fest-empty" hidden>No big festivals in our list this month. Check the season tip above.</p>
  <p class="hint">Festival dates change every year and some follow the lunar calendar. Always confirm on the official site before you book.</p>
</section>"""


IDEAS = [
    ("First time in Korea", "5 days · Seoul, Busan", "The classics: palaces, markets, K-pop streets and the beach city.", "seoul,busan", "food,history,kpop", 5),
    ("K-pop & city nights", "4 days · Seoul", "Dance class, idol streets, busking in Hongdae and late-night eats.", "seoul", "kpop,night,food", 4),
    ("Mountains & east coast", "5 days · Seoul, Gangneung, Sokcho", "Seoraksan hikes, seaside cafés and sunrise over the East Sea.", "seoul,gangneung,sokcho", "nature,food,local", 5),
    ("Heritage trail", "6 days · Seoul, Andong, Gyeongju, Busan", "Royal palaces, a living clan village and the Silla capital.", "seoul,andong,gyeongju,busan", "history,culture", 6),
    ("Foodie road trip", "5 days · Seoul, Jeonju, Yeosu", "Market food, Jeonju bibimbap and south-coast seafood.", "seoul,jeonju,yeosu", "food,local,night", 5),
    ("Island & sea", "5 days · Busan, Tongyeong, Jeju", "Harbors, cable cars over islands and volcanic Jeju.", "busan,tongyeong,jeju", "nature,food", 5),
    ("Sports fan's Korea", "5 days · Seoul, Busan", "Baseball chants, K League football, esports and a taekwondo class (baseball runs March to October).", "seoul,busan", "sports,food,night", 5),
    ("Winter snow trip", "4 days · Seoul, Gangneung", "Ski the 2018 Olympic slopes, then the East Sea and soft tofu (December to March).", "seoul,gangneung", "sports,nature,food", 4),
]


def ideas_section():
    cards_html = "".join(f"""<a class="card idea" href="/planner/?city={c}&amp;cat={k}&amp;days={d}">
<span class="eyebrow">{esc(sub)}</span><h3>{esc(t)}</h3><p>{esc(about)}</p><span class="meta">Open in planner →</span></a>""" for t, sub, about, c, k, d in IDEAS)
    return f"""<section class="section" id="ideas">
  <div class="section-h"><h2>Trip ideas to start from</h2><a href="/planner/">Start from scratch →</a></div>
  <div class="cards">{cards_html}</div>
</section>"""


def essentials_section():
    tips = [("Maps", "Use Naver Map or KakaoMap. Google Maps has limited walking and driving directions in Korea."),
            ("Transit card", "Buy a T-money card at any convenience store and top it up with cash. It works on subways, buses and taxis."),
            ("Payments", "Cards work almost everywhere. Keep some cash for traditional markets and street stalls."),
            ("Language", "Download Papago for translation. It reads menus and signs from your camera.")]
    items = "".join(f'<div class="ess"><b>{t}</b><p>{esc(x)}</p></div>' for t, x in tips)
    return f'<section class="section"><div class="section-h"><h2>First-timer essentials</h2></div><div class="ess-grid">{items}</div></section>'


def page_home(posts):
    body = f"""
<section class="hero">
  <div>
    <h1>Plan Korea around what you love.</h1>
    <p>Tell us your dates, cities and interests: food, K-pop, history, local life. Get a day-by-day plan with options for every stop, then read our local guides before you go.</p>
    <div class="actions"><a class="btn" href="/planner/">Build my itinerary</a><a class="btn ghost" href="#map">Explore the map</a></div>
  </div>
  <div class="hero-card" aria-label="Example itinerary">
    <span class="lbl">Example · 3 days, Seoul &amp; Busan</span>
    <div class="day"><b>Day 1</b><span>Gyeongbokgung Palace → Gwangjang Market → Hongdae busking</span></div>
    <div class="day"><b>Day 2</b><span>K-pop dance class → National Museum → Han River chimaek</span></div>
    <div class="day"><b>Day 3</b><span>KTX to Busan → Gamcheon Village → Gwangalli drone show</span></div>
  </div>
</section>
{map_section(posts)}
{whats_on_section()}
{ideas_section()}
<section class="section">
  <div class="section-h"><h2>Latest guides</h2><a href="/guides/">All guides →</a></div>
  {topic_filters(posts)}
  {cards(posts[:6])}
</section>
{essentials_section()}"""
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": CFG["name"], "url": BASE + "/", "description": CFG["description"]}
    return layout(CFG["name"], CFG["description"], "/", body,
                  head_extra=jsonld(ld) + f'\n<script src="/static/home.js?v={ASSET_V}" defer></script>')


def page_destinations(posts):
    grid = "".join(f"""<a class="card" href="{city_url(c['id'])}"><span class="eyebrow">{esc(c['ko'])} · {esc(c['from_seoul'])}</span>
<h3>{esc(c['name'])}</h3><p>{esc(c['tagline'])}</p><span class="meta">{' · '.join(CAT_NAMES[k] for k in c['best_for'])}</span></a>""" for c in DEST["cities"])
    body = f"""<div class="page-h"><h1>Destinations in Korea</h1>
<p>Fourteen places foreign travelers love, from Seoul's palaces to Jeju's volcanoes. Pick a city on the map to compare.</p></div>
{map_section(posts, "Map", intro=False)}
<section class="section"><div class="section-h"><h2>All destinations</h2></div><div class="cards">{grid}</div></section>"""
    return layout("Destinations in Korea", "Where to go in Korea: 14 destinations with travel times from Seoul, highlights and festival seasons.",
                  "/destinations/", body, "destinations", head_extra=f'<script src="/static/home.js?v={ASSET_V}" defer></script>')


def city_filters(posts, current=None):
    used = [c for c in CITIES if any(c in p["cities"] for p in posts)]
    items = [f'<a href="/guides/"{" aria-current=\"page\"" if current is None else ""}>All</a>']
    items += [f'<a href="{city_url(c)}#guides"{" aria-current=\"page\"" if c == current else ""}>{CITIES[c][0]}</a>' for c in used]
    return '<nav class="filters" aria-label="Filter by city">' + "".join(items) + "</nav>"


def topic_url(tid):
    return f"/guides/topic/{tid}/"


def topic_filters(posts, current=None, label="Browse by topic"):
    counts = {t: sum(t in p["topics"] for p in posts) for t in TOPIC_NAMES}
    items = [f'<a href="{topic_url(t)}" data-topic="{t}"{" aria-current=\"page\"" if t == current else ""}>{n} <span class="n">{counts[t]}</span></a>'
             for t, n in TOPIC_NAMES.items() if counts[t]]
    return f'<nav class="filters" aria-label="{label}">' + "".join(items) + "</nav>"


def page_guides(posts):
    used = [c for c in CITIES if any(c in p["cities"] for p in posts)]
    cities = "".join(f'<a href="{city_url(c)}#guides" data-city="{c}">{CITIES[c][0]} <span class="n">{sum(c in p["cities"] for p in posts)}</span></a>' for c in used)
    body = f"""<div class="page-h"><h1>Korea travel guides</h1>
<p>Practical, locally written guides: what to see, where to eat, how to get there from Seoul or Busan, and what foreign visitors should know. New guides every morning.</p></div>
<div class="finder">
  <input type="search" id="guideSearch" placeholder="Search guides, e.g. ski, palace, Jeju" aria-label="Search guides">
  <div class="frow"><span class="lbl">Topic</span>{topic_filters(posts)}</div>
  <div class="frow"><span class="lbl">City</span><nav class="filters" aria-label="Filter by city">{cities}</nav></div>
  <p class="hint" id="guideCount">{len(posts)} guides</p>
</div>
{cards(posts)}
<div class="empty" id="guideEmpty" hidden>No guides match. Try another topic or city, or <a href="/guides/" id="guideReset">show all guides</a>.</div>"""
    return layout("Korea travel guides", "Practical Korea travel guides for foreign visitors: sights, food, transport and local tips.", "/guides/", body, "guides",
                  head_extra=f'<script src="/static/guides.js?v={ASSET_V}" defer></script>')


def page_topic(tid, posts, all_posts):
    name = TOPIC_NAMES[tid]
    body = f"""<p class="crumbs"><a href="/guides/">Guides</a> / {esc(name)}</p>
<div class="page-h"><h1>{esc(name)} guides for Korea</h1>
<p>Every Seoulmate guide about {esc(name.lower())}, newest first. Pick another topic or <a href="/guides/">search all guides</a>.</p></div>
{topic_filters(all_posts, tid)}
{cards(posts)}"""
    return layout(f"{name} guides for Korea", f"Korea travel guides about {name.lower()} for foreign visitors: where to go, how to get there and local tips.",
                  topic_url(tid), body, "guides")


def page_city(c, posts):
    cid, en = c["id"], c["name"]
    cats = " ".join(f"<span>{CAT_NAMES[k]}</span>" for k in c["best_for"])
    hl = "".join(f"<li>{esc(h)}</li>" for h in c["highlights"])
    guides = cards(posts) if posts else f'<div class="empty">Guides for {esc(en)} are coming soon. New guides are published every morning.</div>'
    body = f"""<p class="crumbs"><a href="/destinations/">Destinations</a> / {esc(en)}</p>
<div class="city-hero">
  <div>
    <div class="page-h"><h1>{esc(en)} <span class="hint">{esc(c['ko'])}</span></h1><p>{esc(c['tagline'])}</p></div>
    <dl class="facts"><div><dt>From Seoul</dt><dd>{esc(c['from_seoul'])}</dd></div><div><dt>How long</dt><dd>{esc(c['stay'])}</dd></div></dl>
    <div class="bestfor">{cats}</div>
    <h2 class="sub">Don't miss</h2><ul class="hl">{hl}</ul>
    <p><a class="btn" href="/planner/?city={cid}">Plan days in {esc(en)}</a></p>
  </div>
  <div class="locator">{korea_map(active=cid, interactive=False)}</div>
</div>
<section class="section"><div class="section-h"><h2>Festivals &amp; seasons</h2></div>
  <ul class="fest-list static">{festival_items(c['festivals'])}</ul>
  <p class="hint">Dates change every year. Confirm on the official site before you book.</p>
</section>
<section class="section" id="guides"><div class="section-h"><h2>{esc(en)} guides</h2></div>{guides}</section>"""
    ld = {"@context": "https://schema.org", "@type": "TouristDestination", "name": f"{en}, South Korea", "description": c["tagline"],
          "geo": {"@type": "GeoCoordinates", "latitude": c["lat"], "longitude": c["lon"]}, "url": BASE + city_url(cid)}
    return layout(f"{en} travel guide", f"{en}, Korea: {c['tagline']} Travel time from Seoul, highlights and festival seasons.",
                  city_url(cid), body, "destinations", head_extra=jsonld(ld))


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def page_post(p, posts):
    body, used_aff = resolve_affiliates(p["body"])
    body, toc = add_heading_ids(body)
    city = p["cities"][0] if p["cities"] else None
    crumbs = '<a href="/guides/">Guides</a>'
    if city:
        crumbs += f' / <a href="{city_url(city)}">{CITIES[city][0]}</a>'
    checked = (f'<div class="callout">Prices, opening hours and transit times change often. We last checked them on '
               f'{fmt_date(p["facts_checked"])}. Please confirm on the official site or Naver Map before you go.</div>') if p.get("facts_checked") else ""
    plan_city = next((c for c in p["cities"] if c in PLANNER_CITIES), None)
    cta = (f'<div class="plan-cta"><p><b>Turn this into a day plan</b>Pick your dates and interests and we\'ll build a {CITIES[plan_city][0]} itinerary around them.</p>'
           f'<a class="btn" href="/planner/?city={plan_city}">Plan my {CITIES[plan_city][0]} days</a></div>') if plan_city else \
          ('<div class="plan-cta"><p><b>Planning a Korea trip?</b>Build a day-by-day itinerary around food, K-pop, history and local life.</p>'
           '<a class="btn" href="/planner/">Build my itinerary</a></div>')
    tags = ('<div class="tags">' + "".join(f'<a href="{topic_url(t)}">{TOPIC_NAMES[t]}</a>' for t in p["topics"])
            + "".join(f'<a href="{city_url(c)}">{CITIES[c][0]}</a>' for c in p["cities"]) + "</div>")
    disclosure = '<p class="disclosure">This post contains affiliate links. If you book through them we may earn a small commission at no extra cost to you.</p>' if used_aff else ""
    toc_html = ('<aside class="toc"><span class="lbl">On this page</span><ol>' +
                "".join(f'<li><a href="#{h}">{esc(t)}</a></li>' for h, t in toc) + "</ol></aside>") if len(toc) > 2 else "<aside></aside>"
    related = [x for x in posts if x is not p and set(x["cities"]) & set(p["cities"])][:3]
    if len(related) < 3:
        related += [x for x in posts if x is not p and x not in related][:3 - len(related)]
    rel_html = f'<section class="related"><div class="section-h"><h2>More guides</h2></div>{cards(related)}</section>' if related else ""
    html_body = f"""<p class="crumbs">{crumbs}</p>
<div class="article">
<article>
  <header class="post-h"><h1>{esc(p['title'])}</h1>
  <div class="post-meta"><time datetime="{p['date']}">{fmt_date(p['date'])}</time><span>{p['minutes']} min read</span></div></header>
  {checked}
  <div class="prose">
{body}
  </div>
  {cta}
  {tags}
  {disclosure}
</article>
{toc_html}
</div>
{rel_html}"""
    ld = [{
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["description"],
        "datePublished": p["date"], "dateModified": p.get("updated", p["date"]), "inLanguage": "en",
        "mainEntityOfPage": BASE + p["url"], "author": {"@type": "Organization", "name": CFG["name"], "url": BASE + "/about/"},
        "publisher": {"@type": "Organization", "name": CFG["name"], "url": BASE + "/"}, "keywords": ", ".join(p["tags"]),
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Guides", "item": BASE + "/guides/"},
            {"@type": "ListItem", "position": 2, "name": p["title"], "item": BASE + p["url"]},
        ]}]
    return layout(p["title"], p["description"], p["url"], html_body, "guides",
                  head_extra=jsonld(ld[0]) + jsonld(ld[1]) + f'\n<meta property="article:published_time" content="{p["date"]}">',
                  page_title=f"{p['title']}")


def page_planner(posts):
    guides = {}
    for p in posts:
        for c in p["cities"]:
            guides.setdefault(c, []).append({"title": p["title"], "url": p["url"]})
    body = """<p class="hint no-print" style="margin:0 0 14px">14 destinations: Seoul, Busan, Jeju, Gyeongju, Jeonju, Incheon, Suwon, Gapyeong &amp; Nami Island, Gangneung, Sokcho &amp; Seoraksan, Andong, Daegu, Yeosu and Tongyeong.</p>
<div class="grid">
  <form class="panel sticky" id="tripForm">
    <h2>Your trip</h2>
    <div class="field">
      <span class="lbl">Dates in Korea</span>
      <div class="dates">
        <input type="date" id="arrive" aria-label="Arrival date">
        <input type="date" id="depart" aria-label="Departure date">
      </div>
      <span class="hint" id="dayCount"></span>
    </div>
    <div class="field"><span class="lbl">Cities, in visiting order</span><div class="chips" id="cityChips"></div></div>
    <div class="field"><span class="lbl">What you're into</span><div class="chips" id="catChips"></div></div>
    <div class="field">
      <span class="lbl">Pace</span>
      <div class="seg">
        <label><input type="radio" name="pace" id="pace-easy" value="2">Easy</label>
        <label><input type="radio" name="pace" id="pace-bal" value="3" checked>Balanced</label>
        <label><input type="radio" name="pace" id="pace-full" value="4">Packed</label>
      </div>
    </div>
    <button class="btn" type="submit">Build my itinerary</button>
  </form>
  <div style="min-width:0">
    <div class="trip-head">
      <div><h1 id="tripTitle">Your Korea itinerary</h1>
      <p>Each stop has up to three options. Check traveler reviews on Google Maps, then tap the one you want.</p></div>
      <div class="meter" id="meter"></div>
    </div>
    <div id="days"></div>
    <div class="tools">
      <button class="btn ghost" type="button" id="copyPlan">Copy itinerary</button>
      <button class="btn ghost" type="button" id="printPlan">Print or save as PDF</button>
    </div>
    <p class="toast" id="toast" aria-live="polite"></p>
    <h2 class="no-print" style="margin-top:28px">Want the full plan?</h2>
    <div class="checkout">
      <div class="plan"><span class="lbl">Free</span><div class="price">$0</div>
        <ul><li>This planner, any dates and cities</li><li>Copy or print your plan</li></ul></div>
      <div class="plan rec"><span class="lbl">Trip Plan</span><div class="price" id="pricePlan"></div>
        <ul><li>Maps and transit steps for every day</li><li>Opening hours and booking links</li><li>Free edits until departure</li></ul>
        <span class="soon">Launching soon</span></div>
      <div class="plan"><span class="lbl">Local Concierge</span><div class="price" id="priceConcierge"></div>
        <ul><li>A Seoul local reviews and tunes your plan</li><li>Restaurant and experience picks matched to your plan</li><li>Chat support during your trip</li></ul>
        <span class="soon">Launching soon</span></div>
    </div>
  </div>
</div>"""
    extra = f'<script>window.SEOULMATE_GUIDES={json.dumps(guides, ensure_ascii=False)};</script>\n<script src="/static/planner.js?v={ASSET_V}" defer></script>'
    return layout("Korea trip planner", "Build a free day-by-day Korea itinerary for Seoul, Busan, Jeju, Gyeongju, Gangneung, Sokcho, Yeosu and more, based on your dates and interests.",
                  "/planner/", body, "planner", head_extra=extra)


def page_simple(slug, title, desc, inner, active=""):
    return layout(title, desc, f"/{slug}/", f'<div class="page-h"><h1>{esc(title)}</h1></div><div class="prose" style="margin-top:18px">{inner}</div>', active)


ABOUT = """<p>Seoulmate helps foreign travelers plan Korea trips around what they actually care about, whether that's street food, K-pop, palaces and temples, or simply living like a local for a week.</p>
<p>We're based in Seoul. Our guides are written for people visiting Korea for the first or second time, so we include the things locals take for granted: how to get there from Seoul or Busan, the Korean address to show a taxi driver, which map app works, and when places close.</p>
<h2>How we write guides</h2>
<ul><li>We use official sources such as the Korea Tourism Organization and local government sites, plus recent Korean news and local reviews.</li>
<li>Prices, hours and transit times change. Each guide shows when we last checked them.</li>
<li>Some guides contain affiliate links. They never change what we recommend. See our <a href="/disclosure/">affiliate disclosure</a>.</li></ul>
<h2>The trip planner</h2>
<p>The <a href="/planner/">planner</a> is free. It suggests up to three options for each part of your day so you can choose, and links to Google Maps and Naver Map so you can read what other travelers say.</p>"""

PRIVACY = """<p>Last updated: {date}</p>
<p>This site doesn't require an account. The trip planner runs entirely in your browser; the dates, cities and choices you enter are not sent to us.</p>
<h2>What is collected</h2>
<ul><li>Our hosting provider (Vercel) keeps standard server logs, such as IP address, browser type and pages requested, for security and reliability.</li>
<li>Fonts load from Google Fonts, which receives your IP address when the page loads.</li>
<li>Links to Google Maps, Naver Map and booking partners take you to those sites, which have their own privacy policies.</li></ul>
<h2>Cookies, analytics and ads</h2>
<p>We don't set cookies today. If we add analytics, advertising (such as Google AdSense) or affiliate tracking, we'll update this page and, where required, ask for your consent first.</p>
<h2>Contact</h2>
<p>{contact}</p>"""

DISCLOSURE = """<p>Some links on this site are affiliate links, for example to Klook, Trip.com or Agoda. If you book through them, we may earn a small commission at no extra cost to you.</p>
<p>Affiliate partners don't pay for placement in our guides or in the trip planner, and they can't edit what we write. Posts that contain affiliate links say so at the end of the post.</p>"""


# ---------------------------------------------------------------- feeds

def sitemap(posts):
    today = dt.date.today().isoformat()
    urls = [("/", today), ("/planner/", today), ("/destinations/", today), ("/guides/", posts[0]["date"] if posts else today), ("/about/", today)]
    urls += [(city_url(c), today) for c in DESTS]
    urls += [(topic_url(t), today) for t in TOPIC_NAMES if any(t in p["topics"] for p in posts)]
    urls += [(p["url"], p.get("updated", p["date"])) for p in posts]
    items = "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>\n'


def rss(posts):
    def rfc(d):
        return dt.datetime.combine(dt.date.fromisoformat(d), dt.time(9)).strftime("%a, %d %b %Y %H:%M:%S +0900")
    items = "".join(
        f"<item><title>{esc(p['title'])}</title><link>{BASE}{p['url']}</link><guid>{BASE}{p['url']}</guid>"
        f"<pubDate>{rfc(p['date'])}</pubDate><description>{esc(p['description'])}</description></item>" for p in posts[:30])
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{esc(CFG["name"])} · Korea travel guides</title>'
            f"<link>{BASE}/guides/</link><description>{esc(CFG['description'])}</description><language>en</language>{items}</channel></rss>\n")


# ---------------------------------------------------------------- build

def write(rel, text):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build():
    posts = load_posts()
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT / "static")
    write("index.html", page_home(posts))
    write("planner/index.html", page_planner(posts))
    write("guides/index.html", page_guides(posts))
    write("destinations/index.html", page_destinations(posts))
    for c in DEST["cities"]:
        write(f"destinations/{c['id']}/index.html", page_city(c, [p for p in posts if c["id"] in p["cities"]]))
    for t in TOPIC_NAMES:
        tp = [p for p in posts if t in p["topics"]]
        if tp:
            write(f"guides/topic/{t}/index.html", page_topic(t, tp, posts))
    for p in posts:
        write(f"guides/{p['slug']}/index.html", page_post(p, posts))
    contact = f'Email <a href="mailto:{esc(CFG["contact_email"])}">{esc(CFG["contact_email"])}</a>.' if CFG.get("contact_email") else "Contact details will be listed here soon."
    write("about/index.html", page_simple("about", "About Seoulmate", "Who makes Seoulmate and how we write our Korea travel guides.", ABOUT, "about"))
    write("privacy/index.html", page_simple("privacy", "Privacy policy", "How Seoulmate handles your data.", PRIVACY.format(date=dt.date.today().isoformat(), contact=contact)))
    write("disclosure/index.html", page_simple("disclosure", "Affiliate disclosure", "How affiliate links work on Seoulmate.", DISCLOSURE))
    write("404.html", layout("Page not found", "This page doesn't exist.", "/404.html",
                             '<div class="page-h"><h1>We couldn\'t find that page.</h1><p>Try the <a href="/guides/">travel guides</a> or <a href="/planner/">build an itinerary</a>.</p></div>'))
    write("sitemap.xml", sitemap(posts))
    write("feed.xml", rss(posts))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    log(f"빌드 완료: 글 {len(posts)}개")
    return posts


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def publish():
    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode == 0:
        log("바뀐 내용 없음, 업로드 안 함")
        return
    r = git("commit", "-m", f"Daily guides {dt.date.today().isoformat()}")
    if r.returncode:
        log("커밋 실패: " + (r.stderr or r.stdout).strip())
        return
    if not git("remote").stdout.strip():
        log("GitHub 저장소(remote)가 아직 연결되지 않아 업로드는 건너뜀")
        return
    r = git("push")
    log("업로드 완료 (Vercel이 1~2분 안에 사이트를 갱신해요)" if r.returncode == 0 else "업로드 실패: " + r.stderr.strip())


if __name__ == "__main__":
    args = set(sys.argv[1:])
    try:
        if "--import" in args or "--publish" in args:
            n = import_posts()
            log(f"새 글 {n}개 가져옴")
        build()
        if "--publish" in args:
            publish()
    except Exception as e:  # keep a trace in the log for the scheduled run
        log(f"오류: {e!r}")
        raise

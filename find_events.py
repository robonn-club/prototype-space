#!/usr/bin/env python3
"""The weekly event finder: propose new listings from organisers' own calendars.

Every Sunday the "Find events" workflow runs this script. It reads the calendars
and event lists named under `sources:` in guide/events.yml, drops everything that
is already listed, already proposed, over, off-topic, outside Bonn or not open to
students, reads each remaining event's own page for the details a card shows,
and adds what is left to guide/events.yml. The workflow then opens a pull request
for a person to review: nothing reaches the site without a merge.

    python3 find_events.py                 show what would be proposed
    python3 find_events.py --write         add the proposals to guide/events.yml
    python3 find_events.py --report FILE   also write the summary to FILE

A proposal deleted from the pull request is not proposed again: everything the
finder proposes is remembered in guide/events-seen.yml.
"""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin, urlsplit, urlunsplit, parse_qsl, urlencode
from zoneinfo import ZoneInfo

import yaml

import events as ev

ROOT = Path(__file__).parent.resolve()
EVENTS = ROOT / "guide" / "events.yml"
SEEN = ROOT / "guide" / "events-seen.yml"
BERLIN = ZoneInfo("Europe/Berlin")
AGENT = "Mozilla/5.0 (X11; Linux x86_64) prototype-space-event-finder (+https://github.com/robonn-club/prototype-space)"

# Places in and around Bonn: an event elsewhere is not proposed (fairs further
# afield are added by hand, on step 6's terms).
NEAR = re.compile(r"\b(bonn|sankt augustin|st\. augustin|siegburg|hennef|rheinbach|königswinter|"
                  r"bad godesberg|beuel|rhein-sieg|poppelsdorf|endenich|online|zoom|webex|hybrid|"
                  r"digitalhub|cityhub|rheinhub|enacom|b-it|h-brs)\b", re.IGNORECASE)

# Venues the organisers use, by a word from their address or name. The card shows
# the venue and the city, never the street.
VENUES = [
    (r"am hauptbahnhof 6|cityhub", "DIGITALHUB.DE CITYHUB, Bonn (at the main station)"),
    (r"rheinwerkallee|rheinhub", "DIGITALHUB.DE RHEINHUB, Bonn"),
    (r"propsthof|brühler str|transfer center enacom", "Transfer Center enaCom, Bonn"),
    (r"hirzebruch|\bb-it\b", "b-it building, Poppelsdorf campus, Bonn"),
    (r"grantham|campus sankt augustin|sankt augustin", "H-BRS campus, Sankt Augustin"),
    (r"dechenstr|rektorat", "Uni Bonn Rektorat, Bonn"),
    (r"martin-luther-king|sprinteins", "SprintEins office, Bonn"),
    (r"kennedyallee 18|makerspace", "MakerSpace Bonn"),
    (r"digitalhub", "DIGITALHUB.DE, Bonn"),
]
ONLINE = re.compile(r"\b(online|zoom|webex|virtual|virtuell|livestream)\b", re.IGNORECASE)

# What a listing is about, read from its title, description and the organiser's
# own topic field. An event that matches none of these is not proposed.
TOPIC_WORDS = {
    "ai": r"\b(ai|ki|künstliche[nr]? intelligenz|artificial intelligence|machine learning|maschinelle[sn]? lernen|"
          r"deep learning|llms?|genai|generative|agentic|neural)\b",
    "robotics": r"robot|embodied|drohne|drone|autonomous|autonome",
    "making": r"3d[- ]?(druck|print)|laser|\bcnc\b|löten|solder|elektronik|electronics|arduino|raspberry|"
              r"freecad|\bcad\b|maker|werkstatt|fräse",
    "software": r"hackathon|software|coding|programmier|python|\bcode\b",
    "design": r"design thinking|product design|produktdesign|prototyp|use case|ideation|visual thinking|"
              r"user experience|\bux\b",
    "founding": r"start-?ups?\b|gründ|founder|entrepreneur|pitch|business model|geschäftsmodell|financing|"
                r"finanzierung|venture|accelerator|selbstständig|selbständig|ideenwettbewerb|ideas competition",
    "ip": r"patent|intellectual property|\bip\b|schutzrecht|trademark|copyright|urheberrecht|licensing",
}

# Kinds of event, by the first pattern that matches the title.
FORMAT_WORDS = [
    ("hackathon", r"hackathon"),
    ("competition", r"wettbewerb|competition|\bcup\b|challenge"),
    ("pitch night", r"pitch"),
    ("meetup", r"meet ?up|stammtisch|treff|breakfast|frühstück|summit"),
    ("course", r"\bkurs|\bcourse|summer school|spring school|winter school"),
    ("webinar", r"webinar"),
    ("workshop", r"workshop"),
    ("talk", r"\btalk\b|vortrag|lecture|keynote|info session|infoveranstaltung"),
    ("fair", r"forum|\bfair\b|messe|expo"),
]
GERMAN_MONTHS = {m: i for i, m in enumerate(
    ["januar", "februar", "märz", "april", "mai", "juni", "juli", "august", "september", "oktober",
     "november", "dezember"], 1)}
LANGUAGES = {"englisch": "English", "english": "English", "deutsch": "German", "german": "German"}
STUDENTS = re.compile(r"student|studierende|all interested|alle interessierten|everyone|alle", re.IGNORECASE)
STOPWORDS = {"the", "a", "an", "of", "to", "and", "for", "in", "on", "with", "your", "you", "mit", "der",
             "die", "das", "und", "für", "im", "am", "zu", "ihr", "dein", "part", "teil"}


# --- fetching and reading -------------------------------------------------------

def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept-Language": "en,de;q=0.8"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                return response.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(3)
    return ""


def text_of(fragment: str) -> str:
    """Visible text of an HTML fragment, on one line."""
    fragment = re.sub(r"<br\s*/?>|</p>|</li>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def tidy(title: str) -> str:
    """A title as a title: 'FEMALE FOUNDERS SUMMIT 2027' becomes 'Female Founders Summit 2027'."""
    letters = [c for c in title if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.8:
        return " ".join(w if len(w) <= 3 and w.isupper() else w.capitalize() for w in title.split())
    return title


def clean_url(url: str) -> str:
    """The same address without tracking parameters or a trailing slash."""
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.startswith(("utm_", "aff", "recId", "recSource",
                                                                             "searchId", "eventOrigin"))]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


@dataclass
class Found:
    """One event as an organiser's calendar or page describes it."""
    title: str
    url: str
    start: dt.datetime | dt.date
    end: dt.datetime | dt.date | None = None
    location: str = ""
    description: str = ""
    organiser: str = ""
    source: str = ""
    details: dict = field(default_factory=dict)    # read from the event's own page

    @property
    def day(self) -> dt.date:
        return self.start.date() if isinstance(self.start, dt.datetime) else self.start

    @property
    def last_day(self) -> dt.date:
        if self.end is None:
            return self.day
        return self.end.date() if isinstance(self.end, dt.datetime) else self.end


def parse_ics(text: str, organiser: str = "", source: str = "") -> list[Found]:
    """Events in an iCalendar file, with times in Bonn time."""
    lines: list[str] = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        if raw[:1] in (" ", "\t") and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    found, current, depth = [], None, 0
    for line in lines:
        if line == "BEGIN:VEVENT":
            current, depth = {}, 0
        elif line == "END:VEVENT" and current is not None:
            found.append(current)
            current = None
        elif current is not None and line.startswith("BEGIN:"):
            depth += 1                                      # an alarm inside the event
        elif current is not None and line.startswith("END:"):
            depth -= 1
        elif current is not None and depth == 0 and ":" in line:
            head, value = line.split(":", 1)
            name, *params = head.split(";")
            current[name.upper()] = (value, dict(p.split("=", 1) for p in params if "=" in p))

    def moment(prop):
        if not prop:
            return None
        value, params = prop
        if params.get("VALUE") == "DATE" or re.fullmatch(r"\d{8}", value):
            return dt.datetime.strptime(value[:8], "%Y%m%d").date()
        stamp = dt.datetime.strptime(value[:15], "%Y%m%dT%H%M%S")
        if value.endswith("Z"):
            return stamp.replace(tzinfo=dt.timezone.utc).astimezone(BERLIN)
        try:
            zone = ZoneInfo(params.get("TZID", "Europe/Berlin").strip('"'))
        except Exception:                                   # noqa: BLE001 — unknown zone name
            zone = BERLIN
        return stamp.replace(tzinfo=zone).astimezone(BERLIN)

    def unescape(value: str) -> str:
        value = (value.replace("\\n", "\n").replace("\\N", "\n").replace("\\,", ",")
                 .replace("\\;", ";").replace("\\\\", "\\"))
        return re.sub(r"\\([*_#\[\]()~`>-])", r"\1", value)    # Markdown escapes from Meetup

    out = []
    for item in found:
        start = moment(item.get("DTSTART"))
        if start is None or "SUMMARY" not in item:
            continue
        end = moment(item.get("DTEND"))
        if isinstance(end, dt.date) and not isinstance(end, dt.datetime):
            end = end - dt.timedelta(days=1)                # all-day ends are exclusive
        out.append(Found(
            title=tidy(text_of(unescape(item["SUMMARY"][0]))),
            url=unescape(item.get("URL", ("",))[0]).strip(),
            start=start, end=end,
            location=text_of(unescape(item.get("LOCATION", ("",))[0])),
            description=text_of(unescape(item.get("DESCRIPTION", ("",))[0])),
            organiser=organiser, source=source))
    return out


def read_enacom(page: str) -> dict:
    """The labelled fields on an enaCom event page: Location, Languages, Target groups, ..."""
    fields = {}
    for m in re.finditer(r'<div class="item-title">\s*<span>([^<]+)</span>\s*</div>\s*'
                         r'<div class="item-value">(.*?)</div>\s*</div>', page, re.S):
        label, value = m.group(1).strip(), m.group(2)
        fields[label] = text_of(value)
        if label.startswith("Registration"):
            link = re.search(r'href="([^"]+)"', value)
            if link:
                fields[label] = html.unescape(link.group(1))
    return fields


def read_hbrs_list(page: str, base: str) -> list[str]:
    return sorted({urljoin(base, h) for h in re.findall(r'href="(/de/gruenden/termin/[^"#?]+)"', page)})


def german_date(text: str) -> list[dt.date]:
    return [dt.date(int(y), GERMAN_MONTHS[m.lower()], int(d)) for d, m, y in re.findall(
        r"(\d{1,2})\.\s*(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\s+(\d{4})",
        text)]


def read_hbrs_event(page: str, url: str, organiser: str, source: str) -> Found | None:
    """An H-BRS event page: title, then Datum, Zeit and Standort in its info box."""
    title = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    box = {m.group(1): text_of(m.group(2)) for m in re.finditer(
        r'<p class="infobox-item__title">\s*<i[^>]*></i>\s*(Datum|Zeit|Standort)\s*</p>\s*'
        r'<p class="h\d">(.*?)</p>', page, re.S)}
    days = german_date(box.get("Datum", ""))
    if not title or not days:
        return None
    times = re.findall(r"(\d{1,2}):(\d{2})", box.get("Zeit", ""))
    start: dt.datetime | dt.date = days[0]
    end: dt.datetime | dt.date | None = days[-1] if len(days) > 1 else None
    if times and len(days) == 1:
        start = dt.datetime(days[0].year, days[0].month, days[0].day, int(times[0][0]), int(times[0][1]), tzinfo=BERLIN)
        if len(times) > 1:
            end = dt.datetime(days[0].year, days[0].month, days[0].day, int(times[1][0]), int(times[1][1]), tzinfo=BERLIN)
    body = page[title.end():]
    stop = body.find("Kontakt")
    body = body[:stop] if stop > 0 else body
    paragraphs = [text_of(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", body, re.S)]
    description = " ".join(p for p in paragraphs if len(p) > 60)[:1500]
    free = re.search(r"eintritt ist frei|kostenlos|kostenfrei|teilnahme ist frei", text_of(body), re.IGNORECASE)
    return Found(title=tidy(text_of(title.group(1))), url=url, start=start, end=end,
                 location=box.get("Standort", ""), description=description,
                 organiser=organiser, source=source,
                 details={"cost": "Free" if free else "not stated",
                          "language": "not stated (page in German)"})


def read_digitalhub(page: str, base: str, organiser: str, source: str) -> list[Found]:
    """DIGITALHUB.DE's event cards: title, subtitle, start, end and hub, then the link."""
    found = {}
    for chunk in page.split('class="div-block-448')[1:]:
        title = re.search(r'textblock bold">(.*?)</div>', chunk, re.S)
        sub = re.search(r'textblock">(.*?)</div>', chunk, re.S)
        values = [text_of(v) for v in re.findall(r'textblock center bold">(.*?)</div>', chunk, re.S)]
        link = re.search(r'href="(/en/eventkalender-intern/[^"#?]+)"', chunk)
        stamps = [v for v in values if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4} \d{1,2}:\d{2}", v)]
        if not (title and link and stamps):
            continue
        parse = [dt.datetime.strptime(s, "%d.%m.%Y %H:%M").replace(tzinfo=BERLIN) for s in stamps]
        place = next((v for v in values if v not in stamps), "")
        url = urljoin(base, link.group(1))
        found[url] = Found(title=tidy(text_of(title.group(1))), url=url, start=parse[0],
                           end=parse[1] if len(parse) > 1 else None,
                           location=f"{place}, Bonn" if place else "Bonn",
                           description=text_of(sub.group(1)) if sub else "",
                           organiser=organiser, source=source)
    return list(found.values())


def collect(sources: list[dict], log: list[str]) -> list[Found]:
    """Everything every configured source currently lists."""
    out = []
    for source in sources:
        name = source["name"]
        organiser = source.get("organiser", name)
        try:
            if source.get("calendar"):
                items = parse_ics(fetch(source["calendar"]), organiser, name)
            elif source.get("reader") == "hbrs":
                items = []
                for url in read_hbrs_list(fetch(source["url"]), source["url"]):
                    item = read_hbrs_event(fetch(url), url, organiser, name)
                    if item:
                        items.append(item)
            elif source.get("reader") == "digitalhub":
                items, seen_pages = [], set()
                for n in range(1, 5):
                    url = source["url"] + ("" if n == 1 else f"?70d60845_page={n}")
                    batch = read_digitalhub(fetch(url), source["url"], organiser, name)
                    fresh = [i for i in batch if i.url not in seen_pages]
                    if not fresh:
                        break
                    seen_pages.update(i.url for i in fresh)
                    items += fresh
            else:
                continue
        except Exception as error:                          # noqa: BLE001 — one source down is not fatal
            log.append(f"- **{name}**: could not be read ({type(error).__name__}: {str(error)[:80]})")
            continue
        if items:
            note = ""
        elif source.get("calendar"):
            note = " (its calendar lists nothing right now)"
        else:
            note = " (nothing found: if the organiser's page lists events, its layout may have changed)"
        log.append(f"- **{name}**: {len(items)} events read{note}")
        for item in items:
            item.details.setdefault("reader", source.get("reader", ""))
        out += items
    return out


# --- deciding -------------------------------------------------------------------

def words(title: str) -> set[str]:
    title = re.sub(r"start-up", "startup", title.lower())
    return {w for w in re.findall(r"[a-zäöüß0-9]+", title) if w not in STOPWORDS and not re.fullmatch(r"\d+", w)}


def same_title(a: str, b: str) -> bool:
    x, y = words(a), words(b)
    return bool(x and y) and len(x & y) / min(len(x), len(y)) >= 0.5


def listed(item: Found, entries: list[dict], urls: set[str]) -> bool:
    """Whether an event is already on the list: by its address, or by its title on one of
    the days an entry names (its date, end, deadline or announced dates)."""
    if item.url and clean_url(item.url) in urls:
        return True
    for entry in entries:
        days = {entry.get(k) for k in ("date", "end", "deadline")} | set(entry.get("next") or [])
        if item.day in days and same_title(item.title, entry["title"]):
            return True
    return False


def topics(item: Found) -> list[str]:
    haystack = " ".join([item.title, item.description[:800], item.details.get("Topic", "")])
    return [t for t, pattern in TOPIC_WORDS.items() if re.search(pattern, haystack, re.IGNORECASE)]


def kind(item: Found) -> str:
    for name, pattern in FORMAT_WORDS:
        if re.search(pattern, item.title, re.IGNORECASE):
            return name
    given = item.details.get("Event format", "").lower()
    return {"workshop": "workshop", "talk": "talk"}.get(given, "meetup")


def place(raw: str) -> str:
    """A venue and a city, never a street."""
    online = bool(ONLINE.search(raw))
    for pattern, name in VENUES:
        if re.search(pattern, raw, re.IGNORECASE):
            return name + (", and online" if online else "")
    if online:
        return "Online"
    parts = [p.strip() for p in re.split(r"[,(|]", raw) if p.strip()]
    keep = [p for p in parts if not ev.ADDRESS.search(p) and not re.search(r"\d", p)]
    text = ", ".join(keep[:2]) or "Bonn"
    return text if re.search(r"bonn|augustin|siegburg|hennef", text, re.IGNORECASE) else f"{text}, Bonn"


def summary(item: Found) -> str:
    """The first plain sentence of the description that fits on a card, or a pointer."""
    text = item.description
    for prefix in (item.title, item.organiser, item.organiser.split(" (")[0]):
        if prefix and text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].lstrip(" :–-|")
    # A sentence ends at . ! or ? before a capital letter, but not after a number:
    # "Am 4. März" is one sentence.
    sentences = re.split(r"(?<=[^\d\s][.!?])\s+(?=[A-ZÄÖÜ])", text)
    for s in sentences:
        s = s.strip()
        if (30 <= len(s) <= 175 and s.endswith(".") and not ev.EMAIL.search(s)
                and not ev.PHONE.search(s) and not ev.ADDRESS.search(s)):
            return s
    for s in sentences:
        s = s.strip().rstrip("!") + "." if s.strip().endswith("!") else ""
        if 30 <= len(s) <= 175 and not ev.ADDRESS.search(s):
            return s
    return "See the organiser's page for the details."


def entry(item: Found, day: dt.date) -> dict:
    """A proposal in the shape of guide/events.yml."""
    d = item.details
    out = {"title": item.title, "organiser": item.organiser, "topics": topics(item), "format": kind(item)}
    location = d.get("Location") or item.location
    out["place"] = place(location)
    out["region"] = "online" if out["place"] == "Online" else "bonn"
    out["date"] = item.day
    if item.last_day != item.day:
        out["end"] = item.last_day
    if isinstance(item.start, dt.datetime) and item.last_day == item.day:
        span = item.start.strftime("%H:%M")
        if isinstance(item.end, dt.datetime) and item.end > item.start:
            span += "–" + item.end.strftime("%H:%M")
        out["time"] = span
    else:
        out["time"] = None
    if d.get("reader") == "enacom":
        price = d.get("Admission price", "")
        out["cost"] = "Free" if re.search(r"free|kostenlos|frei", price, re.IGNORECASE) else (price or "not stated")
        langs = [LANGUAGES[w] for w in re.findall(r"[A-Za-z]+", d.get("Languages", "").lower()) if w in LANGUAGES]
        out["language"] = " and ".join(dict.fromkeys(langs)) if langs else "not stated"
        if d.get("Target groups"):
            out["who"] = d["Target groups"]
        if d.get("Registration/Ticket", "").startswith("http"):
            out["register"] = clean_url(d["Registration/Ticket"])
    else:
        out["cost"] = d.get("cost")
        out["language"] = d.get("language")
    out["source"] = item.url
    out["checked"] = day
    out["summary"] = summary(item)
    return out


def decide(found: list[Found], entries: list[dict], seen: list[dict], skip: list[str], day: dt.date,
           enrich) -> tuple[list[tuple[Found, dict]], dict[str, list[str]]]:
    """Which found events to propose, and why each other one is not."""
    urls = {clean_url(str(e.get(k))) for e in entries for k in ("source", "register", "more")
            if str(e.get(k) or "").startswith("http")}
    remembered = {clean_url(s["url"]) for s in seen}
    reasons: dict[str, list[str]] = {}
    proposals: list[tuple[Found, dict]] = []
    closed: list[Found] = []            # not open to students, as one organiser's page says

    def drop(why: str, item: Found) -> None:
        reasons.setdefault(why, []).append(f"{item.title} ({item.day})")

    for item in sorted(found, key=lambda i: (i.day, i.details.get("reader") != "enacom", i.title)):
        if item.last_day < day:
            drop("over", item)
        elif listed(item, entries, urls):
            drop("already listed", item)
        elif item.url and clean_url(item.url) in remembered:
            drop("proposed before", item)
        elif any(word.lower() in item.title.lower() for word in skip):
            drop("matched a skip word", item)
        elif not topics(item):
            drop("off-topic", item)
        elif any(same_title(item.title, f.title) and item.day == f.day for f, _ in proposals):
            drop("found twice", item)
        elif any(same_title(item.title, f.title) and item.day == f.day for f in closed):
            drop("not open to students", item)
        else:
            enrich(item)
            location = item.details.get("Location") or item.location
            if location and not NEAR.search(location):
                drop("outside Bonn", item)
                continue
            audience = item.details.get("Target groups", "")
            if audience and not STUDENTS.search(audience):
                drop("not open to students", item)
                closed.append(item)
                continue
            data = entry(item, day)
            problems = ev.check(data, day)
            if problems:
                drop(f"could not be filled in ({problems[0]})", item)
                continue
            proposals.append((item, data))
    return proposals, reasons


def enrich_from_page(item: Found) -> None:
    """Read the event's own page for what its calendar entry leaves out."""
    if item.details.get("reader") == "enacom" and item.url:
        try:
            item.details.update(read_enacom(fetch(item.url)))
        except Exception:                                   # noqa: BLE001 — propose with what we have
            pass


# --- writing --------------------------------------------------------------------

ORDER = ["title", "organiser", "topics", "format", "region", "date", "end", "time", "place", "cost", "who",
         "language", "register", "source", "checked", "summary"]


def as_yaml(data: dict) -> str:
    def value(v):
        if v is None:
            return "~"
        if isinstance(v, dt.date):
            return v.isoformat()
        if isinstance(v, list):
            return "[" + ", ".join(v) + "]"
        if re.fullmatch(r"[a-z][a-z ]*", v):          # tokens such as `meetup` or `not stated`
            return v
        return json.dumps(v, ensure_ascii=False)
    lines = [f"  - {k}: {value(data[k])}" if i == 0 else f"    {k}: {value(data[k])}"
             for i, k in enumerate(k for k in ORDER if k in data)]
    return "\n".join(lines) + "\n"


def insert(text: str, block: str) -> str:
    """Put new entries at the end of the events list, before the sources and their comments."""
    lines = text.splitlines(keepends=True)
    at = next(i for i, line in enumerate(lines) if line.startswith("sources:"))
    while at > 0 and (lines[at - 1].startswith("#") or not lines[at - 1].strip()):
        at -= 1
    return "".join(lines[:at]).rstrip("\n") + "\n\n" + block + "\n" + "".join(lines[at:])


def report(proposals, reasons, log, day: dt.date) -> str:
    out = [f"# New events found, {day.isoformat()}", ""]
    if proposals:
        out += [f"The weekly finder read the organisers' own calendars and proposes **{len(proposals)} new "
                f"listing{'s' if len(proposals) != 1 else ''}**, added to the end of the events list in "
                "`guide/events.yml`.", "",
                "**To review:** open each event's page, rewrite the summary in plain English, check place, "
                "cost and language, and delete any proposal that does not suit students building a "
                "prototype. Then merge. A deleted proposal is remembered and not proposed again.", "",
                f"## Proposed ({len(proposals)})", ""]
        for item, data in proposals:
            when = ev.day_name(data["date"]) + (f", {data['time']}" if data.get("time") else "")
            out.append(f"- [ ] **{data['title']}** · {when} · {data['place']} · {item.source} · "
                       f"[event page]({data['source']})")
    else:
        out += ["Nothing new this week."]
    out += ["", "## Not proposed", ""]
    for why, items in sorted(reasons.items(), key=lambda kv: -len(kv[1])):
        out.append(f"<details><summary>{len(items)} {why}</summary>\n\n" + "\n".join(f"- {i}" for i in items)
                   + "\n\n</details>")
    out += ["", "## Sources read", ""] + log
    out += ["", "Add an organiser's calendar or change the skip words under `sources:` and `finder_skip:` "
            "in `guide/events.yml`; see CONTRIBUTING.md, \"Adding an event\"."]
    return "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    day = ev.today()
    raw = yaml.safe_load(EVENTS.read_text(encoding="utf-8")) or {}
    listings, sources, problems = ev.load(EVENTS, day)
    if problems:
        for p in problems:
            print(f"error: guide/{p}", file=sys.stderr)
        return 2
    seen_data = yaml.safe_load(SEEN.read_text(encoding="utf-8")) if SEEN.exists() else None
    seen = (seen_data or {}).get("seen") or []
    readable = [s for s in sources if s.get("calendar") or s.get("reader") in ("hbrs", "digitalhub")]

    log: list[str] = []
    found = collect(readable, log)
    proposals, reasons = decide(found, raw.get("events") or [], seen, raw.get("finder_skip") or [], day,
                                enrich_from_page)
    text = report(proposals, reasons, log, day)
    print(text)
    if "--report" in argv:
        Path(argv[argv.index("--report") + 1]).write_text(text, encoding="utf-8")

    if "--write" in argv and proposals:
        block = (f"  # --- proposed by the weekly finder on {day.isoformat()}: check each against its page,\n"
                 f"  # rewrite the summary, fix place, cost and language, delete what does not fit ---\n\n"
                 + "\n".join(as_yaml(data) for _, data in proposals))
        EVENTS.write_text(insert(EVENTS.read_text(encoding="utf-8"), block), encoding="utf-8")
        keep = [s for s in seen if dt.date.fromisoformat(str(s["date"])) >= day - dt.timedelta(days=31)]
        keep += [{"url": clean_url(data["source"]), "date": data["date"].isoformat(), "title": data["title"]}
                 for _, data in proposals]
        SEEN.write_text(
            "# Written by find_events.py: every event the weekly finder has proposed, so a proposal\n"
            "# deleted from its pull request is not proposed again. Entries go a month after the event.\n\n"
            + yaml.safe_dump({"seen": keep}, allow_unicode=True, sort_keys=False), encoding="utf-8")
        _, _, problems = ev.load(EVENTS, day)
        if problems:
            for p in problems:
                print(f"error after writing: guide/{p}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

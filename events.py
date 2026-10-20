"""Workshops and events: load, check, expire, render and export.

The listings live in guide/events.yml, one entry per event or recurring
programme, each copied from the organiser's own page with the date it was
checked there. This module turns that file into the events page, the
"what's on" lists on the front page, the step pages and the Bonn page,
step 6's dates to show a build at, a calendar file, and the weekly review.

Nothing here edits the file. A dated event disappears from the site the day
after it ends because every build compares it with today's date in Bonn, and
the site is rebuilt every night; the review (`python3 build.py --events`)
tells a maintainer what to delete, recheck or fill in.
"""

from __future__ import annotations

import datetime as dt
import html
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

BERLIN = ZoneInfo("Europe/Berlin")

TOPICS = {
    "ai": "AI",
    "robotics": "Robotics",
    "making": "Making",
    "software": "Software & data",
    "design": "Design thinking",
    "founding": "Founding",
    "ip": "Patents & IP",
    "showcase": "Show your build",
}
FORMATS = {"workshop", "talk", "meetup", "hackathon", "competition", "consultation",
           "course", "open house", "fair", "pitch night", "webinar", "team"}
REGIONS = {"bonn": "Bonn and region", "online": "Online", "further": "Further afield"}
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# Which topics each step of the guide is about, for its "workshops and events" box.
STEP_TOPICS = {
    "plan": ["design", "founding"],
    "simulate": ["ai", "software"],
    "parts": ["making"],
    "build": ["making", "robotics"],
    "test": ["robotics", "making"],
    "after": ["founding", "ip"],
}

REQUIRED = {"title", "organiser", "topics", "format", "region", "place", "cost", "source",
            "checked", "summary"}
# Kept in the data for the calendar file and for maintainers, not shown on the cards.
OPTIONAL = {"date", "end", "deadline", "time", "recurring", "next", "weekday", "note", "more",
            "who", "register", "language"}
MAY_BE_EMPTY = {"cost", "who", "language", "register", "time"}   # ~ means "not checked yet"

# How old a check may get before the review asks for another look.
RECHECK_SOON_DAYS = 7         # a dated event starting within two weeks
RECHECK_RECURRING_DAYS = 90   # a recurring programme
SOON_DAYS = 14

# The repository holds no personal data and no postal addresses (CONTRIBUTING.md).
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"\+?\d[\d ()/-]{7,}\d")
ADDRESS = re.compile(r"\b\d{5}\b|(straße|strasse|str\.|allee|weg|platz|gasse|ring|ufer)\s+\d+",
                     re.IGNORECASE)
URL = re.compile(r"^https?://\S+$")


def today() -> dt.date:
    """Today in Bonn. PROTOTYPE_TODAY=YYYY-MM-DD pretends it is another day."""
    forced = os.environ.get("PROTOTYPE_TODAY")
    return dt.date.fromisoformat(forced) if forced else dt.datetime.now(BERLIN).date()


def esc(text) -> str:
    return html.escape(str(text), quote=True)


def slug(text: str) -> str:
    text = text.lower().replace("ü", "ue").replace("ö", "oe").replace("ä", "ae").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


@dataclass
class Event:
    data: dict
    line: int
    id: str = ""
    dates: list = field(default_factory=list)   # upcoming occurrences, for recurring entries

    def __getitem__(self, key):
        return self.data.get(key)

    @property
    def recurring(self) -> bool:
        return "recurring" in self.data

    @property
    def start(self) -> dt.date | None:
        return self.data.get("date")

    @property
    def finish(self) -> dt.date | None:
        return self.data.get("end") or self.data.get("date")

    def past(self, day: dt.date) -> bool:
        return not self.recurring and self.finish < day

    def next_date(self) -> dt.date | None:
        return self.start if not self.recurring else (self.dates[0] if self.dates else None)



# --- loading and checking ---------------------------------------------------

def load(path: Path, day: dt.date) -> tuple[list[Event], list[dict], list[str]]:
    """Every entry in events.yml, checked; occurrences computed for `day`."""
    text = path.read_text(encoding="utf-8")
    raw = yaml.safe_load(text) or {}
    problems: list[str] = []
    where = path.name
    lines = text.splitlines()

    def line_of(title: str) -> int:
        for i, line in enumerate(lines, 1):
            if line.strip().startswith("- title:") and title in line:
                return i
        return 0

    events, seen = [], set()
    for data in raw.get("events") or []:
        title = str(data.get("title", "?"))
        event = Event(data, line_of(title))
        at = f"{where}:{event.line} ({title})"
        messages = check(data, day)
        problems += [f"{at}: {m}" for m in messages]
        if any(m.startswith("missing") for m in messages):
            continue
        event.id = slug(title + ("" if event.recurring else f"-{data.get('date')}"))
        if event.id in seen:
            problems.append(f"{at}: listed twice")
        seen.add(event.id)
        if event.recurring:
            event.dates = occurrences(data, day)
        events.append(event)

    sources = raw.get("sources") or []
    for source in sources:
        if not URL.match(str(source.get("url", ""))):
            problems.append(f"{where}: source {source.get('name')!r} needs a url")
        if "calendar" in source and not URL.match(str(source["calendar"])):
            problems.append(f"{where}: source {source.get('name')!r}: `calendar` must be a web address")
    return events, sources, problems


def check(data: dict, day: dt.date) -> list[str]:
    out = []
    keys = set(data)
    if missing := REQUIRED - keys:
        return [f"missing {', '.join(sorted(missing))}"]
    if unknown := keys - REQUIRED - OPTIONAL:
        out.append(f"unknown field {', '.join(sorted(unknown))} (see CONTRIBUTING.md)")
    if ("date" in data) == ("recurring" in data):
        out.append("needs either `date` (one event) or `recurring` (a programme), not both")
    if "date" in data and "time" not in data:
        out.append("a dated event needs `time` (~ if not checked yet)")
    for key in ("date", "end", "deadline", "checked"):
        if key in data and not isinstance(data[key], dt.date):
            out.append(f"`{key}` must be a date like 2026-11-04")
    if isinstance(data.get("end"), dt.date) and isinstance(data.get("date"), dt.date) \
            and data["end"] < data["date"]:
        out.append("`end` is before `date`")
    if isinstance(data.get("checked"), dt.date) and data["checked"] > day:
        out.append("`checked` is in the future")
    for key in ("next", "weekday"):
        if key in data and "recurring" not in data:
            out.append(f"`{key}` belongs to recurring programmes")
    if "next" in data and not all(isinstance(d, dt.date) for d in data["next"] or []):
        out.append("`next` must be a list of dates")
    if "weekday" in data and data["weekday"] not in WEEKDAYS:
        out.append(f"`weekday` must be one of {', '.join(WEEKDAYS)}")
    topics = data.get("topics") or []
    if not topics or not set(topics) <= set(TOPICS):
        out.append(f"`topics` must come from {', '.join(TOPICS)}")
    if data.get("format") not in FORMATS:
        out.append(f"`format` must be one of {', '.join(sorted(FORMATS))}")
    if data.get("region") not in REGIONS:
        out.append(f"`region` must be one of {', '.join(REGIONS)}")
    for key in ("source", "more"):
        if key in data and not URL.match(str(data[key])):
            out.append(f"`{key}` must be a web address")
    for key, value in data.items():
        if value is None and key not in MAY_BE_EMPTY:
            out.append(f"`{key}` is empty")
        if not isinstance(value, str) or URL.match(value):
            continue
        if EMAIL.search(value) or PHONE.search(value):
            out.append(f"`{key}` contains contact details; link the organiser's page instead")
        if ADDRESS.search(value):
            out.append(f"`{key}` looks like a postal address; give the venue and the city")
    summary = str(data.get("summary") or "")
    if not summary.endswith(".") or len(summary) > 180:
        out.append("`summary` is one sentence, ending with a full stop, under 180 characters")
    return out


def occurrences(data: dict, day: dt.date, count: int = 3) -> list[dt.date]:
    """The next dates of a recurring programme: announced ones, or computed weekly."""
    if data.get("weekday"):
        ahead = (WEEKDAYS.index(data["weekday"]) - day.weekday()) % 7
        first = day + dt.timedelta(days=ahead)
        return [first + dt.timedelta(weeks=i) for i in range(count)]
    return sorted(d for d in data.get("next") or [] if d >= day)


def upcoming(events: list[Event], day: dt.date, *, topics=None, regions=None,
             dated=True, recurring=True) -> list[Event]:
    """Events not yet over, in date order; recurring ones after, by next date."""
    chosen = []
    for e in events:
        if e.past(day) or (e.recurring and not recurring) or (not e.recurring and not dated):
            continue
        if topics and not set(topics) & set(e["topics"]):
            continue
        if regions and e["region"] not in regions:
            continue
        chosen.append(e)
    far = dt.date.max
    return sorted(chosen, key=lambda e: (e.recurring, e.next_date() or far, e["title"]))


# --- words for dates and values ---------------------------------------------

def day_name(d: dt.date, year: bool = True) -> str:
    return d.strftime("%a %-d %b" + (" %Y" if year else ""))


def span(e: Event, year: bool = True) -> str:
    """'Thu 15 Oct 2026', or 'Mon 16 – Sun 22 Nov 2026' for several days."""
    start, end = e.start, e.finish
    if start == end:
        return day_name(start, year)
    if (start.year, start.month) == (end.year, end.month):
        return f"{start.strftime('%a %-d')} – {day_name(end, year)}"
    return f"{day_name(start, False)} – {day_name(end, year)}"


def value(v) -> str:
    """What the organiser said, or plainly that it is missing."""
    if v is None:
        return "Not checked yet"
    if str(v).lower().startswith("not stated"):
        return "Not stated" + str(v)[len("not stated"):]
    return str(v)


def known(v) -> bool:
    """Whether a field holds something the organiser actually said."""
    return v is not None and not str(v).lower().startswith("not stated")


def when_text(e: Event, day: dt.date) -> str:
    if not e.recurring:
        time = f", {e['time']}" if known(e["time"]) else ""
        return span(e) + time
    text = e["recurring"]
    if e.dates:
        shown = ", ".join(day_name(d, False) for d in e.dates[:3])
        text += f". Next: {shown}"
    return text


# --- rendering ---------------------------------------------------------------

def date_block(e: Event) -> str:
    d = e.next_date()
    if d is None:
        return '<div class="ev-when"><span class="ev-day">↻</span><span class="ev-mon">Regular</span></div>'
    if not e.recurring and e.finish != e.start:
        day = f"{e.start.day}–{e.finish.day}" if e.start.month == e.finish.month else f"{e.start.day}+"
    else:
        day = str(d.day)
    label = "Next" if e.recurring else d.strftime("%a")
    return (f'<div class="ev-when"><span class="ev-day">{day}</span>'
            f'<span class="ev-mon">{d.strftime("%b")}</span><span class="ev-wd">{label}</span></div>')


def card(e: Event, day: dt.date) -> str:
    """One listing: when, what, where, the cost if the organiser states one, and a link
    to the event's own page. Everything else is on that page."""
    facts = [("When", when_text(e, day)), ("Where", e["place"])]
    if known(e["cost"]):
        facts.append(("Cost", e["cost"]))
    rows = "".join(f"<div><dt>{k}</dt><dd>{esc(v)}</dd></div>" for k, v in facts)
    flag = ""
    if e["deadline"]:
        flag = (f'<p class="ev-flag">Apply by {day_name(e["deadline"])}</p>' if e["deadline"] >= day
                else f'<p class="ev-flag ev-flag-closed">Applications closed on {day_name(e["deadline"])}</p>')
    kind = "ev-regular" if e.recurring else "ev-dated"
    return (f'<article class="ev {kind}" id="{e.id}">'
            f'<div class="ev-top">{date_block(e)}'
            f'<p class="ev-meta">{esc(e["format"].capitalize())} · {esc(e["organiser"])}</p></div>'
            f'<h3 class="ev-title"><a href="{esc(e["source"])}" rel="noopener">{esc(e["title"])}</a></h3>'
            f'<p class="ev-sum">{esc(e["summary"])}</p>{flag}'
            f'<dl class="ev-facts">{rows}</dl>'
            f'<a class="ev-btn" href="{esc(e["source"])}" rel="noopener" '
            f'aria-label="Page for {esc(e["title"])}">Page</a></article>')


def compact(e: Event, day: dt.date, link: str) -> str:
    """One line in a short list elsewhere on the site, pointing into the events page."""
    when = span(e, year=False) if not e.recurring else (
        f"Next {day_name(e.dates[0], False)}" if e.dates else "Regular")
    cost = str(e["cost"]) if known(e["cost"]) and len(str(e["cost"])) < 40 else None
    meta = " · ".join(x for x in (e["place"], cost) if x)
    return (f'<li><a class="wo" href="{esc(link)}#{e.id}">'
            f'<span class="wo-date">{esc(when)}</span>'
            f'<span class="wo-title">{esc(e["title"])}</span>'
            f'<span class="wo-meta">{esc(meta)}</span></a></li>')


def page(events: list[Event], sources: list[dict], day: dt.date, *, ics_href, repo: str) -> str:
    """The events page body: upcoming events, regular meetings and further afield, each as
    a grid of cards, then the organisers' pages the listings come from."""
    near = ("bonn", "online")
    dated = upcoming(events, day, regions=near, recurring=False)
    regular = upcoming(events, day, regions=near, dated=False)
    away = upcoming(events, day, regions=("further",))

    def grid(items, empty):
        if not items:
            return f'<p class="ev-none">{empty}</p>'
        return f'<div class="ev-grid">{"".join(card(e, day) for e in items)}</div>'

    sourced = "".join(f'<li><a href="{esc(s["url"])}" rel="noopener">{esc(s["name"])}</a></li>'
                      for s in sources)
    return f"""
## Upcoming events {{#upcoming}}

{grid(dated, "No dated events are listed right now; the regular meetings below still run.")}

## Regular meetings {{#regular}}

{grid(regular, "No regular meetings are listed right now.")}

## Further afield {{#further}}

Fairs and competitions outside Bonn to show a build at, reachable by train.

{grid(away, "Nothing further afield is listed right now.")}

## Resources {{#resources}}

<ul class="ev-sources">{sourced}</ul>

<p class="ev-origin">Every listing is copied from the organiser's own page.</p>
"""

def whatson(events: list[Event], day: dt.date, link: str, *, topics=None, regions=("bonn", "online"),
            limit: int = 4, recurring: bool = False) -> str:
    items = upcoming(events, day, topics=topics, regions=regions)
    if not recurring:
        items = [e for e in items if not e.recurring] or items
    return "".join(compact(e, day, link) for e in items[:limit])


def showcase(events: list[Event], day: dt.date, link: str, where: str) -> str:
    """Step 6's 'pick a date': fairs and competitions, wherever they are."""
    rows = []
    for e in upcoming(events, day, topics=["showcase"]):
        when = span(e) if not e.recurring else (e["recurring"].split(";")[0].split(",")[0])
        rows.append(f'<div class="date"><p class="d-when">{esc(when)}</p>'
                    f'<p class="d-what"><a href="{esc(link)}#{e.id}">{esc(e["title"])}</a>'
                    f'<span class="d-where">{esc(e["place"])}</span></p>'
                    f'<p class="d-good">{esc(e["summary"])}</p></div>')
    return f'<div class="dates">{"".join(rows)}</div>'


# --- calendar files -----------------------------------------------------------

TIME = re.compile(r"(\d{1,2}):(\d{2})\s*[–-]\s*(\d{1,2}):(\d{2})")


def ics(items: list[Event], day: dt.date, now: dt.datetime, site: str) -> str:
    """An iCalendar file. Times given as 'HH:MM–HH:MM' become timed events in
    Bonn time; anything else becomes an all-day event."""
    def text(s: str) -> str:
        return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

    def fold(line: str) -> str:
        out, data = [], line.encode("utf-8")
        while len(data) > 75:
            cut = 75 if not out else 74
            while (data[cut] & 0xC0) == 0x80:      # never split a UTF-8 character
                cut -= 1
            out.append(data[:cut].decode("utf-8"))
            data = data[cut:]
        out.append(data.decode("utf-8"))
        return "\r\n ".join(out)

    stamp = now.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Robonn//Prototype Space events//EN",
             "CALSCALE:GREGORIAN", "X-WR-CALNAME:Prototype Space · workshops and events in Bonn"]
    for e in items:
        dates = e.dates if e.recurring else [e.start]
        for i, d in enumerate(dates):
            match = TIME.search(str(e["time"] or e["recurring"] or ""))
            lines += ["BEGIN:VEVENT", f"UID:{e.id}-{d.isoformat()}@prototype-space", f"DTSTAMP:{stamp}"]
            if match and (e.recurring or e.start == e.finish):
                h1, m1, h2, m2 = map(int, match.groups())
                begin = dt.datetime(d.year, d.month, d.day, h1, m1, tzinfo=BERLIN)
                finish = dt.datetime(d.year, d.month, d.day, h2 % 24, m2, tzinfo=BERLIN)
                if finish <= begin:
                    finish += dt.timedelta(days=1)
                for key, moment in (("DTSTART", begin), ("DTEND", finish)):
                    lines.append(f"{key}:{moment.astimezone(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}")
            else:
                last = d if e.recurring else e.finish
                lines += [f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
                          f"DTEND;VALUE=DATE:{(last + dt.timedelta(days=1)).strftime('%Y%m%d')}"]
            about = [e["summary"]] + [f"{label}: {e[key]}" for label, key in
                                      (("Cost", "cost"), ("Who", "who"), ("Language", "language"))
                                      if known(e[key])]
            if e["register"]:
                about.append(f"Register: {e['register']}")
            about.append(f"Check before you go: {e['source']}")
            lines += [fold(f"SUMMARY:{text(e['title'])}"), fold(f"LOCATION:{text(e['place'])}"),
                      fold(f"DESCRIPTION:{text(chr(10).join(about))}"), fold(f"URL:{e['source']}"),
                      "END:VEVENT"]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


# --- the weekly review ---------------------------------------------------------

def report(events: list[Event], sources: list[dict], day: dt.date) -> tuple[str, bool]:
    """What a maintainer should do this week, as Markdown; True if anything at all."""
    sections: list[tuple[str, str, list[str]]] = []

    def at(e: Event) -> str:
        return f"**{e['title']}** ({span(e) if not e.recurring else 'recurring'}) · `guide/events.yml` line {e.line}"

    past = [e for e in events if e.past(day)]
    sections.append(("Delete: these have ended",
                     "They are already hidden on the site; deleting keeps the file short.",
                     [at(e) for e in past]))
    soon = [e for e in events if not e.recurring and not e.past(day)
            and (e.start - day).days <= SOON_DAYS and (day - e["checked"]).days > RECHECK_SOON_DAYS]
    sections.append(("Recheck: starting within two weeks",
                     "Open the organiser's page and confirm the date, time and registration still hold.",
                     [f"{at(e)}, last checked {e['checked']}: {e['source']}" for e in soon]))
    old = [e for e in events if e.recurring and (day - e["checked"]).days > RECHECK_RECURRING_DAYS]
    sections.append(("Recheck: recurring programmes not checked for three months", "",
                     [f"{at(e)}, last checked {e['checked']}: {e['source']}" for e in old]))
    empty = [e for e in events if e.recurring and not e.dates and e["next"] is not None]
    sections.append(("Update: announced dates have all passed",
                     "Add the next dates from the organiser's page, or remove `next`.",
                     [f"{at(e)}: {e['source']}" for e in empty]))
    closed = [e for e in events if e["deadline"] and e["deadline"] < day and not e.past(day)]
    sections.append(("Note: application deadline has passed",
                     "The site already says applications are closed; remove `deadline` if the page now says otherwise.",
                     [at(e) for e in closed]))
    def unchecked(e: Event) -> list[str]:
        return [k for k in ("time", "cost") if k in e.data and e[k] is None]

    gaps = [e for e in events if not e.past(day) and unchecked(e)]
    sections.append(("Fill in: fields not checked yet",
                     "A missing cost is left off the card, and a missing time leaves just the date.",
                     [f"{at(e)}: {', '.join(unchecked(e))}" for e in gaps]))

    live = upcoming(events, day)
    horizon = day + dt.timedelta(days=60)
    thin = [TOPICS[t] for t in TOPICS if t != "showcase" and not any(
        t in e["topics"] and (e.recurring or e.start <= horizon) for e in live)]
    counts = ", ".join(f"{TOPICS[t]} {sum(t in e['topics'] for e in live)}" for t in TOPICS)

    out = [f"# Events review, {day.isoformat()}", "",
           f"{len(live)} listings are live: {sum(not e.recurring for e in live)} dated and "
           f"{sum(e.recurring for e in live)} recurring. By topic: {counts}.", ""]
    actionable = False
    for title, why, items in sections:
        if not items:
            continue
        actionable = True
        out += [f"## {title} ({len(items)})", ""] + ([why, ""] if why else [])
        out += [f"- [ ] {i}" for i in items] + [""]
    if thin:
        out += ["## Thin coverage", "",
                f"Nothing in the next 60 days for: {', '.join(thin)}. Worth a look at the sources below.", ""]
    out += ["## Where to look for new events", ""]
    out += [f"- [{s['name']}]({s['url']})" + (f": {s['note']}" if s.get("note") else "") for s in sources]
    out += ["", "Copy only what the organiser's page says, and set `checked` to today. "
            "See CONTRIBUTING.md, \"Adding an event\"."]
    if not actionable:
        out.insert(4, "Nothing to delete, recheck or fill in this week.\n")
    return "\n".join(out) + "\n", actionable

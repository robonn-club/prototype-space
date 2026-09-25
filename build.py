#!/usr/bin/env python3
"""Build the prototype-space site: a guide from a robot idea to a credible
first build in Bonn, standing on a directory of checked resources.

Two layers of markdown, both edited by hand and reviewed in pull requests:

    guide/   the route: six steps, seven tracks (one per kind of machine),
             the Bonn page and the front page's quick answers
    docs/    the directory: every resource as one line, in one strict shape
             - **[Name](url)** — one sentence on why it matters — `tag` · `tag`

The guide cites the directory by name, as [[ROS 2]], and this script resolves
every citation, so renaming or removing an entry fails the build instead of
leaving a dead reference behind. The front page, the step and track headers,
the per-track table on every step, the overview pages and the filterable
browse view are all generated from those two layers: nothing is typed twice.

    python3 build.py            stage into _build/docs for `mkdocs build`
    python3 build.py --serve    stage, then start the dev server
    python3 build.py --check    after `mkdocs build`: every internal link and
                                anchor in _build/site must resolve
"""

from __future__ import annotations

import html
import json
import posixpath
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml
from markdown.extensions.toc import slugify as _slugify

ROOT = Path(__file__).parent.resolve()
DIRECTORY = ROOT / "docs"
GUIDE = ROOT / "guide"
STAGE = ROOT / "_build"
DOCS = STAGE / "docs"
SITE = STAGE / "site"
REPO = "https://github.com/robonn-club/prototype-space"
DISCORD = "https://discord.gg/sm8nDRntRE"
JOIN = "https://tally.so/r/Pd8Zae"

PROBLEMS: list[str] = []


def problem(message: str) -> None:
    PROBLEMS.append(message)


def slugify(text: str) -> str:
    """The anchor MkDocs gives a heading, so generated links land on it."""
    return _slugify(text, "-")


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


# --- the directory -------------------------------------------------------
# One page per source file. The files stay the unit people contribute to, and
# each keeps its sections, so every section keeps an anchor the guide can cite.


@dataclass
class Source:
    file: str
    slug: str
    nav: str
    blurb: str
    title: str = ""
    text: str = ""
    count: int = 0
    sections: list = field(default_factory=list)

    @property
    def page(self) -> str:
        return f"directory/{self.slug}.md"

    @property
    def path(self) -> Path:
        return DIRECTORY / self.file


SOURCES = [
    Source("prototyping_resources.md", "tools", "Tools",
           "Software, simulators, kits and CAD, organised by the type of system."),
    Source("generative_ai_agents.md", "ai", "AI",
           "Models that write the code, or run inside the robot."),
    Source("datasets.md", "datasets", "Datasets",
           "Data to train on and benchmark against, starting with Bonn's own."),
    Source("nrw_hardware_contacts.md", "hardware", "Hardware",
           "Workshops, shops and fabrication services, nearest first."),
    Source("bonn_physical_spaces.md", "spaces", "Spaces",
           "Where in Bonn to meet, build and test."),
    Source("work_exhibit.md", "showing", "Showing",
           "Competitions, publishing and events."),
    Source("nrw_investor_contacts.md", "funding", "Funding",
           "For the point at which a prototype becomes a company."),
    Source("certification_resources.md", "compliance", "Compliance",
           "What the rules require once it is sold."),
    Source("builder_helpers.md", "city", "City playbook",
           "Bonn as a place to live: costs, arrival, research and industry."),
]
SOURCE_OF = {s.file: s for s in SOURCES}

# The tags in the markdown are a controlled vocabulary; grouping them into
# facets is what makes the browse view filterable. See CONTRIBUTING.md.
COST = ["free", "free tier", "under €250", "€250–1,000", "€1,000–5,000",
        "over €5,000", "€", "€€", "€€€"]
PLACE = ["bonn", "köln", "düsseldorf", "aachen", "dortmund", "münster",
         "siegen", "nrw", "berlin", "hamburg", "münchen", "bayern",
         "niedersachsen", "germany", "eu", "china", "universities"]
LICENCE = ["MIT", "Apache-2.0", "AGPL-3.0", "proprietary", "CC BY-SA 4.0",
           "CC BY-NC-SA 3.0", "CC BY-NC-SA 4.0", "mixed licences"]
ACCESS = ["membership", "library card", "open access", "open evenings",
          "free advice"]
FACETS = [("cost", "Cost", COST), ("place", "Where", PLACE),
          ("licence", "Licence", LICENCE), ("access", "Access", ACCESS)]
FACET_OF = {tag: key for key, _, tags in FACETS for tag in tags}

ENTRY = re.compile(r"^- \*\*\[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)\*\* — (?P<rest>.+)$")
TAIL = re.compile(r"\s+—\s+(?P<tags>`[^`]+`(?:\s*·\s*`[^`]+`)*)\s*$")
TAG = re.compile(r"`([^`]+)`")
LINK = re.compile(r"(?<!!)\[([^\[\]]+)\]\(([^)\s]+)\)")
HEADING = re.compile(r"^## (?P<text>.+?)(?:\s*\{#(?P<id>[\w-]+)\})?\s*$")


def split_entry(line: str):
    """Name, url, sentence (markdown) and tags of an entry line, or None."""
    match = ENTRY.match(line)
    if not match:
        return None
    rest, tags = match.group("rest"), []
    if tail := TAIL.search(rest):
        tags = TAG.findall(tail.group("tags"))
        rest = rest[: tail.start()]
    return match.group("name"), match.group("url"), rest.rstrip(" .") + ".", tags


def parse_source(source: Source) -> list[dict]:
    """Every entry in one directory file, with the section it sits in."""
    entries, section = [], None
    for line in source.text.splitlines():
        if line.startswith("# ") and not source.title:
            source.title = line[2:].strip()
        if line.startswith("## "):
            section = line[3:].strip()
            source.sections.append(section)
            continue
        if not (parts := split_entry(line)):
            continue
        name, url, desc, tags = parts
        facets = {key: [] for key, _, _ in FACETS}
        kinds = []
        for tag in tags:
            facets.get(FACET_OF.get(tag, ""), kinds).append(tag)
        anchor = slugify(section) if section else ""
        entries.append({
            "name": name, "url": url, "desc_md": desc, "tags": tags,
            "kind": kinds, **facets,
            "group": source.slug, "group_nav": source.nav,
            "section": section or source.nav,
            "anchor": f"directory/{source.slug}/" + (f"#{anchor}" if anchor else ""),
        })
    source.count = len(entries)
    return entries


# --- pages and links -----------------------------------------------------
# Every staged page is named by its path under _build/docs ("steps/plan.md").
# Markdown links are left as relative .md paths for MkDocs to resolve and
# validate; HTML the build writes itself needs the URL the browser will see.


def page_url(page: str) -> str:
    stem = page.removesuffix(".md")
    if stem == "index":
        return ""
    if stem.endswith("/index"):
        return stem.removesuffix("index")
    return stem + "/"


def href(src: str, dst: str, anchor: str = "") -> str:
    """A relative URL from one staged page to another."""
    if src == dst and anchor:
        return f"#{anchor}"
    rel = posixpath.relpath(page_url(dst) or ".", page_url(src) or ".")
    out = "./" if rel == "." else rel + "/"
    return out + (f"#{anchor}" if anchor else "")


LINKS: list[tuple[str, str, str]] = []   # (from page, to page, where written)


def staged(path: Path) -> str | None:
    """Where a repository markdown file ends up on the staged site."""
    if path.is_relative_to(DIRECTORY):
        source = SOURCE_OF.get(path.relative_to(DIRECTORY).as_posix())
        return source.page if source else None
    if path.is_relative_to(GUIDE):
        return path.relative_to(GUIDE).as_posix()
    return None


def resolve(target: str, src_file: Path, page: str, *, url: bool) -> str:
    """Rewrite a link written against the repository so it works on the site.

    Authors link between files as they sit in the repository, so the links
    also work when the markdown is read on GitHub; the site moves the files,
    so each link is re-pointed here."""
    if re.match(r"^[a-z][a-z+.-]*:", target) or target.startswith("#"):
        return target
    path, _, anchor = target.partition("#")
    dest = staged((src_file.parent / path).resolve())
    if dest is None:
        problem(f"{repo_path(src_file)}: link {target!r} points outside the site")
        return target
    LINKS.append((page, dest, repo_path(src_file)))
    if url:
        return href(page, dest, anchor)
    rel = posixpath.relpath(dest, posixpath.dirname(page) or ".")
    return rel + (f"#{anchor}" if anchor else "")


# --- citing the directory ------------------------------------------------
# [[Name]] cites an entry; [[Name|text]] changes the link text; [[Name#tools]]
# picks the entry in one directory file when the same name appears in several
# with different links. A list item that is only a citation becomes a full
# row (name, sentence, tags), and "- [[Name]] — note" replaces the sentence.

REF = re.compile(r"\[\[(?P<name>[^\[\]|#]+?)(?:#(?P<group>[a-z-]+))?(?:\|(?P<label>[^\[\]]+))?\]\]")
ROW = re.compile(r"^- (?P<ref>\[\[[^\]]+\]\])(?:\s+—\s+(?P<note>.+?))?\s*$")


class Refs:
    def __init__(self, entries: list[dict]):
        self.by_name: dict[str, list[dict]] = {}
        for entry in entries:
            self.by_name.setdefault(entry["name"], []).append(entry)
        self.cited: set[str] = set()

    def get(self, match: re.Match, where: str) -> dict | None:
        name, group = match.group("name").strip(), match.group("group")
        found = self.by_name.get(name, [])
        if group:
            found = [e for e in found if e["group"] == group]
        if not found:
            problem(f"{where}: no directory entry named {name!r}"
                    + (f" in {group}" if group else ""))
            return None
        if len({e["url"] for e in found}) > 1:
            problem(f"{where}: {name!r} is in several files with different links; "
                    f"cite one, e.g. [[{name}#{found[0]['group']}]]")
        self.cited.add(found[0]["url"])
        return found[0]


def display(text: str) -> str:
    """Link text that is a bare filename reads as the page it became."""
    source = SOURCE_OF.get(text)
    return source.nav if source else text


def inline_html(md: str, src_file: Path, page: str, refs: Refs | None = None) -> str:
    """Render the small subset of markdown used inside a sentence, for HTML the
    build emits itself (rows, tables, the front page)."""
    if refs:
        md = REF.sub(lambda m: ref_link(m, refs, repo_path(src_file)), md)
    out = html.escape(md, quote=False)

    def link(m: re.Match) -> str:
        target = resolve(html.unescape(m.group(2)), src_file, page, url=True)
        external = ' rel="noopener"' if target.startswith("http") else ""
        return f'<a href="{esc(target)}"{external}>{display(m.group(1))}</a>'

    out = LINK.sub(link, out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def plain(md: str) -> str:
    """The same sentence with the markup stripped, for use inside a link."""
    md = REF.sub(lambda m: (m.group("label") or m.group("name")).strip(), md)
    md = LINK.sub(lambda m: m.group(1), md)
    return re.sub(r"\*\*?([^*]+)\*\*?", r"\1", md)


def ref_link(match: re.Match, refs: Refs, where: str) -> str:
    entry = refs.get(match, where)
    label = (match.group("label") or match.group("name")).strip()
    return f"[{label}]({entry['url']})" if entry else label


def row_html(entry: dict, desc: str, label: str | None = None) -> str:
    chips = "".join(f"<span>{esc(t)}</span>" for t in entry["tags"])
    return (f'<div class="row"><a class="row-name" href="{esc(entry["url"])}" rel="noopener">'
            f'{esc(label or entry["name"])}</a>'
            f'<div class="row-desc">{desc}</div>'
            f'<div class="row-tags">{chips}</div></div>')


def entry_desc(entry: dict, page: str) -> str:
    source = next(s for s in SOURCES if s.slug == entry["group"])
    return inline_html(entry["desc_md"], source.path, page)


def guide_markdown(text: str, src_file: Path, page: str, refs: Refs) -> str:
    """Resolve citations and links in a guide page's markdown."""
    where = repo_path(src_file)
    out, rows = [], []

    def flush() -> None:
        if rows:
            out.extend(["", '<div class="rows">' + "".join(rows) + "</div>", ""])
            rows.clear()

    for line in text.splitlines():
        if match := ROW.match(line):
            ref = REF.fullmatch(match.group("ref"))
            entry = refs.get(ref, where) if ref else None
            if entry:
                note = match.group("note")
                desc = (inline_html(note, src_file, page, refs) if note
                        else entry_desc(entry, page))
                rows.append(row_html(entry, desc, ref.group("label")))
            continue
        flush()
        out.append(line)
    flush()
    md = REF.sub(lambda m: ref_link(m, refs, where), "\n".join(out))
    return LINK.sub(lambda m: f"[{m.group(1)}]({resolve(m.group(2), src_file, page, url=False)})", md)


# --- the guide -----------------------------------------------------------

STEPS = ["plan", "simulate", "parts", "build", "test", "show"]
AFTER = "after"
TRACKS = ["mobile", "arm", "field", "drone", "legged", "sensor", "software"]

STEP_KEYS = {"name", "situation", "goal", "done"}
TRACK_KEYS = {"name", "does", "lede", "first", "examples", "budget", "time", "hardest"}


def front_matter(text: str, where: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        problem(f"{where}: missing front matter")
        return {}, text
    head, _, body = text[4:].partition("\n---\n")
    return yaml.safe_load(head) or {}, body.lstrip("\n")


@dataclass
class Step:
    slug: str
    n: int | None
    meta: dict
    body: str

    @property
    def page(self) -> str:
        return f"steps/{self.slug}.md"

    @property
    def path(self) -> Path:
        return GUIDE / "steps" / f"{self.slug}.md"

    @property
    def name(self) -> str:
        return self.meta["name"]

    @property
    def label(self) -> str:
        return f"{self.n} · {self.name}" if self.n else self.meta.get("title", self.name)


@dataclass
class Track:
    slug: str
    meta: dict
    body: str
    parts: dict = field(default_factory=dict)   # step slug -> (summary, rest)
    extra: str = ""

    @property
    def page(self) -> str:
        return f"tracks/{self.slug}.md"

    @property
    def path(self) -> Path:
        return GUIDE / "tracks" / f"{self.slug}.md"

    @property
    def name(self) -> str:
        return self.meta["name"]


def load_steps() -> list[Step]:
    steps = []
    for n, slug in enumerate(STEPS + [AFTER], 1):
        path = GUIDE / "steps" / f"{slug}.md"
        meta, body = front_matter(path.read_text(encoding="utf-8"), repo_path(path))
        if missing := STEP_KEYS - meta.keys():
            problem(f"{repo_path(path)}: front matter lacks {sorted(missing)}")
        step = Step(slug, n if slug != AFTER else None, meta, body)
        if slug != AFTER and "{{ tracks }}" not in body:
            problem(f"{repo_path(path)}: no {{{{ tracks }}}} placeholder for the per-track table")
        steps.append(step)
    return steps


def load_tracks(steps: list[Step]) -> list[Track]:
    names = {s.name.lower(): s.slug for s in steps if s.n}
    tracks = []
    for slug in TRACKS:
        path = GUIDE / "tracks" / f"{slug}.md"
        where = repo_path(path)
        meta, body = front_matter(path.read_text(encoding="utf-8"), where)
        if missing := TRACK_KEYS - meta.keys():
            problem(f"{where}: front matter lacks {sorted(missing)}")
        track = Track(slug, meta, body)
        chunks = re.split(r"^(?=## )", body, flags=re.M)
        order = []
        for chunk in chunks:
            if not chunk.startswith("## "):
                if chunk.strip():
                    problem(f"{where}: text before the first step heading")
                continue
            heading, _, rest = chunk.partition("\n")
            step_slug = names.get(heading[3:].strip().lower())
            if not step_slug:
                track.extra += chunk
                continue
            paragraphs = rest.strip().split("\n\n", 1)
            summary = " ".join(paragraphs[0].split())
            if not summary or summary.startswith(("-", "*", "|")):
                problem(f"{where}: '{heading}' must open with a one-sentence summary")
            track.parts[step_slug] = (summary, paragraphs[1] if len(paragraphs) > 1 else "")
            order.append(step_slug)
        if order != STEPS:
            problem(f"{where}: step sections must be {STEPS}, found {order}")
        tracks.append(track)
    return tracks


def parse_answers(path: Path) -> list[tuple[str, str, tuple[str, str] | None]]:
    _, body = front_matter(path.read_text(encoding="utf-8"), repo_path(path))
    answers = []
    for block in re.split(r"^## ", body, flags=re.M)[1:]:
        question, _, rest = block.partition("\n")
        paragraphs = [" ".join(p.split()) for p in rest.strip().split("\n\n") if p.strip()]
        more = LINK.fullmatch(paragraphs[-1]) if paragraphs else None
        if not more or len(paragraphs) < 2:
            problem(f"{repo_path(path)}: '{question}' needs an answer and a closing link line")
            continue
        answers.append((question.strip(), " ".join(paragraphs[:-1]), (more.group(1), more.group(2))))
    return answers


def glance(text: str) -> dict[str, str]:
    """The two-column 'at a glance' table from the city playbook."""
    found: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 2 and cells[0] and set(cells[0]) != {"-"}:
            found[cells[0]] = cells[1]
    return found


# --- shared pieces of generated HTML --------------------------------------

# Generated markup is written without whitespace between elements, which reads
# fine on screen but runs words together in the search index and for screen
# readers ("Mobile robotStart from…"). A newline after each closing tag that is
# followed by another tag separates them without changing the layout.
TIGHT = re.compile(r"(</(?:a|b|span|div|p|dt|dd|li|ul|ol|dl|h1|h2|header|nav|section|button|tr|td|th)>)(?=<)")


def page_file(meta: dict, body: str) -> str:
    body = TIGHT.sub(r"\1\n", body)
    head = "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items()
                     if not isinstance(v, list))
    lists = "".join(f"{k}:\n" + "".join(f"  - {x}\n" for x in v)
                    for k, v in meta.items() if isinstance(v, list))
    return f"---\n{head}\n{lists}---\n\n{body.strip()}\n"


def page_head(eyebrow: str, title: str, lede: str = "", extra: str = "") -> str:
    lede_html = f'<p class="lede">{lede}</p>' if lede else ""
    return (f'<header class="page-head"><p class="eyebrow">{eyebrow}</p>'
            f'<h1 class="page-title">{esc(title)}</h1>{lede_html}{extra}</header>')


def progress(page: str, steps: list[Step], current: str | None, *, anchors: bool = False) -> str:
    """The six steps as a line of stops, the current one filled in."""
    route = [s for s in steps if s.n]
    # A track page has no current step; the page after the route has passed all six.
    at = next((s.n for s in route if s.slug == current), 0 if anchors else len(route) + 1)
    items = []
    for s in route:
        state = "current" if s.n == at else ("past" if s.n < at else "future")
        target = f"#{s.slug}" if anchors else href(page, s.page)
        aria = ' aria-current="step"' if state == "current" else ""
        items.append(f'<li class="{state}"><a href="{target}"{aria}>'
                     f'<span class="p-n">{s.n}</span><span class="p-name">{esc(s.name)}</span></a></li>')
    label = "Jump to a step" if anchors else "The six steps"
    return f'<nav class="progress" aria-label="{label}"><ol>{"".join(items)}</ol></nav>'


def facts(pairs: list[tuple[str, str]], cls: str) -> str:
    rows = "".join(f"<div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in pairs if v)
    return f'<dl class="{cls}">{rows}</dl>'


def bar_html(step: Step) -> str:
    items = "".join(f'<li><span class="bar-t">{esc(b["title"])}</span>'
                    f'<span class="bar-x">{esc(b["text"])}</span></li>'
                    for b in step.meta.get("bar", []))
    return f'<ol class="bar">{items}</ol>'


def dates_html(page: str, step: Step, refs: Refs) -> str:
    """Events to build towards, one row each: a date, what and where, and who it suits."""
    rows = "".join(
        f'<div class="date"><p class="d-when">{esc(d["when"])}</p>'
        f'<p class="d-what">{inline_html(d["what"], step.path, page, refs)}'
        f'<span class="d-where">{esc(d["where"])}</span></p>'
        f'<p class="d-good">{esc(d["good"])}</p></div>'
        for d in step.meta.get("dates", []))
    return f'<div class="dates">{rows}</div>'


def track_table(page: str, step: Step, tracks: list[Track]) -> str:
    rows = []
    for t in tracks:
        summary = plain(t.parts.get(step.slug, ("", ""))[0])
        rows.append(f'<a class="tt-row" data-track="{t.slug}" href="{href(page, t.page, step.slug)}">'
                    f'<span class="tt-name">{esc(t.name)}</span>'
                    f'<span class="tt-sum">{esc(summary)}</span>'
                    f'<span class="tt-go" aria-hidden="true">→</span></a>')
    return f'<div class="track-table">{"".join(rows)}</div>'


def improve(path: Path) -> str:
    return (f'<p class="improve"><a href="{REPO}/edit/main/{repo_path(path)}" rel="noopener">'
            f"Something wrong or missing? Improve this page on GitHub</a></p>")


# --- guide pages ---------------------------------------------------------

def stage_step(step: Step, steps: list[Step], tracks: list[Track], refs: Refs) -> str:
    page = step.page
    route = [s for s in steps if s.n]
    body = step.body.replace("{{ tracks }}", f"\n{track_table(page, step, tracks)}\n")
    body = body.replace("{{ bar }}", f"\n{bar_html(step)}\n")
    body = body.replace("{{ dates }}", f"\n{dates_html(page, step, refs)}\n")
    body = guide_markdown(body, step.path, page, refs)

    info = [("You're here if", esc(step.meta["situation"]))]
    info += [(k, esc(step.meta.get(key, ""))) for k, key in (("Takes", "time"), ("Costs", "cost"))]
    eyebrow = f"Step {step.n} of {len(route)}" if step.n else "Once the bar is met"
    head = (progress(page, steps, step.slug)
            + page_head(eyebrow, step.meta.get("title", step.name), esc(step.meta["goal"]))
            + facts(info, "step-facts")
            + f'<div class="done-when"><p class="dw-k">Done when</p><p class="dw-v">{esc(step.meta["done"])}</p></div>')

    i = STEPS.index(step.slug) if step.n else len(STEPS)
    nxt = steps[i + 1] if step.n else None
    prev = steps[i - 1] if i > 0 else None
    if nxt:
        forward = (f'<a class="sn-next" href="{href(page, nxt.page)}">'
                   f'<span class="sn-k">Done? Next step</span>'
                   f'<span class="sn-name">{esc(nxt.label)}</span>'
                   f'<span class="sn-goal">{esc(nxt.meta["goal"])}</span></a>')
    else:
        first = steps[0]
        forward = (f'<a class="sn-next" href="{href(page, first.page)}">'
                   f'<span class="sn-k">Ready for version two?</span>'
                   f'<span class="sn-name">Back to {esc(first.label)}</span>'
                   f'<span class="sn-goal">{esc(first.meta["goal"])}</span></a>')
    back = ""
    if prev:
        back = (f'<a class="sn-prev" href="{href(page, prev.page)}">'
                f'<span class="sn-k">Not there yet?</span>'
                f'<span class="sn-name">{esc(prev.label)}</span></a>')
    foot = f'<nav class="step-next" aria-label="Where next">{forward}{back}</nav>{improve(step.path)}'

    meta = {"title": step.label if step.n else step.meta.get("title", step.name),
            "description": step.meta["goal"], "kind": "guide"}
    return page_file(meta, f"{head}\n\n{body}\n\n{foot}")


def stage_track(track: Track, steps: list[Step], tracks: list[Track], refs: Refs) -> str:
    page = track.page
    by_slug = {s.slug: s for s in steps}
    parts = []
    for slug in STEPS:
        step = by_slug[slug]
        summary, rest = track.parts[slug]
        link = (f'<p class="to-step"><span class="k">Done when</span> {esc(step.meta["done"])} '
                f'<a href="{href(page, step.page)}">Step {step.n} in full →</a></p>')
        parts.append(f"## {step.n} · {step.name} {{#{slug}}}\n\n{summary}\n{{: .sum }}\n\n{rest.strip()}\n\n{link}\n")
    body = guide_markdown("\n".join(parts) + "\n" + track.extra, track.path, page, refs)

    m = track.meta
    examples = "".join(f"<li>{esc(x)}</li>" for x in m["examples"])
    info = facts([("A credible first build", esc(m["first"])), ("Budget", esc(m["budget"])),
                  ("Time", esc(m["time"])), ("Hardest part", esc(m["hardest"]))], "track-facts")
    notice = (f'<p class="notice">{inline_html(m["notice"], track.path, page, refs)}</p>'
              if m.get("notice") else "")
    head = (page_head(f"Track · {esc(m['does'])}", track.name, esc(m["lede"]))
            + info + notice
            + f'<div class="examples"><p class="ex-k">Other first builds on this track</p><ul>{examples}</ul></div>'
            + f'<span hidden data-track-page="{track.slug}"></span>'
            + progress(page, steps, None, anchors=True))

    others = "".join(f'<a href="{href(page, t.page)}">{esc(t.name)}</a>'
                     for t in tracks if t.slug != track.slug)
    foot = (f'<nav class="track-next" aria-label="Other tracks"><p class="tn-k">Other tracks</p>'
            f'<div class="tn-list">{others}</div></nav>{improve(track.path)}')
    meta = {"title": track.name, "description": m["lede"], "kind": "guide"}
    return page_file(meta, f"{head}\n\n{body}\n\n{foot}")


def stage_bonn(refs: Refs, facts_table: dict[str, str], moved: dict[str, str]) -> str:
    path = GUIDE / "bonn.md"
    page = "bonn.md"
    meta, body = front_matter(path.read_text(encoding="utf-8"), repo_path(path))
    table = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in facts_table.items())
    body = body.replace("{{ glance }}", f'\n<dl class="glance">{table}</dl>\n')
    body = guide_markdown(body, path, page, refs)
    sections = re.findall(r"^## (.+?)\s*\{#([\w-]+)\}", body, flags=re.M)
    jump = "".join(f'<a href="#{i}">{esc(t)}</a>' for t, i in sections)
    head = page_head("Bonn", meta["title"], esc(meta["lede"]),
                     f'<nav class="jump" aria-label="On this page">{jump}</nav>')
    # Old links into the city playbook, which used to live at this address.
    data = f"<span hidden data-moved='{esc(json.dumps(moved))}'></span>"
    return page_file({"title": meta["title"], "description": meta["lede"], "kind": "guide",
                      "hide": ["navigation"]},
                     f"{head}{data}\n\n{body}\n\n{improve(path)}")


# --- overview pages ------------------------------------------------------

def stage_steps_index(steps: list[Step]) -> str:
    page = "steps/index.md"
    route = [s for s in steps if s.n]
    show = next(s for s in steps if s.slug == "show")
    after = next(s for s in steps if s.slug == AFTER)
    items = []
    for s in route + [after]:
        n = f'<span class="rs-n">{s.n}</span>' if s.n else '<span class="rs-n rs-after">+</span>'
        details = facts([("Done when", esc(s.meta["done"])), ("Takes", esc(s.meta.get("time", ""))),
                         ("Costs", esc(s.meta.get("cost", "")))], "rs-facts")
        items.append(f'<li class="rs"><a class="rs-link" href="{href(page, s.page)}">{n}'
                     f'<span class="rs-main"><span class="rs-if">{esc(s.meta["situation"])}</span>'
                     f'<span class="rs-name">{esc(s.meta.get("title", s.name))}</span>'
                     f'<span class="rs-goal">{esc(s.meta["goal"])}</span></span></a>{details}</li>')
    body = (page_head(f"The route · {len(route)} steps", "Six steps to a credible first build",
                      "Each step ends with a finish line you can check. Start at the step that "
                      "matches where you are, and skip nothing after it.")
            + f'<ol class="route-steps">{"".join(items)}</ol>'
            + f'<section class="bar-block"><h2 id="the-bar">What makes a first build credible</h2>'
              f'<p>Step 6 ends when all five hold. They are the finish line for everything before it.</p>'
            + bar_html(show) + "</section>")
    return page_file({"title": "The six steps", "description": "Six steps from a robot idea to a "
                      "credible first build, each with a finish line you can check.",
                      "kind": "guide", "hide": ["toc"]}, body)


def stage_tracks_index(tracks: list[Track]) -> str:
    page = "tracks/index.md"
    cards = []
    for t in tracks:
        m = t.meta
        cards.append(
            f'<a class="track-card" data-track="{t.slug}" href="{href(page, t.page)}">'
            f'<span class="tc-does">{esc(m["does"])}</span>'
            f'<span class="tc-name">{esc(t.name)}</span>'
            f'<span class="tc-lede">{esc(m["lede"])}</span>'
            f'<span class="tc-first"><b>First build</b> {esc(m["first"])}</span>'
            f'<span class="tc-meta"><span>{esc(m["budget"])}</span><span>{esc(m["time"])}</span></span></a>')
    rows = "".join(f'<tr><td><a href="{href(page, t.page)}">{esc(t.name)}</a></td>'
                   f'<td>{esc(t.meta["budget"])}</td><td>{esc(t.meta["time"])}</td>'
                   f'<td>{esc(t.meta["hardest"])}</td></tr>' for t in tracks)
    body = (page_head(f"Tracks · {len(tracks)} kinds of machine", "What are you building?",
                      "Each track walks the six steps for one kind of machine, naming the software, "
                      "the kits and the places for each. When two tracks fit the idea, take the "
                      "cheaper one.")
            + f'<div class="track-grid track-grid-full">{"".join(cards)}</div>'
            + '<h2 id="compared">The tracks compared</h2>'
            + '<div class="table-wrap"><table class="compare"><thead><tr><th>Track</th><th>Budget</th>'
              f'<th>Time</th><th>Hardest part</th></tr></thead><tbody>{rows}</tbody></table></div>'
            + '<p class="note">Budgets are rough ranges for a first build, not quotes. Each '
              "project's own bill of materials decides the real figure.</p>")
    return page_file({"title": "Tracks", "description": "Seven tracks from idea to first build, "
                      "one per kind of machine.", "kind": "guide", "hide": ["toc"]}, body)


def stage_directory_index(entries: list[dict]) -> str:
    page = "directory/index.md"
    blocks = []
    for s in SOURCES:
        sections = "".join(f'<a href="{href(page, s.page, slugify(x))}">{esc(x)}</a>'
                           for x in s.sections)
        blocks.append(f'<div class="dir-src"><a class="ds-name" href="{href(page, s.page)}">{esc(s.nav)} '
                      f'<span class="ds-n">{s.count}</span></a>'
                      f'<p class="ds-blurb">{esc(s.blurb)}</p><div class="ds-sections">{sections}</div></div>')
    links = len({e["url"] for e in entries})
    body = (page_head(f"Directory · {links} links", "Directory",
                      "Every resource behind the guide, each with one sentence on why it matters. "
                      "Search and filter all of it at once, or read it by topic.")
            + f'<p class="dir-search"><a class="btn" href="{href(page, "browse.md")}">'
              f"Search and filter all {len(entries)} entries →</a></p>"
            + f'<div class="dir-list">{"".join(blocks)}</div>'
            + f'<p class="note">Every external link is checked weekly, and a dead one opens an issue. '
              f'Missing something? <a href="{REPO}/blob/main/CONTRIBUTING.md">Add an entry</a>.</p>')
    return page_file({"title": "Directory", "description": "Every resource behind the guide, "
                      "with one sentence on why each matters.", "kind": "directory",
                      "hide": ["toc"]}, body)


def stage_directory(source: Source, refs: Refs) -> str:
    page = source.page
    text = source.text
    body = text.split("\n", 1)[1].lstrip("\n") if text.startswith("# ") else text
    out = []
    for line in body.splitlines():
        if parts := split_entry(line):
            name, url, desc, tags = parts
            entry = {"name": name, "url": url, "tags": tags}
            out.append(row_html(entry, inline_html(desc, source.path, page)))
            continue
        out.append(LINK.sub(lambda m: f"[{display(m.group(1))}]"
                            f"({resolve(m.group(2), source.path, page, url=False)})", line))
    head = page_head(f"Directory · {source.nav} · {source.count} entries", source.title,
                     esc(source.blurb))
    return page_file({"title": source.nav, "description": source.blurb, "kind": "directory"},
                     head + "\n\n" + "\n".join(out) + "\n\n" + improve(source.path))


def stage_browse(entries: list[dict]) -> str:
    groups = []
    sections = "".join(
        f'<button type="button" class="chip" data-facet="group" data-value="{s.slug}">{esc(s.nav)} '
        f'<span class="chip-n">{s.count}</span></button>' for s in SOURCES)
    groups.append(f'<div class="facet"><h3>Page</h3><div class="chips">{sections}</div></div>')
    for key, label, order in FACETS:
        present = [t for t in order if any(t in e[key] for e in entries)]
        chips = "".join(
            f'<button type="button" class="chip" data-facet="{key}" data-value="{esc(t)}">{esc(t)} '
            f'<span class="chip-n">{sum(1 for e in entries if t in e[key])}</span></button>'
            for t in present)
        if chips:
            groups.append(f'<div class="facet"><h3>{label}</h3><div class="chips">{chips}</div></div>')
    body = (page_head(f"Directory · all {len(entries)} entries", "Search everything",
                      "Every entry from every page of the directory. Filter by what it costs, where "
                      "it is and what licence it carries; filters combine.")
            + f"""
<div class="browse" markdown="0">
  <input type="search" id="q" class="search" placeholder="Search {len(entries)} entries…"
         autocomplete="off" spellcheck="false" aria-label="Search the directory">
  <button type="button" class="filter-toggle" aria-expanded="false" aria-controls="facets">Filters</button>
  <div class="facets" id="facets">{"".join(groups)}</div>
  <div class="browse-bar">
    <span id="count" aria-live="polite"></span>
    <button type="button" id="reset" class="reset" hidden>Clear filters</button>
  </div>
  <div id="results" class="rows"></div>
  <p id="empty" class="empty" hidden>Nothing matches. Clear a filter, or try a shorter word.</p>
</div>""")
    return page_file({"title": "Search everything", "description": "Search and filter every "
                      "resource in the directory.", "kind": "browse", "hide": ["toc"]}, body)


# --- the front page ------------------------------------------------------

def home(steps: list[Step], tracks: list[Track], answers, facts_table: dict[str, str],
         entries: list[dict], refs: Refs) -> str:
    """The front page asks where the visitor is, and points at the next step.

    Every row of the finder is a plain link to one step, so the answer is one
    tap away with or without JavaScript; the tracks, quick answers and the bar
    are read from the guide's own files."""
    page = "index.md"
    show = next(s for s in steps if s.slug == "show")
    rows = []
    for s in steps:
        n = str(s.n) if s.n else "+"
        rows.append(f'<li><a class="finder-row" href="{href(page, s.page)}">'
                    f'<span class="f-now">{esc(s.meta["situation"])}</span>'
                    f'<span class="f-next"><span class="f-n">{n}</span>'
                    f'<span class="f-name">{esc(s.meta.get("title", s.name))}</span>'
                    f'<span class="f-hook">{esc(s.meta.get("hook", ""))}</span></span>'
                    f'<span class="f-go" aria-hidden="true">→</span></a></li>')

    cards = "".join(
        f'<a class="track-card" data-track="{t.slug}" href="{href(page, t.page)}">'
        f'<span class="tc-does">{esc(t.meta["does"])}</span>'
        f'<span class="tc-name">{esc(t.name)}</span>'
        f'<span class="tc-first">{esc(t.meta["first"])}</span>'
        f'<span class="tc-meta"><span>{esc(t.meta["budget"])}</span><span>{esc(t.meta["time"])}</span></span></a>'
        for t in tracks)

    qa = []
    for question, answer, (label, target) in answers:
        qa.append(f'<div class="qa"><h3>{esc(question)}</h3>'
                  f'<p>{inline_html(answer, GUIDE / "answers.md", page, refs)}</p>'
                  f'<a class="qa-more" href="{esc(resolve(target, GUIDE / "answers.md", page, url=True))}">'
                  f"{esc(label)} →</a></div>")

    glance_rows = "".join(f'<div class="fact"><dt>{esc(k)}</dt><dd>{esc(facts_table[k])}</dd></div>'
                          for k in GLANCE)
    links = len({e["url"] for e in entries})
    route = [s for s in steps if s.n]

    return page_file({"template": "home.html", "title": "From a robot idea to a credible first build",
                      "description": "A step-by-step guide for students in Bonn: from a robot idea to "
                      "a credible first build, with the tools, places and people for each step.",
                      "kind": "home", "hide": ["navigation", "toc"]}, f"""
<div class="wrap hero">
  <div class="hero-say">
    <p class="eyebrow-rule">Robonn · Universität Bonn</p>
    <h1>From a robot idea to a credible first build, in Bonn.</h1>
    <p class="hero-what">A step-by-step guide for students. Each step says what to do, when
    it is done, and where in Bonn to do it, for the kind of robot you are building.</p>
    <p class="meta">{len(route)} steps · {len(tracks)} tracks · {links} checked links</p>
  </div>
  <nav class="finder" aria-labelledby="finder-h">
    <h2 id="finder-h">Where are you now?</h2>
    <ol class="finder-list">{"".join(rows)}</ol>
  </nav>
</div>

<section class="wrap block" aria-labelledby="tracks-h">
  <div class="block-head">
    <p class="eyebrow-rule">What are you building?</p>
    <h2 id="tracks-h">Pick a track: the tools and parts for your kind of machine</h2>
  </div>
  <div class="track-grid">{cards}</div>
</section>

<section class="wrap block" aria-labelledby="answers-h">
  <div class="block-head">
    <p class="eyebrow-rule">Quick answers</p>
    <h2 id="answers-h">The questions everyone asks first</h2>
  </div>
  <div class="answers">{"".join(qa)}</div>
</section>

<section class="wrap block" aria-labelledby="bar-h">
  <div class="block-head">
    <p class="eyebrow-rule">The finish line</p>
    <h2 id="bar-h">What makes a first build credible</h2>
  </div>
  {bar_html(show)}
  <p class="block-more"><a href="{href(page, show.page)}">How to get there: step 6, Show →</a></p>
</section>

<section class="ground" aria-labelledby="bonn-h">
  <div class="wrap ground-in">
    <div class="ground-say">
      <p class="eyebrow-rule">Where it all happens</p>
      <h2 id="bonn-h">Bonn</h2>
      <p class="ground-what">An open workshop, rooms for registered student groups, research
      teams that win at RoboCup, and no venue that rents out space to test a robot. All of it
      written down: where to make, work, test and buy, who to ask, and where money comes from.</p>
      <a class="ground-all" href="{href(page, "bonn.md")}">Building in Bonn →</a>
    </div>
    <dl class="facts">{glance_rows}</dl>
  </div>
</section>

<div class="wrap colophon">
  <p class="colophon-what">Kept by Robonn, the robotics club at Universität Bonn, and built on a
  directory of {len(entries)} entries, each with one sentence on why it matters. Every external
  link is checked weekly; a dead one opens an issue.</p>
  <p class="colophon-links">
    <a href="{DISCORD}" rel="noopener">Robonn Discord →</a>
    <a href="{JOIN}" rel="noopener">Join Robonn →</a>
    <a href="{href(page, "directory/index.md")}">Directory →</a>
    <a href="{REPO}/blob/main/CONTRIBUTING.md" rel="noopener">Contribute →</a>
  </p>
</div>
""")


# Rows of the city's "at a glance" table quoted on the front page.
GLANCE = ["Room rent", "Monthly total", "Main tradeoff"]


# --- old addresses ---------------------------------------------------------
# The site used to have one page per category. Those addresses now forward to
# the directory page that holds the same section, anchor included.

OLD_PAGES = {
    "build": ["prototyping_resources.md", "generative_ai_agents.md", "datasets.md"],
    "make": ["nrw_hardware_contacts.md", "bonn_physical_spaces.md"],
    "grow": ["nrw_investor_contacts.md", "certification_resources.md", "work_exhibit.md"],
}


def redirect_stub(old: str) -> str:
    sources = [SOURCE_OF[f] for f in OLD_PAGES[old]]
    fallback = f"../{page_url(sources[0].page)}"
    moved = {slugify(sec): f"../{page_url(s.page)}" for s in sources for sec in s.sections}
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Moved</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{fallback}">
<script>
  var moved = {json.dumps(moved)}, id = decodeURIComponent(location.hash.slice(1));
  location.replace((moved[id] || "{fallback}") + location.hash);
</script>
<noscript><meta http-equiv="refresh" content="0; url={fallback}"></noscript>
</head><body><p>This page has moved to the <a href="{fallback}">directory</a>.</p></body></html>
"""


# --- checks ----------------------------------------------------------------

def check_nav(pages: set[str]) -> None:
    """Every staged page must be in the nav, and the nav must name only real pages."""
    class Loader(yaml.SafeLoader):
        pass
    Loader.add_multi_constructor("", lambda loader, suffix, node: None)
    config = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=Loader)

    def walk(items):
        for item in items or []:
            if isinstance(item, str):
                yield item
            elif isinstance(item, dict):
                for value in item.values():
                    yield from (walk(value) if isinstance(value, list) else [value])

    listed = set(walk(config.get("nav")))
    for page in sorted(pages - listed):
        problem(f"mkdocs.yml: {page} is built but missing from the nav")
    for page in sorted(listed - pages):
        problem(f"mkdocs.yml: the nav lists {page}, which the build does not produce")


class _Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])


def check_site() -> int:
    """Crawl the built site: every internal link must reach a page, and every
    anchor an element on it. MkDocs checks the markdown's own links; this also
    covers the HTML the build writes."""
    if not SITE.exists():
        print("error: no built site; run `mkdocs build` first", file=sys.stderr)
        return 1
    parsed: dict[Path, _Anchors] = {}

    def parse(path: Path) -> _Anchors:
        if path not in parsed:
            parser = _Anchors()
            parser.feed(path.read_text(encoding="utf-8"))
            parsed[path] = parser
        return parsed[path]

    # The 404 page links from the site root, e.g. /prototype-space/steps/.
    config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    root_path = urlsplit(re.search(r"^site_url:\s*(\S+)", config, re.M).group(1)).path
    pages = [p for p in SITE.rglob("*.html") if "search" not in p.parts]
    broken = []
    for path in pages:
        for link in parse(path).links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc or link.startswith(("mailto:", "javascript:")):
                continue
            if parts.path.startswith(root_path):
                target = (SITE / unquote(parts.path[len(root_path):])).resolve()
            else:
                target = path if not parts.path else (path.parent / unquote(parts.path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists() or not target.is_relative_to(SITE):
                broken.append(f"{path.relative_to(SITE)}: {link} → no such page")
                continue
            anchor = unquote(parts.fragment)
            if anchor and target.suffix == ".html" and anchor not in parse(target).ids:
                broken.append(f"{path.relative_to(SITE)}: {link} → no #{anchor} on that page")
    for line in broken:
        print(f"error: {line}", file=sys.stderr)
    print(f"checked internal links on {len(pages)} pages: "
          f"{'no problems' if not broken else f'{len(broken)} broken'}")
    return 1 if broken else 0


# --- main ------------------------------------------------------------------

def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    DOCS.mkdir(parents=True)

    entries: list[dict] = []
    for source in SOURCES:
        source.text = source.path.read_text(encoding="utf-8")
        entries += parse_source(source)
    refs = Refs(entries)

    steps = load_steps()
    tracks = load_tracks(steps)
    answers = parse_answers(GUIDE / "answers.md")
    if PROBLEMS:                                # staging malformed files only adds noise
        for message in dict.fromkeys(PROBLEMS):
            print(f"error: {message}", file=sys.stderr)
        return 1
    city = next(s for s in SOURCES if s.file == "builder_helpers.md")
    facts_table = glance(city.text)
    for label in GLANCE:
        if label not in facts_table:
            problem(f"{city.file}: 'at a glance' table has no {label!r} row")

    moved = {slugify(sec): f"../{page_url(city.page)}" for sec in city.sections}
    pages: dict[str, str] = {}
    for step in steps:
        pages[step.page] = stage_step(step, steps, tracks, refs)
    for track in tracks:
        pages[track.page] = stage_track(track, steps, tracks, refs)
    pages["steps/index.md"] = stage_steps_index(steps)
    pages["tracks/index.md"] = stage_tracks_index(tracks)
    pages["bonn.md"] = stage_bonn(refs, facts_table, moved)
    for source in SOURCES:
        pages[source.page] = stage_directory(source, refs)
    pages["directory/index.md"] = stage_directory_index(entries)
    for entry in entries:                       # rendered once, for the browse page
        entry["desc"] = entry_desc(entry, "browse.md")
    pages["browse.md"] = stage_browse(entries)
    pages["index.md"] = home(steps, tracks, answers, facts_table, entries, refs)

    for src, dest, where in LINKS:
        if dest not in pages:
            problem(f"{where}: links to {dest}, which is not a page")
    check_nav(set(pages))

    if PROBLEMS:
        for message in dict.fromkeys(PROBLEMS):
            print(f"error: {message}", file=sys.stderr)
        return 1

    for name, content in pages.items():
        target = DOCS / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    for old in OLD_PAGES:
        (DOCS / old).mkdir()
        (DOCS / old / "index.html").write_text(redirect_stub(old), encoding="utf-8")

    assets = DOCS / "assets"
    shutil.copytree(ROOT / "site_assets", assets)
    public = [{k: v for k, v in e.items() if k != "desc_md"} for e in entries]
    (assets / "resources.json").write_text(
        json.dumps(public, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    uncited = len({e["url"] for e in entries}) - len(refs.cited)
    print(f"staged {len(pages)} pages → {DOCS.relative_to(ROOT)}")
    print(f"  guide      {len(steps)} step pages, {len(tracks)} tracks, "
          f"{len(answers)} quick answers, {len(refs.cited)} entries cited")
    print(f"  directory  {len(entries)} entries in {len(SOURCES)} pages "
          f"({uncited} links reachable only through the directory)")
    for source in SOURCES:
        print(f"      {source.count:>4}  {source.file}")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check_site())
    code = main()
    if code == 0 and "--serve" in sys.argv:
        code = subprocess.call(["mkdocs", "serve"], cwd=ROOT)
    sys.exit(code)

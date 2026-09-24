#!/usr/bin/env python3
"""Build the prototype-space site.

The markdown files in docs/ stay the single source of truth: they are
readable on GitHub and edited by hand in a pull request. This script copies them
into a staging docs/ directory for MkDocs and, because every entry follows the
same shape, also parses them into resources.json so the site can offer one
filterable view over everything.

    - **[Name](url)** — one sentence on why it matters — `tag` · `tag`

Every number on the landing page is counted from that data rather than typed in,
so the site cannot drift from the markdown.

    python3 build.py            stage, then run `mkdocs build`
    python3 build.py --serve    stage and start the dev server
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).parent.resolve()
SRC = ROOT / "docs"
STAGE = ROOT / "_build"
DOCS = STAGE / "docs"
REPO = "https://github.com/robonn-club/prototype-space"

# --- four categories -----------------------------------------------------
# Three of them are kinds of thing: what you build with, where you make it,
# what happens after. The fourth is the place all of that happens in. Each
# source markdown file survives inside its category as a numbered group, so the
# files stay the unit people contribute to and every section keeps its own
# anchor.


@dataclass
class Group:
    """One source markdown file, rendered as a numbered block in its category."""
    source: str
    name: str
    blurb: str
    count: int = 0
    sections: list = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.source.removesuffix(".md")


@dataclass
class Category:
    slug: str
    nav: str
    title: str
    hook: str
    lede: str
    groups: list

    @property
    def count(self) -> int:
        return sum(g.count for g in self.groups)


CATEGORIES = [
    Category(
        "build", "Build", "Build",
        "Software, AI and data. Starts at zero euros.",
        "Everything that runs on a laptop before anything is bought: the "
        "simulators, the navigation and perception stacks, the models, and the "
        "datasets to train and benchmark them against.",
        [
            Group("prototyping_resources.md", "Tools",
                  "Organised by the type of system being built."),
            Group("generative_ai_agents.md", "AI",
                  "Models that write the code, or run inside the robot."),
            Group("datasets.md", "Datasets",
                  "Data to train on and benchmark against."),
        ]),
    Category(
        "make", "Make", "Make",
        "Machines, parts and space — nearest first.",
        "Where the CAD file becomes a part and the part becomes a robot. "
        "Workshops you can walk to from campus, suppliers that ship to Bonn, "
        "and rooms to build and test in.",
        [
            Group("nrw_hardware_contacts.md", "Hardware",
                  "Machines to use and parts to order, nearest first."),
            Group("bonn_physical_spaces.md", "Spaces",
                  "Where in Bonn to meet, build and test."),
        ]),
    Category(
        "grow", "Grow", "Grow",
        "Funding, rules and audiences.",
        "What happens once the prototype works: the money that scales it, the "
        "regulation that applies if it is sold, and the competitions and events "
        "that get it finished and seen.",
        [
            Group("nrw_investor_contacts.md", "Funding",
                  "For the point at which a prototype becomes a company."),
            Group("certification_resources.md", "Compliance",
                  "What the rules require, if it becomes a product."),
            Group("work_exhibit.md", "Exhibit",
                  "Competitions, publishing and events."),
        ]),
    Category(
        "bonn", "Bonn", "Bonn",
        "The city itself. Costs, arrival, research and industry.",
        "Everything above assumes a place to do it in. What Bonn is good at and "
        "what it is not, what a month costs, what an arriving student has to do "
        "first, and which research groups and employers sit within reach.",
        [
            Group("builder_helpers.md", "City",
                  "Bonn as a place to build, not only a place to study."),
        ]),
]

GROUPS = [g for c in CATEGORIES for g in c.groups]
CATEGORY_OF = {g.source: c for c in CATEGORIES for g in c.groups}


# --- the route -----------------------------------------------------------
# The front page draws the journey the collection already describes. The stops
# are a second *reading* of the same markdown, not a second taxonomy: each
# names the source files it covers, so its count is summed from parsed entries
# rather than typed, and each links into the category page that already holds
# those files. Nothing here changes a URL or an anchor.
#
# Exhibit is its own stop rather than part of Grow, because a deadline is what
# finishes a student project and it comes before any question of funding.


@dataclass
class Station:
    n: str
    name: str
    page: str
    hook: str
    lede: str
    sources: list
    picks: list = field(default_factory=list)
    section: str = ""       # deep-link into a section of the category page
    label: str = ""         # what the destination is called once you land there
    counted: bool = True

    @property
    def count(self) -> int:
        return sum(g.count for g in GROUPS if g.source in self.sources)

    @property
    def dest(self) -> str:
        """A stop and the page it lands on need not share a name: Show lands in
        the Exhibit group of the Grow page, so say Exhibit rather than Grow."""
        return self.label or self.page.title()

    @property
    def href(self) -> str:
        return f"{self.page}/#{slugify(self.section)}" if self.section else f"{self.page}/"


START = Station(
    "00", "Start here", "build",
    "Four things, whatever you build", "",
    ["prototyping_resources.md"],
    section="Start here — applicable to any build", counted=False)

STATIONS = [
    Station(
        "01", "Build", "build",
        "Software, AI and data",
        "Nothing has to be bought yet. A laptop, a simulator and someone "
        "else's dataset take a robot idea further than most people expect.",
        ["prototyping_resources.md", "generative_ai_agents.md", "datasets.md"],
        ["ROS 2", "Gazebo", "Nav2", "PhenoBench"]),
    Station(
        "02", "Make", "make",
        "Machines, parts and space",
        "Where the CAD file becomes a part and the part becomes a robot. "
        "Workshops within reach of campus, suppliers that ship to Bonn, and "
        "rooms to build and test in.",
        ["nrw_hardware_contacts.md", "bonn_physical_spaces.md"],
        ["MakerSpace Bonn e.V.", "BerryBase", "reichelt elektronik",
         "AStA — student groups"]),
    Station(
        "03", "Show", "grow",
        "Competitions, publishing",
        "A fixed date finishes projects that nothing else finishes. "
        "Competitions give the deadline, publishing gives the feedback, and "
        "events give the audience.",
        ["work_exhibit.md"],
        ["RoboCup", "Field Robot Event", "Hackaday.io", "Weekly Robotics"],
        section="Competitions worth entering", label="Exhibit"),
    Station(
        "04", "Grow", "grow",
        "Funding and the rules",
        "What happens once the prototype works: the money that scales it, and "
        "the regulation that applies the moment it is sold rather than merely "
        "demonstrated.",
        ["nrw_investor_contacts.md", "certification_resources.md"],
        ["enaCom — Uni Bonn Transfer Center", "Gründungsstipendium.NRW",
         "EXIST-Gründungsstipendium", "CE marking"]),
]

# The city is the ground the route stands on rather than a stop along it.
GROUND = "builder_helpers.md"

# Rows lifted from the "Bonn at a glance" table so the band cannot drift from
# the markdown it summarises.
GLANCE = ["Room rent", "Monthly total", "Main tradeoff"]


# --- facets --------------------------------------------------------------
# The tags already in the markdown are a vocabulary, not decoration. Grouping
# them into facets is what turns the collection into something filterable.

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


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-")


def link_target(href: str) -> str:
    """Point a cross-file link at the category page that absorbed that file."""
    if href in CATEGORY_OF:
        return f"../{CATEGORY_OF[href].slug}/"
    return href


def inline_html(md: str) -> str:
    """Render the small subset of markdown that appears inside a description.

    Descriptions are rendered here rather than by MkDocs, so links between the
    source files have to be redirected to their category page at this point."""
    out = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                 lambda m: f'<a href="{link_target(m.group(2))}" rel="noopener">'
                           f"{m.group(1)}</a>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def parse(group: Group, category: Category, text: str) -> list[dict]:
    """Pull every entry out of one source file, with its section context."""
    entries, section, blurb = [], None, None
    for line in text.splitlines():
        if line.startswith("## "):
            section, blurb = line[3:].strip(), None
            group.sections.append(section)
            continue
        # The italic line under a heading explains why the section exists.
        if section and blurb is None and re.fullmatch(r"\*[^*].*\*", line.strip()):
            blurb = line.strip()[1:-1]
            continue
        match = ENTRY.match(line)
        if not match:
            continue
        rest = match.group("rest")
        tags: list[str] = []
        if tail := TAIL.search(rest):
            tags = TAG.findall(tail.group("tags"))
            rest = rest[: tail.start()]
        facets = {key: [] for key, _, _ in FACETS}
        kinds = []
        for tag in tags:
            facets.get(FACET_OF.get(tag, ""), kinds).append(tag)
        entries.append({
            "name": match.group("name"),
            "url": match.group("url"),
            "desc": inline_html(rest.rstrip(" .") + "."),
            "tags": tags,
            "kind": kinds,
            **facets,
            "page": category.slug,
            "page_nav": category.nav,
            "group": group.name,
            "section": section or group.name,
            "anchor": f"{category.slug}/#{slugify(section)}" if section else category.slug,
        })
    return entries


# --- staging -------------------------------------------------------------

def row(line: str) -> str:
    """Render one entry as a hairline row rather than a bullet.

    The reference robotics sites present lists of things as rows — name, one
    line, labels — with rules doing the work that borders and cards would. Only
    the staged copy changes; the markdown keeps its bullets."""
    match = ENTRY.match(line)
    if not match:
        return line
    rest = match.group("rest")
    tags: list[str] = []
    if tail := TAIL.search(rest):
        tags = TAG.findall(tail.group("tags"))
        rest = rest[: tail.start()]
    chips = "".join(f"<span>{t}</span>" for t in tags)
    return (f'<div class="row">'
            f'<a class="row-name" href="{match.group("url")}" rel="noopener">'
            f'{match.group("name")}</a>'
            f'<div class="row-desc">{inline_html(rest.rstrip(" .") + ".")}</div>'
            f'<div class="row-tags">{chips}</div></div>')


def stage_body(text: str) -> str:
    """Drop the file's own H1 and turn its entry bullets into rows."""
    body = text.split("\n", 1)[1].lstrip("\n") if text.startswith("# ") else text
    out, in_list = [], False
    for line in body.splitlines():
        rendered = row(line)
        if rendered is not line:
            # Rows are block-level HTML, so they must not sit inside a <ul>.
            out.append(rendered)
            in_list = True
            continue
        if in_list and line.strip() == "":
            in_list = False
        out.append(line)
    return "\n".join(out)


def stage_category(category: Category, texts: dict[str, str]) -> str:
    """Concatenate a category's source files, each as a numbered group."""
    blocks = []
    for i, group in enumerate(category.groups, 1):
        blocks.append(
            f'<div class="group-head">'
            f'<span class="group-n">{i:02d}</span>'
            f'<span class="group-main">'
            f'<span class="group-name">{group.name}</span>'
            f'<span class="group-blurb">{group.blurb}</span>'
            f"</span>"
            f'<span class="group-count">{group.count}</span>'
            f"</div>\n\n" + stage_body(texts[group.source]))
    return (f"---\nhide:\n  - navigation\n---\n\n"
            f'<p class="eyebrow">{category.count} resources · '
            f'{len(category.groups)} sources</p>\n'
            f'<h1 class="page-title">{category.title}</h1>\n'
            f'<p class="lede">{category.lede}</p>\n\n'
            + "\n\n".join(blocks))


def glance(text: str) -> dict[str, str]:
    """Read the two-column 'at a glance' table out of the city file.

    The band on the front page quotes a few of these rows, so they are parsed
    rather than retyped; main() fails if a quoted row stops existing."""
    found: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 2 and cells[0] and set(cells[0]) != {"-"}:
            found[cells[0]] = cells[1]
    return found


# --- landing page --------------------------------------------------------

def home(entries: list[dict], facts: dict[str, str]) -> str:
    """The front page: the route from an idea to a working robot.

    The collection already describes a journey, so the page draws it rather
    than listing four categories and leaving the reader to infer the order.
    It is still an index kept by a club: no hero image, no stats band, and
    every number summed from the parsed entries. The named picks under each
    stop are the one piece of hand-curation on the site, and main() checks
    each one against the markdown so a rename fails the build."""
    sections = sum(len(g.sections) for g in GROUPS)
    url_of = {e["name"]: e["url"] for e in entries}
    ground = next(g for g in GROUPS if g.source == GROUND)

    nodes = []
    for station in [START] + STATIONS:
        count = (f'<span class="node-n">{station.count}</span>'
                 if station.counted else "")
        nodes.append(
            f'<a class="node{"" if station.counted else " node-start"}" '
            f'href="{station.href}">'
            f'<span class="node-dot">{station.n}</span>'
            f'<span class="node-name">{station.name}</span>'
            f'<span class="node-hook">{station.hook}{count}</span></a>')

    stops = []
    for station in STATIONS:
        picks = " · ".join(
            f'<a href="{url_of[p]}" rel="noopener">{p}</a>'
            for p in station.picks if p in url_of)
        stops.append(f"""<div class="stop">
  <span class="stop-n">{station.n}</span>
  <div class="stop-main">
    <a class="stop-name" href="{station.href}">{station.name}</a>
    <p class="stop-lede">{station.lede}</p>
    <p class="stop-picks">{picks}</p>
  </div>
  <a class="stop-all" href="{station.href}">{station.count} in {station.dest} →</a>
</div>""")

    rows = "".join(
        f'<div class="fact"><dt>{label}</dt><dd>{facts[label]}</dd></div>'
        for label in GLANCE)

    return f"""---
template: home.html
hide:
  - navigation
  - toc
---

<div class="wrap">
  <header class="masthead">
    <p class="eyebrow-rule">Robonn · Universität Bonn</p>
    <h1>From an idea to a robot that actually works.</h1>
    <p class="masthead-what">Everything in between, in the order it is needed —
    the software that costs nothing, the machines within reach of campus, the
    deadlines that force a project to finish, and the money that comes after.
    One line per entry on why it matters, so the useful thing is findable
    without reading twelve listicles.</p>
    <p class="meta">{len(entries)} entries · {sections} sections ·
    {len(GROUPS)} files · <a href="browse/">browse everything</a></p>
  </header>

  <nav class="route" aria-label="The route">
    <span class="route-line" aria-hidden="true"></span>
    <div class="route-nodes">{"".join(nodes)}</div>
  </nav>

  <div class="stops">{"".join(stops)}</div>
</div>

<section class="ground">
  <div class="wrap ground-in">
    <div class="ground-say">
      <p class="eyebrow-rule">The ground it all stands on</p>
      <h2>Bonn</h2>
      <p class="ground-what">Bonn carries more robotics and AI research than a
      city of its size would suggest — and there is nowhere in it to test a
      robot. Both halves are written down: what a month costs, what an arriving
      student has to do first, and which groups and employers sit within reach.</p>
      <a class="ground-all" href="{CATEGORY_OF[GROUND].slug}/">{ground.count} entries on the city →</a>
    </div>
    <dl class="facts">{rows}</dl>
  </div>
</section>

<div class="wrap colophon">
  <p class="colophon-what">Kept by
  <a href="https://github.com/robonn-club" rel="noopener">Robonn</a>, the robotics
  club at Universität Bonn. {len(entries)} entries across {len(GROUPS)} markdown
  files, added by pull request; every external link is checked weekly, and a dead
  one opens an issue rather than sitting there.</p>
  <p class="colophon-links">
    <a href="{REPO}/blob/main/CONTRIBUTING.md" rel="noopener">Add an entry →</a>
    <a href="browse/">Browse all {len(entries)} →</a>
    <a href="https://github.com/robonn-club" rel="noopener">Join Robonn →</a>
  </p>
</div>
"""


def browse(entries: list[dict]) -> str:
    groups = []
    for key, label, order in FACETS:
        present = [t for t in order if any(t in e[key] for e in entries)]
        if not present:
            continue
        chips = "".join(
            f'<button class="chip" data-facet="{key}" data-value="{t}">{t}'
            f'<span class="chip-n">{sum(1 for e in entries if t in e[key])}</span></button>'
            for t in present)
        groups.append(f'<div class="facet"><h3>{label}</h3><div class="chips">{chips}</div></div>')
    topics = "".join(
        f'<button class="chip" data-facet="page" data-value="{c.slug}">{c.nav}'
        f'<span class="chip-n">{c.count}</span></button>' for c in CATEGORIES)
    groups.insert(0, f'<div class="facet"><h3>Category</h3><div class="chips">{topics}</div></div>')
    return f"""---
hide:
  - navigation
  - toc
---

<p class="eyebrow">Everything · {len(entries)} resources</p>
<h1 class="page-title">Browse</h1>
<p class="lede">Every entry from all three categories in one place. Filter by
what it costs, where it is, and what licence it carries.</p>

<div class="browse" markdown="0">
  <input type="search" id="q" class="search" placeholder="Search {len(entries)} resources…"
         autocomplete="off" spellcheck="false" aria-label="Search resources">
  <div class="facets">{"".join(groups)}</div>
  <div class="browse-bar">
    <span id="count" aria-live="polite"></span>
    <button id="reset" class="reset" hidden>Clear filters</button>
  </div>
  <div id="results" class="rows"></div>
  <p id="empty" class="empty" hidden>Nothing matches those filters.</p>
</div>
"""


def check(entries: list[dict], facts: dict[str, str]) -> list[str]:
    """Everything the route asserts about the markdown, verified once.

    The route names entries, sections and table rows by hand. Without this the
    front page would quietly drop a renamed pick — the same silent failure
    CONTRIBUTING.md warns about for malformed entries."""
    problems = []
    names = {e["name"] for e in entries}
    for station in STATIONS:
        for pick in station.picks:
            if pick not in names:
                problems.append(f"station {station.name}: no entry named {pick!r}")

    anchors = {(e["page"], e["section"]) for e in entries}
    for station in [START] + STATIONS:
        if station.section and (station.page, station.section) not in anchors:
            problems.append(f"station {station.name}: {station.page}.md has no "
                            f"section {station.section!r}")

    routed = {s for station in STATIONS for s in station.sources}
    for group in GROUPS:
        if group.source != GROUND and group.source not in routed:
            problems.append(f"{group.source} sits on no station of the route")

    for label in GLANCE:
        if label not in facts:
            problems.append(f"'Bonn at a glance' has no {label!r} row")
    return problems


def main() -> int:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    DOCS.mkdir(parents=True)

    entries: list[dict] = []
    texts: dict[str, str] = {}
    for category in CATEGORIES:
        for group in category.groups:
            text = (SRC / group.source).read_text(encoding="utf-8")
            texts[group.source] = text
            found = parse(group, category, text)
            group.count = len(found)
            entries += found

    facts = glance(texts[GROUND])
    if problems := check(entries, facts):
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return 1

    for category in CATEGORIES:
        (DOCS / f"{category.slug}.md").write_text(
            stage_category(category, texts), encoding="utf-8")
    (DOCS / "index.md").write_text(home(entries, facts), encoding="utf-8")
    (DOCS / "browse.md").write_text(browse(entries), encoding="utf-8")

    # Cross-links between source files now point at the category that absorbed
    # them, keeping the section anchor where the target section is named.
    rename = {g.source: f"{CATEGORY_OF[g.source].slug}.md" for g in GROUPS}
    for md in DOCS.glob("*.md"):
        body = md.read_text(encoding="utf-8")
        for source, target in rename.items():
            body = body.replace(f"({source})", f"({target})")
        md.write_text(body, encoding="utf-8")

    assets = DOCS / "assets"
    shutil.copytree(ROOT / "site_assets", assets)
    (assets / "resources.json").write_text(
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")

    print(f"staged {len(entries)} entries → {DOCS}")
    for category in CATEGORIES:
        print(f"  {category.count:>4}  {category.nav}")
        for group in category.groups:
            print(f"        {group.count:>4}  {group.source}")
    route = " → ".join(f"{s.name} {s.count}" for s in STATIONS)
    print(f"  route  {route}  ·  on {GROUND}")
    return 0


if __name__ == "__main__":
    code = main()
    if code == 0 and "--serve" in sys.argv:
        code = subprocess.call(["mkdocs", "serve"], cwd=ROOT)
    sys.exit(code)

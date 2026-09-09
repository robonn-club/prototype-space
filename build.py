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

# --- three categories ----------------------------------------------------
# Navigation is three entries, because there are really only three kinds of
# thing here. Each source markdown file survives inside its category as a
# numbered group, so the files stay the unit people contribute to and every
# section keeps its own anchor.


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
]

GROUPS = [g for c in CATEGORIES for g in c.groups]
CATEGORY_OF = {g.source: c for c in CATEGORIES for g in c.groups}


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
            f'<span class="group-name">{group.name}</span>'
            f'<span class="group-blurb">{group.blurb}</span>'
            f'<span class="group-count">{group.count}</span>'
            f"</div>\n\n" + stage_body(texts[group.source]))
    return (f"---\nhide:\n  - navigation\n---\n\n"
            f'<p class="eyebrow">{category.count} resources · '
            f'{len(category.groups)} sources</p>\n'
            f'<h1 class="page-title">{category.title}</h1>\n'
            f'<p class="lede">{category.lede}</p>\n\n'
            + "\n\n".join(blocks))


# --- landing page --------------------------------------------------------

def home(entries: list[dict]) -> str:
    """The front page: a masthead and the contents, and nothing else.

    This is an index kept by a club, not a product being launched, so there is
    no hero, no call to action and no stats band. Counts appear once, as facts,
    and every number is read from the parsed data."""
    sections = sum(len(g.sections) for g in GROUPS)

    index = []
    for i, category in enumerate(CATEGORIES, 1):
        groups = "".join(
            f'<span class="idx-group">{g.name}<i>{g.count}</i></span>'
            for g in category.groups)
        index.append(f"""<a class="idx" href="{category.slug}/">
  <span class="idx-n">{i:02d}</span>
  <span class="idx-main">
    <span class="idx-name">{category.nav}</span>
    <span class="idx-hook">{category.hook}</span>
    <span class="idx-groups">{groups}</span>
  </span>
  <span class="idx-count">{category.count}</span>
</a>""")

    return f"""---
template: home.html
hide:
  - navigation
  - toc
---

<div class="wrap">
  <header class="masthead">
    <h1>prototype</h1>
    <p class="masthead-what">An index of robotics resources, kept by
    <a href="https://github.com/robonn-club" rel="noopener">Robonn</a> — the robotics
    club at Universität Bonn. One line per entry on why it matters, so you can find
    the useful thing without reading twelve listicles.</p>
    <p class="meta">{len(entries)} entries · {sections} sections ·
    {len(GROUPS)} files · <a href="browse/">browse everything</a></p>
  </header>

  <div class="index">{"".join(index)}</div>

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

    for category in CATEGORIES:
        (DOCS / f"{category.slug}.md").write_text(
            stage_category(category, texts), encoding="utf-8")
    (DOCS / "index.md").write_text(home(entries), encoding="utf-8")
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
    return 0


if __name__ == "__main__":
    code = main()
    if code == 0 and "--serve" in sys.argv:
        code = subprocess.call(["mkdocs", "serve"], cwd=ROOT)
    sys.exit(code)

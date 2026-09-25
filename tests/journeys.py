#!/usr/bin/env python3
"""Can a visitor find their next step? Walk the main journeys like one would.

Each journey starts on the front page, clicks only what a visitor would see
(a row, a card, a link text; never a URL typed in), and passes when the answer
it came for is on screen after landing, not merely somewhere on the page.
Every journey runs twice: on a laptop screen and on a phone.

    python3 build.py && mkdocs build --strict
    python3 -m http.server 8000 --directory _build/site &
    python3 tests/journeys.py http://localhost:8000/ [--shots DIR]

Needs Playwright:  pip install playwright && playwright install chromium
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright

DEVICES = {
    "laptop": dict(viewport={"width": 1366, "height": 900}),
    "phone": dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True,
                  device_scale_factor=2),
}


@dataclass
class Visit:
    page: Page
    base: str
    clicks: int = 0

    def home(self) -> None:
        self.page.goto(self.base, wait_until="networkidle")

    def click(self, locator, url: str) -> None:
        """Click as a visitor would, then wait for the address to change."""
        locator.scroll_into_view_if_needed()
        locator.click()
        self.page.wait_for_url(re.compile(url), timeout=10_000)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(250)          # anchor scroll after instant loading
        self.clicks += 1

    def on_screen(self, locator) -> None:
        expect(locator.first).to_be_in_viewport(timeout=5_000)


def finder(v: Visit, situation: str):
    return v.page.locator(".finder-row", has_text=situation)


# --- the journeys ------------------------------------------------------------
# Each takes a Visit and returns a short note on what the visitor ended up with.

def idea_to_plan(v: Visit) -> str:
    """'I have an idea for a weeding robot. What do I do first?'"""
    v.home()
    v.click(finder(v, "I have an idea"), r"/steps/plan/$")
    v.on_screen(v.page.locator(".done-when"))
    v.page.get_by_text("Write the claim in one sentence").first.scroll_into_view_if_needed()
    v.click(v.page.locator(".track-table .tt-row", has_text="Field robot"), r"/tracks/field/#plan$")
    v.on_screen(v.page.get_by_text("Bring the field indoors"))
    return "step 1, then the field track's plan"


def sim_to_parts(v: Visit) -> str:
    """'My mobile robot drives in Gazebo. What now?'"""
    v.home()
    v.click(finder(v, "It works in simulation"), r"/steps/parts/$")
    v.on_screen(v.page.get_by_role("heading", name="Parts"))
    v.click(v.page.locator(".track-table .tt-row", has_text="Mobile robot"), r"/tracks/mobile/#parts$")
    v.on_screen(v.page.locator("p.sum", has_text="TurtleBot"))
    return "step 3, then which base to buy"


def parts_to_build(v: Visit) -> str:
    """'The parts for my arm arrived.'"""
    v.home()
    v.click(finder(v, "The parts are here"), r"/steps/build/$")
    v.on_screen(v.page.locator(".done-when"))
    v.click(v.page.locator(".track-table .tt-row", has_text="Robot arm"), r"/tracks/arm/#build$")
    v.on_screen(v.page.locator("p.sum", has_text="calibrate"))
    return "step 4, then calibrate before training"


def bench_to_test(v: Visit) -> str:
    """'It runs on the bench. Where in Bonn can I actually test it?'"""
    v.home()
    v.click(finder(v, "It runs on the bench"), r"/steps/test/$")
    v.on_screen(v.page.locator(".done-when", has_text="five times in a row"))
    v.page.get_by_role("heading", name="Where to test in Bonn").scroll_into_view_if_needed()
    v.on_screen(v.page.get_by_text("A seminar room").first)
    return "step 5 and its list of places to test"


def works_to_show(v: Visit) -> str:
    """'It works. How do I make people believe it?'"""
    v.home()
    v.click(finder(v, "It works in its real setting"), r"/steps/show/$")
    v.on_screen(v.page.locator(".done-when"))
    bar = v.page.locator("ol.bar li")
    expect(bar).to_have_count(5)
    v.page.get_by_role("heading", name="Pick a date").scroll_into_view_if_needed()
    v.on_screen(v.page.get_by_role("link", name="Maker Faire Ruhr"))
    return "step 6: the five-point bar and dated events"


def credible_to_after(v: Visit) -> str:
    """'It's credible. Could it become a company?'"""
    v.home()
    v.click(finder(v, "It's credible"), r"/steps/after/$")
    v.page.get_by_role("heading", name="Start a company").scroll_into_view_if_needed()
    v.on_screen(v.page.get_by_role("link", name="enaCom — Uni Bonn Transfer Center"))
    return "after: talk to enaCom first"


def where_to_print(v: Visit) -> str:
    """'Where can I 3D print a bracket in Bonn?' — answered on the front page."""
    v.home()
    answer = v.page.locator(".qa", has_text="Where can I 3D print")
    answer.scroll_into_view_if_needed()
    expect(answer).to_contain_text("MakerSpace Bonn")
    v.click(answer.get_by_role("link", name=re.compile("Places to make")), r"/bonn/#make$")
    v.on_screen(v.page.locator(".row-name", has_text="MakerSpace Bonn e.V."))
    return "front page answer, then the Bonn page"


def drone_rules(v: Visit) -> str:
    """'Can I fly my drone over the Rheinaue?'"""
    v.home()
    answer = v.page.locator(".qa", has_text="Can I fly a drone")
    answer.scroll_into_view_if_needed()
    v.click(answer.get_by_role("link", name=re.compile("drone rules")), r"/tracks/drone/#before-you-fly$")
    v.on_screen(v.page.get_by_text("Registration.").first)
    expect(v.page.get_by_role("link", name="dipul map tool").first).to_be_visible()
    return "the drone rules, with the official map"


def money(v: Visit) -> str:
    """'Is there money for parts?'"""
    v.home()
    answer = v.page.locator(".qa", has_text="Is there money for parts")
    answer.scroll_into_view_if_needed()
    v.click(answer.get_by_role("link", name=re.compile("Money in Bonn")), r"/bonn/#money$")
    v.on_screen(v.page.get_by_text("not a budget for parts"))
    return "an honest answer on the Bonn page"


def track_first(v: Visit) -> str:
    """'I want to build a drone' — then the steps remember it."""
    v.home()
    v.click(v.page.locator(".track-card", has_text="Drone"), r"/tracks/drone/$")
    v.on_screen(v.page.get_by_text("A credible first build"))
    step = v.page.locator(".to-step", has_text="Step 5 in full").get_by_role("link")
    v.click(step, r"/steps/test/$")
    first = v.page.locator(".track-table .tt-row").first
    first.scroll_into_view_if_needed()
    expect(first).to_have_class(re.compile("is-mine"))
    expect(first).to_contain_text("Drone")
    return "drone track, then step 5 with the drone row first"


def find_dataset(v: Visit) -> str:
    """'Is there a dataset of sugar beet fields?'"""
    v.home()
    if v.page.viewport_size["width"] < 1220:     # tabs fold into the drawer on phones
        v.page.locator("label.md-header__button[for='__drawer']").click()
        v.page.wait_for_timeout(300)
        v.click(v.page.locator(".md-nav--primary").get_by_role("link", name="Directory").first,
                r"/directory/$")
    else:
        v.click(v.page.locator(".md-tabs").get_by_role("link", name="Directory"), r"/directory/$")
    v.click(v.page.get_by_role("link", name=re.compile("Search and filter")), r"/browse/$")
    v.page.locator("#q").fill("sugar beet")
    v.on_screen(v.page.locator("#results .row-name", has_text="Sugar Beets 2016"))
    return "directory search, first screen"


def site_search(v: Visit) -> str:
    """'Where can I laser cut?' typed into the search box instead."""
    v.home()
    if v.page.viewport_size["width"] < 960:      # the search box folds into an icon on phones
        v.page.locator("label.md-header__button[for='__search']").click()
    else:
        v.page.locator(".md-search__input").click()
    v.page.keyboard.type("laser", delay=40)      # search reacts to keys, as a person types
    results = v.page.locator(".md-search-result__item")
    expect(results.first).to_be_visible(timeout=10_000)
    expect(v.page.locator(".md-search-result")).to_contain_text("MakerSpace")
    return f"{results.count()} search results, MakerSpace among them"


JOURNEYS = [idea_to_plan, sim_to_parts, parts_to_build, bench_to_test, works_to_show,
            credible_to_after, where_to_print, drone_rules, money, track_first, find_dataset,
            site_search]

# Old addresses that must still land on the same content.
REDIRECTS = [
    ("build/#mobile-robot", r"/directory/tools/#mobile-robot$"),
    ("build/#agriculture-and-plants", r"/directory/datasets/#agriculture-and-plants$"),
    ("make/", r"/directory/hardware/$"),
    ("grow/#licences", r"/directory/compliance/#licences$"),
    ("bonn/#arriving-and-registering", r"/directory/city/#arriving-and-registering$"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("base", nargs="?", default="http://localhost:8000/")
    parser.add_argument("--shots", type=Path, help="save a screenshot where each journey ends")
    args = parser.parse_args()
    base = args.base.rstrip("/") + "/"
    if args.shots:
        args.shots.mkdir(parents=True, exist_ok=True)

    failures = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for device, options in DEVICES.items():
            print(f"\n{device}  {options['viewport']['width']}×{options['viewport']['height']}")
            for journey in JOURNEYS:
                context = browser.new_context(**options)
                page = context.new_page()
                errors: list[str] = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                visit = Visit(page, base)
                started = time.monotonic()
                try:
                    note = journey(visit)
                    if errors:
                        raise AssertionError(f"script error: {errors[0]}")
                    overflow = page.evaluate("document.documentElement.scrollWidth > innerWidth")
                    if overflow:
                        raise AssertionError("the page scrolls sideways")
                    status = f"ok    {visit.clicks} click{'s' if visit.clicks != 1 else ''}  {note}"
                except Exception as error:                      # noqa: BLE001 — report and go on
                    failures += 1
                    status = f"FAIL  {str(error).splitlines()[0][:110]}"
                if args.shots:
                    page.screenshot(path=args.shots / f"{device}-{journey.__name__}.png")
                took = time.monotonic() - started
                print(f"  {journey.__name__:<18} {status}  ({took:.1f}s)  → {page.url.removeprefix(base)}")
                context.close()

        context = browser.new_context(**DEVICES["laptop"])
        page = context.new_page()
        print("\nold addresses")
        for old, expected in REDIRECTS:
            page.goto(base + old, wait_until="networkidle")
            try:
                page.wait_for_url(re.compile(expected), timeout=5_000)
                print(f"  ok    {old:<32} → {page.url.removeprefix(base)}")
            except Exception:                                   # noqa: BLE001
                failures += 1
                print(f"  FAIL  {old:<32} → {page.url.removeprefix(base)}")
        browser.close()

    print(f"\n{'all journeys passed' if not failures else f'{failures} failed'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

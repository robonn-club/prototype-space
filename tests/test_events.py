"""The rules that keep the workshops and events list honest over time.

    python3 -m unittest discover tests

No browser needed; the deploy workflow runs these before every build.
"""

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import events as ev  # noqa: E402

FILE = ROOT / "guide" / "events.yml"
SAMPLE = Path(__file__).parent / "events_sample.yml"   # frozen; the real file changes weekly
D = dt.date


def load(day):
    listings, sources, problems = ev.load(SAMPLE, day)
    return {e["title"]: e for e in listings}, listings, problems


def entry(**changes):
    base = {"title": "A workshop", "organiser": "Someone", "topics": ["ai"], "format": "workshop",
            "region": "bonn", "date": D(2026, 11, 1), "time": "10:00–12:00", "place": "Somewhere, Bonn",
            "cost": "Free", "who": "Students", "language": "English", "register": "https://example.org/r",
            "source": "https://example.org/", "checked": D(2026, 10, 1), "summary": "Short and clear."}
    base.update(changes)
    return {k: v for k, v in base.items() if v is not ...}


class TheRealFile(unittest.TestCase):
    def test_every_entry_is_valid_today(self):
        listings, _, problems = ev.load(FILE, ev.today())
        self.assertEqual(problems, [])
        self.assertTrue(listings)

    def test_every_listing_names_its_source_and_check_date(self):
        listings, _, _ = ev.load(FILE, ev.today())
        for e in listings:
            self.assertTrue(e["source"].startswith("http"), e["title"])
            self.assertIsInstance(e["checked"], dt.date, e["title"])


class Expiry(unittest.TestCase):
    def test_an_event_shows_on_its_day_and_disappears_the_next(self):
        by, listings, _ = load(D(2026, 10, 15))
        self.assertIn(by["KI Summit Bonn"], ev.upcoming(listings, D(2026, 10, 15)))
        self.assertNotIn(by["KI Summit Bonn"], ev.upcoming(listings, D(2026, 10, 16)))

    def test_a_multi_day_event_stays_until_its_last_day(self):
        by, listings, _ = load(D(2026, 11, 22))
        hackathon = by["Green Bonn Hackathon 2026"]
        self.assertIn(hackathon, ev.upcoming(listings, D(2026, 11, 22)))
        self.assertNotIn(hackathon, ev.upcoming(listings, D(2026, 11, 23)))

    def test_a_deadline_turns_into_applications_closed(self):
        by, _, _ = load(D(2026, 10, 20))
        hackathon = by["Green Bonn Hackathon 2026"]
        self.assertIn("Apply by", ev.card(hackathon, D(2026, 10, 20)))
        self.assertIn("Applications closed", ev.card(hackathon, D(2026, 10, 30)))

    def test_recurring_programmes_move_to_the_next_announced_date(self):
        by, _, _ = load(D(2026, 10, 15))
        self.assertEqual(by["Gründungsstammtisch (founders' meetup)"].dates[0], D(2026, 12, 9))

    def test_a_programme_whose_dates_have_passed_says_so_and_is_reported(self):
        day = D(2026, 10, 20)
        by, listings, _ = load(day)
        makerspace = by["Offene Tür (open evening)"]
        self.assertEqual(makerspace.dates, [])
        self.assertIn("Regular", ev.date_block(makerspace))
        text, actionable = ev.report(listings, [], day)
        self.assertTrue(actionable)
        self.assertIn("Offene Tür", text.split("announced dates have all passed")[1])

    def test_weekly_programmes_compute_their_next_dates(self):
        by, _, _ = load(D(2026, 10, 13))                        # a Tuesday
        self.assertEqual(by["Offener Burgabend (open evening)"].dates[:2], [D(2026, 10, 13), D(2026, 10, 20)])
        by, _, _ = load(D(2026, 10, 14))
        self.assertEqual(by["Offener Burgabend (open evening)"].dates[0], D(2026, 10, 20))

    def test_the_review_lists_past_events_for_deletion(self):
        day = D(2027, 1, 1)
        _, listings, _ = load(day)
        text, actionable = ev.report(listings, [], day)
        self.assertTrue(actionable)
        self.assertIn("KI Summit Bonn", text.split("Delete")[1].split("##")[0])


class Checks(unittest.TestCase):
    day = D(2026, 10, 10)

    def problems(self, data):
        return ev.check(data, self.day)

    def test_a_good_entry_passes(self):
        self.assertEqual(self.problems(entry()), [])

    def test_no_postal_addresses(self):
        self.assertTrue(self.problems(entry(place="Bornheimer Straße 25, Bonn")))
        self.assertTrue(self.problems(entry(place="Venue, 53111 Bonn")))

    def test_no_contact_details(self):
        self.assertTrue(self.problems(entry(note="Write to someone@example.org")))
        self.assertTrue(self.problems(entry(note="Call +49 228 123456")))

    def test_shape(self):
        self.assertTrue(self.problems(entry(topics=["cooking"])))
        self.assertTrue(self.problems(entry(recurring="Every Monday")))          # date and recurring
        self.assertTrue(self.problems(entry(date=..., recurring=...)))           # neither
        self.assertTrue(self.problems(entry(end=D(2026, 10, 1))))                # ends before it starts
        self.assertTrue(self.problems(entry(checked=D(2026, 12, 1))))            # checked in the future
        self.assertTrue(self.problems(entry(source="example.org")))
        self.assertTrue(self.problems(entry(summary=...)))                       # missing field
        self.assertTrue(self.problems(entry(summary="No full stop")))

    def test_unchecked_fields_are_allowed_but_reported(self):
        data = entry(cost=None)
        self.assertEqual(self.problems(data), [])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.yml"
            path.write_text("events:\n  - " + "\n    ".join(
                f"{k}: {v if not isinstance(v, list) else '[' + ', '.join(v) + ']'}" if v is not None else f"{k}: ~"
                for k, v in data.items()) + "\n", encoding="utf-8")
            listings, _, problems = ev.load(path, self.day)
            self.assertEqual(problems, [])
            text, _ = ev.report(listings, [], self.day)
            self.assertIn("Fill in", text)
            self.assertNotIn("<dt>Cost</dt>", ev.card(listings[0], self.day))


class Cards(unittest.TestCase):
    """What a card shows: kept short on purpose."""
    day = D(2026, 10, 10)

    def card(self, **changes):
        listings, _, problems = self.load(entry(**changes))
        self.assertEqual(problems, [])
        return ev.card(listings[0], self.day)

    def load(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.yml"
            import yaml
            path.write_text(yaml.safe_dump({"events": [data]}, allow_unicode=True), encoding="utf-8")
            return ev.load(path, self.day)

    def test_one_link_called_page_to_the_events_own_page(self):
        html = self.card(note="Bring a laptop.", who="Students", register="https://example.org/form")
        self.assertIn('href="https://example.org/" rel="noopener" aria-label="Page for A workshop">Page</a>', html)
        for gone in ("Register", "Organiser", "calendar", "Checked", "<dt>Who</dt>", "Bring a laptop",
                     "Confirmed", "https://example.org/form"):
            self.assertNotIn(gone, html)

    def test_cost_only_when_the_organiser_states_it(self):
        self.assertIn("<dt>Cost</dt><dd>Free</dd>", self.card(cost="Free"))
        self.assertNotIn("<dt>Cost</dt>", self.card(cost="not stated"))
        self.assertNotIn("<dt>Cost</dt>", self.card(cost=None))


class Calendar(unittest.TestCase):
    def test_times_are_in_bonn_time(self):
        by, _, _ = load(D(2026, 10, 10))
        text = ev.ics([by["KI Summit Bonn"]], D(2026, 10, 10), dt.datetime(2026, 10, 10, tzinfo=dt.timezone.utc), "")
        self.assertIn("DTSTART:20261015T160000Z", text)              # 18:00 summer time in Bonn
        self.assertIn("DTEND:20261015T190000Z", text)
        self.assertTrue(text.startswith("BEGIN:VCALENDAR\r\n"))
        for line in text.split("\r\n"):
            self.assertLessEqual(len(line.encode("utf-8")), 75)

    def test_multi_day_events_are_all_day(self):
        by, _, _ = load(D(2026, 10, 10))
        text = ev.ics([by["Green Bonn Hackathon 2026"]], D(2026, 10, 10),
                      dt.datetime(2026, 10, 10, tzinfo=dt.timezone.utc), "")
        self.assertIn("DTSTART;VALUE=DATE:20261116", text)
        self.assertIn("DTEND;VALUE=DATE:20261123", text)


if __name__ == "__main__":
    unittest.main()

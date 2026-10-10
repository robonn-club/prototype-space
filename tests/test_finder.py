"""The weekly event finder, tested on small copies of what the organisers publish.

    python3 -m unittest discover tests

No network: every calendar and page below is a trimmed copy of the real thing
(October 2026), so a change in the finder's rules shows up here first.
"""

import datetime as dt
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import events as ev  # noqa: E402
import find_events as fe  # noqa: E402

D = dt.date
DAY = D(2026, 10, 10)

ICS = (
    "BEGIN:VCALENDAR\r\nVERSION:2.0\r\n"
    "BEGIN:VTIMEZONE\r\nTZID:Europe/Berlin\r\nBEGIN:STANDARD\r\nDTSTART:19701025T030000\r\nEND:STANDARD\r\nEND:VTIMEZONE\r\n"
    "BEGIN:VEVENT\r\nSUMMARY:From an AI Idea to the First Prototype\r\n"
    "DTSTART;TZID=Europe/Berlin:20270218T100000\r\nDTEND;TZID=Europe/Berlin:20270218T140000\r\n"
    "URL:https://www.uni-bonn.de/en/events/from-an-ai-idea-to-the-first-prototype\r\n"
    "DESCRIPTION:You have an idea but are wondering how to test it. In this workshop you\r\n"
    " will learn to state a clear problem\\, and a hypothesis.\r\n"
    "BEGIN:VALARM\r\nDESCRIPTION:Reminder\r\nEND:VALARM\r\n"
    "END:VEVENT\r\n"
    "BEGIN:VEVENT\r\nSUMMARY:9. KI Stammtisch Bonn\r\nDTSTART:20270121T163000Z\r\nDTEND:20270121T193000Z\r\n"
    "URL:https://www.meetup.com/bonner-ki-meetup/events/316350115/\r\nLOCATION:Bonn\r\n"
    "DESCRIPTION:Offen für Teilnehmer\\*innen aller Unternehmen und Privatleute\\, die sich zu KI austauschen.\r\n"
    "END:VEVENT\r\n"
    "BEGIN:VEVENT\r\nSUMMARY:Green Bonn Hackathon 2026\r\nDTSTART;VALUE=DATE:20261116\r\nDTEND;VALUE=DATE:20261123\r\n"
    "URL:https://example.org/hackathon\r\nEND:VEVENT\r\n"
    "END:VCALENDAR\r\n")

ENACOM_PAGE = """
<div class="content-item"> <div class="item-title"> <span>Event format</span> </div>
 <div class="item-value"> <span>Workshop</span> </div> </div>
<div class="content-item"> <div class="item-title"> <span>Target groups</span> </div>
 <div class="item-value"> <p>Researchers</p> </div> </div>
<div class="content-item"> <div class="item-title"> <span>Languages</span> </div>
 <div class="item-value"> <span>Englisch</span> </div> </div>
<div class="content-item"> <div class="item-title"> <span>Location</span> </div>
 <div class="item-value"> <span>Transfer Center enaCom, NEW ADDRESS: Am Propsthof 49, 53121 Bonn</span> </div> </div>
<div class="content-item"> <div class="item-title"> <span>Registration/Ticket</span> </div>
 <div class="item-value"> <a href="https://www.uni-bonn.de/register?aff=x">https://www.uni-bonn.de/register</a> </div> </div>
"""

HBRS_PAGE = """
<h1 class="page-title">Founders Talk: Gründung als Karriereweg</h1>
<div class="infobox-event"><p class="infobox-item__title"> <i class="icon-hbrs icon-hbrs-calendar"></i> Datum </p>
 <p class="h3"> Mittwoch, 04. November 2026 </p>
 <p class="infobox-item__title"> <i class="icon-hbrs icon-hbrs-clock"></i> Zeit </p> <p class="h3"> 11:00 - 12:00 </p>
 <p class="infobox-item__title"> <i class="icon-hbrs icon-hbrs-place"></i> Standort </p>
 <p class="h4"> Flex Raum, Bibliothek Campus Sankt Augustin </p></div>
<p>Du willst deinen eigenen Weg gehen statt dich ins klassische Angestelltenverhältnis einzuordnen? Beim Founder
 Talk erfährst du aus erster Hand, wie das aussehen kann. Der Eintritt ist frei.</p>
<h2>Kontakt</h2><p>Someone, someone@h-brs.de</p>
"""

DIGITALHUB_PAGE = """
<div class="div-block-448 klein60"><div class="textblock bold">KI Meetup</div>
<div class="textblock">Taucht mit uns ein in die Welt der Künstlichen Intelligenz!</div></div>
<div class="div-block-464"><div class="event-intern-date"><div class="textblock center bold">18.11.2026 17:00</div></div>
<div class="event-intern-date"><div class="textblock center bold">18.11.2026 19:00</div></div>
<div class="event-intern-date"><div class="textblock center bold">CITYHUB</div></div></div>
<div class="div-block-449"><a href="/en/eventkalender-intern/ki-meetup-3">WATCH EVENT</a></div>
"""


def found(title, day, **kw):
    return fe.Found(title=title, url=kw.pop("url", "https://example.org/" + fe.ev.slug(title)), start=day, **kw)


class Reading(unittest.TestCase):
    def test_ics_times_folds_escapes_and_all_day_ends(self):
        items = fe.parse_ics(ICS, "Org", "Src")
        self.assertEqual(len(items), 3)
        ai, stammtisch, hackathon = items
        self.assertEqual(ai.start.strftime("%Y-%m-%d %H:%M"), "2027-02-18 10:00")
        self.assertIn("state a clear problem, and a hypothesis.", ai.description)
        self.assertNotIn("Reminder", ai.description)                 # the alarm is not the event
        self.assertEqual(stammtisch.start.strftime("%H:%M"), "17:30")  # 16:30 UTC is 17:30 in Bonn in winter
        self.assertIn("Teilnehmer*innen", stammtisch.description)
        self.assertEqual((hackathon.day, hackathon.last_day), (D(2026, 11, 16), D(2026, 11, 22)))

    def test_enacom_fields(self):
        fields = fe.read_enacom(ENACOM_PAGE)
        self.assertEqual(fields["Target groups"], "Researchers")
        self.assertEqual(fields["Languages"], "Englisch")
        self.assertTrue(fields["Registration/Ticket"].startswith("https://www.uni-bonn.de/register"))

    def test_hbrs_event_page(self):
        item = fe.read_hbrs_event(HBRS_PAGE, "https://www.h-brs.de/de/gruenden/termin/founders-talk", "H-BRS", "H-BRS")
        self.assertEqual(item.title, "Founders Talk: Gründung als Karriereweg")
        self.assertEqual(item.start.strftime("%Y-%m-%d %H:%M"), "2026-11-04 11:00")
        self.assertEqual(item.end.strftime("%H:%M"), "12:00")
        self.assertIn("Sankt Augustin", item.location)
        self.assertEqual(item.details["cost"], "Free")
        self.assertNotIn("someone@", item.description)                # the contact block is not read

    def test_digitalhub_cards(self):
        items = fe.read_digitalhub(DIGITALHUB_PAGE, "https://www.digitalhub.de/en/events/eventkalender-intern", "DH", "DH")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].url, "https://www.digitalhub.de/en/eventkalender-intern/ki-meetup-3")
        self.assertEqual(items[0].start.strftime("%Y-%m-%d %H:%M"), "2026-11-18 17:00")
        self.assertIn("CITYHUB", items[0].location)

    def test_shouting_titles_are_tidied(self):
        self.assertEqual(fe.tidy("FEMALE FOUNDERS VENTURE SUMMIT 2027"), "Female Founders Venture Summit 2027")
        self.assertEqual(fe.tidy("KI Meetup"), "KI Meetup")


class Deciding(unittest.TestCase):
    entries = [
        {"title": "Start-up Career Forum 2026", "date": D(2026, 10, 27), "source": "https://www.uni-bonn.de/a/"},
        {"title": "Ideas Competition 2026", "date": D(2026, 12, 1), "deadline": D(2026, 11, 8),
         "source": "https://www.uni-bonn.de/b"},
        {"title": "Gründungsstammtisch (founders' meetup)", "recurring": "monthly",
         "next": [D(2026, 12, 9)], "source": "https://www.h-brs.de/s"},
    ]
    urls = {fe.clean_url(e["source"]) for e in entries}

    def test_already_listed_by_address_title_deadline_or_announced_date(self):
        self.assertTrue(fe.listed(found("x", D(2026, 1, 1), url="https://www.uni-bonn.de/a?utm_source=y"),
                                  self.entries, self.urls))
        self.assertTrue(fe.listed(found("Start-up Karriere Forum", D(2026, 10, 27)), self.entries, self.urls))
        self.assertTrue(fe.listed(found("Call for ideas: Ideas Competition 2026", D(2026, 11, 8)), self.entries, self.urls))
        self.assertTrue(fe.listed(found("Gründungsstammtisch", D(2026, 12, 9)), self.entries, self.urls))
        self.assertFalse(fe.listed(found("Gründer Grusel: Fuckups mit Gänsehautfaktor", D(2026, 10, 27)),
                                   self.entries, self.urls))

    def decide(self, items, seen=(), skip=()):
        return fe.decide(items, self.entries, list(seen), list(skip), DAY, lambda item: None)

    def test_reasons(self):
        items = [
            found("Machine learning meetup", D(2026, 9, 1)),                             # over
            found("Game Design Studio Session", D(2026, 11, 1), description="A start-up idea."),
            found("Company visit", D(2026, 11, 2)),                                       # no topic
            found("AI pitch night", D(2026, 11, 3), location="Hörsaal, Dortmund"),       # outside Bonn
            found("Robotics hackathon", D(2026, 11, 4), url="https://seen.example/1"),   # proposed before
        ]
        proposals, reasons = self.decide(items, seen=[{"url": "https://seen.example/1", "date": "2026-11-04"}],
                                         skip=["game design"])
        self.assertEqual(proposals, [])
        self.assertEqual(set(reasons), {"over", "matched a skip word", "off-topic", "outside Bonn", "proposed before"})

    def test_an_event_closed_to_students_stays_out_in_every_copy(self):
        enacom = found("Own Your Code: IP strategies", D(2026, 11, 3), details={"reader": "enacom",
                                                                                 "Target groups": "Researchers"})
        lamarr = found("Seminar | Own Your Code – IP strategies", D(2026, 11, 3), location="Bonn")
        proposals, reasons = self.decide([lamarr, enacom])
        self.assertEqual(proposals, [])
        self.assertEqual(len(reasons["not open to students"]), 2)

    def test_a_proposal_is_a_valid_entry_without_addresses(self):
        item = found("From an AI Idea to the First Prototype", D(2027, 2, 18),
                     description="You have an idea. In this workshop you will learn to test it properly.",
                     details={"reader": "enacom", **fe.read_enacom(ENACOM_PAGE.replace("Researchers", "Students"))})
        item.start = dt.datetime(2027, 2, 18, 10, 0, tzinfo=fe.BERLIN)
        item.end = dt.datetime(2027, 2, 18, 14, 0, tzinfo=fe.BERLIN)
        proposals, _ = self.decide([item])
        data = proposals[0][1]
        self.assertEqual(ev.check(data, DAY), [])
        self.assertEqual(data["place"], "Transfer Center enaCom, Bonn")
        self.assertEqual((data["time"], data["language"], data["cost"]), ("10:00–14:00", "English", "not stated"))
        self.assertEqual(data["topics"], ["ai", "design"])
        self.assertEqual(data["register"], "https://www.uni-bonn.de/register")


class Writing(unittest.TestCase):
    def test_places_never_include_a_street(self):
        self.assertEqual(fe.place("Am Hauptbahnhof 6, 53111 Bonn"), "DIGITALHUB.DE CITYHUB, Bonn (at the main station)")
        self.assertEqual(fe.place("Hybrid: Online and at b-it, Friedrich-Hirzebruch-Allee 6"),
                         "b-it building, Poppelsdorf campus, Bonn, and online")
        self.assertEqual(fe.place("Zoom"), "Online")
        self.assertEqual(fe.place("Brotfabrik, Kreuzstraße 16, 53225 Bonn"), "Brotfabrik, Bonn")

    def test_summaries_are_one_plain_sentence(self):
        self.assertEqual(fe.summary(found("t", DAY, description="Am 4. März 2027 dreht sich alles um Gründerinnen!")),
                         "Am 4. März 2027 dreht sich alles um Gründerinnen.")
        self.assertEqual(fe.summary(found("KI Meetup", DAY, organiser="KI Meetup",
                                          description="KI Meetup Wir treffen uns, um über neue Modelle zu sprechen.")),
                         "Wir treffen uns, um über neue Modelle zu sprechen.")
        self.assertEqual(fe.summary(found("t", DAY, description="Wer? Wo?")), "See the organiser's page for the details.")

    def test_proposals_go_before_the_sources_and_load_cleanly(self):
        text = (ROOT / "guide" / "events.yml").read_text(encoding="utf-8")
        data = {"title": "A test", "organiser": "Org", "topics": ["ai"], "format": "meetup", "region": "bonn",
                "date": D(2026, 12, 1), "time": None, "place": "Bonn", "cost": None, "language": None,
                "source": "https://example.org/x", "checked": DAY, "summary": "A short sentence."}
        out = fe.insert(text, fe.as_yaml(data))
        self.assertLess(out.index('title: "A test"'), out.index("\nsources:"))
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.yml"
            path.write_text(out, encoding="utf-8")
            listings, _, problems = ev.load(path, DAY)
        self.assertEqual(problems, [])
        self.assertIn("A test", [e["title"] for e in listings])


if __name__ == "__main__":
    unittest.main()

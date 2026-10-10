# Contributing

The site has two layers, and `build.py` parses both:

- **the directory** (`docs/`): every resource as one line in a strict shape;
- **the guide** (`guide/`): the steps, the tracks, the Bonn page and the front page's quick
  answers, which cite directory entries by name, and the workshops and events in
  `guide/events.yml` (see [Adding an event](#adding-an-event)).

The build is strict on purpose. A malformed guide page, a citation to an entry that does not exist,
a broken link or a broken anchor all fail it, so mistakes surface in the pull request rather than
on the site.

---

## Adding to the directory

An entry that does not match the format is not rejected loudly: it silently disappears from the
site while still looking correct on GitHub. The rules below exist mainly to prevent that.

### The entry format

```markdown
- **[Name](https://example.org/)** — One sentence on why it matters. — `tag`
```

Three parts, in order: a bold link, a single sentence, and zero or more tags.

**The em dash `—` is structural.** It separates the link from the sentence, and the sentence from
the tags. A hyphen `-` or an en dash `–` in either position breaks parsing. This is the most common
mistake; copy the line above rather than retyping it.

Multiple tags are separated by a middle dot:

```markdown
- **[Name](https://example.org/)** — One sentence. — `free` · `bonn`
```

### The tag vocabulary

Tags are a controlled vocabulary, not free text. `build.py` sorts them into the site's filters:

| Facet | Tags |
|---|---|
| **Cost** | `free`, `free tier`, `under €250`, `€250–1,000`, `€1,000–5,000`, `over €5,000`, `€`, `€€`, `€€€` |
| **Where** | `bonn`, `köln`, `düsseldorf`, `aachen`, `dortmund`, `münster`, `siegen`, `nrw`, `berlin`, `hamburg`, `münchen`, `bayern`, `niedersachsen`, `germany`, `eu`, `china`, `universities` |
| **Licence** | `MIT`, `Apache-2.0`, `AGPL-3.0`, `proprietary`, `CC BY-SA 4.0`, `CC BY-NC-SA 3.0`, `CC BY-NC-SA 4.0`, `mixed licences` |
| **Access** | `membership`, `library card`, `open access`, `open evenings`, `free advice` |

A tag outside these lists still renders, but it will not become a filter. Extending the vocabulary
means editing the `COST`, `PLACE`, `LICENCE` and `ACCESS` lists in `build.py` in the same pull
request.

### The editorial rules

These are what keep the collection trustworthy as it grows.

**Verify the link.** It must return HTTP 200 before submission. A resource that cannot be verified
does not go in, however well known it is. Several otherwise obvious entries have been left out on
this rule alone.

**One sentence, and make it specific.** State why the resource matters or what it gives, not what
category it belongs to. "The navigation stack, removing the need to implement path planning from
scratch" earns its line; "a navigation framework" does not.

**Formal register.** Third person, no direct address, no colloquialisms or superlatives.

**Tag a licence only when the licence is clearly stated.** No tag is better than a guess. An absent
licence tag means the terms must be checked directly — it does not mean the resource is
unrestricted.

**Costs are ranges, never single figures.** A range is self-evidently an estimate; `€7,000+` implies
a precision nobody has. Order-of-magnitude only.

**Organisations, not people.** No individual names, email addresses, telephone numbers or street
addresses anywhere in this repository. Link the organisation's official page and stop. City names
are fine; postal addresses are not.

**Mark what is stale.** If a repository is archived or a programme has ended, say so in the
sentence. A dead project that looks alive costs a reader more than an omission does.

**Renaming an entry is a change to the guide too.** The guide cites entries by name, so a rename
fails the build until every `[[Old name]]` citation is updated. That is the point.

---

## Editing the guide

The guide answers one question for a student in Bonn: *what is my next step?* Every page is judged
by whether it answers that faster.

### Voice

The directory is formal; the guide talks to the reader. Second person, plain words, short
sentences. Each numbered action opens with a bold imperative ("**Order long-lead parts now.**")
and then says why in a sentence or two. No superlatives, no filler, no marketing.

### Citing the directory

Name tools, places and organisations by citing their directory entry, never by pasting a URL:

```markdown
Map the room with [[slam_toolbox]], then send [[Nav2]] the goals.
The [[ULB Bonn group rooms|university library]] has free rooms.     ← different link text
Bonn's hub, [[DIGITALHUB.DE#funding]], runs accelerators.           ← one file's entry, when a name appears in several
- [[MakerSpace Bonn e.V.]]                                          ← a list item that is only a citation becomes a full row
- [[TurtleBot]] — The platform most tutorials assume.               ← a row with your own sentence
```

If the thing you want to mention is not in the directory, add it there first, under the directory
rules above.

### Facts that change

Dates, fees, opening arrangements and rules go stale. State the month they were checked ("Dates
checked 2026-09") and cite the official source. Do not claim that something does not exist in Bonn
unless you have checked; "no venue rents out space to test robots" is a claim the guide makes only
because it was checked.

### The shape of the files

- **Steps** (`guide/steps/*.md`): front matter `name`, `situation` (where the reader is when this
  step applies), `hook`, `goal`, `time`, `cost` and `done` (the finish line). Each step except
  *after* must contain `{{ tracks }}`, where the build places each track's version of the step.
  The step order lives in `STEPS` in `build.py`.
- **Tracks** (`guide/tracks/*.md`): front matter `name`, `does`, `lede`, `first` (the credible first
  build), `examples`, `budget`, `time` and `hardest`, plus an optional `notice`. The body has
  exactly six sections, `## Plan` to `## Show`, in step order. Each opens with a one-sentence
  summary, which also appears in the table on that step's page. Further sections may follow the
  six, like the drone track's rules. The track order lives in `TRACKS` in `build.py`.
- **Links between files** use their paths in the repository (`../../docs/datasets.md#slam-and-odometry`,
  `show.md#pick-a-date`), so they work on GitHub too; the build re-points them for the site.

---

## Adding an event

Workshops, meetups, hackathons, courses and regular meetings live in
[`guide/events.yml`](guide/events.yml). The build turns them into the
[events page](https://robonn-club.github.io/prototype-space/events/), the "what's on" lists on the
front page, the steps and the Bonn page, step 6's dates, and a calendar file.

Each card on the events page is kept short: the date, the format and organiser, the title and
summary, when, where, the cost if the organiser states one, the language, and one *Page* button to
the `source`. Everything else stays on the organiser's page.

### What belongs here

Something in or around Bonn, or online from an organiser in the region, that helps a student build a
prototype: AI, robotics, making, software and data, design thinking, founding, patents and IP, or a
place to show a build. Students must be able to take part; leave out events only for researchers,
companies or children, and say so in the pull request.

### The rules

**Copy from the organiser's own page, and link it as `source`.** Not a newsletter, aggregator,
search result or social post: twice while this list was first researched, search summaries gave a
wrong date.

**Set `checked` to the day you looked.** The weekly review uses it to decide what to recheck.

**Write what the page says.** `cost: not stated` when you checked and the page says nothing, and
`cost: ~` when you have not checked; either way the card leaves the cost out, and the weekly review
lists every `~` to fill in. `language` works the same, but the card shows "Not stated" or "Not
checked yet". Never guess.

**Venue and city, no addresses or people.** `place: DIGITALHUB.DE CITYHUB, Bonn (at the main
station)`, not a street. No names, email addresses or phone numbers; if registration is by email,
write `register: By email, as described on the organiser's page`. The build rejects anything that
looks like a postal address or contact details.

### The fields

| Field | What to write |
|---|---|
| `title`, `organiser` | As the organiser names them. |
| `topics` | One or more of `ai`, `robotics`, `making`, `software`, `design`, `founding`, `ip`, `showcase`. |
| `format` | One of `workshop`, `talk`, `meetup`, `hackathon`, `competition`, `consultation`, `course`, `open house`, `fair`, `pitch night`, `webinar`, `team`. |
| `region` | `bonn` (Bonn and the Rhein-Sieg district), `online`, or `further` (worth a train ride). |
| `date`, `end` | A single event: `date: 2026-11-18`, and `end` if it runs several days. |
| `deadline` | Optional: the last day to apply. The site shows "Apply by", then "Applications closed". |
| `time` | A single event's time, as `"17:00–19:00"` where possible, so calendar files get it right. |
| `recurring` | A programme instead of a date: `recurring: Every Tuesday from 18:00`. |
| `next` | Optional, with `recurring`: the dates the organiser has announced, `[2026-12-09, 2027-01-13]`. |
| `weekday` | Optional, with `recurring`, only for strictly weekly programmes: `weekday: tuesday`. |
| `place`, `cost`, `language` | As above. |
| `source` | The organiser's page for this event; the card's *Page* button opens it. |
| `summary` | One sentence on what a student gets from it, ending with a full stop. |
| `who`, `register`, `note`, `more` | Optional, and not shown on the card: who may take part, the registration link, one thing to know, a second organiser page. Worth recording for maintainers; `register` also goes into the calendar file. |

### Keeping it current

Three things run on their own:

- **Every night** the site rebuilds, and every build compares the dates with today in Bonn, so
  past events disappear by themselves. You never need to delete an event on the day it ends.
- **Every Sunday at 06:00 UTC** the **Find events** workflow runs `find_events.py`. It reads the
  organisers' own calendars and event pages (each source under `sources:` with a `calendar` or a
  `reader`), leaves out what is already listed, already proposed, over, off-topic, outside Bonn or
  not open to students, and opens or updates one pull request, *New events to review*, that adds
  the rest to the end of the events list.
- **An hour later** the **Events review** workflow runs `python3 build.py --events` and opens or
  updates an issue listing what has ended (delete it), what starts within two weeks and was last
  checked more than a week ago (recheck it), regular meetings not checked for three months,
  announced dates that have all passed, and fields still marked `~`.

**Reviewing the Sunday pull request** takes a few minutes. Open each proposed event's page, then
in `guide/events.yml`:

- rewrite the `summary` as one plain English sentence (the finder copies the first usable sentence
  from the organiser, often in German);
- check `place`, `cost` and `language`, filling in any `~` you can;
- delete any proposal that does not suit students building a prototype. It will not be proposed
  again: everything the finder proposes is remembered in `guide/events-seen.yml`, which the
  finder keeps itself;
- merge. The site updates with the next build.

If the same kind of unsuitable event keeps coming back, add a word from its title to
`finder_skip:` at the end of `guide/events.yml`. To follow a new organiser, add it under
`sources:`: with `calendar:` if it publishes an iCal address (any calendar works), or ask for a
page reader in `find_events.py` if it only has a web page. The pull request's *Sources read*
section says when a source could not be read or suddenly lists nothing, which usually means its
page changed.

The finder reads only what organisers publish themselves. DPMA, IHK, VHS and Datenburg have no
calendar to read; the weekly review's source list is the reminder to look at them by hand.

Suggestions from students arrive as issues through the *Suggest an event* form. Check them against
the organiser's page like any other entry.

The Sunday pull request needs one setting, once: *Settings → Actions → General → Workflow
permissions → Allow GitHub Actions to create and approve pull requests*. GitHub also pauses
scheduled workflows in a repository with no activity for 60 days; if the nightly rebuild or a
Sunday workflow stops, re-enable it under *Actions*.

### Before opening a pull request for an event

- [ ] Copied from the organiser's own page, linked as `source`, with `checked` set to today.
- [ ] `python3 -m unittest discover tests` and `python3 build.py` pass.

---

## Before opening a pull request

- [ ] Every new link returns 200.
- [ ] Directory entries match the entry format, em dashes included, with tags from the vocabulary.
- [ ] Directory sentences: one sentence, formal register, no second person.
- [ ] Guide text: things are cited with `[[Name]]`, and facts that change carry a checked date.
- [ ] No personal data of any kind.
- [ ] `python3 build.py && mkdocs build --strict && python3 build.py --check` passes.
- [ ] For a change to the steps, tracks or front page: `tests/journeys.py` passes (see README).

## Licensing of contributions

Contributions are published under CC BY 4.0; see [LICENSE](LICENSE).

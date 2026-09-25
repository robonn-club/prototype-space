# Contributing

The site has two layers, and `build.py` parses both:

- **the directory** (`docs/`): every resource as one line in a strict shape;
- **the guide** (`guide/`): the steps, the tracks, the Bonn page and the front page's quick
  answers, which cite directory entries by name.

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

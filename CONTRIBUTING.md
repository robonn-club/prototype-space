# Contributing

Every entry in this repository follows one shape, and `build.py` parses that shape to generate the
browsable site. An entry that does not match is not rejected loudly — it silently disappears from
the site while still looking correct on GitHub. The rules below exist mainly to prevent that.

## The entry format

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

## The tag vocabulary

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

## The editorial rules

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

## Before opening a pull request

- [ ] The link returns 200.
- [ ] The line matches the entry format, em dashes included.
- [ ] Tags come from the vocabulary above, or `build.py` is updated in the same change.
- [ ] One sentence, formal register, no second person.
- [ ] A licence tag only if the licence is stated at the source.
- [ ] No personal data of any kind.
- [ ] `python3 build.py` runs and the entry appears in the browse view.

## Licensing of contributions

Contributions are published under CC BY 4.0; see [LICENSE](LICENSE).

# prototype-space

A step-by-step guide for students in Bonn, from a robot idea to a credible first build: what to do
next, when each step is done, and where in Bonn to do it. It stands on a directory of checked
resources, each with one sentence on why it matters.

**→ [robonn-club.github.io/prototype-space](https://robonn-club.github.io/prototype-space/)**

## What is in it

**The guide** (`guide/`) is organised around one question: where are you now?

- **[Six steps](guide/steps/)**: Plan, Simulate, Parts, Build, Test, Show, plus
  [what comes after](guide/steps/after.md). Each has a finish line you can check ("Done when"),
  concrete actions, what it takes, and what it costs.
- **[Seven tracks](guide/tracks/)**, one per kind of machine: mobile robot, robot arm, field robot,
  drone, legged robot, sensor rig and software prototype. Each walks the six steps with the kits,
  software and places for that machine.
- **[Building in Bonn](guide/bonn.md)**: where to make, work, test and buy, who to ask, and where
  money comes from, including what the city does not have.
- **[Quick answers](guide/answers.md)**: the questions everyone asks first, shown on the front page.

**The directory** (`docs/`) holds every resource the guide cites, and more:

- **[prototyping_resources.md](docs/prototyping_resources.md)**: tools to build with, organised by the type of system.
- **[generative_ai_agents.md](docs/generative_ai_agents.md)**: AI tools that shorten the path to a working prototype.
- **[datasets.md](docs/datasets.md)**: data to train on and benchmark against.
- **[nrw_hardware_contacts.md](docs/nrw_hardware_contacts.md)**: where to access machines and buy parts, starting in Bonn.
- **[bonn_physical_spaces.md](docs/bonn_physical_spaces.md)**: where in Bonn to meet, build and test.
- **[work_exhibit.md](docs/work_exhibit.md)**: competitions, publishing and events, where the finished thing goes.
- **[nrw_investor_contacts.md](docs/nrw_investor_contacts.md)**: funding contacts, should the project become a startup.
- **[certification_resources.md](docs/certification_resources.md)**: what the rules require, if it becomes a product.
- **[builder_helpers.md](docs/builder_helpers.md)**: the city playbook, covering costs, arrival, research and industry.

The guide cites directory entries by name (`[[ROS 2]]`), and the build resolves every citation. If
an entry is renamed or removed, the build fails instead of leaving a dead reference.

## Building the site

```bash
pip install -r requirements.txt
python3 build.py --serve                # stage guide + directory, then start a live preview
```

For a full check, as the deploy workflow runs it:

```bash
python3 build.py && mkdocs build --strict && python3 build.py --check
```

`build.py` stages both layers into `_build/docs`, generates the front page, the overviews and the
search view, and fails on a broken citation, a malformed guide file or a page missing from the nav.
`mkdocs build --strict` fails on a broken link or anchor in the markdown. `build.py --check` then
crawls the built site and fails on any internal link or anchor that does not resolve.

To check that visitors can still find their next step, run the journey tests against a local copy
(needs `pip install playwright && playwright install chromium`):

```bash
python3 -m http.server 8000 --directory _build/site &
python3 tests/journeys.py http://localhost:8000/
```

## Contributing

Entries and guide pages follow formats that the build parses. See [CONTRIBUTING.md](CONTRIBUTING.md)
before opening a pull request.

## Licence

This repository is licensed under [CC BY 4.0](LICENSE).

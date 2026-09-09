# Certification and compliance

The rules that apply to a finished product, and how to certify that a project is genuinely open.

Almost none of this applies during prototyping. These obligations attach when a product is
**placed on the market** — sold, or made available to others — not when a robot is demonstrated at
a hackathon. Rules and dates change; official pages should be consulted before relying on anything
here.

---

## The umbrella

- **[CE marking](https://single-market-economy.ec.europa.eu/single-market/ce-marking_en)** — The Commission's explanation of what CE marking means and which products require it. — `start here` · `eu`

---

## Rules for the machine

- **[Machinery Regulation (EU) 2023/1230](https://osha.europa.eu/en/legislation/directive/regulation-20231230eu-machinery)** — Replaces the Machinery Directive from 20 January 2027 and is the first to cover autonomous mobile machinery, software integrity and updates. — `required` · `from 2027`
- **[General Product Safety Regulation](https://commission.europa.eu/business-economy-euro/product-safety-and-requirements/product-safety_en)** — The baseline duty that any consumer product be safe, in force since December 2024, layered on top of CE rules rather than replacing them. — `required` · `in force`
- **[Radio Equipment Directive](https://single-market-economy.ec.europa.eu/sectors/electrical-and-electronic-engineering-industries-eei/radio-equipment-directive-red_en)** — Applies to any device containing Wi-Fi, Bluetooth or another radio. — `required` · `eu`
- **[RoHS Directive](https://environment.ec.europa.eu/topics/waste-and-recycling/rohs-directive_en)** — Restricts hazardous substances in electronics, which constrains the components permissible in a saleable board. — `required` · `eu`

---

## Rules for the intelligence

- **[EU regulatory framework for AI](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)** — The Commission's official page on the AI Act, including which risk tier a system falls into. — `required` · `phased`
- **[AI Act Explorer](https://artificialintelligenceact.eu/)** — A readable, searchable version of the Act's text, easier to navigate than the regulation itself. — `reference` · `eu`

---

## Standards to design against

*Conformity with a harmonised standard is how compliance with the law is demonstrated.*

- **[Harmonised standards](https://single-market-economy.ec.europa.eu/single-market/european-standards/harmonised-standards_en)** — The official lists of standards that give presumption of conformity with each piece of EU legislation. — `reference` · `eu`
- **[CEN-CENELEC](https://www.cencenelec.eu/)** — The European standards bodies, where machinery and robot safety standards are developed and published. — `reference` · `eu`

---

## Licences

*Without a licence no one may legally reuse the work, and the licence on any code built upon
constrains what may be done with the result.*

Permissive licences (MIT, Apache-2.0, BSD) permit sale of the resulting work. Strong copyleft
(GPL, and AGPL in particular) requires modifications to be released under the same terms — which is
why the `AGPL-3.0` tag on Ultralytics YOLO in
[generative_ai_agents.md](generative_ai_agents.md) warrants attention before it is built into a product.

- **[choosealicense.com](https://choosealicense.com/)** — Selects a licence in about a minute, with the consequences of each set out plainly. — `start here` · `free`
- **[SPDX licence list](https://spdx.org/licenses/)** — The standard identifiers such as `MIT`, `Apache-2.0` and `AGPL-3.0`, which are the tags used across this repo. — `reference` · `free`
- **[OSI approved licences](https://opensource.org/licenses)** — The formal definition of open source and the list of licences that actually meet it. — `reference` · `free`
- **[GNU licence list](https://www.gnu.org/licenses/licenses.html)** — Explains copyleft and how the GPL family, AGPL included, propagates to derivative work. — `reference` · `free`
- **[Creative Commons](https://creativecommons.org/share-your-work/)** — For documentation, drawings and CAD, where software licences are a poor fit. — `reference` · `free`

---

## Certifying the project as open

- **[OSHWA certification](https://certification.oshwa.org/)** — Certifies that a hardware project meets the community definition of open source, and gives it a unique ID. — `free` · `voluntary`
- **[Open Source Hardware Definition](https://www.oshwa.org/definition/)** — The definition that certification tests against, and the standard around which documentation should be designed. — `reference` · `free`
- **[CERN Open Hardware Licence v2](https://ohwr.org/licences/)** — The only OSI-approved licence written specifically for hardware, available in permissive, weakly reciprocal and strongly reciprocal variants. — `licence` · `free`
- **[CERN-OHL-S on OSI](https://opensource.org/license/cern-ohl-s-2-0)** — The strongly reciprocal variant, for when derivatives must stay open too. — `licence` · `free`
- **[Open Know-How](https://github.com/iop-alliance/OpenKnowHow)** — A machine-readable manifest describing how a design is made, allowing it to be indexed and found. — `standard` · `free`

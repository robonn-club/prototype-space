---
name: Software prototype
does: Something on a screen
lede: >-
  A dashboard, a planner or a model that other people can use counts as a prototype, and it costs
  nothing but time.
first: A web demo that runs one robot task on real or recorded data, and that a stranger can use without your help.
examples:
  - A fleet dashboard for a simulated warehouse (logistics)
  - A weed-spotting demo on real field images (agriculture)
  - A route planner for a drone inspecting a solar park (energy)
budget: €0
time: 1–4 weeks
hardest: Making it usable by someone else. A demo only its author can run convinces nobody.
---

## Plan

One task and one user: who opens the demo, and what do they get from it within a minute?

- Write down the one thing the user should see or decide, and cut every screen that does not
  serve it.

## Simulate

Build against recorded or public data first: [[PhenoBench]] for crops, [[KITTI]] for driving,
[[LeRobot datasets]] for manipulation.

- Check the dataset's licence before building on it. [[KITTI]], for one, is non-commercial.
- For a planner, a simple simulator such as [[pyrobosim]] is enough to show behaviour.

## Parts

No parts, only tools: [[Streamlit]] or [[Gradio]] for the interface, [[Rerun]] or [[Foxglove]]
for robot data.

- [[v0]] or [[bolt.new]] when a clickable front end is needed quickly.

## Build

Make it run from one command, then put it online.

- AI coding tools shorten this step considerably: [[Claude Code]], [[Cline]] or [[Aider]].
- Freeze the environment with [[Docker]], so the demo still runs next month.

## Test

Hand it to three people who have never seen it, and watch without helping.

- Every question they ask is something to fix.

## Show

Publish the link and the repository, with a one-minute screen recording for anyone who will not
click.

- Put the recording at the top of the README, above the installation steps.

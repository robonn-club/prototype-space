---
name: Legged robot
does: Something that walks
lede: >-
  The hardest track for a first build. Start from a kit that already walks, and make the first
  build one new behaviour rather than a whole new robot.
first: A kit quadruped that walks a marked two-metre course on a new surface with a gait you tuned or trained, five times in a row.
examples:
  - Crossing a strip of mock rough terrain (agriculture)
  - Stepping up and over a single kerb (logistics)
  - Turning on the spot to face a marker, then walking to it
budget: €250–5,000
time: 8–16 weeks
hardest: Balance. Small errors in timing or calibration end in a fall.
---

## Plan

One new behaviour on a walking kit, not a robot designed from scratch.

- A new gait, a new surface, or a new trigger. Pick one.
- If the claim works on wheels, switch to the [mobile track](mobile.md). Legs earn their place on
  steps, rubble and grass.

## Simulate

Tune or train the gait in [[MuJoCo]] or [[Isaac Lab]] before it touches the floor.

- Check whether your kit publishes a simulation model, and start from theirs.
- The gap between simulation and reality is the whole problem on this track: vary friction, mass
  and motor strength in simulation so the gait survives the difference.

## Parts

A quadruped that already walks: [[OpenCat]] or [[Mini Pupper]] as kits, [[Stanford Pupper]] to
build yourself, or [[Open Duck Mini]] for a small biped.

- [[Mini Pupper]] — ROS-capable, and designed to be taken apart and repaired.
- [[OpenCat]] — Aimed at makers and educators rather than research labs.
- [[Stanford Pupper]] — Built by a student club, fully documented.
- [[Berkeley Humanoid Lite]] and the [[Open Dynamic Robot Initiative]] are research-grade: a
  second build, not a first.

## Build

Hang the robot up before the first power-on. Legs thrash when a calibration is wrong.

- Suspend it so the feet clear the floor, and test each joint's direction and limits one at a
  time.
- Record joint commands and positions from the start; falls are only explainable from the log.

## Test

Test on the real surface with a spotter's hand ready, and count completed courses rather than
steps.

- Start each run from the same pose and battery level, or runs cannot be compared.

## Show

Film the course uncut from the side, with the simulated run beside it.

- Bonn's own humanoid team, [[NimbRo]], shows where this track leads.

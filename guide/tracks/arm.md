---
name: Robot arm
does: Something that picks things up
lede: >-
  The cheapest way into physical AI. A printable arm costs under €250, and open software trains
  it from a few dozen demonstrations.
first: An arm that picks one kind of object from a marked area and places it in a box, five times in a row.
examples:
  - Sorting parcels into two bins by label (logistics)
  - Picking ripe from unripe fruit, or convincing fakes (agriculture)
  - Plugging a charging cable into a socket (energy)
budget: €100–1,000
time: 4–8 weeks
hardest: Grasping reliably. Objects slip, rotate and hide from the camera.
---

## Plan

One object, one start area, one target: the demo is pick, move, place.

- Choose rigid objects that are easy to grasp. Soft, shiny or tangled ones are version two.
- Decide between teaching by demonstration with [[LeRobot]] and planning with [[MoveIt 2]]. On a
  cheap printed arm, demonstration is usually the faster route to a first result.

## Simulate

Try the task in [[MuJoCo]] or [[robosuite]], but order the arm first. On this track, real
demonstrations often teach more than a simulator.

- The arm kits are cheap and delivery is the slow part, so order at the start of this step.
- Browse [[LeRobot datasets]] for recorded demonstrations of similar tasks.

## Parts

A printed arm that [[LeRobot]] supports: the [[SO-ARM100]] or the [[Koch v1.1]], built as a pair
so one arm leads and the other follows.

- [[SO-ARM100]] — Under €250 per arm, and the most widely built.
- [[Koch v1.1]] — The alternative, designed for teleoperation from the start.
- [[BCN3D Moveo]] — When the task needs more reach than a desktop arm.
- One or two USB cameras. Steady lighting matters more than resolution.

## Build

Assemble, calibrate, and teleoperate before training anything.

- Calibrate every joint's zero and range first. A miscalibrated arm teaches a policy that fails.
- Record a few dozen demonstrations with the leader arm, then train a first policy with
  [[LeRobot]].

## Test

Test with the table, lighting and objects of the demo, and move the object a little on every run.

- First policies fail most often on positions they never saw. Vary the positions while recording
  demonstrations, not only while testing.
- Keep a count: successes out of ten, then five in a row.

## Show

Publish the dataset and the trained policy along with the video, so others can replay the
result.

- Upload both to the Hugging Face hub in LeRobot format, alongside the other
  [[LeRobot datasets]].
- For the next version, compare against open foundation policies: [[OpenVLA]] and [[openpi]].

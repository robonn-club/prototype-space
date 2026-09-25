---
name: Field robot
does: Something that works among crops
lede: >-
  Robonn's home ground, and Bonn's research strength. The data is local and excellent; the hard
  part is getting to real crop rows.
first: A robot that follows a row of potted plants and photographs each one, five times in a row.
examples:
  - Following a crop row and counting the plants (agriculture)
  - Spotting weeds between crop plants in images (agriculture)
  - A garden bed that waters each plant on its own schedule (agriculture)
budget: €100–5,000
time: 8–16 weeks
hardest: The outdoors. Light, mud and uneven ground break what worked indoors.
---

## Plan

Bring the field indoors for the first build: a corridor of potted plants stands in for a crop
row.

- Pick one job along the row: count, photograph, or find weeds. Not all three.
- Decide whether the first build drives the row, or is a perception system that runs on recorded
  field data. The second is cheaper, and still credible.

## Simulate

Develop the perception on Bonn's own field data before building anything that drives.

- Train a crop and weed detector on [[PhenoBench]] or [[Sugar Beets 2016]], both published by
  Uni Bonn.
- Drive a simulated rover along rows in [[Gazebo]]; the navigation software is the same as on
  the [mobile track](mobile.md).

## Parts

A small rover base with a camera, as on the [mobile track](mobile.md#parts), or a [[FarmBot]]
for a garden bed.

- [[FarmBot]] — The reference for complete open-hardware documentation, at €1,000–5,000.
- [[AgOpenGPS]] — When the idea is steering real farm machinery rather than a small robot.
- Keep the first build indoors, and leave waterproofing for version two.

## Build

Build as for a mobile robot, then fix the camera at one height and angle. A detector only works
from the viewpoint it was trained on.

- Mount the camera rigidly and measure its pose. A camera that shifts invalidates the detector.
- Log images together with position, so every detection can be traced to a plant.

## Test

Test in the potted-plant corridor first; move to real rows through the people who work with them.

- [[Campus Klein-Altendorf]] is where PhenoRob runs its field experiments, and it is reached
  through the groups that work there.
- Record every run with [[rosbag2]] and note the time of day. Outdoor light changes by the
  minute.

## Show

Aim for the [[Field Robot Event]], the student contest built for exactly this.

- Share it with the [[ROS Agriculture]] community, and publish any images you labelled.
- For more open agricultural technology to build on, see [[awesome-agriculture]].

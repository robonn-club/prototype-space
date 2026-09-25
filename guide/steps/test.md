---
name: Test
situation: It runs on the bench
hook: Make it work where it's meant to
goal: Run the whole demo where the robot is meant to work, until it works every time.
time: Two to six weeks
cost: Little money; the cost is in the runs
done: >-
  The full demo works five times in a row in its real setting, with nobody touching the robot
  between runs. Sensor rigs and software demos have their own version of this bar, set in their
  track.
---

A robot that works on the bench has not yet met the floor, the light, the Wi-Fi or a half-empty
battery. Testing is a loop: run, record, find the most common failure, fix it, run again.

## Do this

1. **Find a space that matches the demo.** See *Where to test in Bonn* below, and book it for a
   series of sessions rather than one.
2. **Run the whole demo, never pieces.** Full runs find the failures that live between
   subsystems.
3. **Record every run.** Video plus logs, named by date and run number. [[Rerun]] and
   [[Foxglove]] make a run replayable.
4. **Keep a failure list.** One line per failed run: what happened, and the suspected cause.
   Fix the most frequent failure first.
5. **Change one thing between runs.** Otherwise you will not know what fixed it, or what broke
   it.
6. **Count.** Five full runs in a row, untouched, is the bar; your track may set its own
   equivalent. Until then it is a demo on a good day.

## Where to test in Bonn

No venue in Bonn rents out space for driving or flying robots, so testing is improvised:

- **A seminar room** booked through the [[AStA — student groups|AStA]], which registered student
  groups can do, with floor enough for a mobile base.
- **The [[MakerSpace Bonn e.V.|MakerSpace]] floor**, where running machines is expected.
- **Campus corridors and courtyards** outside teaching hours. Ask the building's caretaker
  first.
- **Real crop rows** at [[Campus Klein-Altendorf]], the university's outdoor laboratory,
  reached through the research groups that work there.
- **Anything that flies**: indoors first, and outdoors only once
  [the drone rules](../tracks/drone.md#before-you-fly) are met.

## For your track

{{ tracks }}

## Traps

- **Testing only where it already works.** The same corner, a full battery, good light. The demo
  will happen somewhere else.
- **Fixing without recording.** A fix you cannot explain comes back.
- **Moving the goalposts.** If the demo keeps failing, shrink the claim. Do not redefine success
  after the run.

## Go deeper

- [Spaces in Bonn, and the testing gap](../../docs/bonn_physical_spaces.md#somewhere-to-test-a-robot)
- [Tools for replaying runs](../../docs/prototyping_resources.md#dashboard-software-prototype)
- [Datasets to benchmark against](../../docs/datasets.md)

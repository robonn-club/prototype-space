---
name: Drone
does: Something that flies
lede: >-
  Spectacular, and the least forgiving: every crash costs parts, and flying outdoors in Bonn comes
  with rules. Start small, and start indoors.
first: A palm-sized drone that takes off, flies a fixed square indoors and lands on its pad, five times in a row.
examples:
  - Flying a fixed inspection path along a mock row of solar panels (energy)
  - Counting plants from above on a printed field map (agriculture)
  - Carrying a small marker between two landing pads (logistics)
budget: €250–1,000
time: 6–12 weeks
hardest: Crashes. Every failed test can end the session, so simulate everything first.
notice: >-
  **Before any outdoor flight:** liability insurance is compulsory, and above 249 g or with a
  camera you must also register with the LBA. [Read the rules](#before-you-fly).
---

## Plan

Plan the first build small and indoors: a drone under 250 grams, in a closed room.

- Below 250 grams and without a camera, no operator registration is needed, and a crash costs
  little. Read [the rules](#before-you-fly) before planning anything outdoors.
- Define the mission as waypoints (take off, fly a square, land) so it can be flown in
  simulation first.

## Simulate

Fly the whole mission in simulation: [[PX4]] runs in the loop with [[Gazebo]], and
[[QGroundControl]] plans the mission.

- [[ArduPilot]] is the alternative flight stack, with its own software-in-the-loop simulator.
- Do not move to hardware until the simulated mission ends on the pad every time.

## Parts

A [[Crazyflie]] for indoor autonomy; a frame running [[PX4]] only when the plan truly needs to
fly outdoors.

- [[Crazyflie]] — Palm-sized, open, and safe enough to fly indoors while learning.
- [[Betaflight]] is for manually flown FPV craft rather than autonomy; skip it for this track.
- LiPo batteries need care: see the battery note in [step 4](../steps/build.md).

## Build

Bench-test with the propellers off. Always.

- Every firmware and motor test happens without propellers; they go on only in the flying space.
- Keep the flight log of every flight, and read it after every crash.

## Test

Fly indoors first, in a closed room over a soft floor, with nobody inside the flight area.

- Outdoors only once the [rules below](#before-you-fly) are met, and only after checking the
  [[dipul map tool]] before every flight.
- Count completed missions that land on the pad, not take-offs.

## Show

Film the uncut mission, and publish the flight log beside the video. The log is the proof of
autonomy.

- Put the mission, the parameters and the logs in the repository, so the flight can be
  reproduced.

## Before you fly {#before-you-fly}

Rules checked 2026-09 on [[dipul]], the federal drone portal. They apply to flying outdoors in
Germany; read the official pages before the first flight.

- **Registration.** Operators must register with the Federal Aviation Office (LBA) if the drone
  weighs more than 249 g or carries a camera or other sensor that can record personal data. It
  costs €20 and gives an e-ID that goes on every drone you fly.
- **Insurance.** Liability insurance is compulsory for drone operators in Germany. Check whether
  an existing personal liability policy covers it before buying one.
- **Competence.** Above 249 g, the pilot needs the EU certificate of competency A1/A3: an online
  course and test at the LBA, for €25.
- **Where.** Bonn is full of geographical zones: federal agencies, the UN campus, the Rhine as a
  federal waterway, hospitals and nature reserves among them. Check the [[dipul map tool]]
  before every flight.

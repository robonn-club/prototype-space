---
name: Show
situation: It works in its real setting
hook: Make it credible
goal: Make it credible to someone who wasn't there, with proof, a repository and a public date.
time: One to two weeks, then the event
cost: Nothing, apart from travel to an event
done: >-
  The build meets all five points of the bar below, and someone outside the team has seen it
  run.
bar:
  - title: It does one job, end to end
    text: The one-sentence claim from step 1. The whole task, not one subsystem.
  - title: It works every time, not once
    text: >-
      Five full runs in a row where it was built to work, untouched between runs. A sensor rig:
      a week of data without a gap. A software demo: three people use it without help.
  - title: There is proof
    text: An uncut video of a full run, and the logs that go with it.
  - title: Someone else could rebuild it
    text: Code, bill of materials with prices, CAD and wiring, in a public repository with a licence.
  - title: You can say where it fails
    text: The known limits, and what version two would change.
---

A first build is credible when someone who wasn't in the room believes it works, and could
check. That takes three things: proof, a repository, and an audience.

## The bar

{{ bar }}

## Do this

1. **Film the uncut run.** One take, start to finish, with whatever proves success in the frame.
   A cut hides exactly what a viewer wants to know: did it work in one go?
2. **Finish the repository.** A README with the claim, the video, how to run it, the bill of
   materials, the wiring diagram and the CAD. Choose a licence with [[choosealicense.com]]; for
   hardware, the [[CERN Open Hardware Licence v2]]. [[OSHWA certification#tools]] lists what complete
   documentation includes.
3. **Archive a release.** [[Zenodo]] gives it a DOI, so it stays findable and citable.
4. **Write it up where builders read.** A project page on [[Hackaday.io]], a note to
   [[Weekly Robotics]], and ROS work on [[Open Robotics Discourse]].
5. **Show it in person.** A live audience finds failures that testing does not. Pick a date
   below.
6. **Ask someone who knows for critique.** A research group, a competition team, or the
   [[Robonn]] Discord. Ask what would break the claim.

## For your track

{{ tracks }}

## Pick a date

Fairs and competitions to build towards. Each links to its listing among the
[workshops and events](../events/index.md), which says when the date was checked; confirm on the
organiser's site before planning around it.

{{ dates }}

## In Bonn

- **The local audience.** The [[Nacht der Technik Bonn/Rhein-Sieg]] happens every two years; the
  next is on 1 October 2027.
- **Competition-grade builds next door.** [[NimbRo]] at Uni Bonn and [[b-it-bots]] at H-BRS show
  what a RoboCup entry looks like, and b-it-bots is open to students at any level of study.
- **The club.** Post the video in the [[Robonn]] Discord before any event, and ask what breaks
  the claim.

## Traps

- **Editing the video.** After one cut, a viewer can no longer tell whether it worked in one go.
- **A repository only you can run.** Ask someone to follow the README on a fresh machine, and
  fix whatever they trip over.
- **Waiting until it is perfect.** The bar is five runs and a README, not a product.

## Go deeper

- [Competitions, publishing and events](../../docs/work_exhibit.md)
- [Making it reproducible](../../docs/prototyping_resources.md#making-it-reproducible)
- [Certifying the project as open](../../docs/certification_resources.md#certifying-the-project-as-open)

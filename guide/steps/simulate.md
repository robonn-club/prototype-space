---
name: Simulate
situation: I know what the first build should do
hook: Make it work on screen, for free
goal: Make the demo work in software, for free, before buying anything.
time: One to three weeks
cost: Nothing
done: >-
  The whole demo runs in simulation, or on recorded data, from one command, on a laptop that
  is not yours.
---

Simulation is where mistakes are cheap: a planner that drives into a wall costs nothing on
screen. It also answers the questions the parts list depends on (which sensors, which motors,
how much computing) before any money is spent.

## Do this

1. **Order long-lead parts now.** If your track starts from a kit (see the table below), order
   it at the start of this step and simulate while it ships. Everything else waits until the
   simulation says what you need.
2. **Set up your track's software in a container.** Put it in [[Docker]] from the first day, so
   the setup that works today still works on a teammate's laptop, and later on the robot. Most
   tracks build on [[ROS 2]].
3. **Model the robot roughly.** A box with wheels, or an arm made of cylinders, is enough.
   Describe it so the simulator can load it: [[URDF tutorials]].
4. **Run the demo end to end, badly.** Get the whole sequence from step 1 working in its
   crudest form first, then improve the weakest part. A perfect component inside a demo that
   does not run is worth nothing yet.
5. **Keep it in git from the first commit.** A public repository with a README that says how
   to run it. Large CAD and mesh files go in [[Git LFS]].
6. **Write down what the simulation taught you.** Speed, payload, sensor range, battery life,
   computing needs. That list is the specification for the parts in step 3.

## For your track

{{ tracks }}

## In Bonn

- **Somewhere to work.** Group rooms at the [[ULB Bonn group rooms|university library]], the
  [[H-BRS library group rooms|H-BRS library]] and the city's [[Stadtbibliothek Bonn]] are free.
- **Help with the software.** [[Datenburg e.V.|Datenburg]], Bonn's hackspace, holds an open
  evening for guests every Tuesday; or ask in the [[Robonn]] Discord.
- **Data from Bonn itself.** For field and plant work, start with the university's own
  datasets: the [[IPB dataset index]] and [[PhenoBench]].

## Traps

- **Perfecting the simulation.** It only has to be good enough to choose the parts and prove
  the logic. The real robot will behave differently anyway.
- **Never trying a second machine.** "It works on my laptop" is the most common reason a
  project stalls on the day a teammate joins.
- **Choosing the simulator for its looks.** Use the one your track's software supports out of
  the box.

## Go deeper

- [Every simulator, compared](../../docs/prototyping_resources.md#simulation-only)
- [AI that writes the code](../../docs/generative_ai_agents.md#ai-that-assists-development)
- [Datasets to test against](../../docs/datasets.md)

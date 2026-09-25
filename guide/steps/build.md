---
name: Build
situation: The parts are here
hook: Bring it up on the bench
goal: Assemble it, and make every part work on the bench, one at a time.
time: Two to six weeks
cost: Mostly time, plus a few replacement parts
done: >-
  Every subsystem works on the bench (power, computer, sensors, motors), and the software from
  step 2 drives the real hardware.
---

Bring-up is where most first builds stall: everything is wired, nothing works, and nothing says
why. The cure is order. Connect one subsystem at a time, and test each before adding the next.

## Do this

1. **Power first.** Measure every voltage with a multimeter before anything that computes is
   connected. Put a fuse and an off switch you can reach between the battery and everything
   else.
2. **Then one subsystem at a time.** The computer boots; one sensor reads; one motor turns;
   then the next. Test each with the smallest possible script before connecting another.
3. **Record from the first power-on.** [[rosbag2]] on ROS tracks, a plain CSV file otherwise,
   viewed in [[PlotJuggler]] or [[Foxglove]]. When something fails you want the recording, not
   a memory.
4. **Swap the simulator for the real drivers.** The code from step 2 should drive the hardware
   with as few changes as possible; on ROS tracks, that is what [[ros2_control]] is for.
5. **Document while you build.** A photo of every wiring stage, a wiring diagram, the CAD in the
   repository. It takes minutes now and saves days later.
6. **Treat lithium batteries with respect.** Charge LiPo packs in a fire-safe bag on a surface
   that cannot burn, never unattended, and retire any pack that swells.

## For your track

{{ tracks }}

## In Bonn

- **A bench, tools, and people who have seen it before.** [[MakerSpace Bonn e.V.|MakerSpace Bonn]]
  has soldering, 3D printers and a metal shop under one roof, so a broken part can be remade on
  the spot.
- **Electronics and software questions.** Bring the board to [[Datenburg e.V.|Datenburg]]'s open
  evening on a Tuesday, or post the plot in the [[Robonn]] Discord.

## Traps

- **Wiring everything, then switching on.** When it fails, nothing tells you which of twenty
  connections is at fault.
- **Debugging without data.** "It jerks sometimes" becomes solvable the moment there is a plot.
- **Loose connectors.** Most intermittent faults on a moving robot are mechanical. Crimp
  properly, relieve the strain, and label every cable.

## Go deeper

- [Tools for seeing what a robot is doing](../../docs/prototyping_resources.md#dashboard-software-prototype)
- [Boards, sensors and debugging tools](../../docs/prototyping_resources.md#sensor-rig-data-collection)
- [Open workshops across NRW](../../docs/nrw_hardware_contacts.md#open-workshops)

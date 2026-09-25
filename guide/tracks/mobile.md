---
name: Mobile robot
does: Something that drives
lede: >-
  The most forgiving track, and the best supported. The software for driving around a room is
  mature, and bases that already drive are affordable.
first: A robot that drives itself between two marked stations in a room and back, five times in a row.
examples:
  - A parcel shuttle between two desks (logistics)
  - A robot that maps a room and returns to its start
  - A row follower along potted plants in a corridor (agriculture)
budget: €100–1,000
time: 6–12 weeks
hardest: Knowing where it is. Localisation drifts, and everything downstream inherits the error.
---

## Plan

A route the robot drives on its own: from one station to another and back, in one room.

- Mark both stations on the floor. The demo is the robot leaving one and stopping within a hand's
  width of the other.
- Indoors, on a flat floor, at walking pace. Outdoors is version two.

## Simulate

Drive the route in [[Gazebo]] with [[Nav2]] before buying a wheel.

- Build the room as a Gazebo world, map it with [[slam_toolbox]], and send Nav2 the two stations
  as goals.
- If you plan to buy a [[TurtleBot]], simulate that exact robot; its simulation packages match the
  real one.

## Parts

Start from a base that already drives: a [[TurtleBot]] if the budget allows, a self-built
[[Linorobot2]], or a [[Donkey Car]] for camera-only driving.

- [[TurtleBot]] — The platform most ROS 2 tutorials assume, so every problem has been met before.
- [[Linorobot2]] — Cheaper, and yours: several drivetrains, documented part by part.
- [[Donkey Car]] — Under €250, driving from a camera alone rather than mapping.
- A 2D lidar makes mapping far easier than a camera. With only a depth camera, use [[RTAB-Map]].

## Build

Bring the base up with [[ros2_control]], then add the lidar, then navigation.

- Check odometry before anything else: command one metre, measure with a tape. If odometry is
  wrong, nothing after it will work.
- Once the basics run, fuse wheel odometry with an IMU using [[robot_localization]].

## Test

Test on the real floor, among the furniture of the real room, and count arrivals within a hand's
width of the station.

- Test at the battery level the demo will have. Motors behave differently on a half-empty
  battery.
- A seminar room booked through the AStA is the usual space; corridors outside teaching hours
  give longer runs.

## Show

Film one uncut round trip, with the map and the planned path shown beside it.

- Record the navigation view in [[Foxglove]] and place it next to the video; it makes the run
  legible to anyone.
- For fast driving, [[RoboRacer]] is the competition route; for driving outdoors, the
  [[Field Robot Event]].

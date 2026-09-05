# Prototyping resources

Organised by **what you're making**. Every entry is one sentence on why it matters, plus
what it costs to start.

`cost` is what you spend before it's useful · `needs` is what you must already have.

---

## Start here — anything you build

*Three things make the difference between a prototype and a prototype someone else can run.*

- **[ROS 2](https://docs.ros.org/)** — The common language of robot software, so your parts talk to everyone else's. — `free` · `linux`
- **[Docker](https://docs.docker.com/)** — Freezes your environment so it still runs on someone else's machine. — `free` · `laptop`
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** — Turns a folder of markdown into a documentation site in an afternoon. — `free` · `python`

---

## Simulation only

*The zero-budget path — a laptop is the whole lab. Start here even if you plan to build hardware.*

- **[Gazebo](https://gazebosim.org/)** — The default ROS-native simulator, best when you need a whole world rather than one contact. — `free` · `linux`
- **[MuJoCo](https://github.com/google-deepmind/mujoco)** — Fast contact-rich physics, the one to reach for when grasping or legged contact is the hard part. — `free` · `python`
- **[Webots](https://github.com/cyberbotics/webots)** — Batteries-included simulator with dozens of robot models ready to drive. — `free` · `laptop`
- **[pyrobosim](https://github.com/sea-bass/pyrobosim)** — A deliberately simple 2D simulator for testing robot *behaviour* before physics matters. — `free` · `python`
- **[Isaac Lab](https://github.com/isaac-sim/IsaacLab)** — GPU-accelerated simulation for training policies at scale. — `free` · `nvidia gpu`
- **[Genesis](https://github.com/Genesis-Embodied-AI/Genesis)** — A fast general-purpose physics engine aimed at embodied AI work. — `free` · `python`
- **[best-of-robot-simulators](https://github.com/knmcguire/best-of-robot-simulators)** — An index of simulators regenerated weekly, so you can compare before committing. — `free` · `nothing`

---

## Mobile robot

*Something that drives. Get it navigating in Gazebo first, then swap the sim for wheels.*

- **[TurtleBot](https://www.turtlebot.com/)** — The reference ROS 2 mobile platform almost every tutorial assumes. — `€300+` · `ros 2`
- **[Nav2](https://github.com/ros-navigation/navigation2)** — The navigation stack, so you don't write path planning from scratch. — `free` · `ros 2`
- **[slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)** — Builds a map while driving, the standard answer for 2D SLAM. — `free` · `ros 2 + lidar`
- **[Duckietown](https://duckietown.com/)** — A cheap autonomy platform with a full curriculum, designed for exactly our situation. — `€150+` · `raspberry pi`
- **[F1TENTH](https://f1tenth.org/)** — Autonomous racing at 1/10 scale, with teaching modules and real competitions. — `€800+` · `ros 2`
- **[JetBot](https://github.com/NVIDIA-AI-IOT/jetbot)** — A small Jetson-powered robot for learning vision-driven driving. — `€250+` · `jetson`

---

## Robot arm

*Something that picks things up. The cheapest honest entry point into physical intelligence.*

- **[LeRobot](https://github.com/huggingface/lerobot)** — The most complete open robot-learning stack, spanning cheap arms to humanoids with one interface. — `free` · `python`
- **[SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)** — A 3D-printable robot arm cheap enough for a student to own outright. — `€120+` · `3d printer`
- **[MoveIt 2](https://moveit.ai/)** — Motion planning and collision checking, the standard arm brain in ROS 2. — `free` · `ros 2`
- **[robosuite](https://github.com/ARISE-Initiative/robosuite)** — Simulated manipulation tasks with benchmarks, so results are comparable. — `free` · `mujoco`
- **[OpenVLA](https://github.com/openvla/openvla)** — An open vision-language-action model you can fine-tune on your own demonstrations. — `free` · `gpu`

---

## Drone / UAV

*Something that flies. Simulate it fully before anything leaves the ground.*

- **[PX4](https://github.com/PX4/PX4-Autopilot)** — A modern open flight stack with strong simulation support built in. — `free` · `linux`
- **[ArduPilot](https://github.com/ArduPilot/ardupilot)** — The mature, deeply battle-tested autopilot across planes, copters and rovers. — `free` · `linux`
- **[Betaflight](https://github.com/betaflight/betaflight)** — Firmware for small fast FPV craft, the hobbyist end of the field. — `free` · `flight controller`
- **[Crazyflie](https://github.com/bitcraze/crazyflie-firmware)** — A palm-sized open drone safe enough to fly indoors while you learn. — `€250+` · `python`

---

## Sensor rig / data collection

*Something that measures. Often the fastest route to a result worth showing.*

- **[Arduino](https://www.arduino.cc/)** — The shortest path from a sensor to a number on your screen. — `€25+` · `nothing`
- **[PlatformIO](https://platformio.org/)** — Real development tooling for microcontrollers, once the Arduino IDE starts hurting. — `free` · `vs code`
- **[Raspberry Pi](https://github.com/raspberrypi/documentation)** — A full Linux computer small enough to bolt onto the thing you built. — `€60+` · `nothing`
- **[NVIDIA Jetson](https://developer.nvidia.com/embedded-computing)** — Onboard GPU compute for when perception has to run on the robot itself. — `€250+` · `linux`
- **[rosbag2](https://github.com/ros2/rosbag2)** — Records every message so you can debug a run you can't repeat. — `free` · `ros 2`
- **[OpenCV](https://github.com/opencv/opencv)** — The default toolbox for getting something useful out of a camera. — `free` · `python`

---

## Dashboard / software prototype

*Something you can show on a screen. This counts as a prototype.*

- **[Streamlit](https://github.com/streamlit/streamlit)** — Turns a Python script into a shareable web app without touching frontend code. — `free` · `python`
- **[Gradio](https://github.com/gradio-app/gradio)** — Wraps a model in a usable interface in about ten lines. — `free` · `python`
- **[Rerun](https://github.com/rerun-io/rerun)** — Logs and replays multimodal robot data visually, enormously faster than print statements. — `free` · `python`
- **[Foxglove](https://foxglove.dev/)** — A purpose-built viewer for robotics data and recordings. — `free tier` · `ros 2`
- **[Grafana](https://github.com/grafana/grafana)** — Live dashboards for anything you're logging over time. — `free` · `a data source`

---

## Designing and making the parts

*Where a CAD file becomes a thing on the table.*

- **[FreeCAD](https://www.freecad.org/)** — Fully open parametric CAD, no licence to expire mid-project. — `free` · `patience`
- **[Onshape](https://www.onshape.com/)** — Browser CAD, free as long as your projects are public — which ours are. — `free` · `browser`
- **[KiCad](https://www.kicad.org/)** — Open PCB design that professionals actually ship with. — `free` · `laptop`
- **[PrusaSlicer](https://github.com/prusa3d/PrusaSlicer)** — Turns your model into printable instructions, with sane defaults. — `free` · `3d printer`

---

## Making it reproducible

*The bar for "someone else can run it." Most projects skip this and quietly die.*

- **[OSHWA certification](https://certification.oshwa.org/basics.html)** — A checklist of what must be public before hardware counts as open. — `free` · `nothing`
- **[Open Know-How](https://github.com/iop-alliance/OpenKnowHow)** — A machine-readable manifest describing how to make your thing. — `free` · `nothing`
- **[Open hardware documentation guide](https://opensource.com/article/20/10/open-hardware-documentation)** — Three concrete fixes for documentation nobody can follow. — `free` · `nothing`

---

## Where to look when this list runs out

- **[awesome-ros2](https://github.com/fkromer/awesome-ros2)** — Curated ROS 2 libraries and tools.
- **[awesome-robotics-projects](https://github.com/mjyc/awesome-robotics-projects)** — Affordable and lesser-known robotics projects.
- **[awesome-open-hardware](https://github.com/delftopenhardware/awesome-open-hardware)** — Open hardware projects, tools and communities.
- **[awesome-weekly-robotics](https://github.com/msadowski/awesome-weekly-robotics)** — Projects from the Weekly Robotics newsletter.
- **[build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)** — Rebuild real systems from scratch, for when you want to understand rather than use.

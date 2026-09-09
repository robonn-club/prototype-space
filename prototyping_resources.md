# Prototyping resources

Organised by **what you're making**. Every entry is one sentence on why it matters, plus
what it costs to start.

`cost` is what you spend before it's useful.

Costs are order-of-magnitude estimates. Check the project's own bill of materials
before budgeting.

---

## Start here — anything you build

*Three things make the difference between a prototype and a prototype someone else can run.*

- **[ROS 2](https://docs.ros.org/)** — The common language of robot software, so your parts talk to everyone else's. — `free`
- **[Docker](https://docs.docker.com/)** — Freezes your environment so it still runs on someone else's machine. — `free`
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** — Turns a folder of markdown into a documentation site in an afternoon. — `free`
- **[Git LFS](https://git-lfs.com/)** — Keeps CAD files and STLs from bloating a repo everyone has to clone. — `free`

---

## Simulation only

*The zero-budget path — a laptop is the whole lab. Start here even if you plan to build hardware.*

- **[Gazebo](https://gazebosim.org/)** — The default ROS-native simulator, best when you need a whole world rather than one contact. — `free`
- **[MuJoCo](https://github.com/google-deepmind/mujoco)** — Fast contact-rich physics, the one to reach for when grasping or legged contact is the hard part. — `free`
- **[Webots](https://github.com/cyberbotics/webots)** — Batteries-included simulator with dozens of robot models ready to drive. — `free`
- **[pyrobosim](https://github.com/sea-bass/pyrobosim)** — A deliberately simple 2D simulator for testing robot *behaviour* before physics matters. — `free`
- **[Isaac Lab](https://github.com/isaac-sim/IsaacLab)** — GPU-accelerated simulation for training policies at scale. — `free`
- **[Genesis](https://github.com/Genesis-Embodied-AI/Genesis)** — A fast general-purpose physics engine aimed at embodied AI work. — `free`
- **[PyBullet](https://github.com/bulletphysics/bullet3)** — A long-established physics engine with a gentle Python API, still the quickest way to get a robot falling over on screen. — `free`
- **[CoppeliaSim](https://www.coppeliarobotics.com/)** — A mature simulator with a visual scene editor, easier than Gazebo if you think in pictures. — `free`
- **[Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub)** — Connects ROS to Unity, for when the demo has to look convincing to non-engineers. — `free`
- **[ManiSkill](https://github.com/haosulab/ManiSkill)** — GPU-parallel manipulation tasks with benchmarks, for training grasping policies at speed. — `free`
- **[URDF tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html)** — How to describe your own robot so a simulator can load it, which is the first wall after installing ROS 2. — `free`
- **[best-of-robot-simulators](https://github.com/knmcguire/best-of-robot-simulators)** — An index of simulators regenerated weekly, so you can compare before committing. — `free`

---

## Mobile robot

*Something that drives. Get it navigating in Gazebo first, then swap the sim for wheels.*

- **[Nav2](https://github.com/ros-navigation/navigation2)** — The navigation stack, so you don't write path planning from scratch. — `free`
- **[slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)** — Builds a map while driving, the standard answer for 2D SLAM. — `free`
- **[ros2_control](https://github.com/ros-controls/ros2_control)** — The standard way to talk to motors, so swapping hardware doesn't mean rewriting your control code. — `free`
- **[robot_localization](https://github.com/cra-ros-pkg/robot_localization)** — Fuses wheel odometry, IMU and GPS into one position estimate you can trust. — `free`
- **[RTAB-Map](https://github.com/introlab/rtabmap_ros)** — Visual SLAM from a depth camera, when you have no lidar to spare. — `free`
- **[Cartographer](https://github.com/ros2/cartographer_ros)** — Google's SLAM system, the alternative to try when slam_toolbox drifts. — `free`

**Or start from a finished build**

- **[TurtleBot](https://www.turtlebot.com/)** — The reference ROS 2 mobile platform almost every tutorial assumes. — `€250–1,000`
- **[Duckietown](https://duckietown.com/)** — A low-cost autonomy platform with a full curriculum, designed for exactly this kind of club. — `under €250`
- **[JetBot](https://github.com/NVIDIA-AI-IOT/jetbot)** — A small Jetson-powered robot for learning vision-driven driving. — `€250–1,000`
- **[Donkey Car](https://github.com/autorope/donkeycar)** — A self-driving RC car with a large community, the gentlest way into autonomous driving. — `under €250`
- **[ExoMy](https://github.com/esa-prl/ExoMy)** — ESA's six-wheeled Mars rover, printable at home with a full assembly guide, though the repo has been archived since 2021. — `€250–1,000`
- **[JPL Open Source Rover](https://github.com/nasa-jpl/open-source-rover)** — NASA JPL's scaled-down six-wheel rover, built entirely from off-the-shelf parts. — `€1,000–5,000`
- **[F1TENTH](https://f1tenth.org/)** — Autonomous racing at 1/10 scale, with teaching modules and real competitions. — `€250–1,000`
- **[Linorobot2](https://github.com/linorobot/linorobot2)** — A DIY ROS 2 robot base you assemble yourself, with several drivetrains supported out of the box. — `€250–1,000`

---

## Robot arm

*Something that picks things up. The cheapest honest entry point into physical intelligence.*

- **[LeRobot](https://github.com/huggingface/lerobot)** — The most complete open robot-learning stack, spanning cheap arms to humanoids with one interface. — `free`
- **[MoveIt 2](https://moveit.ai/)** — Motion planning and collision checking, the standard arm brain in ROS 2. — `free`
- **[robosuite](https://github.com/ARISE-Initiative/robosuite)** — Simulated manipulation tasks with benchmarks, so results are comparable. — `free`
- **[OpenVLA](https://github.com/openvla/openvla)** — An open vision-language-action model you can fine-tune on your own demonstrations. — `free`
- **[openpi](https://github.com/Physical-Intelligence/openpi)** — Physical Intelligence's open robot policies, the natural thing to compare OpenVLA against. — `free`
- **[Drake](https://github.com/RobotLocomotion/drake)** — Toyota Research's toolbox for serious model-based control and optimisation. — `free`

**Or start from a finished build**

- **[SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)** — A 3D-printable robot arm cheap enough for a student to own outright. — `under €250`
- **[BCN3D Moveo](https://github.com/BCN3D/BCN3D-Moveo)** — A printed five-axis arm published with CAD, firmware, bill of materials and an assembly manual. — `€250–1,000`
- **[Koch v1.1](https://github.com/jess-moss/koch-v1-1)** — A low-cost printed arm designed for teleoperation and imitation learning, and well supported by LeRobot. — `under €250`

---

## Legged and humanoid

*Something that walks. Harder than it looks, and the best of these were built by students.*

- **[Stanford Pupper](https://github.com/stanfordroboticsclub/StanfordQuadruped)** — A Raspberry Pi quadruped from Stanford's student robotics club, fully documented and genuinely reproducible. — `€250–1,000`
- **[Stanford Doggo](https://github.com/Nate711/StanfordDoggoProject)** — An open quadruped that trots, jumps and backflips, with the full mechanical design published. — `€1,000–5,000`
- **[Mini Pupper](https://github.com/mangdangroboticsclub/QuadrupedRobot)** — A small ROS-capable robot dog designed to be taken apart and repaired repeatedly. — `€250–1,000`
- **[OpenCat](https://github.com/PetoiCamp/OpenCat-Quadruped-Robot)** — A hackable quadruped framework aimed at makers and educators rather than labs. — `€250–1,000`
- **[Berkeley Humanoid Lite](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite)** — A modular full-body humanoid built from affordable off-the-shelf parts. — `€1,000–5,000`
- **[InMoov](https://inmoov.fr/)** — The first life-size 3D-printed open humanoid, printable in pieces over months. — `€250–1,000`
- **[Poppy](https://www.poppy-project.org/en/)** — A modular printed humanoid platform built for education and experimentation. — `over €5,000`
- **[Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini)** — A small printed bipedal robot that actually walks, and one of the cheapest ways into legged control. — `€250–1,000`
- **[Reachy Mini](https://github.com/pollen-robotics/reachy_mini)** — An open-hardware desktop robot from the Reachy lineage, priced for a student rather than a lab. — `€250–1,000`
- **[Open Dynamic Robot Initiative](https://open-dynamic-robot-initiative.github.io/)** — Open torque-controlled actuators and the Solo quadruped, the research-grade end of open legged hardware. — `€1,000–5,000`

---

## Drone / UAV

*Something that flies. Simulate it fully before anything leaves the ground.*

- **[PX4](https://github.com/PX4/PX4-Autopilot)** — A modern open flight stack with strong simulation support built in. — `free`
- **[ArduPilot](https://github.com/ArduPilot/ardupilot)** — The mature, deeply battle-tested autopilot across planes, copters and rovers. — `free`
- **[Betaflight](https://github.com/betaflight/betaflight)** — Firmware for small fast FPV craft, the hobbyist end of the field. — `free`
- **[QGroundControl](https://qgroundcontrol.com/)** — The ground station for planning missions and watching telemetry while something is in the air. — `free`
- **[Aerostack2](https://github.com/aerostack2/aerostack2)** — A ROS 2 framework for multi-drone systems, when one aircraft stops being enough. — `free`

**Or start from a finished build**

- **[Crazyflie](https://github.com/bitcraze/crazyflie-firmware)** — A palm-sized open drone safe enough to fly indoors while you learn. — `€250–1,000`

---

## Agriculture and field

*Robonn's home ground, and where open-source robotics is strongest outside the lab.*

- **[FarmBot](https://farm.bot/)** — A CNC farming machine published with CAD, bill of materials and step-by-step assembly, the reference for complete open hardware documentation. — `€1,000–5,000`
- **[AgOpenGPS](https://github.com/AgOpenGPS-Official/AgOpenGPS)** — Precision mapping, guidance and section control that turns ordinary farm machinery into autosteer. — `free`
- **[ROS Agriculture](https://github.com/ros-agriculture)** — A community building ROS tools for farming, and the place to ask where the field-robotics work is happening. — `free`
- **[awesome-agriculture](https://github.com/brycejohnston/awesome-agriculture)** — An index of open-source technology for farming and growing, when this section runs out. — `free`

---

## Sensor rig / data collection

*Something that measures. Often the fastest route to a result worth showing — and a
multimeter is the first debugging tool, before any of these.*

- **[Arduino](https://www.arduino.cc/)** — The shortest path from a sensor to a number on your screen. — `under €250`
- **[PlatformIO](https://platformio.org/)** — Real development tooling for microcontrollers, once the Arduino IDE starts hurting. — `free`
- **[Raspberry Pi](https://github.com/raspberrypi/documentation)** — A full Linux computer small enough to bolt onto the thing you built. — `under €250`
- **[NVIDIA Jetson](https://developer.nvidia.com/embedded-computing)** — Onboard GPU compute for when perception has to run on the robot itself. — `€250–1,000`
- **[rosbag2](https://github.com/ros2/rosbag2)** — Records every message so you can debug a run you can't repeat. — `free`
- **[OpenCV](https://github.com/opencv/opencv)** — The default toolbox for getting something useful out of a camera. — `free`
- **[sigrok](https://sigrok.org/)** — Open-source signal analysis that drives inexpensive logic analysers, for when you need to see what a wire is actually doing. — `free`
- **[ESPHome](https://esphome.io/)** — Turns an ESP32 into a networked sensor from a short YAML file, with no firmware to write. — `free`
- **[Wokwi](https://wokwi.com/)** — Simulates Arduino and ESP32 circuits in the browser, so you can debug wiring before the parts arrive. — `free tier`
- **[librealsense](https://github.com/IntelRealSense/librealsense)** — The driver stack for RealSense depth cameras, the usual first 3D sensor on a student robot. — `free`

---

## Dashboard / software prototype

*Something you can show on a screen. This counts as a prototype.*

- **[Streamlit](https://github.com/streamlit/streamlit)** — Turns a Python script into a shareable web app without touching frontend code. — `free`
- **[Gradio](https://github.com/gradio-app/gradio)** — Wraps a model in a usable interface in about ten lines. — `free`
- **[Rerun](https://github.com/rerun-io/rerun)** — Logs and replays multimodal robot data visually, enormously faster than print statements. — `free`
- **[Foxglove](https://foxglove.dev/)** — A purpose-built viewer for robotics data and recordings. — `free tier`
- **[Grafana](https://github.com/grafana/grafana)** — Live dashboards for anything you're logging over time. — `free`
- **[PlotJuggler](https://github.com/facontidavide/PlotJuggler)** — Drags robot log files onto a timeline and plots any signal instantly, the fastest way to find out what went wrong. — `free`
- **[Node-RED](https://nodered.org/)** — Wires devices and services together by dragging boxes, useful for a working demo in an afternoon. — `free`

---

## Designing and making the parts

*Where a CAD file becomes a thing on the table.*

- **[FreeCAD](https://www.freecad.org/)** — Fully open parametric CAD, no licence to expire mid-project. — `free`
- **[Onshape](https://www.onshape.com/)** — Browser CAD, free as long as your projects are public — which ours are. — `free`
- **[KiCad](https://www.kicad.org/)** — Open PCB design that professionals actually ship with. — `free`
- **[PrusaSlicer](https://github.com/prusa3d/PrusaSlicer)** — Turns your model into printable instructions, with sane defaults. — `free`
- **[OpenSCAD](https://openscad.org/)** — Describes solid models as code, so parts are versioned and diffed like any other source file. — `free`
- **[build123d](https://github.com/gumyr/build123d)** — Code-CAD in Python, often faster than a GUI if you already think in scripts. — `free`
- **[Blender](https://www.blender.org/)** — Not CAD, but the right tool for renders, meshes and anything that has to look good in a presentation. — `free`

---

## Making it reproducible

*The bar for "someone else can run it." Most projects skip this and quietly die.*

- **[OSHWA certification](https://certification.oshwa.org/basics.html)** — A checklist of what must be public before hardware counts as open. — `free`
- **[Open Know-How](https://github.com/iop-alliance/OpenKnowHow)** — A machine-readable manifest describing how to make your thing. — `free`
- **[Open hardware documentation guide](https://opensource.com/article/20/10/open-hardware-documentation)** — Three concrete fixes for documentation nobody can follow. — `free`
- **[choosealicense.com](https://choosealicense.com/)** — Picks a licence in about a minute; without one, nobody may legally reuse your work. — `free`
- **[Zenodo](https://zenodo.org/)** — Archives a release and mints a DOI, so your project can be cited and still exists in ten years. — `free`

---

## Where to look when this list runs out

- **[awesome-ros2](https://github.com/fkromer/awesome-ros2)** — Curated ROS 2 libraries and tools. — `free`
- **[awesome-robotics-projects](https://github.com/mjyc/awesome-robotics-projects)** — Affordable and lesser-known robotics projects. — `free`
- **[awesome-open-hardware](https://github.com/delftopenhardware/awesome-open-hardware)** — Open hardware projects, tools and communities. — `free`
- **[awesome-weekly-robotics](https://github.com/msadowski/awesome-weekly-robotics)** — Projects from the Weekly Robotics newsletter. — `free`
- **[build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)** — Rebuild real systems from scratch, for when you want to understand rather than use. — `free`
- **[Hackaday.io](https://hackaday.io/)** — Thousands of documented hardware builds at exactly the scale one person finishes in a semester. — `free`
- **[ROS Discourse](https://discourse.ros.org/)** — Where the ROS community actually answers questions and announces what's changing. — `free`

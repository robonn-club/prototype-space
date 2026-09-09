# Prototyping resources

Organised by **the type of system being built**. Every entry gives one sentence on why it matters,
plus the cost of starting.

`cost` is the outlay required before a resource becomes useful.

Costs are order-of-magnitude estimates. Each project's own bill of materials should be consulted
before budgeting.

---

## Start here — applicable to any build

*Three things separate a prototype from a prototype others can reproduce.*

- **[ROS 2](https://docs.ros.org/)** — The common language of robot software, allowing components to interoperate with everyone else's. — `free`
- **[Docker](https://docs.docker.com/)** — Freezes the environment so a project still runs on another machine. — `free`
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** — Converts a folder of markdown into a documentation site within an afternoon. — `free`
- **[Git LFS](https://git-lfs.com/)** — Prevents CAD files and STLs from inflating a repository that others must clone. — `free`

---

## Simulation only

*The zero-budget path, requiring only a laptop. Worth starting here even where hardware is planned.*

- **[Gazebo](https://gazebosim.org/)** — The default ROS-native simulator, best suited to simulating a whole environment rather than a single contact. — `free`
- **[MuJoCo](https://github.com/google-deepmind/mujoco)** — Fast contact-rich physics, the appropriate choice where grasping or legged contact is the difficult element. — `free`
- **[Webots](https://github.com/cyberbotics/webots)** — A comprehensive simulator supplied with dozens of ready-to-run robot models. — `free`
- **[pyrobosim](https://github.com/sea-bass/pyrobosim)** — A deliberately simple 2D simulator for testing robot *behaviour* before physics matters. — `free`
- **[Isaac Lab](https://github.com/isaac-sim/IsaacLab)** — GPU-accelerated simulation for training policies at scale. — `free`
- **[Genesis](https://github.com/Genesis-Embodied-AI/Genesis)** — A fast general-purpose physics engine aimed at embodied AI work. — `free`
- **[PyBullet](https://github.com/bulletphysics/bullet3)** — A long-established physics engine with an approachable Python API, and still the quickest route to a robot moving on screen. — `free`
- **[CoppeliaSim](https://www.coppeliarobotics.com/)** — A mature simulator with a visual scene editor, more approachable than Gazebo for visually oriented work. — `free`
- **[Unity Robotics Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub)** — Connects ROS to Unity, for demonstrations that must be convincing to non-engineers. — `free`
- **[ManiSkill](https://github.com/haosulab/ManiSkill)** — GPU-parallel manipulation tasks with benchmarks, for rapid training of grasping policies. — `free`
- **[URDF tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/URDF/URDF-Main.html)** — How to describe a robot so a simulator can load it, and the first obstacle after installing ROS 2. — `free`
- **[best-of-robot-simulators](https://github.com/knmcguire/best-of-robot-simulators)** — An index of simulators regenerated weekly, permitting comparison before committing. — `free`

---

## Mobile robot

*Something that drives. Get it navigating in Gazebo first, then swap the sim for wheels.*

- **[Nav2](https://github.com/ros-navigation/navigation2)** — The navigation stack, removing the need to implement path planning from scratch. — `free`
- **[slam_toolbox](https://github.com/SteveMacenski/slam_toolbox)** — Builds a map while driving, the standard answer for 2D SLAM. — `free`
- **[ros2_control](https://github.com/ros-controls/ros2_control)** — The standard interface to motors, so that changing hardware does not require rewriting control code. — `free`
- **[robot_localization](https://github.com/cra-ros-pkg/robot_localization)** — Fuses wheel odometry, IMU and GPS into a single reliable position estimate. — `free`
- **[RTAB-Map](https://github.com/introlab/rtabmap_ros)** — Visual SLAM from a depth camera, for use where no lidar is available. — `free`
- **[Cartographer](https://github.com/ros2/cartographer_ros)** — Google's SLAM system, the alternative where slam_toolbox drifts. — `free`

**Or start from a finished build**

- **[TurtleBot](https://www.turtlebot.com/)** — The reference ROS 2 mobile platform almost every tutorial assumes. — `€250–1,000`
- **[Duckietown](https://duckietown.com/)** — A low-cost autonomy platform with a full curriculum, designed for precisely this kind of club. — `under €250`
- **[JetBot](https://github.com/NVIDIA-AI-IOT/jetbot)** — A small Jetson-powered robot for learning vision-driven driving. — `€250–1,000`
- **[Donkey Car](https://github.com/autorope/donkeycar)** — A self-driving RC car with a large community, and a widely used entry point to autonomous driving. — `under €250`
- **[ExoMy](https://github.com/esa-prl/ExoMy)** — ESA's six-wheeled Mars rover, printable at home with a full assembly guide, though the repo has been archived since 2021. — `€250–1,000`
- **[JPL Open Source Rover](https://github.com/nasa-jpl/open-source-rover)** — NASA JPL's scaled-down six-wheel rover, built entirely from off-the-shelf parts. — `€1,000–5,000`
- **[F1TENTH](https://f1tenth.org/)** — Autonomous racing at 1/10 scale, with teaching modules and real competitions. — `€250–1,000`
- **[Linorobot2](https://github.com/linorobot/linorobot2)** — A self-assembled ROS 2 robot base, with several drivetrains supported as standard. — `€250–1,000`

---

## Robot arm

*Something that picks things up. The lowest-cost entry point into physical intelligence.*

- **[LeRobot](https://github.com/huggingface/lerobot)** — The most complete open robot-learning stack, spanning cheap arms to humanoids with one interface. — `free`
- **[MoveIt 2](https://moveit.ai/)** — Motion planning and collision checking, the standard arm brain in ROS 2. — `free`
- **[robosuite](https://github.com/ARISE-Initiative/robosuite)** — Simulated manipulation tasks with benchmarks, so results are comparable. — `free`
- **[OpenVLA](https://github.com/openvla/openvla)** — An open vision-language-action model that can be fine-tuned on custom demonstrations. — `free`
- **[openpi](https://github.com/Physical-Intelligence/openpi)** — Physical Intelligence's open robot policies, the natural comparison against OpenVLA. — `free`
- **[Drake](https://github.com/RobotLocomotion/drake)** — Toyota Research's toolbox for serious model-based control and optimisation. — `free`

**Or start from a finished build**

- **[SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)** — A 3D-printable robot arm at a price a student can own outright. — `under €250`
- **[BCN3D Moveo](https://github.com/BCN3D/BCN3D-Moveo)** — A printed five-axis arm published with CAD, firmware, bill of materials and an assembly manual. — `€250–1,000`
- **[Koch v1.1](https://github.com/jess-moss/koch-v1-1)** — A low-cost printed arm designed for teleoperation and imitation learning, and well supported by LeRobot. — `under €250`

---

## Legged and humanoid

*Something that walks. Harder than it appears, and the strongest examples were built by students.*

- **[Stanford Pupper](https://github.com/stanfordroboticsclub/StanfordQuadruped)** — A Raspberry Pi quadruped from Stanford's student robotics club, fully documented and genuinely reproducible. — `€250–1,000`
- **[Stanford Doggo](https://github.com/Nate711/StanfordDoggoProject)** — An open quadruped that trots, jumps and backflips, with the full mechanical design published. — `€1,000–5,000`
- **[Mini Pupper](https://github.com/mangdangroboticsclub/QuadrupedRobot)** — A small ROS-capable quadruped designed for repeated disassembly and repair. — `€250–1,000`
- **[OpenCat](https://github.com/PetoiCamp/OpenCat-Quadruped-Robot)** — A modifiable quadruped framework aimed at makers and educators rather than research labs. — `€250–1,000`
- **[Berkeley Humanoid Lite](https://github.com/HybridRobotics/Berkeley-Humanoid-Lite)** — A modular full-body humanoid built from affordable off-the-shelf parts. — `€1,000–5,000`
- **[InMoov](https://inmoov.fr/)** — The first life-size 3D-printed open humanoid, printable in pieces over months. — `€250–1,000`
- **[Poppy](https://www.poppy-project.org/en/)** — A modular printed humanoid platform built for education and experimentation. — `over €5,000`
- **[Open Duck Mini](https://github.com/apirrone/Open_Duck_Mini)** — A small printed bipedal robot capable of stable walking, and one of the lowest-cost routes into legged control. — `€250–1,000`
- **[Reachy Mini](https://github.com/pollen-robotics/reachy_mini)** — An open-hardware desktop robot from the Reachy lineage, priced for a student rather than a lab. — `€250–1,000`
- **[Open Dynamic Robot Initiative](https://open-dynamic-robot-initiative.github.io/)** — Open torque-controlled actuators and the Solo quadruped, the research-grade end of open legged hardware. — `€1,000–5,000`

---

## Drone / UAV

*Something that flies. Simulate it fully before anything leaves the ground.*

- **[PX4](https://github.com/PX4/PX4-Autopilot)** — A modern open flight stack with strong simulation support built in. — `free`
- **[ArduPilot](https://github.com/ArduPilot/ardupilot)** — The mature, deeply battle-tested autopilot across planes, copters and rovers. — `free`
- **[Betaflight](https://github.com/betaflight/betaflight)** — Firmware for small fast FPV craft, the hobbyist end of the field. — `free`
- **[QGroundControl](https://qgroundcontrol.com/)** — The ground station for planning missions and monitoring telemetry during flight. — `free`
- **[Aerostack2](https://github.com/aerostack2/aerostack2)** — A ROS 2 framework for multi-drone systems, where a single aircraft is no longer sufficient. — `free`

**Or start from a finished build**

- **[Crazyflie](https://github.com/bitcraze/crazyflie-firmware)** — A palm-sized open drone safe enough for indoor flight during early learning. — `€250–1,000`

---

## Agriculture and field

*Robonn's home ground, and where open-source robotics is strongest outside the lab.*

- **[FarmBot](https://farm.bot/)** — A CNC farming machine published with CAD, bill of materials and step-by-step assembly, the reference for complete open hardware documentation. — `€1,000–5,000`
- **[AgOpenGPS](https://github.com/AgOpenGPS-Official/AgOpenGPS)** — Precision mapping, guidance and section control that turns ordinary farm machinery into autosteer. — `free`
- **[ROS Agriculture](https://github.com/ros-agriculture)** — A community building ROS tools for farming, and the place to enquire where field-robotics work is under way. — `free`
- **[awesome-agriculture](https://github.com/brycejohnston/awesome-agriculture)** — An index of open-source technology for farming and growing, for use beyond this section. — `free`

---

## Sensor rig / data collection

*Something that measures. Often the fastest route to a presentable result, and a multimeter
remains the first debugging tool, ahead of any of these.*

- **[Arduino](https://www.arduino.cc/)** — The shortest path from a sensor to a displayed reading. — `under €250`
- **[PlatformIO](https://platformio.org/)** — Full development tooling for microcontrollers, for use once the Arduino IDE becomes limiting. — `free`
- **[Raspberry Pi](https://github.com/raspberrypi/documentation)** — A complete Linux computer small enough to mount on a finished build. — `under €250`
- **[NVIDIA Jetson](https://developer.nvidia.com/embedded-computing)** — Onboard GPU compute for cases where perception must run on the robot itself. — `€250–1,000`
- **[rosbag2](https://github.com/ros2/rosbag2)** — Records every message, allowing a run that cannot be repeated to be debugged afterwards. — `free`
- **[OpenCV](https://github.com/opencv/opencv)** — The default toolbox for extracting usable information from a camera. — `free`
- **[sigrok](https://sigrok.org/)** — Open-source signal analysis that drives inexpensive logic analysers, for establishing what a signal line is doing. — `free`
- **[ESPHome](https://esphome.io/)** — Converts an ESP32 into a networked sensor from a short YAML file, with no firmware required. — `free`
- **[Wokwi](https://wokwi.com/)** — Simulates Arduino and ESP32 circuits in the browser, allowing wiring to be checked before parts arrive. — `free tier`
- **[librealsense](https://github.com/IntelRealSense/librealsense)** — The driver stack for RealSense depth cameras, the most common first 3D sensor on a student robot. — `free`

---

## Dashboard / software prototype

*Something presentable on a screen. This qualifies as a prototype.*

- **[Streamlit](https://github.com/streamlit/streamlit)** — Converts a Python script into a shareable web application without frontend code. — `free`
- **[Gradio](https://github.com/gradio-app/gradio)** — Wraps a model in a usable interface in approximately ten lines. — `free`
- **[Rerun](https://github.com/rerun-io/rerun)** — Logs and replays multimodal robot data visually, substantially faster than inspecting printed output. — `free`
- **[Foxglove](https://foxglove.dev/)** — A purpose-built viewer for robotics data and recordings. — `free tier`
- **[Grafana](https://github.com/grafana/grafana)** — Live dashboards for any quantity logged over time. — `free`
- **[PlotJuggler](https://github.com/facontidavide/PlotJuggler)** — Plots any signal from a robot log file on a timeline, and the fastest route to identifying a fault. — `free`
- **[Node-RED](https://nodered.org/)** — Connects devices and services through a visual flow editor, suited to producing a working demonstration in an afternoon. — `free`

---

## Designing and making the parts

*Where a CAD file becomes a physical part.*

- **[FreeCAD](https://www.freecad.org/)** — Fully open parametric CAD, with no licence that can expire mid-project. — `free`
- **[Onshape](https://www.onshape.com/)** — Browser-based CAD, free while projects remain public, as these are. — `free`
- **[KiCad](https://www.kicad.org/)** — Open PCB design used in professional production. — `free`
- **[PrusaSlicer](https://github.com/prusa3d/PrusaSlicer)** — Converts a model into printable instructions, with well-chosen defaults. — `free`
- **[OpenSCAD](https://openscad.org/)** — Describes solid models as code, so parts are versioned and compared like any other source file. — `free`
- **[build123d](https://github.com/gumyr/build123d)** — Code-CAD in Python, often faster than a graphical tool for those already working in scripts. — `free`
- **[Blender](https://www.blender.org/)** — Not CAD, but the appropriate tool for renders, meshes and presentation material. — `free`

---

## Making it reproducible

*The standard for reproducibility. Most projects omit this, and their work cannot be reused as a result.*

- **[OSHWA certification](https://certification.oshwa.org/basics.html)** — A checklist of what must be published before hardware qualifies as open. — `free`
- **[Open Know-How](https://github.com/iop-alliance/OpenKnowHow)** — A machine-readable manifest describing how a design is made. — `free`
- **[Open hardware documentation guide](https://opensource.com/article/20/10/open-hardware-documentation)** — Three concrete remedies for documentation that cannot be followed. — `free`
- **[choosealicense.com](https://choosealicense.com/)** — Selects a licence in about a minute; without one, no one may legally reuse the work. — `free`
- **[Zenodo](https://zenodo.org/)** — Archives a release and issues a DOI, so a project remains citable and available in ten years. — `free`

---

## Where to look when this list runs out

- **[awesome-ros2](https://github.com/fkromer/awesome-ros2)** — Curated ROS 2 libraries and tools. — `free`
- **[awesome-robotics-projects](https://github.com/mjyc/awesome-robotics-projects)** — Affordable and lesser-known robotics projects. — `free`
- **[awesome-open-hardware](https://github.com/delftopenhardware/awesome-open-hardware)** — Open hardware projects, tools and communities. — `free`
- **[awesome-weekly-robotics](https://github.com/msadowski/awesome-weekly-robotics)** — Projects from the Weekly Robotics newsletter. — `free`
- **[build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)** — Rebuilding real systems from scratch, for understanding rather than use. — `free`
- **[Hackaday.io](https://hackaday.io/)** — Thousands of documented hardware builds at the scale one person completes in a semester. — `free`
- **[ROS Discourse](https://discourse.ros.org/)** — Where the ROS community answers questions and announces changes. — `free`

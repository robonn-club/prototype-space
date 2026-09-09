# AI for fast prototyping

AI that shortens the path to a working prototype, whether by writing the code, running inside the
robot, or turning an idea into a usable interface. Not all of it is generative; all of it saves
time.

Licence tags are read from each project's repository. Where a licence is not clear, no tag is
given rather than a guess.

---

## AI that assists development

*Producing the ROS node, the URDF and the test in an afternoon rather than a week.*

- **[Claude Code](https://claude.com/claude-code)** — A terminal coding agent that reads a repository, edits files and runs commands, suited to the repetitive middle stages of a build. — `proprietary`
- **[Cline](https://github.com/cline/cline)** — An open coding agent that runs inside VS Code, with the full execution loop visible throughout. — `Apache-2.0`
- **[Aider](https://aider.chat/)** — Pair programming from the command line, with every change recorded as its own git commit. — `Apache-2.0`
- **[Cursor](https://cursor.com/)** — An editor built around AI-assisted editing, and the closest of these to a conventional IDE. — `proprietary`
- **[GitHub Copilot](https://github.com/features/copilot)** — Inline completion in most editors, free for students through GitHub Education. — `proprietary`
- **[Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python)** — A harness for building a custom agent, for cases where no existing tool fits. — `MIT`

---

## Running models locally

*A robot often has no connection, latency matters, and per-call costs accumulate during iteration.*

- **[Ollama](https://ollama.com/)** — Pulls and runs open models locally from a single command, and the simplest starting point. — `MIT`
- **[llama.cpp](https://github.com/ggml-org/llama.cpp)** — Runs models efficiently on modest hardware, including single-board computers. — `MIT`
- **[LM Studio](https://lmstudio.ai/)** — A desktop application for evaluating local models without use of a terminal. — `proprietary`
- **[vLLM](https://github.com/vllm-project/vllm)** — High-throughput serving for a single machine handling many concurrent requests. — `Apache-2.0`

---

## AI that runs in the prototype

*Models that become part of the machine rather than part of the development workflow.*

- **[Ultralytics YOLO](https://github.com/ultralytics/ultralytics)** — Fast object detection that runs on a Jetson, though the AGPL licence requires a commercial agreement before any product built on it is sold. — `AGPL-3.0`
- **[Segment Anything](https://github.com/facebookresearch/segment-anything)** — Segments any object in an image without task-specific training. — `Apache-2.0`
- **[Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2)** — Estimates depth from a single conventional camera, where a dedicated depth sensor is out of budget. — `Apache-2.0`
- **[Whisper](https://github.com/openai/whisper)** — Speech recognition that runs locally, enabling spoken rather than typed interaction with a robot. — `MIT`

For vision-language-action policies — **OpenVLA** and **openpi** — see the Robot arm section of
[prototyping_resources.md](prototyping_resources.md), where they accompany the manipulation stack.

---

## Turning an idea into a clickable thing

*A dashboard that others can interact with qualifies as a prototype.*

- **[v0](https://v0.app/)** — Generates a working web interface from a written description, allowing an idea to be shown before it is built. — `proprietary`
- **[bolt.new](https://bolt.new/)** — Builds and runs a complete small application in the browser, deployable within minutes. — `proprietary`

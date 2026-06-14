---
name: robotic-arm
description: "Control a color sorting robotic arm using computer vision and ESP32-C3 motion control."
version: 1.0.0
trigger: robot arm,robotic arm,pick cube,drop cube,move cube,sort red cubes,sort green cubes,cube sorting
risk: low
permissions: device_exec
delegate_preference: board
requires_board: true
approval_level: none
cooldown_seconds: 0
scheduler_template: none
category: Robotics
---

# AI Robotic Arm

## When to use

- User wants to inspect the current scene.
- User wants robot status.
- User wants to pick a cube.
- User wants to drop a cube.
- User wants to move a cube.
- User wants to sort red cubes.
- User wants to sort green cubes.
- User wants to return the arm home.

## Hard rule: re-check the scene first

Before any action that depends on slot or bin contents (`pick`, `move`, `sort_red`, `sort_green`, or any `drop` that assumes a specific cube is held), run:

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py scene
```

Act on the live `scene` output, not on memory of the previous command's result. If the requested action is impossible given the live scene (e.g. "drop the red cube" when no red cube is held, or "pick from A" when A is empty), say so, show the scene, and ask the user to clarify — do not guess.

## Steps

### Show Scene

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py scene
```

### Show Status

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py status
```

### Pick Cube

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py pick A
```

Replace A with A, B or C.

### Drop Cube

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py drop LEFT
```

Replace LEFT with LEFT or RIGHT.

### Move Cube

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py move A LEFT
```

Replace slot and destination as required.

### Sort Red Cubes

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py sort_red
```

### Sort Green Cubes

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py sort_green
```

### Home

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py home
```

## Prerequisites

- ESP32-C3 connected through USB serial.
- arm_api.py available at:

```text
/home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python
```

- OpenCV installed.
- Python serial package installed.
- Camera connected and operational.

## How to verify

### Scene

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py scene
```

Expected:

```text
slots
bins
```

### Status

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py status
```

Expected:

```text
holding_cube
```

### Motion Test

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py pick A
```

Robot should pick a cube.

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py drop LEFT
```

Robot should release the cube.

## Failure Recovery

If serial communication fails:

```bash
ls /dev/ttyACM*
```

Verify ESP32 connection.

If camera detection fails:

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py scene
```

Verify camera is detected and scene information is returned.
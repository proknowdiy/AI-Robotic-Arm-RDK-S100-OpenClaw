# AI Robotic Arm using RDK S100 and OpenClaw

An AI-powered robotic arm that can see, understand natural language commands, and sort colored cubes autonomously.

This project combines computer vision, OpenClaw, WhatsApp integration, and an ESP32-C3 robotic arm controller to create a practical AI robotics system.

---

## Features

### Computer Vision

* Red and green cube detection
* Slot detection (A, B, C)
* Automatic bin position detection
* Real-time scene analysis using OpenCV

### Robotic Arm Control

* Pick and place operation
* Automatic cube sorting
* Manual control commands
* Safe state management

### AI Integration

* OpenClaw custom skill
* Natural language control
* WhatsApp-based interaction
* Scene understanding

---

## Video Demo

📺 YouTube Video:

```text
Coming Soon
```

---

## System Architecture

```text
USB Camera
    ↓
Scene Detector (OpenCV)
    ↓
OpenClaw Agent
    ↓
Python Control Layer
    ↓
ESP32-C3 Controller
    ↓
4DOF Robotic Arm
```

---

## Hardware Used

* RDK S100
* ESP32-C3
* USB Camera
* 4DOF Servo Robotic Arm
* Red and Green Cubes
* Sorting Bins

---

## Project Structure

```text
AI-Robotic-Arm-RDK-S100-OpenClaw
│
├── python/
│   ├── arm_api.py
│   ├── main.py
│   ├── robot_controller.py
│   ├── scene_detector.py
│   └── task_executor.py
│
├── ESP32_Firmware/
│   └── ESP32_C3_Robotic_Arm.ino
│
├── OpenClaw_Skill/
│   └── SKILL.md
│
└── README.md
```

---

## Supported Commands

### Scene Commands

```bash
scene
status
```

### Manual Control

```bash
pick A
pick B
pick C

drop LEFT
drop RIGHT

move A LEFT
move B RIGHT
```

### Autonomous Tasks

```bash
sort_red
sort_green
home
```

---

## WhatsApp Control

After integrating OpenClaw with WhatsApp, the robotic arm can be controlled using natural language.

Examples:

```text
What cubes do you see?

Pick cube A

Drop it in the green bin

Sort all red cubes

Sort all green cubes
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/proknowdiy/AI-Robotic-Arm-RDK-S100-OpenClaw.git

cd AI-Robotic-Arm-RDK-S100-OpenClaw/python
```

### Install Dependencies

```bash
pip install opencv-python numpy pyserial
```

---

## Running the Project

### Option 1: Standalone Control

Run the interactive command-line interface:

```bash
python3 main.py
```

Available commands:

```bash
scene
status

pick A
pick B
pick C

drop LEFT
drop RIGHT

move A LEFT
move B RIGHT

sort_red
sort_green

home
```

---

### Option 2: OpenClaw Integration

The `arm_api.py` script is designed to be used by OpenClaw.

Examples:

```bash
python3 arm_api.py scene
```

```bash
python3 arm_api.py status
```

```bash
python3 arm_api.py pick A
```

```bash
python3 arm_api.py drop RIGHT
```

```bash
python3 arm_api.py sort_red
```

---

## OpenClaw Setup

1. Install OpenClaw on the RDK S100.

2. Open RDK Studio.

3. Navigate to:

```text
Skills Workshop
    ↓
Board Skills
```

4. Create a new skill.

5. Copy the contents of:

```text
OpenClaw_Skill/robotic-arm.md
```

into the skill editor.

6. Save the skill.

After setup, OpenClaw can control the robotic arm using natural language commands.

Examples:

```text
What cubes do you see?

Pick cube A

Drop it in the green bin

Sort all red cubes

Sort all green cubes
```

---

## Troubleshooting

### ESP32-C3 Not Detected

Check available serial ports:

```bash
ls /dev/tty*
```

Typical output:

```text
/dev/ttyACM0
```

If your ESP32 appears on a different port, update:

```python
robot_controller.py
```

Change:

```python
serial.Serial('/dev/ttyACM0', 115200)
```

to the correct port.

Example:

```python
serial.Serial('/dev/ttyUSB0', 115200)
```

---

### USB Camera Not Detected

Check connected cameras:

```bash
ls /dev/video*
```

Test camera:

```bash
v4l2-ctl --list-devices
```

If your camera is not `/dev/video0`, update:

```python
scene_detector.py
```

Change:

```python
cap = cv2.VideoCapture(0)
```

Example:

```python
cap = cv2.VideoCapture(1)
```

---

### No Cubes Detected

Verify:

* Camera is connected.
* Lighting conditions are adequate.
* Red and green cubes are inside the defined detection regions.
* HSV thresholds match your cube colors.

---

### OpenClaw Cannot Control the Arm

Verify:

```bash
python3 arm_api.py status
```

returns:

```text
{'holding_cube': False}
```

before integrating with OpenClaw.

Also ensure:

```text
robotic-arm.md
```

contains the correct path to:

```text
arm_api.py
```

---

### OpenClaw Skill Stops Working After Moving the Project Folder

Update all references inside:

```text
OpenClaw_Skill/robotic-arm.md
```

Example:

```bash
python3 /home/sunrise/Documents/AI-Robotic-Arm-RDK-S100-OpenClaw/python/arm_api.py scene
```

The path must match your actual installation directory.


## Future Improvements

* Voice control
* Dynamic coordinate-based picking
* Inverse kinematics
* YOLO-based object detection
* Multi-color sorting
* Multi-object recognition

---

## License

MIT License

---

## Author

**Vishal Sharma**

YouTube: **Pro Know**

https://www.youtube.com/@ProKnowDIY

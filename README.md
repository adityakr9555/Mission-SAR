# 🚁 Mission-SAR

> Computer Vision-Based Search & Rescue Drone Prototype

Mission-SAR is a software prototype that demonstrates a computer-vision-based approach to Search & Rescue operations.

The system analyzes video footage to detect and track people, monitor changes in the scene, generate SAR alerts, attach simulated GPS coordinates, and detect potential obstacles.

---

## 🧩 What I Built

Mission-SAR combines multiple computer-vision components into one Search & Rescue pipeline:

| Module | Purpose |
|---|---|
| 👤 Person Detection | Detect people using YOLO |
| 🎯 Person Tracking | Track detected people using ByteTrack |
| 👥 People Counting | Monitor the number of tracked people |
| 🚨 SAR Alerts | Detect changes in people count |
| 📍 GPS Simulation | Generate simulated coordinates during alerts |
| 🛑 Obstacle Detection | Detect potential obstacles |
| 🧭 Direction Detection | Identify obstacle position: Left / Center / Right |
| 📊 Mission Report | Summarize alerts and GPS data |

---

## ⚙️ How the System Works

```text
                 INPUT VIDEO
                     │
                     ▼
              ┌──────────────┐
              │     YOLO     │
              │    Person    │
              │  Detection   │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │  ByteTrack   │
              │   Tracking   │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │    People    │
              │    Count     │
              └──────┬───────┘
                     │
                     ▼
             5 Consecutive Frames
                     │
                     ▼
              ┌──────────────┐
              │  SAR ALERT   │
              └──────┬───────┘
                     │
              ┌──────┴───────┐
              ▼              ▼
        GPS Simulation    Alert Log
              │              │
              └──────┬───────┘
                     ▼
              Mission Report
```

---

## 🛑 Obstacle Detection

A separate computer-vision module analyzes each video frame for potential obstacles and determines their position in the frame.

```text
Input Video
     │
     ▼
YOLO Object Detection
     │
     ▼
Obstacle Detected?
     │
 ┌───┴───┐
 │       │
YES      NO
 │       │
 ▼       ▼
Check   PATH
Position CLEAR
 │
 ├── LEFT
 ├── CENTER
 └── RIGHT
```

The prototype currently checks objects such as:

- Bicycle
- Car
- Motorcycle
- Bus
- Truck
- Chair
- Bench
- Suitcase

---

## 🧠 Tech Stack

### Language

- Python

### Computer Vision

- OpenCV
- YOLO
- Ultralytics

### Object Tracking

- ByteTrack

### Development

- VS Code
- Git
- GitHub

---

## 📁 Project Structure

```text
Mission-SAR/
│
├── src/
│   ├── final_sar_system.py
│   ├── gps_tracker.py
│   ├── mission_report.py
│   ├── obstacle_avoidance.py
│   ├── test_yolo.py
│   └── test_yolo_backup.py
│
├── videos/
│   ├── easy_test.mp4
│   └── medium_test.mp4
│
├── test_video.mp4
├── yolo26n.pt
├── .gitignore
├── README.md
└── requirements.txt
```

### Main Files

- `final_sar_system.py` — Runs the integrated SAR pipeline on the test videos.
- `gps_tracker.py` — Provides simulated GPS coordinates for SAR alerts.
- `obstacle_avoidance.py` — Detects potential obstacles and their position in the frame.
- `mission_report.py` — Generates a summary of SAR alerts and GPS locations.
- `test_yolo.py` — Person detection and tracking prototype.
- `requirements.txt` — Lists the Python dependencies required to run the project.

---

## 🚀 Getting Started

Follow these steps to run Mission-SAR locally.

### 1. Clone the Repository

```bash
git clone https://github.com/adityakr9555/Mission-SAR.git
cd Mission-SAR
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Mission-SAR

```bash
python src/final_sar_system.py
```

The system processes the three test videos and generates SAR alerts with simulated GPS coordinates.

### 5. Generate Mission Report

```bash
python src/mission_report.py
```

The report summarizes the SAR alerts and GPS locations recorded during the mission run.

---

## 🧪 Testing

Mission-SAR was tested using three video inputs:

- `test_video.mp4`
- `videos/easy_test.mp4`
- `videos/medium_test.mp4`

The final pipeline successfully processed all three videos.

The system generated:

- Person detection and tracking results
- People-count changes
- SAR alerts
- Simulated GPS coordinates
- Alert log entries
- Mission report output

---

## 📊 Mission Report

The `mission_report.py` script reads the SAR alert log and summarizes:

- Total SAR alerts
- Logged GPS locations
- Recent GPS coordinates
- Mission processing status

Example output:

```text
======================================
       MISSION-SAR REPORT
======================================

Total SAR Alerts     : [generated during run]
GPS Locations Logged : [generated during run]

Latest GPS Locations:
--------------------------------------
Latitude  : [latitude]
Longitude : [longitude]
--------------------------------------

Mission Status : COMPLETE
======================================
```

> `Mission Status : COMPLETE` indicates that the report script completed successfully. It does not represent completion of a real-world rescue mission.

---

## ⚠️ Current Limitations

- GPS coordinates are simulated and are not connected to physical GPS hardware.
- The system currently processes prerecorded video files.
- Obstacle detection is based on objects detected within the video frame.
- Direction detection identifies obstacle position as Left, Center, or Right.
- The prototype does not directly control a physical drone.
- Real-world flight testing has not been performed.

---

## 🔮 Future Development

- Integrate real GPS hardware for live drone coordinates.
- Add real-time camera input instead of prerecorded videos.
- Improve obstacle detection with depth estimation.
- Connect obstacle detection with actual drone flight-control systems.
- Add thermal-camera support for low-visibility search scenarios.
- Improve person detection and tracking for complex environments.
- Add mission-map visualization for detected locations and alerts.

---

## 📌 Project Status

**Current Status:** Working Software Prototype

The current implementation demonstrates the core computer-vision and mission-monitoring pipeline using prerecorded test videos.

---

## 🧪 Testing & Results

Mission-SAR was tested using three prerecorded video scenarios to verify the main computer-vision pipeline.

### Test Scenarios

| Test Video | Purpose |
|---|---|
| `test_video.mp4` | Person detection, tracking and SAR alert testing |
| `easy_test.mp4` | Basic person detection and tracking |
| `medium_test.mp4` | Person detection, tracking and alert generation |

### Verified Components

- YOLO-based person detection
- ByteTrack-based person tracking
- People counting using tracking IDs
- SAR alerts based on consecutive frame changes
- Simulated GPS coordinates during alerts
- Obstacle detection and direction identification
- Mission report generation

### Output

The system processes all three test videos and generates the corresponding video outputs and mission monitoring data.

> **Note:** GPS coordinates used in this prototype are simulated and are not obtained from a physical drone GPS module.

---


## 👨‍💻 Author

**Aditya Kumar**

B.Tech CSE (AIML)

GitHub:  
https://github.com/adityakr9555
# 🚁 Mission-SAR

> **AI-powered Search & Rescue drone software prototype using Computer Vision.**

Mission-SAR is a software prototype that explores how AI and Computer Vision can support autonomous Search & Rescue operations.

The system analyzes video footage to detect and track people, monitor changes in the scene, generate SAR alerts, attach simulated GPS coordinates, and detect potential obstacles.

---

## 🧩 What I Built

Mission-SAR combines multiple computer-vision components into one Search & Rescue pipeline:

| Module | Purpose |
|---|---|
| 👤 Person Detection | Detect people using YOLO |
| 🎯 Person Tracking | Track detected people using ByteTrack |
| 👥 People Counting | Monitor the number of tracked people |
| 🚨 SAR Alerts | Detect significant changes in people count |
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
 YES     NO
 │       │
 ▼       ▼
Check    PATH
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

**Language**
- Python

**Computer Vision**
- OpenCV
- YOLO
- Ultralytics

**Object Tracking**
- ByteTrack

**Development**
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

### 4. Run the Complete SAR System

```bash
python src/final_sar_system.py
```

The system processes the available test videos and performs:

- Person detection
- Person tracking
- People counting
- SAR alert generation
- GPS simulation
- Obstacle detection

### 5. Generate the Mission Report

```bash
python src/mission_report.py
```

The report displays the total SAR alerts and logged GPS locations.

---

## 🧪 Testing & Results

The prototype was tested using three different video inputs to evaluate person detection, tracking, SAR alert generation, GPS simulation, and obstacle detection.

### Test Videos

| Video | Purpose |
|---|---|
| `test_video.mp4` | Person detection and tracking |
| `easy_test.mp4` | Basic SAR detection scenario |
| `medium_test.mp4` | More challenging multi-person scenario |

### System Output

During testing, the system successfully:

- Detected people using YOLO
- Tracked detected people using ByteTrack
- Counted detected persons
- Generated SAR alerts after sustained changes in people count
- Logged simulated GPS coordinates with alerts
- Detected potential obstacles and their frame position
- Processed all three test videos

### Mission Report

The `mission_report.py` script summarizes the generated SAR alerts and GPS locations.

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

> Note: GPS coordinates used in this prototype are simulated and are not obtained from a real drone GPS module.

---

## ⚠️ Current Limitations

Mission-SAR is currently a software prototype focused on demonstrating AI-based Search and Rescue capabilities.

- GPS coordinates are simulated rather than obtained from real GPS hardware.
- Obstacle detection is based on video-frame analysis and does not directly control a physical drone.
- Test scenarios use prerecorded video inputs.
- The system has not yet been deployed on an actual autonomous drone.
- Real-world performance may vary depending on lighting, camera quality, environment, and detection accuracy.

---

## 🔮 Future Development

The project can be extended toward a more complete autonomous Search and Rescue system.

### Planned Improvements

- 🛰️ Integration with real GPS hardware
- 🚁 Real-time drone telemetry
- 🧭 Autonomous waypoint navigation
- 🛑 Real-time obstacle avoidance and flight control
- 🌡️ Thermal-camera-based person detection
- 🧠 Advanced person tracking and re-identification
- 🗺️ Live search-area mapping
- 📡 Real-time communication with a ground station
- 🚨 Improved emergency alert and rescue coordination
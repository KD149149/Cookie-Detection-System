

# Cookie Conveyor Inspection System

**Real-Time Detection, Counting & Quality Classification**

---

## Overview

The **Cookie Conveyor Inspection System** is a real-time computer vision solution designed for **high-speed food production lines**. The system automatically **detects, counts, assigns IDs**, and **classifies cookies** as *perfect* or *faulty (half/broken)* while they move continuously on a conveyor belt.

It provides **live visual feedback**, **accurate counting**, **video recording**, and **downloadable inspection reports**, making it suitable for **industrial quality control, audits, and traceability**.

---

## Key Features

### Camera Input

* Single startup pop-up for camera selection
* Supports:

  * Live USB camera
  * External IP camera (RTSP / HTTP)

### Real-Time Detection & Counting

* Circle-based cookie detection
* Optimized for fast-moving conveyors
* Unique ID assigned to each cookie
* No double counting using spatial filtering

### Quality Classification

* **Green (OK)** → Complete circular cookie
* **Red (Faulty)** → Half / broken cookie
* Once classified, status remains unchanged

### Live Dashboard

* Displays on the UI:

  * Total cookies passed
  * Perfect cookies
  * Faulty cookies

### Video Recording

* Automatically records the inspection
* Saved with date and time
* Useful for audits and historical review

### Report Generation

* Auto-generated **Excel report**
* Includes:

  * Cookie ID
  * Status (OK / Faulty)
  * Quality metric (area ratio)
  * Timestamp

---

## System Architecture (High Level)

**Input Layer**

* USB Camera / IP Camera

**Processing Layer**

* Frame capture
* Noise reduction
* Circle detection (Hough Transform)
* Area-based quality evaluation

**Output Layer**

* Live annotated video feed
* Real-time count dashboard
* Recorded video
* Excel inspection report

---

## Detection Logic

The system uses **geometry-based inspection**, which is fast, explainable, and reliable for uniform food items like cookies.

### Quality Decision Rule

```
Area Ratio = Detected Area / Ideal Circle Area
```

| Area Ratio | Classification      |
| ---------- | ------------------- |
| ≥ 0.75     | Perfect (Green)     |
| < 0.75     | Faulty / Half (Red) |

This approach works effectively for high-speed conveyors and avoids the overhead of deep learning models.

---

## Installation

### Requirements

* Python 3.8+
* OpenCV
* NumPy
* Pandas
* Pillow

### Install Dependencies

```bash
pip install opencv-python numpy pandas pillow
```

---

## How to Run

```bash
python cookie_conveyor_fast_inspection.py
```

1. On startup, select:

   * `1` for Live Camera
   * `2` for IP Camera
2. Camera pop-up closes automatically
3. Inspection window starts
4. System runs continuously until closed
5. Report is generated automatically at exit

---

## Recommended Camera Setup (Important)

For best accuracy:

* Camera angle: **Top-down or 10–15° tilt**
* High shutter speed (≥ 1/1000)
* Uniform, non-reflective conveyor belt
* Stable lighting (no flicker)
* Fixed camera mount (no vibration)

---

## Output Structure

```
output/
 └── YYYY-MM-DD/
     ├── recording_HHMMSS.mp4
     └── cookie_report_HHMMSS.xlsx
```

---

## Future Enhancements (Optional)

* YOLO / Deep Learning integration
* Object tracking (DeepSORT)
* PLC / reject mechanism integration
* Multi-lane conveyor support
* PDF reports
* Edge deployment (Jetson / Industrial PC)

---

## Developer Details

**Developer Name:** Kajal Dadas
**Email:** [kajaldadas149@gmail.com](mailto:kajaldadas149@gmail.com)

For development support, customization, or industrial deployment inquiries, please reach out via email.

---



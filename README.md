# ATTIS — Acoustic Tracking and Target Identification System

> An embedded acoustic perception system for real-time sound-source localization using a three-microphone array, ESP32-based signal processing, and direction-of-arrival estimation.

---

## Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Problem Statement](#problem-statement)
- [Proposed Solution](#proposed-solution)
- [System Architecture](#system-architecture)
- [Hardware](#hardware)
- [Signal Processing & Localization](#signal-processing--localization)
- [Embedded Implementation](#embedded-implementation)
- [Experimental Setup](#experimental-setup)
- [Results](#results)
- [Challenges & Engineering Trade-offs](#challenges--engineering-trade-offs)
- [My Contributions](#my-contributions)
- [Potential Applications](#potential-applications)
- [Future Development](#future-development)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Key Takeaways](#key-takeaways)
- [Project Information](#project-information)
- [Author](#author)
- [License](#license)

---

## Overview

**ATTIS (Acoustic Tracking and Target Identification System)** is a low-cost embedded acoustic localization platform designed to estimate the direction of a sound source in real time.

The system uses a **three-microphone array** arranged in a triangular configuration. Audio signals captured by the microphones are acquired and processed by an **ESP32 microcontroller**, which compares the signals across the array to estimate the direction from which the sound originates.

The project explores acoustic sensing as an alternative and complementary perception modality for autonomous systems, particularly in environments where conventional vision-based perception becomes unreliable.

### Core Pipeline

```text
   Acoustic Source
         │
         ▼
┌─────────────────────┐
│ 3-Microphone Array  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ ESP32 Acquisition & │
│ Signal Processing   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Inter-Microphone    │
│ Signal Comparison   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Direction-of-Arrival│
│ Estimation (θ)      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Spatial Output      │
└─────────────────────┘
```

---

## Motivation

Most autonomous robotic systems rely heavily on cameras and other visual sensors for perception. Vision-based sensing can degrade significantly in environments with:

- Poor visibility or darkness
- Smoke or dust
- Occlusions
- Confined or underground spaces
- Limited line of sight

Sound, in contrast, can propagate around obstacles and does not require a direct visual path to the source. This motivates the use of acoustic perception as a complementary sensing modality.

For example, a robot operating in a disaster environment could use acoustic information to identify the direction of:

- Human voices
- Knocking or tapping
- Machinery
- Alarms
- Other characteristic sound sources

ATTIS was developed as a proof-of-concept to investigate whether a low-cost embedded microphone array can provide useful directional information in real time.

---

## Problem Statement

The objective of ATTIS is to develop an embedded system capable of:

1. Acquiring audio signals from multiple spatially distributed microphones.
2. Processing the signals in real time on a microcontroller.
3. Comparing the signals received at different microphones.
4. Estimating the direction of the incoming sound.
5. Providing a spatially meaningful representation of the detected sound source.

The system was designed with future integration into autonomous robotic platforms in mind.

---

## Proposed Solution

ATTIS uses spatially separated microphones to exploit differences in the sound received at each microphone.

When a sound source is not directly in front of the array, the acoustic wave reaches the microphones at different times and with different signal characteristics. These differences contain information about the **direction of arrival (DOA)** of the sound.

```text
             Acoustic Source
                    │
                    ▼
          ┌──────────────────┐
          │ Microphone Array │
          └────────┬─────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  Signal Acquisition   Signal Comparison
         │                   │
         └─────────┬─────────┘
                   ▼
          Direction Estimation
                   │
                   ▼
             Spatial Output
```

---

## System Architecture

The ATTIS prototype consists of four major subsystems:

| # | Subsystem | Description |
|---|-----------|-------------|
| 1 | **Acoustic Sensing** | Three MAX9814 microphone modules arranged approximately 120° apart provide spatially distributed audio measurements. |
| 2 | **Signal Acquisition** | Microphone outputs are connected to the ESP32's analog inputs, which sample the incoming signals for real-time processing. |
| 3 | **Signal Processing & Localization** | Acquired signals are compared across microphones. Depending on source direction, they differ in **amplitude**, **relative phase**, and **arrival time** — differences used to estimate direction. |
| 4 | **Reporting** | The estimated direction is converted into spatially meaningful, low-latency feedback. |

### Microphone Array Geometry

The three microphones are arranged approximately 120° apart, forming a triangular sensing geometry.

```text
                MIC 1
                  ●
                 / \
                /   \
               /     \
              /       \
             /         \
            ●───────────●
         MIC 2         MIC 3

          ≈ 120° spacing
```

Localization performance depends on the relationship between:

- Microphone spacing
- Array geometry
- Sound wavelength
- Source distance
- Environmental reflections

---

## Hardware

### Components

| Component | Quantity | Purpose |
|-----------|:--------:|---------|
| ESP32-WROOM Development Board | 1 | Embedded processing and signal acquisition |
| MAX9814 Microphone Module | 3 | Acoustic signal acquisition |
| Acoustic Receiver Structure | 1 | Spatial microphone arrangement |
| Breadboard | 1 | Prototype assembly |
| Jumper Wires | — | Electrical connections |
| Power Supply | 1 | System power |

### Electrical Architecture

```text
┌─────────────┐
│ MAX9814 #1  │──┐
└─────────────┘  │
┌─────────────┐  │      ┌─────────────────────────┐
│ MAX9814 #2  │──┼─────►│  ESP32 (ADC inputs)     │
└─────────────┘  │      │                         │
┌─────────────┐  │      │  • Signal acquisition   │
│ MAX9814 #3  │──┘      │  • Signal processing    │
└─────────────┘         │  • Direction estimation │
                        └────────────┬────────────┘
                                     │
                                     ▼
                              Direction Output
```

> **Note:** Exact GPIO assignments should be taken from the firmware in this repository.

---

## Signal Processing & Localization

The microphone signals are continuously sampled by the ESP32 and passed through a simplified processing pipeline:

```text
Raw Microphone Signals
         │
         ▼
    ADC Sampling
         │
         ▼
   Signal Filtering
         │
         ▼
  Signal Comparison
         │
         ▼
Direction Estimation
         │
         ▼
   Spatial Output
```

### Inter-Microphone Signal Comparison

Because the microphones are spatially separated, the same acoustic event produces slightly different signals at each microphone.

```text
                Sound Source
                     \
                      \  Acoustic Wave
                       \
        ┌───────────────\───────────────┐
        │                \              │
        ▼                 ▼             ▼
      MIC 1             MIC 2         MIC 3
        │                 │             │
        ▼                 ▼             ▼
      x₁(t)             x₂(t)         x₃(t)
```

### Direction-of-Arrival Estimation

The primary objective of the localization algorithm is to estimate **θ**, the direction of the sound source, by evaluating relative signal characteristics between microphones:

```text
         Microphone Differences
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
 Amplitude      Phase      Arrival-Time
 Differences  Differences  Differences
     │            │            │
     └────────────┼────────────┘
                  ▼
           DOA Estimation
                  │
                  ▼
             θ estimate
```

The current implementation is a proof-of-concept localization system, with scope for more sophisticated time-delay and frequency-domain methods in future versions.

---

## Embedded Implementation

The ESP32 acts as the central processing unit of ATTIS. Its responsibilities include:

- Acquiring and sampling microphone signals
- Processing the sampled signals
- Comparing signals across the microphone array
- Estimating sound direction
- Generating the system output

The core localization pipeline runs entirely on the microcontroller, without requiring a desktop computer. This makes the system a suitable foundation for future mobile robotic integration.

### Development Workflow

```text
Microphone Selection
        │
        ▼
Array Geometry Design
        │
        ▼
Hardware Integration
        │
        ▼
ESP32 Signal Acquisition
        │
        ▼
Signal Processing
        │
        ▼
Direction Estimation
        │
        ▼
Controlled Experiments
        │
        ▼
Performance Evaluation
```

---

## Experimental Setup

The prototype was tested by placing a sound source at controlled angular positions (θ) relative to the microphone array.

```text
              Sound Source
                   ●
                  /
                 /
                / θ
               ▼
      ┌──────────────────┐
      │    Microphone    │
      │      Array       │
      └──────────────────┘
```

Multiple source positions were evaluated to determine the relationship between the actual and estimated source direction. Testing focused on:

- Directional accuracy
- Operating range
- Noise sensitivity
- Microphone response variation
- Array geometry
- Real-time performance

---

## Results

The prototype successfully demonstrated real-time acoustic direction localization using low-cost hardware.

### Measured Performance

| Parameter | Result |
|-----------|--------|
| Operating range | ~1.5–2 m |
| Direction estimation accuracy | ~±15–25° |
| Processing | Real-time |
| Processing platform | ESP32 |
| Microphone configuration | 3-channel triangular array |

The system was able to distinguish different sound-source directions in controlled environments, demonstrating the feasibility of a compact embedded microphone array as a directional acoustic sensor.

---

## Challenges & Engineering Trade-offs

| Challenge | Description | Implication |
|-----------|-------------|-------------|
| **Microphone sensitivity** | Individual modules vary in sensitivity, introducing errors into amplitude-based comparisons. | Calibration is important for consistent localization. |
| **ADC resolution** | The ESP32's onboard ADC constrains the quality and consistency of analog acquisition. | Higher-quality ADCs or digital microphones could improve future versions. |
| **Environmental noise** | Background sounds interfere with the target signal. | Filtering, frequency-domain processing, and sound classification can improve robustness. |
| **Acoustic reflections** | Reflections from walls and nearby surfaces create multiple paths and distort the apparent direction of arrival. | Reverberant environments require more advanced algorithms. |
| **Array geometry** | Placement trades off spatial resolution, physical size, operating frequency, and directional ambiguity. | Geometry must be co-designed with the target application. |

---

## My Contributions

My primary contributions focused on embedded systems development, hardware integration, and acoustic signal processing.

**Hardware Integration**
- Designed and assembled the three-microphone acquisition system.
- Integrated MAX9814 microphone modules with the ESP32.
- Worked on microphone placement and system calibration.

**Embedded Development**
- Implemented real-time microphone signal acquisition on the ESP32.
- Developed the embedded signal-processing pipeline.
- Implemented logic for comparing signals across the microphone array.

**Acoustic Localization**
- Developed direction-estimation logic using inter-microphone signal characteristics.
- Tested the system under controlled sound-source positions.
- Investigated the effects of noise, microphone sensitivity, and array geometry.

**System Validation**
- Conducted experiments to evaluate directional accuracy and operating range.
- Characterized practical limitations of the low-cost microphone-array architecture.
- Documented system-level trade-offs for future robotic integration.

---

## Potential Applications

- 🚑 **Search and Rescue** — Identify the direction of voices, tapping, or other signals in collapsed structures, smoke-filled or low-visibility environments, and underground spaces.
- 🤖 **Autonomous Robotics** — Serve as an acoustic perception module for robots where visual sensing is unreliable, feeding direction estimates into navigation or target-tracking.
- 🏭 **Industrial Monitoring** — Identify abnormal machinery sounds and estimate their spatial origin.
- 🐦 **Wildlife Monitoring** — Locate animal calls where direct visual observation is difficult.
- 🏢 **Smart Infrastructure** — Distributed acoustic sensors for spatial event detection and environmental monitoring.

---

## Future Development

### 🎵 1. Frequency-Domain Processing

FFT-based processing to identify dominant frequencies and separate target sounds from background noise.

```text
Time-Domain Signal → FFT → Frequency Spectrum → Target Frequency Detection
```

### 🎯 2. Improved Localization Algorithms

- Time Difference of Arrival (TDOA)
- Cross-correlation
- GCC-PHAT
- Beamforming
- Multi-source localization

### 🧠 3. Sound Classification

Combine localization with machine-learning-based classification to determine not only *where* a sound originates but potentially *what* it is.

```text
             Audio Input
                  │
         ┌────────┴────────┐
         ▼                 ▼
    Localization     Classification
         │                 │
         ▼                 ▼
   Source Direction    Sound Type
         │                 │
         └────────┬────────┘
                  ▼
        Acoustic Scene Understanding
```

### 🤖 4. Autonomous Sound Tracking

Integrate ATTIS with a mobile robot so the estimated direction can orient the robot toward the source in a closed loop.

```text
 Sound Source
      │
      ▼
Acoustic Detection ─► Direction Estimation ─► Robot Orientation
                                                     │
      ┌──────────────────────────────────────────────┘
      ▼
Motion Toward Source ─► Continuous Update ─┐
      ▲                                    │
      └────────────────────────────────────┘
```

### 📡 5. Wireless Integration

Transmit localization data wirelessly to a higher-level robotic controller or distributed autonomous system.

### 🧭 6. Sensor Fusion

Combine acoustic localization with complementary sensors — IMU, camera, LiDAR, ultrasonic sensors, and GNSS where available.

```text
Camera ──────┐
LiDAR ───────┤
             ├──► Sensor Fusion ──► Robot Perception
IMU ─────────┤
ATTIS ───────┘
```

### 🚀 Long-Term Vision

The long-term goal is to evolve ATTIS from a simple direction detector into a complete **acoustic perception module** for autonomous robots, combining localization and classification within a multimodal perception stack:

```text
        ┌──────────────────┐
        │ Microphone Array │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ Acoustic         │
        │ Localization     │
        └────────┬─────────┘
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
Source Direction     Sound Classification
      │                     │
      └──────────┬──────────┘
                 ▼
        ┌──────────────────┐
        │  Sensor Fusion   │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ Robot Perception │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ Navigation /     │
        │ Target Tracking  │
        └──────────────────┘
```

---

## Technology Stack

**Hardware**
- ESP32-WROOM
- 3 × MAX9814 microphone modules
- Custom acoustic receiver structure
- Breadboard, jumper wires, power supply

**Software**
- Embedded C/C++
- ESP32 Arduino framework
- Digital signal processing
- Real-time data acquisition
- Serial communication

**Core Concepts**
- Microphone arrays
- Direction of Arrival (DOA)
- Acoustic localization
- Signal processing
- Embedded systems
- Sensor integration
- Robotic perception
- Sensor fusion

---

## Repository Structure

<!-- TODO: Update the folder names below to match the actual repository structure. -->

```text
ATTIS/
│
├── src/          # ESP32 firmware and embedded processing
├── data/         # Experimental data
├── analysis/     # Signal analysis and evaluation scripts
├── hardware/     # Hardware and circuit documentation
├── media/        # Images and demonstration media
└── README.md
```

---

## Key Takeaways

ATTIS demonstrates how a relatively simple and inexpensive sensor configuration can be developed into a real-time perception system, covering:

- Embedded systems and sensor interfacing
- Real-time data acquisition
- Digital signal processing
- Acoustic localization
- Experimental characterization
- Hardware–software integration

The project follows the chain:

**Physical sensing → Embedded acquisition → Signal processing → Spatial inference → Robotic perception**

The resulting prototype provides a foundation for extending acoustic sensing toward autonomous sound-source localization, tracking, and multimodal robotic perception.

---

## Project Information

| Parameter | Details |
|-----------|---------|
| Project | ATTIS — Acoustic Tracking and Target Identification System |
| Domain | Embedded Systems / Acoustic Perception |
| Platform | ESP32 |
| Sensors | 3 × MAX9814 microphones |
| Core Concept | Acoustic Direction-of-Arrival Estimation |
| Output | Real-time sound-source direction |
| Type | Instrumentation Project |
| Operating Range | ~1.5–2 m |
| Measured Directional Accuracy | ~±15–25° |

### Detailed Report

The complete project report covers: problem formulation, motivation and applications, hardware architecture, microphone-array configuration, signal-processing methodology, direction-estimation approach, experimental methodology, results and observations, system limitations, and the future development roadmap.

---

## Author

**Lavanya Bhatnagar**
Mechanical Engineering
Indian Institute of Technology Indore

---

## License

This repository is intended primarily for academic and educational purposes.
If you use or extend this project, please provide appropriate attribution.

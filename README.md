# ATTIS - Acoustic Tracking and Target Identification System

## Overview

ATTIS (Acoustic Tracking and Target Identification System) is a sound localization platform developed to detect and estimate the direction of a sound source in real time using a distributed microphone array and embedded signal processing.

The project was motivated by applications where vision-based systems are unreliable, such as disaster response, underground environments, industrial monitoring, and autonomous robotic exploration. By leveraging acoustic information, ATTIS provides a foundation for future autonomous systems capable of locating and tracking sound sources. :contentReference[oaicite:1]{index=1}

The prototype utilizes a three-microphone array connected to an ESP32 microcontroller, where incoming audio signals are sampled, processed, and compared to estimate the direction of arrival of sound. :contentReference[oaicite:2]{index=2}

---

## Key Features

- Real-time sound direction estimation
- Triangular microphone array configuration
- Embedded signal processing using ESP32
- Sound source localization using amplitude and phase differences
- Low-cost hardware implementation
- Expandable architecture for robotic integration
- Proof-of-concept for autonomous acoustic tracking

---

## Applications

### Search and Rescue
Detecting cries, tapping, or movement sounds from trapped individuals in disaster environments.

### Industrial Monitoring
Detecting abnormal sounds and machine faults before catastrophic failures occur.

### Wildlife Monitoring
Tracking animal calls and identifying suspicious activity in remote areas.

### Security and Defense
Gunshot direction detection and acoustic surveillance.

### Autonomous Robotics
Future integration with mobile robots for autonomous sound-source tracking. :contentReference[oaicite:3]{index=3}

---

## System Architecture

The ATTIS prototype consists of four major subsystems:

### Sound Detection
Three MAX9814 microphones arranged approximately 120° apart capture incoming sound signals.

### Signal Processing
The ESP32 samples microphone outputs using its onboard ADC and performs real-time processing.

### Localization
Direction estimation is achieved by comparing signal amplitudes and phase differences between microphones.

### Reporting
The processed output is converted into spatially aware audio feedback with low latency. :contentReference[oaicite:4]{index=4}

---

## Hardware Components

- ESP32 WROOM Development Board
- 3 × MAX9814 Microphone Modules
- Custom Acoustic Receiver Structure
- Breadboard and Interconnects
- Power Supply

---

## My Contributions

My primary contributions focused on embedded systems development, hardware integration, and signal processing implementation.

- Designed and assembled the microphone acquisition system
- Integrated MAX9814 microphones with ESP32 hardware
- Developed embedded signal acquisition and processing pipeline
- Implemented real-time sound direction estimation logic
- Assisted in testing, calibration, and performance evaluation
- Contributed to system architecture and future robotic integration concepts

---

## Results

The prototype successfully demonstrated acoustic direction localization using low-cost hardware.

### Performance

- Effective range: 1.5–2 m
- Direction estimation accuracy: ±15–25°
- Real-time operation using ESP32 onboard ADC

The system was able to distinguish sound direction and provide basic spatial awareness in controlled environments. :contentReference[oaicite:5]{index=5}

---

## Challenges

- Microphone sensitivity variations
- ADC resolution limitations
- Environmental noise
- Synchronization constraints
- Acoustic receiver geometry optimization

These challenges provided valuable insights into practical sensor integration and real-world signal processing. :contentReference[oaicite:6]{index=6}

---

## Future Improvements

- Integration with a mobile robotic platform
- FFT-based frequency analysis
- Sound source classification
- I2S digital microphone implementation
- Wireless communication
- IMU-assisted localization
- Autonomous sound-source tracking

---

## Detailed Report

The complete project report includes:

- Problem formulation
- Hardware design
- Signal processing methodology
- Experimental setup
- Results and observations
- Future development roadmap

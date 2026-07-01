# SentinelAI

## Autonomous Multi-Sensor Counter-UAS Mission Control System

SentinelAI is a real-time Counter-Unmanned Aircraft System (Counter-UAS) prototype designed to protect a 1 km² Forward Operating Base (FOB). The system demonstrates autonomous threat detection, tracking, visualization, trajectory prediction, and AI-assisted threat classification using a live mission control dashboard.

This project was developed for the **AWS DC Summit 2026 Global Government Hackathon** in response to the Counter-UAS Operations challenge.

---

# Problem Statement

Forward Operating Bases face increasing threats from reconnaissance drones, loitering munitions, and coordinated unmanned aircraft attacks.

Operators must rapidly:

- Detect aerial threats
- Track multiple aircraft simultaneously
- Differentiate hostile and friendly aircraft
- Predict flight paths
- Recommend countermeasures
- Maintain situational awareness while minimizing false positives

SentinelAI provides a prototype mission control system that assists operators with these tasks.

---

# Features

### Live UAS Simulator

- Continuous real-time aircraft simulation
- Multiple aircraft behaviors:
  - Attack Quadcopter
  - Recon Fixed-Wing
  - Loitering Munition
  - Friendly Aircraft
  - Wildlife / Bird

---

### Mission Control Dashboard

- Live tactical map
- Forward Operating Base (FOB)
- Defense rings
- Flight trails
- Predicted trajectories
- Sensor locations
- Mission status panel
- Threat queue
- AI decision panel
- Live track information

---

### Threat Assessment

Each aircraft is evaluated using:

- Distance to FOB
- Flight behavior
- Sensor confidence
- Threat score
- Threat priority
- Countermeasure recommendation

---

### Amazon Bedrock Demonstration

Amazon Bedrock Nova Micro was used to demonstrate AI-assisted threat classification.

The model analyzes:

- Aircraft type
- Distance
- Sensor confidence
- Heading
- Speed
- Friendly identification

and returns:

- Threat classification
- Threat level
- Confidence
- Reasoning
- Recommended action

---

# Technologies

## Map live data
-Streamlit (Used for live data map tracking of UAS)
## Programming

- Python
- Streamlit
- Pandas
- Plotly

## AWS Services

Implemented

- Amazon Bedrock (Nova Micro)
- Amazon Quick (Dashboard and data)
- Kiro – (Assisted with software development, troubleshooting, architecture refinement, and accelerating implementation during the hackathon.)

Planned Production Architecture

- AWS Lambda
- Amazon S3
- Amazon Athena
- Amazon QuickSight

---

# Architecture

## Prototype

```
Python UAS Simulator
        │
        ▼
Live Telemetry (CSV)
        │
        ▼
Mission Control Dashboard (Streamlit) (Amazon Quick)
```

## Production Architecture

```
Edge Sensors (Collect and generate aircraft detections)
        │
        ▼
Amazon Kinesis (Real-time event streaming)
        │
        ▼
AWS Lambda (Automatically process each incoming event)
        │
        ▼
Amazon Bedrock (AI threat reasoning)
        │
        ▼
AI Threat Classification 
        │
        ▼
Amazon S3 (Store operational history)
        │
        ├────────► Amazon Athena (Query historical mission data)
        └────────► Amazon QuickSight (Command-level analytics)
```

---

# Running the Prototype

## Terminal 1

```bash
python3 simulator/uav_simulator.py
```

## Terminal 2

```bash
python3 -m streamlit run dashboard/mission_control.py
```

The simulator continuously generates live telemetry while the Mission Control dashboard updates in real time.

---

# Future Improvements

- Direct Amazon Bedrock integration
- Real-time Kinesis event ingestion
- AWS Lambda event processing
- Amazon S3 data lake
- Amazon Athena analytics
- Amazon QuickSight operational dashboards
- Edge deployment for continuous operation
- Multi-FOB support
- Additional sensor fusion models

---

Prototype Capabilities
Real-time telemetry updates every 2 seconds
Multiple simulated aircraft behaviors
Live trajectory prediction
Threat prioritization
AI-assisted threat reasoning
Interactive mission control visualization

---

# Repository Structure

```
SentinalAI/

dashboard/
    mission_control.py

datasets/
    synthetic/

docs/

simulator/
    uav_simulator.py

README.md
requirements.txt
```

---

# Authors

Developed as part of the **AWS DC Summit 2026 Global Government Hackathon**.

Project: **SentinelAI**

# SentinelAI

Autonomous multi-sensor Counter-UAS mission control system for protecting a 1 km² Forward Operating Base.

## Overview

SentinelAI detects, tracks, classifies, and prioritizes unmanned aerial threats using simulated RF, radar, optical, and acoustic sensor inputs.

The prototype includes:

- Live UAO simulator
- Tactical mission control dashboard
- Threat scoring
- Predicted trajectories
- Sensor fusion concept
- Countermeasure recommendation
- AWS architecture using Kinesis, Lambda, Bedrock, S3, Athena, and QuickSight

## Prototype Features

- Real-time UAO track updates
- Friendly, hostile, recon, loitering, and wildlife contacts
- Defense rings around FOB
- Multi-sensor detection towers
- Flight trails
- Predicted paths
- Neutralization events
- AI decision panel

## Run Locally

Terminal 1:

```bash
python3 simulator/uav_simulator.py

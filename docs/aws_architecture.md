SentinelAI AWS Architecture
Overview

SentinelAI is an autonomous multi-sensor Counter-UAS mission control prototype designed to protect a 1 km² Forward Operating Base (FOB). The prototype demonstrates real-time aerial threat simulation, live mission visualization, trajectory prediction, and AI-assisted threat classification.

Prototype Data Flow
The UAO simulator generates continuous live telemetry.
Telemetry is written to a live dataset.
Mission Control reads the telemetry and updates the tactical display in real time.
Amazon Bedrock Nova Micro is used to demonstrate AI-based threat classification and countermeasure reasoning.
Amazon Kinesis Data Streams was provisioned as the planned real-time streaming layer for future integration.
AWS Services Implemented
Amazon Bedrock (Nova Micro) – AI threat classification demonstration
Amazon Kinesis Data Streams – Provisioned streaming infrastructure
GitHub – Source control and project collaboration
Prototype Architecture
UAO Simulator
        │
        ▼
Live Telemetry Dataset (CSV)
        │
        ▼
Mission Control Dashboard (Streamlit)
        │
        ├────────► Tactical Map
        ├────────► Threat Queue
        ├────────► AI Decision Panel
        └────────► Mission Status
Production AWS Architecture (Future Deployment)

The prototype is designed to evolve into a fully cloud-native architecture:

Edge Sensors / UAO Simulator
        │
        ▼
Amazon Kinesis Data Streams
        │
        ▼
AWS Lambda
        │
        ▼
Amazon Bedrock Nova Micro
        │
        ▼
Threat Classification & ROE Engine
        │
        ▼
Amazon S3
        │
        ├────────► Amazon Athena
        ├────────► Amazon QuickSight
        └────────► Mission Control Dashboard
Future AWS Services

The production architecture is designed to integrate:

Amazon Kinesis Data Streams
AWS Lambda
Amazon Bedrock Nova Micro
Amazon S3
Amazon Athena
Amazon QuickSight
Notes

This hackathon prototype demonstrates the complete operational workflow using a local simulator and Mission Control dashboard. Amazon Bedrock was successfully tested for AI-based threat reasoning, and Amazon Kinesis was provisioned as the planned streaming layer. The remaining AWS services are part of the proposed production deployment and were not implemented during the hackathon timeframe.

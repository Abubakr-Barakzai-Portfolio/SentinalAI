# SentinelAI AWS Architecture

## Overview

SentinelAI is an autonomous multi-sensor Counter-UAS mission control system for protecting a 1 km² Forward Operating Base.

## Data Flow

1. Edge sensors detect aerial contacts.
2. UAO simulator generates live telemetry.
3. Events stream into Amazon Kinesis.
4. AWS Lambda processes each detection.
5. Amazon Bedrock classifies threat intent.
6. Results are stored in Amazon S3.
7. Amazon Athena queries historical events.
8. Amazon QuickSight visualizes performance metrics.
9. Mission Control displays live tactical decisions.

## AWS Services Used

- Amazon Kinesis Data Streams
- AWS Lambda
- Amazon Bedrock Nova Micro
- Amazon S3
- Amazon Athena
- Amazon QuickSight
- Amazon Rekognition
- AWS IAM
- Amazon CloudWatch

## Architecture

```text
Edge Sensors / UAO Simulator
        |
        v
Amazon Kinesis Data Streams
        |
        v
AWS Lambda Processing Layer
        |
        v
Amazon Bedrock Nova Micro
        |
        v
Threat Classification + ROE Engine
        |
        v
Amazon S3 Data Lake
        |
        +------> Amazon Athena
        |
        +------> Amazon QuickSight
        |
        v
SentinelAI Mission Control Dashboard
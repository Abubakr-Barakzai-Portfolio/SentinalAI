import csv
import random
import time
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("datasets/synthetic/live_uav_events.csv")

DRONE_TYPES = ["quadcopter", "fixed-wing", "bird", "friendly-uav", "unknown"]
WEATHER = ["clear", "rain", "fog", "dust", "wind"]


def create_event():
    drone_type = random.choice(DRONE_TYPES)
    friendly = drone_type == "friendly-uav"

    radar_confidence = round(random.uniform(0.55, 0.99), 2)
    rf_confidence = round(random.uniform(0.40, 0.99), 2)
    optical_confidence = round(random.uniform(0.30, 0.98), 2)
    acoustic_confidence = round(random.uniform(0.25, 0.95), 2)

    threat_score = round(
        (radar_confidence * 0.30)
        + (rf_confidence * 0.25)
        + (optical_confidence * 0.25)
        + (acoustic_confidence * 0.20),
        2,
    )

    if friendly:
        threat_level = "friendly"
        countermeasure = "track only"
    elif drone_type == "bird":
        threat_level = "low"
        countermeasure = "ignore"
    elif threat_score >= 0.85:
        threat_level = "high"
        countermeasure = "rf jammer"
    elif threat_score >= 0.70:
        threat_level = "medium"
        countermeasure = "monitor and warn"
    else:
        threat_level = "low"
        countermeasure = "continue tracking"

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "drone_id": f"UAV-{random.randint(1, 12):03d}",
        "x_position_m": random.randint(0, 1000),
        "y_position_m": random.randint(0, 1000),
        "altitude_m": random.randint(20, 300),
        "speed_mps": round(random.uniform(4, 35), 1),
        "heading_deg": random.randint(0, 359),
        "drone_type": drone_type,
        "weather": random.choice(WEATHER),
        "friendly": friendly,
        "radar_confidence": radar_confidence,
        "rf_confidence": rf_confidence,
        "optical_confidence": optical_confidence,
        "acoustic_confidence": acoustic_confidence,
        "threat_score": threat_score,
        "threat_level": threat_level,
        "countermeasure": countermeasure,
    }


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = OUTPUT_FILE.exists()

    with OUTPUT_FILE.open("a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=create_event().keys())

        if not file_exists:
            writer.writeheader()

        print("Generating live UAV events. Press Ctrl+C to stop.")

        while True:
            event = create_event()
            writer.writerow(event)
            csvfile.flush()
            print(event)
            time.sleep(1)


if __name__ == "__main__":
    main()

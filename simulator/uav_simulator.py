import csv
import math
import random
import time
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path("datasets/synthetic/live_uao_events.csv")

UPDATE_SECONDS = 2
FOB_X, FOB_Y = 500, 500

ENGAGEMENT_DISTANCE_M = 70
MAX_ACTIVE_UAOS = 3
SHOOTDOWN_CHANCE = 0.15

UAO_TYPES = [
    "attack-quadcopter",
    "recon-fixed-wing",
    "loitering-munition",
    "friendly-uao",
    "bird",
]


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def random_edge_position():
    edge = random.choice(["north", "south", "east", "west"])

    if edge == "north":
        return random.randint(0, 1000), 1000
    if edge == "south":
        return random.randint(0, 1000), 0
    if edge == "east":
        return 1000, random.randint(0, 1000)

    return 0, random.randint(0, 1000)


def random_wide_target():
    return random.randint(80, 920), random.randint(80, 920)


def random_inner_target():
    return random.randint(250, 750), random.randint(250, 750)


def spawn_uao(uao_number):
    x, y = random_edge_position()

    uao_type = random.choices(
        UAO_TYPES,
        weights=[20, 25, 15, 25, 15],
        k=1
    )[0]

    friendly = uao_type == "friendly-uao"

    if uao_type == "attack-quadcopter":
        mission = "probing attack"
        target_x, target_y = random_inner_target()
        speed = random.randint(14, 24)

    elif uao_type == "recon-fixed-wing":
        mission = "perimeter recon"
        target_x, target_y = random.choice([
            (120, 120), (880, 120), (880, 880), (120, 880),
            (500, 120), (880, 500), (500, 880), (120, 500)
        ])
        speed = random.randint(18, 30)

    elif uao_type == "loitering-munition":
        mission = "loiter"
        target_x, target_y = random_inner_target()
        speed = random.randint(10, 18)

    elif uao_type == "friendly-uao":
        mission = "friendly patrol"
        target_x, target_y = random.choice([
            (200, 500), (500, 800), (800, 500), (500, 200),
            (300, 300), (700, 300), (700, 700), (300, 700)
        ])
        speed = random.randint(10, 18)

    else:
        mission = "wildlife"
        target_x, target_y = random_wide_target()
        speed = random.randint(5, 12)

    return {
        "drone_id": f"UAO-{uao_number:03d}",
        "drone_type": uao_type,
        "mission": mission,
        "x": float(x),
        "y": float(y),
        "target_x": float(target_x),
        "target_y": float(target_y),
        "speed": speed,
        "friendly": friendly,
        "status": "active",
        "age": 0,
        "shot_down_timer": 0,
    }


def choose_new_target(uao):
    if uao["drone_type"] == "attack-quadcopter":
        uao["mission"] = random.choice(["probing attack", "evasive approach", "sector penetration"])
        uao["target_x"], uao["target_y"] = random_inner_target()

    elif uao["drone_type"] == "recon-fixed-wing":
        uao["target_x"], uao["target_y"] = random.choice([
            (120, 120), (880, 120), (880, 880), (120, 880),
            (500, 120), (880, 500), (500, 880), (120, 500)
        ])

    elif uao["drone_type"] == "loitering-munition":
        if uao["age"] > 14 and random.random() < 0.35:
            uao["mission"] = "terminal attack"
            uao["target_x"], uao["target_y"] = random_inner_target()
        else:
            uao["mission"] = "loiter"
            uao["target_x"], uao["target_y"] = random_inner_target()

    elif uao["drone_type"] == "friendly-uao":
        uao["target_x"], uao["target_y"] = random.choice([
            (200, 500), (500, 800), (800, 500), (500, 200),
            (300, 300), (700, 300), (700, 700), (300, 700)
        ])

    else:
        uao["target_x"], uao["target_y"] = random_wide_target()


def create_event(uao, dist_to_fob, threat_level, threat_score, countermeasure):
    dx = uao["target_x"] - uao["x"]
    dy = uao["target_y"] - uao["y"]

    heading = math.degrees(math.atan2(dy, dx)) % 360

    predicted_x = uao["x"] + math.cos(math.radians(heading)) * uao["speed"] * 10
    predicted_y = uao["y"] + math.sin(math.radians(heading)) * uao["speed"] * 10

    predicted_x = max(0, min(1000, predicted_x))
    predicted_y = max(0, min(1000, predicted_y))

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "drone_id": uao["drone_id"],
        "x_position_m": round(uao["x"], 2),
        "y_position_m": round(uao["y"], 2),
        "predicted_x_m": round(predicted_x, 2),
        "predicted_y_m": round(predicted_y, 2),
        "target_x_m": round(uao["target_x"], 2),
        "target_y_m": round(uao["target_y"], 2),
        "altitude_m": 0 if uao["status"] == "shot_down" else random.randint(60, 260),
        "speed_mps": 0 if uao["status"] == "shot_down" else uao["speed"],
        "heading_deg": round(heading, 1),
        "drone_type": uao["drone_type"],
        "mission": uao["mission"],
        "weather": random.choice(["clear", "rain", "fog", "dust", "wind"]),
        "friendly": uao["friendly"],
        "status": uao["status"],
        "radar_confidence": round(random.uniform(0.70, 0.98), 2),
        "rf_confidence": round(random.uniform(0.55, 0.96), 2),
        "optical_confidence": round(random.uniform(0.45, 0.94), 2),
        "acoustic_confidence": round(random.uniform(0.35, 0.88), 2),
        "distance_to_fob_m": round(dist_to_fob, 2),
        "threat_score": threat_score,
        "threat_level": threat_level,
        "countermeasure": countermeasure,
    }


def update_uao(uao):
    uao["age"] += 1

    if uao["status"] == "shot_down":
        uao["shot_down_timer"] += 1
        return create_event(
            uao,
            distance(uao["x"], uao["y"], FOB_X, FOB_Y),
            "shot_down",
            1.0,
            "target neutralized"
        )

    dx = uao["target_x"] - uao["x"]
    dy = uao["target_y"] - uao["y"]
    dist_to_target = math.sqrt(dx**2 + dy**2)

    if dist_to_target < 50:
        choose_new_target(uao)

    dx = uao["target_x"] - uao["x"]
    dy = uao["target_y"] - uao["y"]
    dist_to_target = math.sqrt(dx**2 + dy**2)

    if dist_to_target > 1:
        uao["x"] += (dx / dist_to_target) * uao["speed"] * UPDATE_SECONDS
        uao["y"] += (dy / dist_to_target) * uao["speed"] * UPDATE_SECONDS

    uao["x"] = max(0, min(1000, uao["x"]))
    uao["y"] = max(0, min(1000, uao["y"]))

    dist_to_fob = distance(uao["x"], uao["y"], FOB_X, FOB_Y)

    if not uao["friendly"] and uao["drone_type"] != "bird" and dist_to_fob <= ENGAGEMENT_DISTANCE_M:
        if random.random() < SHOOTDOWN_CHANCE:
            uao["status"] = "shot_down"
            return create_event(uao, dist_to_fob, "shot_down", 1.0, "target neutralized")
        return create_event(uao, dist_to_fob, "high", 0.97, "engagement attempted - continue tracking")

    if uao["friendly"]:
        return create_event(uao, dist_to_fob, "friendly", 0.05, "track only")

    if uao["drone_type"] == "bird":
        return create_event(uao, dist_to_fob, "low", 0.10, "ignore")

    if dist_to_fob < 180:
        return create_event(uao, dist_to_fob, "high", 0.90, "prepare countermeasure")

    if dist_to_fob < 320:
        return create_event(uao, dist_to_fob, "medium", 0.70, "monitor and warn")

    return create_event(uao, dist_to_fob, "low", 0.35, "continue tracking")


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    uaos = []
    next_uao_number = 1

    for _ in range(8):
        uaos.append(spawn_uao(next_uao_number))
        next_uao_number += 1

    with OUTPUT_FILE.open("w", newline="") as csvfile:
        writer = None

        print("SentinelAI advanced UAO simulation running. Press Ctrl+C to stop.")

        while True:
            active_count = len([u for u in uaos if u["status"] == "active"])

            if active_count < MAX_ACTIVE_UAOS and random.random() < 0.35:
                uaos.append(spawn_uao(next_uao_number))
                next_uao_number += 1

            events = []

            for uao in uaos:
                events.append(update_uao(uao))

            uaos = [
                u for u in uaos
                if not (u["status"] == "shot_down" and u["shot_down_timer"] > 5)
            ]

            for event in events:
                if writer is None:
                    writer = csv.DictWriter(csvfile, fieldnames=event.keys())
                    writer.writeheader()

                writer.writerow(event)
                print(event)

            csvfile.flush()
            time.sleep(UPDATE_SECONDS)


if __name__ == "__main__":
    main()
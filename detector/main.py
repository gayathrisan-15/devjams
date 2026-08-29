import json
import time
import paho.mqtt.client as mqtt

# ---- Simple in-memory trust score tracker ----
trust_scores = {}  # e.g. {"drone-1": 100}

def get_trust(drone_id):
    return trust_scores.get(drone_id, 100)

def penalize(drone_id, amount=20):
    trust_scores[drone_id] = max(0, get_trust(drone_id) - amount)

def reward(drone_id, amount=1):
    trust_scores[drone_id] = min(100, get_trust(drone_id) + amount)

def is_blocked(drone_id):
    return get_trust(drone_id) < 30

# ---- Keep last known position to detect "teleporting" ----
last_position = {}  # e.g. {"drone-1": (lat, lon)}

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        drone_name = data.get("drone_id", "Unknown Drone")
        battery_level = data.get("battery", 100)
        lat = data.get("lat", 0.0)
        lon = data.get("lon", 0.0)

        anomaly_found = False

        # ---- Check 1: low battery ----
        if battery_level < 10:
            print(f"⚠️ ALERT! {drone_name} battery is dangerously low!")
            anomaly_found = True

        # ---- Check 2: impossible position jump (GPS spoof) ----
        if drone_name in last_position:
            old_lat, old_lon = last_position[drone_name]
            # rough distance check — real GPS shouldn't jump this much in 2 seconds
            jump = abs(lat - old_lat) + abs(lon - old_lon)
            if jump > 1.0:  # tune this number based on your simulated movement
                print(f"🚨 ALERT! {drone_name} teleported — possible GPS spoof!")
                anomaly_found = True
        last_position[drone_name] = (lat, lon)

        # ---- Update trust score ----
        if anomaly_found:
            penalize(drone_name)
        else:
            reward(drone_name)

        blocked = is_blocked(drone_name)

        print(f"[{drone_name}] Battery: {battery_level}% | "
              f"Location: ({lat:.4f}, {lon:.4f}) | "
              f"Trust: {get_trust(drone_name)} | "
              f"{'🔴 BLOCKED' if blocked else '🟢 OK'}")

        # ---- Publish status so the dashboard can see it too ----
        status = {
            "drone_id": drone_name,
            "trust_score": get_trust(drone_name),
            "blocked": blocked,
            "anomaly": anomaly_found,
            "timestamp": time.time()
        }
        client.publish(f"devjams_gayathri_drones/{drone_name}/status", json.dumps(status))

    except Exception as e:
        print("Received malformed data:", e)


police_bot = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
police_bot.on_message = on_message
police_bot.connect("localhost", 1883, 60)  # <-- switched to local broker
topic = "devjams_gayathri_drones/+/telemetry"

police_bot.subscribe(topic)

print(f"Detector is running and listening on '{topic}'...")
police_bot.loop_forever()
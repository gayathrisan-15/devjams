import os
import json
import time
import pandas as pd
import paho.mqtt.client as mqtt
import joblib


# ============================================================
# LOAD TRAINED RANDOM FOREST MODEL
# ============================================================

# Use paths relative to this file, so it works no matter which
# folder you run the script from.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR,  "real_attack_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR,  "real_model_features.pkl")

model = joblib.load(MODEL_PATH)
model_features = joblib.load(FEATURES_PATH)

print("Random Forest model loaded successfully!")
print(f"Number of trees: {len(model.estimators_)}")
print(f"Expected features: {model_features}")


# ------------------------------------------------------------
# SAFETY CHECK: make sure our feature dict keys match exactly
# what the model expects. If they don't match, pandas will
# silently fill missing columns with NaN and the model will
# make garbage predictions without any error being raised.
# ------------------------------------------------------------

EXPECTED_FEATURE_KEYS = [
    "frame.len",
    "wlan.duration",
    "wlan.frag",
    "wlan.seq",
    "ip.hdr_len",
    "ip.len",
    "ip.ttl",
    "tcp.window_size",
    "data.len",
    "wlan.fc.type",
    "wlan.fc.subtype",
    "time_since_last_packet",
]

missing_features = [f for f in model_features if f not in EXPECTED_FEATURE_KEYS]

if missing_features:
    print(
        "⚠️  WARNING: the following model_features are NOT produced by "
        "create_ml_features() and will be filled with NaN, which will "
        "break predictions:",
        missing_features,
    )
else:
    print("✅ Feature check passed — all model_features are accounted for.")


# ============================================================
# TRUST SCORE
# ============================================================

trust_scores = {}


def get_trust(drone_id):
    return trust_scores.get(drone_id, 100)


def penalize(drone_id, amount=20):
    trust_scores[drone_id] = max(
        0,
        get_trust(drone_id) - amount
    )


def reward(drone_id, amount=1):
    trust_scores[drone_id] = min(
        100,
        get_trust(drone_id) + amount
    )


def is_blocked(drone_id):
    return get_trust(drone_id) < 30


# ============================================================
# CREATE FEATURES FOR RANDOM FOREST
# ============================================================

def create_ml_features(data, time_since_last_packet):

    features = {
        "frame.len": data.get("frame.len", 100),
        "wlan.duration": data.get("wlan.duration", 0),
        "wlan.frag": data.get("wlan.frag", 0),
        "wlan.seq": data.get("wlan.seq", 0),
        "ip.hdr_len": data.get("ip.hdr_len", 20),
        "ip.len": data.get("ip.len", 100),
        "ip.ttl": data.get("ip.ttl", 64),
        "tcp.window_size": data.get("tcp.window_size", 0),
        "data.len": data.get("data.len", 0),
        "wlan.fc.type": data.get("wlan.fc.type", 2),
        "wlan.fc.subtype": data.get("wlan.fc.subtype", 0),
        "time_since_last_packet": time_since_last_packet
    }

    return pd.DataFrame(
        [features],
        columns=model_features
    )


# ============================================================
# TRACK DRONE POSITION AND MESSAGE TIME
# ============================================================

last_position = {}
last_message_time = {}


# ============================================================
# MQTT MESSAGE HANDLER
# ============================================================

def on_message(client, userdata, msg):

    try:

        # ----------------------------------------------------
        # Read incoming MQTT message
        # ----------------------------------------------------

        data = json.loads(msg.payload.decode())

        drone_name = data.get(
            "drone_id",
            "Unknown Drone"
        )

        battery_level = data.get(
            "battery",
            100
        )

        lat = data.get(
            "lat",
            0.0
        )

        lon = data.get(
            "lon",
            0.0
        )

        anomaly_found = False

        now = time.time()


        # ====================================================
        # CALCULATE TIME BETWEEN PACKETS
        # ====================================================

        if drone_name in last_message_time:

            time_since_last_packet = (
                now - last_message_time[drone_name]
            )

        else:

            time_since_last_packet = 0

        last_message_time[drone_name] = now


        # ====================================================
        # RANDOM FOREST PREDICTION
        # ====================================================

        ml_features = create_ml_features(
            data,
            time_since_last_packet
        )

        prediction = model.predict(
            ml_features
        )[0]

        print(
            f"🌲 Random Forest prediction: {prediction}"
        )


        # ----------------------------------------------------
        # If Random Forest detects an attack
        # ----------------------------------------------------

        if str(prediction) != "0":

            print(
                f"🚨 AI DETECTED ATTACK: "
                f"{prediction} "
                f"from {drone_name}"
            )

            anomaly_found = True


        # ====================================================
        # CHECK 1 — LOW BATTERY
        # ====================================================

        if battery_level < 10:

            print(
                f"⚠️ ALERT! {drone_name} "
                f"battery is dangerously low!"
            )

            anomaly_found = True


        # ====================================================
        # CHECK 2 — GPS SPOOF / IMPOSSIBLE JUMP
        # ====================================================

        if drone_name in last_position:

            old_lat, old_lon = last_position[
                drone_name
            ]

            jump = (
                abs(lat - old_lat)
                +
                abs(lon - old_lon)
            )

            if jump > 1.0:

                print(
                    f"🚨 ALERT! {drone_name} "
                    f"teleported — possible GPS spoof!"
                )

                anomaly_found = True


        last_position[drone_name] = (
            lat,
            lon
        )


        # ====================================================
        # UPDATE TRUST SCORE
        # ====================================================

        if anomaly_found:

            penalize(drone_name)

        else:

            reward(drone_name)


        blocked = is_blocked(
            drone_name
        )


        # ====================================================
        # PRINT DRONE STATUS
        # ====================================================

        print(
            f"[{drone_name}] "
            f"Battery: {battery_level}% | "
            f"Location: ({lat:.4f}, {lon:.4f}) | "
            f"ML: {prediction} | "
            f"Trust: {get_trust(drone_name)} | "
            f"{'🔴 BLOCKED' if blocked else '🟢 OK'}"
        )


        # ====================================================
        # SEND STATUS TO DASHBOARD
        # ====================================================

        status = {

            "drone_id": drone_name,

            "trust_score": get_trust(
                drone_name
            ),

            "blocked": blocked,

            "anomaly": anomaly_found,

            "prediction": str(
                prediction
            ),

            "battery": battery_level,

            "lat": lat,

            "lon": lon,

            "timestamp": time.time()
        }


        client.publish(

            f"devjams_gayathri_drones/"
            f"{drone_name}/status",

            json.dumps(status)
        )


    except Exception as e:

        print(
            "Received malformed data:",
            e
        )


# ============================================================
# START MQTT DETECTOR
# ============================================================

police_bot = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

police_bot.on_message = on_message


# Connect to local Mosquitto broker

police_bot.connect(
    "localhost",
    1883,
    60
)


# Listen to all drone telemetry

topic = (
    "devjams_gayathri_drones/+/telemetry"
)

police_bot.subscribe(topic)


print(
    f"Detector is running and listening "
    f"on '{topic}'..."
)


# Keep detector running

police_bot.loop_forever()
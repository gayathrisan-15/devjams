import json
import time
import pandas as pd
import paho.mqtt.client as mqtt
import pydeck as pdk
import streamlit as st
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Drone Defense Command Center", layout="wide")

# Automatically refresh UI every 2 seconds to reflect new incoming telemetry
st_autorefresh(interval=2000, key="datarefresh")

# Initialize shared session state for drones & trust scores
if "drones" not in st.session_state:
    st.session_state.drones = {}

if "trust_scores" not in st.session_state:
    st.session_state.trust_scores = {}


# --- MQTT LISTENER THREAD ---
def start_mqtt_client():
    def on_message(client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            drone_id = payload.get("drone_id", "Unknown")
            lat = payload.get("lat", 0.0)
            lon = payload.get("lon", 0.0)
            battery = payload.get("battery", 100.0)

            # Check Trust Engine Logic directly inside UI thread
            prev_data = st.session_state.drones.get(drone_id, None)
            trust_score = st.session_state.trust_scores.get(drone_id, 100)
            is_isolated = trust_score < 50

            if prev_data:
                # Spoofing Check: Impossible movement distance calculation
                dlat = abs(lat - prev_data["lat"])
                dlon = abs(lon - prev_data["lon"])
                if dlat > 0.05 or dlon > 0.05:  # Sudden massive spatial jump
                    trust_score = max(0, trust_score - 40)
                    st.session_state.trust_scores[drone_id] = trust_score

            # Save state
            st.session_state.drones[drone_id] = {
                "drone_id": drone_id,
                "lat": lat,
                "lon": lon,
                "battery": battery,
                "trust_score": trust_score,
                "status": "ISOLATED 🚨" if is_isolated else "ACTIVE 🟢",
            }
        except Exception as e:
            pass

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.subscribe("devjams_gayathri_drones/#")
    client.loop_start()


if "mqtt_started" not in st.session_state:
    start_mqtt_client()
    st.session_state.mqtt_started = True

# --- HEADER & METRICS ---
st.title("🛰️ Autonomous Drone Anomaly & Security Command")
st.caption(
    "Real-time telemetry tracking, GPS spoofing detection, and automated trust score quarantine."
)

active_drones = len(st.session_state.drones)
isolated_drones = sum(
    1
    for d in st.session_state.drones.values()
    if d["status"] == "ISOLATED 🚨"
)

col1, col2, col3 = st.columns(3)
col1.metric("Connected Drones", active_drones)
col2.metric("Threat Isolation Queue", isolated_drones)
col3.metric("System Security Level", "ENFORCED", delta="ACTIVE")

st.divider()

# --- REAL-TIME MAP & TABLE DISPLAY ---
df = pd.DataFrame(st.session_state.drones.values())

if not df.empty:
    # Set map center around current active drones
    view_state = pdk.ViewState(
        latitude=df["lat"].mean(), longitude=df["lon"].mean(), zoom=13
    )

    # Color drones based on isolation status (Green = Normal, Red = Isolated)
    df["color_r"] = df["status"].apply(
        lambda x: 255 if "ISOLATED" in x else 0
    )
    df["color_g"] = df["status"].apply(
        lambda x: 0 if "ISOLATED" in x else 255
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_color=["color_r", "color_g", 0, 200],
        get_radius=150,
        pickable=True,
    )

    st.subheader("🌐 Fleet Tactical Map")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

    st.subheader("📋 Telemetry & Trust Score Matrix")
    st.dataframe(
        df[
            [
                "drone_id",
                "battery",
                "trust_score",
                "status",
                "lat",
                "lon",
            ]
        ],
        use_container_width=True,
    )
else:
    st.warning(
        "Waiting for telemetry data... Run `python drones/drone.py` in a separate terminal!"
    )
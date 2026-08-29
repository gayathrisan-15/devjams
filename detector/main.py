import json
import paho.mqtt.client as mqtt

def check_letter(client, userdata, msg):
    try:
        # Unpack the telemetry payload
        data = json.loads(msg.payload.decode())
        
        # Extract fields
        drone_name = data.get("drone_id", "Unknown Drone")
        battery_level = data.get("battery", 100)
        lat = data.get("lat", 0.0)
        lon = data.get("lon", 0.0)
        
        # Display incoming telemetry
        print(f"[{drone_name}] Battery: {battery_level}% | Location: ({lat:.4f}, {lon:.4f})")
        
        # Check for low battery anomaly
        if battery_level < 10:
            print(f"⚠️ ALERT! {drone_name} battery is dangerously low!")

    except Exception as e:
        print("Received malformed data:", e)

# Initialize MQTT Client with Callback API v2
police_bot = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set callbacks and connect to public broker
police_bot.on_message = check_letter
police_bot.connect("broker.hivemq.com", 1883, 60)

# Subscribe to your team's unique topic
topic = "devjams_gayathri_drones/#"
police_bot.subscribe(topic)

print(f" Detector is running and listening on '{topic}'...")
police_bot.loop_forever()
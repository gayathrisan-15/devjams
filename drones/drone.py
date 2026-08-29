import random
import time
import json
import paho.mqtt.client as mqtt


class Drone:
    def __init__(self, drone_id, start_lat, start_lon):
        self.id = drone_id
        self.lat = start_lat
        self.lon = start_lon
        self.battery = 100

        self.client = mqtt.Client()
        self.client.connect("localhost", 1883)

    def update(self):
        self.lat += random.uniform(-0.0005, 0.0005)
        self.lon += random.uniform(-0.0005, 0.0005)
        self.battery -= random.uniform(0.01, 0.05)

    def to_dict(self):
        return {
            "id": self.id,
            "lat": self.lat,
            "lon": self.lon,
            "battery": round(self.battery, 2),
            "timestamp": time.time()
        }

    def send(self):
        topic = f"drones/{self.id}/telemetry"
        payload = json.dumps(self.to_dict())

        self.client.publish(topic, payload)

        print(f"Sent: {payload}")


if __name__ == "__main__":
    import sys

    drone_id = sys.argv[1] if len(sys.argv) > 1 else "drone-1"

    d = Drone(drone_id, 28.6139, 77.2090)

    while True:
        d.update()
        d.send()
        time.sleep(2)
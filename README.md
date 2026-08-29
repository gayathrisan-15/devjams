
# DevJams - Real-Time Drone Anomaly Detector

A distributed IoT monitoring system built for real-time telemetry streaming and anomaly detection. Drone nodes simulate flight and battery parameters, broadcasting data over MQTT to a centralized detector service that flags low-battery warnings.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Messaging Protocol:** MQTT (via `paho-mqtt`)
* **Broker:** HiveMQ Cloud Public Broker (`broker.hivemq.com`)
* **Data Format:** JSON

---

## 📂 Project Structure

```text
devjams/
├── detector/
│   └── main.py       # MQTT subscriber & anomaly detection logic
├── drones/
│   └── drone.py      # MQTT publisher simulating drone telemetry
└── README.md

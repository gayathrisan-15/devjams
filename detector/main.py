import json
import paho.mqtt.client as mqtt

def check_letter(client, userdata, msg):
    try:
        # Unpack the letter
        data = json.loads(msg.payload.decode())
        
        # Grab the info
        drone_name = data.get("drone_id", "Unknown Drone")
        battery_level = data.get("battery", 100)
        
        # Print what came in
        print(f"[{drone_name}] Battery: {battery_level}%")
        
        # Check for anomalies
        if battery_level < 10:
            print(f"⚠️ ALERT! {drone_name} battery is dangerously low!")

    except Exception as e:
        print("Received malformed data:", e)

# Create the listener robot (CallbackAPIVersion prevents depreciation errors)
police_bot = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set up callbacks and connection
police_bot.on_message = check_letter
# Use the free online test server instead of local
police_bot.connect("broker.hivemq.com", 1883, 60)
# Change this line:
git add drones/main.py
git commit -m "Update drone script to use public broker and matching keys"
git push origin main
print("Detector is running and listening on 'drones/#'...")
police_bot.loop_forever()
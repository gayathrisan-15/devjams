import math

class SecurityEngine:
    def __init__(self, initial_trust=100):
        self.last_positions = {}
        self.trust_scores = {}
        self.initial_trust = initial_trust

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """Haversine formula to compute distance in km."""
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

    def evaluate_telemetry(self, telemetry):
        drone_id = telemetry.get("drone_id", "Unknown")
        lat = telemetry.get("lat", 0.0)
        lon = telemetry.get("lon", 0.0)
        
        # Initialize trust score if new drone
        if drone_id not in self.trust_scores:
            self.trust_scores[drone_id] = self.initial_trust

        threat_detected = False
        anomaly_type = None

        # Check for GPS Spoofing (Improbable Jump)
        if drone_id in self.last_positions:
            prev_lat, prev_lon = self.last_positions[drone_id]
            dist = self.calculate_distance(prev_lat, prev_lon, lat, lon)

            # If movement exceeds 5 km in 2 seconds -> GPS Spoofing
            if dist > 5.0:
                threat_detected = True
                anomaly_type = f"GPS Spoofing Jump ({dist:.2f} km)"
                self.trust_scores[drone_id] = max(0, self.trust_scores[drone_id] - 40)

        # Update last known position
        self.last_positions[drone_id] = (lat, lon)

        # Check quarantine status (Trust Score < 50)
        is_isolated = self.trust_scores[drone_id] < 50

        return {
            "drone_id": drone_id,
            "trust_score": self.trust_scores[drone_id],
            "threat_detected": threat_detected,
            "anomaly_type": anomaly_type,
            "is_isolated": is_isolated
        }
    
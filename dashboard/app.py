import asyncio
import random
import time
import math
import json
import hashlib
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# ==========================================
# 1. DATA MODELS & TELEMETRY DEFINITION
# ==========================================

@dataclass
class TelemetryPacket:
    drone_id: str
    timestamp: float
    seq_num: int
    x: float
    y: float
    speed: float
    battery: float
    payload_hash: str
    encrypted_payload: str

@dataclass
class DroneState:
    drone_id: str
    x: float
    y: float
    speed: float
    battery: float
    trust_score: float = 100.0
    status: str = "HEALTHY"
    last_seq_num: int = 0
    anomalies: List[str] = None

    def __post_init__(self):
        if self.anomalies is None:
            self.anomalies = []

# ==========================================
# 2. ZERO-TRUST & CYBER DEFENSE ENGINE
# ==========================================

class SecurityEngine:
    def verify_encryption_and_identity(self, packet: TelemetryPacket, state: DroneState) -> Tuple[bool, str]:
        if packet.seq_num <= state.last_seq_num:
            return False, "REPLAY_ATTACK_DETECTED"
        
        computed_hash = hashlib.sha256(packet.encrypted_payload.encode()).hexdigest()[:12]
        if packet.payload_hash != computed_hash:
            return False, "ENCRYPTION_TAMPERING_DETECTED"
            
        return True, "VERIFIED"

    def detect_anomalies(self, packet: TelemetryPacket, state: DroneState) -> List[str]:
        flags = []
        dist = math.hypot(packet.x - state.x, packet.y - state.y)
        if dist > 35.0:
            flags.append("GPS_SPOOFING")
            
        if packet.battery > state.battery + 0.2:
            flags.append("BATTERY_SPIKE_ANOMALY")

        if packet.speed > 40.0:
            flags.append("EXCESSIVE_SPEED_COMMAND")

        return flags

    def process_trust(self, state: DroneState, valid: bool, auth_msg: str, anomalies: List[str]) -> Tuple[float, str]:
        score = state.trust_score
        
        if not valid:
            score -= 40.0 if auth_msg == "REPLAY_ATTACK_DETECTED" else 50.0
                
        for a in anomalies:
            if a == "GPS_SPOOFING": score -= 35.0
            elif a == "BATTERY_SPIKE_ANOMALY": score -= 20.0
            elif a == "EXCESSIVE_SPEED_COMMAND": score -= 25.0

        if valid and not anomalies and score < 100.0:
            score = min(100.0, score + 1.5)

        score = max(0.0, score)
        status = "ISOLATED" if score < 40.0 else ("SUSPICIOUS" if score < 75.0 else "HEALTHY")
        return score, status

# ==========================================
# 3. SWARM RADAR SIMULATOR WITH TRIGGER CONTROLS
# ==========================================

class DroneSimulator:
    def __init__(self):
        self.engine = SecurityEngine()
        self.reset_swarm()

    def reset_swarm(self):
        self.drones: Dict[str, DroneState] = {
            "DR-01": DroneState("DR-01", 50.0, 110.0, 12.0, 98.0),
            "DR-03": DroneState("DR-03", -120.0, 80.0, 14.0, 95.0),
            "DR-05": DroneState("DR-05", 110.0, -140.0, 10.0, 91.0),
            "DR-06": DroneState("DR-06", 140.0, 60.0, 15.0, 88.0)
        }
        self.seq_counters = {d_id: 1 for d_id in self.drones}
        self.cycle = 0
        self.manual_attack = None

    def trigger_attack(self, attack_type: str, drone_id: str = "DR-03"):
        self.manual_attack = {"type": attack_type, "drone_id": drone_id}

    def generate_packet(self, drone_id: str) -> TelemetryPacket:
        state = self.drones[drone_id]
        seq = self.seq_counters[drone_id]
        self.seq_counters[drone_id] += 1

        angle = (self.cycle * 0.05) + (list(self.drones.keys()).index(drone_id) * (math.pi / 2))
        radius = 100.0 + random.uniform(-5, 5)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        speed = max(4.0, state.speed + random.uniform(-0.5, 0.5))
        battery = max(0.0, state.battery - 0.05)
        
        payload_str = f"ENC_DATA_{drone_id}_{seq}_{time.time()}"
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()[:12]

        if self.manual_attack and self.manual_attack["drone_id"] == drone_id:
            atk = self.manual_attack["type"]
            if atk == "GPS_SPOOF":
                x += 120.0
            elif atk == "TAMPER":
                payload_hash = "INVALID_HASH"
            elif atk == "REPLAY":
                seq = state.last_seq_num
            self.manual_attack = None

        return TelemetryPacket(drone_id, time.time(), seq, x, y, speed, battery, payload_hash, payload_str)

    async def step(self) -> dict:
        self.cycle += 1
        events = []

        for drone_id, state in self.drones.items():
            if state.status == "ISOLATED":
                events.append({
                    "type": "SYSTEM",
                    "drone_id": drone_id,
                    "message": f"Drone {drone_id} ISOLATED. Swarm mesh rerouted around threat."
                })
                continue

            packet = self.generate_packet(drone_id)
            valid, msg = self.engine.verify_encryption_and_identity(packet, state)
            anomalies = self.engine.detect_anomalies(packet, state) if valid else []
            score, status = self.engine.process_trust(state, valid, msg, anomalies)

            state.x, state.y = packet.x, packet.y
            state.speed, state.battery = packet.speed, packet.battery
            state.trust_score, state.status = score, status
            if valid: state.last_seq_num = packet.seq_num
            state.anomalies = anomalies

            if not valid:
                events.append({"type": "ATTACK", "drone_id": drone_id, "message": f"Auth Defeated: {msg}"})
            for a in anomalies:
                events.append({"type": "ATTACK", "drone_id": drone_id, "message": f"Anomaly Flagged: {a}"})
            if status == "ISOLATED":
                events.append({"type": "ISOLATION", "drone_id": drone_id, "message": f"Trust Score Critical ({score:.1f}). Node automatically isolated."})

        return {
            "drones": {d_id: asdict(s) for d_id, s in self.drones.items()},
            "events": events,
            "cycle": self.cycle
        }

sim = DroneSimulator()

# ==========================================
# 4. ENHANCED HIGH-TECH DASHBOARD INTERFACE
# ==========================================

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Autonomous Zero-Trust Drone Platform</title>
    <style>
        :root {
            --dark-bg: #04171c;
            --panel-bg: rgba(142, 198, 216, 0.12);
            --dark-blue: #092c35;
            --medium-blue: #1e5a6c;
            --cyan-accent: #54b2cf;
            --light-cyan: #8ec6d8;
            --text-main: #e2f4f9;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
        }

        html { scroll-behavior: smooth; }

        body {
            margin: 0;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            background-color: var(--dark-bg);
            color: var(--text-main);
            overflow-y: auto;
        }

        /* Continuous CSS Spin Animation for Quadcopter Rotors */
        @keyframes prop-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .rotor-blade {
            transform-origin: center;
            animation: prop-spin 0.15s linear infinite;
        }

        .rotor-left { transform-origin: 90px 87px; }
        .rotor-right { transform-origin: 410px 87px; }

        /* Navbar Styling */
        .navbar {
            background: rgba(9, 44, 53, 0.85);
            backdrop-filter: blur(16px);
            color: #ffffff;
            padding: 12px 45px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid rgba(84, 178, 207, 0.25);
            box-shadow: 0 4px 25px rgba(0,0,0,0.4);
        }

        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: 0.5px;
            color: #ffffff;
        }

        .nav-logo-svg {
            width: 42px;
            height: 24px;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .nav-logo-svg:hover { transform: scale(1.15); }

        .nav-links { display: flex; gap: 28px; font-size: 0.9rem; font-weight: 600; }
        .nav-links a { color: var(--light-cyan); text-decoration: none; transition: 0.2s; position: relative; }
        .nav-links a:hover { color: #ffffff; }
        .nav-links a::after {
            content: '';
            position: absolute;
            width: 0; height: 2px;
            bottom: -4px; left: 0;
            background-color: var(--cyan-accent);
            transition: width 0.3s ease;
        }
        .nav-links a:hover::after { width: 100%; }

        /* Hero Section with Interactive Particles & Glassmorphic Banner */
        .hero-section {
            position: relative;
            width: 100%;
            background: linear-gradient(135deg, #54b2cf 0%, #8ec6d8 50%, #3a97b4 100%);
            padding: 65px 40px 75px 40px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        #bg-canvas {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 1;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .hero-logo-container {
            width: 170px;
            height: 100px;
            margin-bottom: 12px;
            filter: drop-shadow(0 10px 15px rgba(9, 44, 53, 0.3));
            transition: transform 0.3s ease, filter 0.3s ease;
        }
        .hero-logo-container:hover {
            transform: translateY(-5px) scale(1.05);
            filter: drop-shadow(0 15px 25px rgba(9, 44, 53, 0.45));
        }

        .tag-badge {
            background: var(--dark-blue);
            color: var(--light-cyan);
            padding: 6px 18px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 1.5px;
            margin-bottom: 16px;
            border: 1px solid rgba(142, 198, 216, 0.4);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .hero-section h1 {
            margin: 0 0 12px 0;
            font-size: 3rem;
            color: var(--dark-blue);
            font-weight: 900;
            line-height: 1.15;
            letter-spacing: -0.5px;
            text-shadow: 0 2px 4px rgba(255,255,255,0.3);
        }

        .hero-section p {
            margin: 0 0 35px 0;
            font-size: 1.15rem;
            color: #062128;
            font-weight: 500;
            opacity: 0.95;
            max-width: 720px;
        }

        .hero-metrics-grid {
            width: 100%;
            max-width: 1150px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            z-index: 2;
        }

        .metric-card {
            background: rgba(9, 44, 53, 0.18);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 20px 24px;
            border: 1px solid rgba(255, 255, 255, 0.35);
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(255, 255, 255, 0.6);
            background: rgba(9, 44, 53, 0.25);
        }

        .metric-card .label { font-size: 0.78rem; text-transform: uppercase; font-weight: 800; opacity: 0.85; color: var(--dark-blue); letter-spacing: 0.5px; }
        .metric-card .value { font-size: 2.2rem; font-weight: 900; color: var(--dark-blue); margin-top: 4px; }

        /* Main Workspace Flow */
        .main-section {
            background: linear-gradient(180deg, #3a97b4 0%, #1e5a6c 35%, #04171c 100%);
            padding: 45px 40px 80px 40px;
        }

        .workspace-container {
            max-width: 1380px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.35fr 1fr;
            gap: 28px;
        }

        .panel-block {
            background: var(--panel-bg);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(142, 198, 216, 0.2);
            border-radius: 20px;
            padding: 26px;
            color: #ffffff;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
            transition: border-color 0.3s ease;
        }
        .panel-block:hover {
            border-color: rgba(142, 198, 216, 0.4);
        }

        .panel-block h3 {
            margin: 0 0 18px 0;
            font-size: 1.25rem;
            color: #ffffff;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .radar-container {
            position: relative;
            height: 470px;
            background: #020d10;
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid rgba(84, 178, 207, 0.35);
            box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
        }

        canvas#radarCanvas { display: block; width: 100%; height: 100%; }

        /* Interactive Controls Bar */
        .controls-wrapper {
            margin-top: 20px;
            background: rgba(9, 44, 53, 0.4);
            border-radius: 12px;
            padding: 16px;
            border: 1px solid rgba(84, 178, 207, 0.2);
        }

        .target-selector {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            font-size: 0.85rem;
            color: var(--light-cyan);
            font-weight: 600;
        }

        .target-selector select {
            background: var(--dark-blue);
            color: #ffffff;
            border: 1px solid rgba(142, 198, 216, 0.4);
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 700;
            outline: none;
            cursor: pointer;
        }

        .controls-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }

        .btn {
            background: var(--dark-blue);
            color: var(--light-cyan);
            border: 1px solid rgba(142, 198, 216, 0.3);
            padding: 11px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        .btn:hover {
            background: #0e3d4a;
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
        }
        .btn-danger {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border-color: rgba(239, 68, 68, 0.4);
        }
        .btn-danger:hover {
            background: var(--accent-red);
            color: #ffffff;
            border-color: var(--accent-red);
        }

        /* Tables & Console */
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px 10px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 0.88rem; color: #e2f4f9; }
        th { color: var(--light-cyan); font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px; }

        .trust-bar-bg {
            width: 100%; height: 6px;
            background: rgba(255,255,255,0.1);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 4px;
        }
        .trust-bar-fill { height: 100%; transition: width 0.3s ease; }

        .badge { padding: 4px 8px; border-radius: 6px; font-weight: 800; font-size: 0.72rem; color: #fff; letter-spacing: 0.5px; }
        .badge-HEALTHY { background: var(--accent-green); box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }
        .badge-SUSPICIOUS { background: var(--accent-yellow); box-shadow: 0 0 8px rgba(245, 158, 11, 0.4); }
        .badge-ISOLATED { background: var(--accent-red); box-shadow: 0 0 8px rgba(239, 68, 68, 0.4); }

        .console {
            background: #02090c;
            color: #bfe7f3;
            font-family: 'Consolas', 'Fira Code', monospace;
            padding: 14px;
            border-radius: 10px;
            height: 200px;
            overflow-y: auto;
            font-size: 0.8rem;
            border: 1px solid rgba(84, 178, 207, 0.25);
            box-shadow: inset 0 0 10px rgba(0,0,0,0.7);
        }
        .entry { margin-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.04); padding-bottom: 4px; display: flex; gap: 8px; }
        .entry-ATTACK { color: #fca5a5; }
        .entry-ISOLATION { color: #f87171; font-weight: bold; }
        .entry-SYSTEM { color: #93c5fd; }
    </style>
</head>
<body>

    <!-- Sticky Navigation Bar with SVG Animated Drone Logo -->
    <div class="navbar">
        <div class="nav-brand">
            <svg class="nav-logo-svg" viewBox="0 0 500 250">
                <path fill="#54b2cf" d="M 60 115 C 130 95, 370 95, 440 115 C 475 125, 475 145, 440 155 C 370 175, 130 175, 60 155 C 25 145, 25 125, 60 115 Z"/>
                <path fill="#8ec6d8" d="M 180 140 C 210 185, 290 185, 320 140 C 310 100, 190 100, 180 140 Z"/>
                <path fill="#54b2cf" d="M 210 110 C 230 85, 270 85, 290 110 Z"/>
                <rect fill="#ffffff" x="84" y="95" width="12" height="35" rx="3"/>
                <rect fill="#ffffff" x="404" y="95" width="12" height="35" rx="3"/>
                <path fill="none" stroke="#54b2cf" stroke-width="12" stroke-linecap="round" d="M 180 155 L 155 210 M 320 155 L 345 210"/>
                <g class="rotor-blade rotor-left">
                    <polygon fill="#ffffff" points="65,87 90,81 115,87 90,93"/>
                </g>
                <g class="rotor-blade rotor-right">
                    <polygon fill="#ffffff" points="385,87 410,81 435,87 410,93"/>
                </g>
            </svg>
            AERO-TRUST ZERO
        </div>
        <div class="nav-links">
            <a href="#hero">Overview</a>
            <a href="#radar">Radar Telemetry</a>
            <a href="#matrix">Swarm Matrix</a>
            <a href="#console">Security Stream</a>
        </div>
    </div>

    <!-- Interactive Hero Section -->
    <div class="hero-section" id="hero">
        <canvas id="bg-canvas"></canvas>

        <div class="hero-content">
            <div class="hero-logo-container">
                <svg viewBox="0 0 500 250" width="100%" height="100%">
                    <path fill="#092c35" d="M 60 115 C 130 95, 370 95, 440 115 C 475 125, 475 145, 440 155 C 370 175, 130 175, 60 155 C 25 145, 25 125, 60 115 Z"/>
                    <path fill="#092c35" d="M 175 135 C 205 190, 295 190, 325 135 C 315 90, 185 90, 175 135 Z"/>
                    <path fill="#092c35" d="M 205 105 C 230 80, 270 80, 295 105 Z"/>
                    <rect fill="#092c35" x="84" y="95" width="12" height="35" rx="3"/>
                    <rect fill="#092c35" x="404" y="95" width="12" height="35" rx="3"/>
                    <path fill="none" stroke="#092c35" stroke-width="14" stroke-linecap="round" d="M 180 155 L 155 210 M 320 155 L 345 210"/>
                    <path fill="none" stroke="#092c35" stroke-width="8" stroke-linecap="round" d="M 167 182 L 200 190 M 333 182 L 300 190"/>
                    <g class="rotor-blade rotor-left">
                        <polygon fill="#092c35" points="60,87 90,80 120,87 90,94"/>
                    </g>
                    <g class="rotor-blade rotor-right">
                        <polygon fill="#092c35" points="380,87 410,80 440,87 410,94"/>
                    </g>
                </svg>
            </div>

            <div class="tag-badge">SWARM DEFENSE CONTROLLER</div>
            <h1>Autonomous Zero-Trust Drone Platform</h1>
            <p>Continuous cryptographic handshake, real-time spatial anomaly defense, and automated node isolation.</p>
        </div>

        <div class="hero-metrics-grid">
            <div class="metric-card">
                <div class="label">Active Units</div>
                <div class="value" id="m-active">4 / 4</div>
            </div>
            <div class="metric-card">
                <div class="label">Isolated Threat Nodes</div>
                <div class="value" id="m-isolated" style="color: var(--accent-red);">0</div>
            </div>
            <div class="metric-card">
                <div class="label">Swarm Trust Index</div>
                <div class="value" id="m-trust">100.0%</div>
            </div>
            <div class="metric-card">
                <div class="label">Mesh Protocol</div>
                <div class="value" style="color: var(--dark-blue);">Active</div>
            </div>
        </div>
    </div>

    <!-- Main Workspace Section -->
    <div class="main-section">
        <div class="workspace-container">
            <!-- Left Panel: Radar Grid & Interactive Threat Injection -->
            <div class="panel-block" id="radar">
                <h3>Swarm Telemetry Radar Grid <span>LIVE</span></h3>
                <div class="radar-container" id="radar-box">
                    <canvas id="radarCanvas"></canvas>
                </div>

                <div class="controls-wrapper">
                    <div class="target-selector">
                        <label for="targetDrone">Target Vector Node:</label>
                        <select id="targetDrone">
                            <option value="DR-03">DR-03 (Default Target)</option>
                            <option value="DR-01">DR-01</option>
                            <option value="DR-05">DR-05</option>
                            <option value="DR-06">DR-06</option>
                        </select>
                    </div>
                    <div class="controls-grid">
                        <button class="btn btn-danger" onclick="triggerAttack('GPS_SPOOF')">Inject GPS Spoof</button>
                        <button class="btn btn-danger" onclick="triggerAttack('TAMPER')">Tamper Payload</button>
                        <button class="btn btn-danger" onclick="triggerAttack('REPLAY')">Replay Attack</button>
                        <button class="btn" onclick="resetSwarm()" style="background: var(--accent-green); color: #fff; border-color: var(--accent-green);">Reset Swarm</button>
                    </div>
                </div>
            </div>

            <!-- Right Panel: Telemetry Matrix & Event Console -->
            <div style="display: flex; flex-direction: column; gap: 28px;">
                <div class="panel-block" id="matrix">
                    <h3>Swarm Telemetry Matrix</h3>
                    <table>
                        <thead>
                            <tr><th>Drone ID</th><th>Status</th><th>Trust Score</th><th>Speed</th><th>Battery</th></tr>
                        </thead>
                        <tbody id="drone-table"></tbody>
                    </table>
                </div>

                <div class="panel-block" id="console">
                    <h3>Security Event Stream Log</h3>
                    <div class="console" id="console-box"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Interactive Hero Canvas Background Animation
        const bgCanvas = document.getElementById('bg-canvas');
        const bgCtx = bgCanvas.getContext('2d');
        let bgParticles = [];

        function resizeBgCanvas() {
            bgCanvas.width = bgCanvas.parentElement.clientWidth;
            bgCanvas.height = bgCanvas.parentElement.clientHeight;
        }
        window.addEventListener('resize', resizeBgCanvas);
        resizeBgCanvas();

        class Particle {
            constructor() {
                this.x = Math.random() * bgCanvas.width;
                this.y = Math.random() * bgCanvas.height;
                this.vx = (Math.random() - 0.5) * 0.8;
                this.vy = (Math.random() - 0.5) * 0.8;
                this.radius = Math.random() * 2 + 1;
            }
            update() {
                this.x += this.vx;
                this.y += this.vy;
                if (this.x < 0 || this.x > bgCanvas.width) this.vx *= -1;
                if (this.y < 0 || this.y > bgCanvas.height) this.vy *= -1;
            }
            draw() {
                bgCtx.beginPath();
                bgCtx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
                bgCtx.fillStyle = "rgba(9, 44, 53, 0.25)";
                bgCtx.fill();
            }
        }

        for (let i = 0; i < 40; i++) bgParticles.push(new Particle());

        function animateBg() {
            bgCtx.clearRect(0, 0, bgCanvas.width, bgCanvas.height);
            for (let i = 0; i < bgParticles.length; i++) {
                bgParticles[i].update();
                bgParticles[i].draw();
                for (let j = i + 1; j < bgParticles.length; j++) {
                    const dx = bgParticles[i].x - bgParticles[j].x;
                    const dy = bgParticles[i].y - bgParticles[j].y;
                    const dist = Math.hypot(dx, dy);
                    if (dist < 120) {
                        bgCtx.beginPath();
                        bgCtx.moveTo(bgParticles[i].x, bgParticles[i].y);
                        bgCtx.lineTo(bgParticles[j].x, bgParticles[j].y);
                        bgCtx.strokeStyle = `rgba(9, 44, 53, ${0.15 * (1 - dist / 120)})`;
                        bgCtx.lineWidth = 1;
                        bgCtx.stroke();
                    }
                }
            }
            requestAnimationFrame(animateBg);
        }
        animateBg();

        // Radar Canvas Rendering
        const canvas = document.getElementById("radarCanvas");
        const ctx = canvas.getContext("2d");
        const container = document.getElementById("radar-box");

        function resizeCanvas() {
            canvas.width = container.clientWidth;
            canvas.height = container.clientHeight;
        }
        window.addEventListener("resize", resizeCanvas);
        resizeCanvas();

        let sweepAngle = 0;
        let dronePositions = {};

        function drawRadar() {
            const width = canvas.width;
            const height = canvas.height;
            const centerX = width / 2;
            const centerY = height / 2;
            const maxRadius = Math.min(width, height) * 0.42;

            ctx.clearRect(0, 0, width, height);

            ctx.strokeStyle = "rgba(84, 178, 207, 0.12)";
            ctx.lineWidth = 1;
            const gridSize = 35;
            for (let x = 0; x < width; x += gridSize) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
            }
            for (let y = 0; y < height; y += gridSize) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
            }

            ctx.strokeStyle = "rgba(84, 178, 207, 0.35)";
            for (let r = 1; r <= 3; r++) {
                ctx.beginPath();
                ctx.arc(centerX, centerY, (maxRadius / 3) * r, 0, Math.PI * 2);
                ctx.stroke();
            }

            ctx.beginPath(); ctx.moveTo(centerX - maxRadius, centerY); ctx.lineTo(centerX + maxRadius, centerY); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(centerX, centerY - maxRadius); ctx.lineTo(centerX, centerY + maxRadius); ctx.stroke();

            sweepAngle += 0.02;
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, maxRadius, sweepAngle - 0.3, sweepAngle);
            ctx.closePath();
            ctx.fillStyle = "rgba(84, 178, 207, 0.18)";
            ctx.fill();
            ctx.restore();

            ctx.fillStyle = "#8ec6d8";
            ctx.strokeStyle = "#04171c";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.rect(centerX - 8, centerY - 8, 16, 16);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = "#ffffff";
            ctx.font = "10px monospace";
            ctx.fillText("GCS-0", centerX - 15, centerY + 24);

            for (const [id, drone] of Object.entries(dronePositions)) {
                const px = centerX + (drone.x / 200) * maxRadius;
                const py = centerY + (drone.y / 200) * maxRadius;

                if (drone.status !== "ISOLATED") {
                    ctx.strokeStyle = "rgba(142, 198, 216, 0.35)";
                    ctx.setLineDash([4, 4]);
                    ctx.beginPath();
                    ctx.moveTo(centerX, centerY);
                    ctx.lineTo(px, py);
                    ctx.stroke();
                    ctx.setLineDash([]);
                }

                const color = drone.status === "HEALTHY" ? "#10b981" : (drone.status === "SUSPICIOUS" ? "#f59e0b" : "#ef4444");
                
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(px, py, 7, 0, Math.PI * 2);
                ctx.fill();

                ctx.fillStyle = "rgba(4, 23, 28, 0.85)";
                ctx.fillRect(px - 18, py + 10, 36, 16);
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 9px monospace";
                ctx.fillText(id, px - 14, py + 22);
            }

            requestAnimationFrame(drawRadar);
        }

        drawRadar();

        // WebSocket & Data Update Stream
        const ws = new WebSocket("ws://" + location.host + "/ws");
        ws.onmessage = (evt) => {
            const data = JSON.parse(evt.data);
            dronePositions = data.drones;

            let activeCount = 0;
            let isolatedCount = 0;
            let totalTrust = 0;
            const totalDrones = Object.keys(data.drones).length;

            const tbody = document.getElementById("drone-table");
            tbody.innerHTML = "";

            for (const [id, drone] of Object.entries(data.drones)) {
                if (drone.status !== "ISOLATED") activeCount++;
                else isolatedCount++;
                totalTrust += drone.trust_score;

                const trustColor = drone.trust_score > 75 ? "#10b981" : (drone.trust_score > 40 ? "#f59e0b" : "#ef4444");

                tbody.innerHTML += `
                    <tr>
                        <td><b>${id}</b></td>
                        <td><span class="badge badge-${drone.status}">${drone.status}</span></td>
                        <td>
                            ${drone.trust_score.toFixed(1)}
                            <div class="trust-bar-bg">
                                <div class="trust-bar-fill" style="width: ${drone.trust_score}%; background: ${trustColor};"></div>
                            </div>
                        </td>
                        <td>${drone.speed.toFixed(1)} m/s</td>
                        <td>${drone.battery.toFixed(1)}%</td>
                    </tr>
                `;
            }

            document.getElementById("m-active").innerText = `${activeCount} / ${totalDrones}`;
            document.getElementById("m-isolated").innerText = isolatedCount;
            document.getElementById("m-trust").innerText = `${(totalTrust / totalDrones).toFixed(1)}%`;

            const consoleBox = document.getElementById("console-box");
            data.events.forEach(e => {
                const div = document.createElement("div");
                div.className = "entry entry-" + e.type;
                div.innerHTML = `<span>[Cycle ${data.cycle}]</span> <span>[${e.drone_id}]</span> <span>${e.message}</span>`;
                consoleBox.prepend(div);
            });
        };

        function triggerAttack(type) {
            const target = document.getElementById("targetDrone").value;
            fetch(`/api/trigger-attack?type=${type}&drone_id=${target}`, { method: 'POST' });
        }

        function resetSwarm() {
            fetch('/api/reset-swarm', { method: 'POST' });
        }
    </script>
</body>
</html>
"""

@app.get("/")
async def get_dashboard():
    return HTMLResponse(DASHBOARD_HTML)

@app.post("/api/trigger-attack")
async def trigger_attack(type: str, drone_id: str = "DR-03"):
    sim.trigger_attack(type, drone_id)
    return {"status": "ok", "attack": type, "drone_id": drone_id}

@app.post("/api/reset-swarm")
async def reset_swarm():
    sim.reset_swarm()
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await sim.step()
            await websocket.send_json(data)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
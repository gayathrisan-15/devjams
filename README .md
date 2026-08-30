# 🚁 Autonomous Disaster Intelligence & Adaptive Rescue Coordination Platform

An AI-powered drone and communication security platform designed to
support disaster-response operations when normal communication networks
are unavailable or unreliable.

The platform provides a centralized dashboard to monitor drones,
communication activity, security threats, and system events. It is
designed to help rescue teams understand the situation quickly and
coordinate operations more safely.

## 🎯 Problem Statement

During disasters such as floods, earthquakes, cyclones, and wildfires,
normal communication infrastructure can become unavailable. Rescue teams
may then have difficulty communicating with drones, sharing information,
identifying threats, and understanding what is happening across the
affected area.

This project aims to provide a secure and intelligent communication and
monitoring platform that can continue operating with limited
connectivity and help rescue authorities make faster decisions.

## 💡 Our Solution

The platform combines:

-   🚁 Drone fleet monitoring
-   📡 Secure communication and relay-node monitoring
-   🗺️ Live disaster/drone map
-   🛡️ Cyber-threat and anomaly detection
-   📊 Real-time security dashboard
-   📜 Audit and event logs
-   🤖 AI-assisted threat identification and prioritization
-   🔄 Data synchronization when connectivity is restored

## 🖥️ Frontend

The frontend is being developed using:

-   Next.js
-   React
-   TypeScript
-   Tailwind CSS

### Main Pages

  -----------------------------------------------------------------------
  Page                                Purpose
  ----------------------------------- -----------------------------------
  Dashboard                           Shows overall security status,
                                      attacks, anomalies, and important
                                      events

  Fleet                               Displays connected drones, battery
                                      levels, locations, and connection
                                      status

  Live Map                            Shows drones, relay nodes, and
                                      potential threat areas

  Security                            Displays detected security threats
                                      such as GPS spoofing, DoS/flood
                                      attacks, and battery anomalies

  Audit Logs                          Displays system and communication
                                      events in chronological order
  -----------------------------------------------------------------------

## 🔐 Security Monitoring

The platform currently focuses on detecting suspicious drone/network
behaviour such as:

### GPS Spoofing

Detects unusual or sudden changes in drone position that may indicate
manipulated GPS data.

### Flood / DoS Detection

Monitors message traffic and identifies abnormal message bursts that may
indicate a flooding or denial-of-service attempt.

### Battery Anomaly

Monitors drone battery behaviour and raises an alert when battery levels
become unusually low or behaviour appears abnormal.

### Unknown Drone Detection

Identifies drone IDs that are not part of the trusted fleet.

## 🧠 AI / Intelligent Detection

The system can use telemetry and communication data to identify
suspicious behaviour and assign appropriate severity levels.

Possible future intelligent features include:

-   Threat prioritization
-   Risk scoring
-   Anomaly classification
-   High-risk zone identification
-   Emergency-request prioritization
-   Rescue-route recommendations

## 📡 Communication Architecture

The intended system can operate through multiple communication paths:

``` text
                 ┌──────────────────┐
                 │   Rescue Team    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Frontend     │
                 │ Command Dashboard│
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Backend      │
                 │ Detection / API  │
                 └────────┬─────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Drone 1      Drone 2      Drone 3
             │            │            │
             └────────────┼────────────┘
                          ▼
                    Relay / Mesh
                       Nodes
```

When internet connectivity is unavailable, drones and relay nodes can
continue exchanging local information where the underlying communication
hardware/network supports it.

When connectivity returns, collected information can be synchronized
with the central system.

## 📁 Project Structure

``` text
project/
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── components/
│   │       │   ├── Navbar.tsx
│   │       │   └── AttacksView.tsx
│   │       │
│   │       ├── fleet/
│   │       │   └── page.tsx
│   │       │
│   │       ├── map/
│   │       │   └── page.tsx
│   │       │
│   │       ├── security/
│   │       │   └── page.tsx
│   │       │
│   │       ├── logs/
│   │       │   └── page.tsx
│   │       │
│   │       ├── page.tsx
│   │       ├── layout.tsx
│   │       └── globals.css
│   │
│   └── package.json
│
└── backend/
    └── ...
```

## 🚀 How to Run the Frontend

### 1. Open the project

Open the project folder in VS Code.

### 2. Open the terminal

Go inside the frontend folder:

``` bash
cd frontend
```

### 3. Install dependencies

``` bash
npm install
```

### 4. Start the development server

``` bash
npm run dev
```

### 5. Open the website

Open:

``` text
http://localhost:3000
```

## 🔌 Backend Integration

The backend will be integrated with the frontend after the UI is
completed.

The frontend will eventually receive real data such as:

-   Drone ID
-   GPS coordinates
-   Battery percentage
-   Connection status
-   Threat type
-   Threat severity
-   Telemetry information
-   Security events
-   Timestamps

The frontend will then replace the current demo/static values with live
backend data.


## 🎯 Hackathon MVP

For the hackathon, the minimum working prototype will demonstrate:

1.  A rescue/security command dashboard
2.  Multiple drones visible in the fleet
3.  Drone health and battery information
4.  Drone locations on a live-style map
5.  Detection of suspicious behaviour
6.  Security alerts
7.  Audit logs
8.  Backend-to-frontend data integration
9.  A clear demonstration of how the system can help rescue teams during
    communication failures

## 🌟 Future Scope

The platform can be extended with:

-   Mesh-network communication between drones
-   Edge AI for offline threat detection
-   Automatic emergency prioritization
-   Computer vision for disaster-area analysis
-   Victim/person detection
-   Dynamic rescue-route planning
-   Multi-agency coordination
-   Secure end-to-end communication
-   Blockchain-based audit trails
-   Automatic cloud synchronization
-   Predictive drone maintenance

## 👥 Team Goal

Our goal is to build a practical prototype that demonstrates how drones,
intelligent threat detection, and resilient communication can work
together to support faster and safer disaster-response operations.

------------------------------------------------------------------------


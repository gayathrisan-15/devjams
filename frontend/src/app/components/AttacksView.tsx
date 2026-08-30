"use client"

import { useState } from "react"
import {
  ShieldCheck,
  AlertTriangle,
  Radio,
  BatteryCharging,
  Activity,
  Terminal,
  RotateCcw,
  Volume2,
  VolumeX,
} from "lucide-react"

type AttackType =
  | "gps"
  | "flood"
  | "battery"
  | null

export default function AttacksView() {

  const [activeAttack, setActiveAttack] =
    useState<AttackType>(null)

  const [soundMuted, setSoundMuted] =
    useState(false)

  const [logs, setLogs] = useState<string[]>([
    "[SYSTEM] Security monitoring initialized.",
    "[SYSTEM] Zero-trust verification enabled.",
    "[SYSTEM] Waiting for telemetry events...",
  ])


  function addLog(
    message: string
  ) {

    const time =
      new Date().toLocaleTimeString()

    setLogs((previous) => [
      `[${time}] ${message}`,
      ...previous,
    ])

  }


  function triggerAttack(
    attack: AttackType
  ) {

    setActiveAttack(attack)

    if (attack === "gps") {

      addLog(
        "[CAUTION] GPS spoofing attack detected on DR-03."
      )

    }

    if (attack === "flood") {

      addLog(
        "[CAUTION] Flood / DoS attack detected on DR-02."
      )

    }

    if (attack === "battery") {

      addLog(
        "[CAUTION] Battery anomaly detected on DR-05."
      )

    }

  }


  function resetFleet() {

    setActiveAttack(null)

    setLogs([
      "[SYSTEM] Fleet reset completed.",
      "[SYSTEM] All cyber defense channels nominal.",
      "[SYSTEM] Zero-trust verification enabled.",
    ])

  }


  const gpsActive =
    activeAttack === "gps"

  const floodActive =
    activeAttack === "flood"

  const batteryActive =
    activeAttack === "battery"

  const anyAttackActive =
    activeAttack !== null


  return (

    <div className="w-full max-w-7xl mx-auto py-6 px-4 sm:px-6">

      {/* HEADER */}

      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b-2 border-white/20 pb-5">

        <div>

          <div className="text-[13px] font-bold uppercase tracking-widest text-blue-200">

            Cyber Defense & Anomaly Sentinel

          </div>

          <h1 className="text-3xl sm:text-4xl font-black tracking-tight text-white mt-1">

            Attacks & Anomaly Monitor

          </h1>

        </div>


        <div className="flex items-center gap-3 flex-wrap">

          <button
            onClick={() =>
              setSoundMuted(
                !soundMuted
              )
            }
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#203c62] hover:bg-white text-white hover:text-[#172f4d] border-2 border-white text-[13px] font-bold transition-all hover:scale-105 shadow-md"
          >

            {soundMuted ? (
              <VolumeX size={16} />
            ) : (
              <Volume2 size={16} />
            )}

            <span>

              {soundMuted
                ? "Sound Muted"
                : "Emergency Audio Alert Active"}

            </span>

          </button>


          <button
            onClick={resetFleet}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-white hover:bg-slate-200 text-[#172f4d] border-2 border-white text-[13px] font-black transition-all hover:scale-105 shadow-md"
          >

            <RotateCcw size={16} />

            <span>
              Reset Fleet
            </span>

          </button>

        </div>

      </div>


      {/* STATUS */}

      {anyAttackActive ? (

        <div className="mb-8 p-6 bg-[#7f1d1d] border-4 border-white rounded-3xl text-white shadow-2xl animate-pulse">

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">

            <div className="flex items-start gap-4">

              <div className="w-12 h-12 rounded-2xl bg-white text-[#7f1d1d] flex items-center justify-center shrink-0">

                <AlertTriangle size={28} />

              </div>


              <div>

                <div className="flex items-center gap-2.5 flex-wrap">

                  <span className="px-3 py-1 bg-white text-[#7f1d1d] font-black text-[12px] rounded-md">

                    CAUTION WARNING ACTIVE

                  </span>


                  <h3 className="text-xl sm:text-2xl font-black tracking-wide uppercase">

                    {gpsActive &&
                      "Critical: GPS Spoofing Injected"}

                    {floodActive &&
                      "Critical: Mesh Ingestion Flood Attack"}

                    {batteryActive &&
                      "Critical: Abnormal Battery Voltage Collapse"}

                  </h3>

                </div>


                <p className="text-[13px] text-red-100 mt-2 max-w-3xl leading-relaxed">

                  Defensive quarantine initiated.
                  Swarm mesh rerouting around threatened nodes.

                </p>

              </div>

            </div>


            <button
              onClick={resetFleet}
              className="px-5 py-3 bg-white text-[#7f1d1d] hover:bg-slate-200 font-black text-[13px] rounded-xl transition-all hover:scale-105 shadow-xl whitespace-nowrap"
            >

              Acknowledge & Restore

            </button>

          </div>

        </div>

      ) : (

        <div className="mb-8 p-5 bg-[#203c62] border-2 border-white rounded-2xl flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-[13px] font-bold text-white shadow-xl">

          <div className="flex items-center gap-3">

            <ShieldCheck
              size={22}
              className="text-blue-200"
            />

            <span>

              ALL CYBER DEFENSE CHANNELS NOMINAL.
              NO ACTIVE ANOMALIES DETECTED.

            </span>

          </div>


          <span className="text-blue-200">

            ZERO-TRUST VERIFICATION: ENFORCED

          </span>

        </div>

      )}


      {/* THREAT CARDS */}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">


        {/* GPS CARD */}

        <div
          className={`p-6 rounded-3xl border-2 border-white flex flex-col justify-between transition-all hover:scale-[1.02] shadow-xl ${
            gpsActive
              ? "bg-[#7f1d1d]"
              : "bg-[#203c62]"
          }`}
        >

          <div>

            <div className="flex items-center justify-between mb-4">

              <div className="flex items-center gap-2">

                <Radio size={20} />

                <h3 className="text-xl font-black">

                  GPS Spoofing Defense

                </h3>

              </div>


              <span className="px-3 py-1 text-[12px] font-black rounded-lg border-2 border-white bg-white text-[#172f4d]">

                {gpsActive
                  ? "CAUTION"
                  : "SECURE"}

              </span>

            </div>


            <p className="text-[13px] text-blue-100 mb-4 leading-relaxed">

              Monitors kinematic coordinates against
              acceleration thresholds. Flags impossible
              spatial jumps exceeding 35m in consecutive
              telemetry bursts.

            </p>


            <div className="space-y-3 text-[13px] border-t border-white/20 pt-4 mb-5">

              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Spatial Tolerance
                </span>

                <span className="font-extrabold text-white">
                  35.0 Meters
                </span>

              </div>


              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Ephemeris Cipher
                </span>

                <span className="font-extrabold text-white">
                  SHA-256 Validated
                </span>

              </div>


              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Trust Score Penalty
                </span>

                <span className="font-extrabold text-white">
                  -40.0 Points
                </span>

              </div>

            </div>

          </div>


          <button
            onClick={() =>
              triggerAttack("gps")
            }
            className="w-full py-3 px-4 rounded-xl text-[13px] font-extrabold uppercase transition-all hover:scale-105 border-2 border-white shadow-md bg-[#142844] hover:bg-white text-white hover:text-[#172f4d]"
          >

            {gpsActive
              ? "Re-Inject GPS Spoof"
              : "Simulate GPS Spoof (DR-03)"}

          </button>

        </div>


        {/* FLOOD CARD */}

        <div
          className={`p-6 rounded-3xl border-2 border-white flex flex-col justify-between transition-all hover:scale-[1.02] shadow-xl ${
            floodActive
              ? "bg-[#7f1d1d]"
              : "bg-[#203c62]"
          }`}
        >

          <div>

            <div className="flex items-center justify-between mb-4">

              <div className="flex items-center gap-2">

                <Activity size={20} />

                <h3 className="text-xl font-black">

                  Flood / DoS Sentinel

                </h3>

              </div>


              <span className="px-3 py-1 text-[12px] font-black rounded-lg border-2 border-white bg-white text-[#172f4d]">

                {floodActive
                  ? "CAUTION"
                  : "SECURE"}

              </span>

            </div>


            <p className="text-[13px] text-blue-100 mb-4 leading-relaxed">

              Detects packet volume surges, replay attempts,
              and mesh buffer saturation. Automatically
              isolates misbehaving routing nodes to maintain
              swarm throughput.

            </p>


            <div className="space-y-3 text-[13px] border-t border-white/20 pt-4 mb-5">

              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Ingest Rate Limit
                </span>

                <span className="font-extrabold text-white">
                  120 Pkts/sec
                </span>

              </div>


              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Token Bucket
                </span>

                <span className="font-extrabold text-white">
                  Active Enforced
                </span>

              </div>


              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Trust Score Penalty
                </span>

                <span className="font-extrabold text-white">
                  -35.0 Points
                </span>

              </div>

            </div>

          </div>


          <button
            onClick={() =>
              triggerAttack("flood")
            }
            className="w-full py-3 px-4 rounded-xl text-[13px] font-extrabold uppercase transition-all hover:scale-105 border-2 border-white shadow-md bg-[#142844] hover:bg-white text-white hover:text-[#172f4d]"
          >

            {floodActive
              ? "Re-Inject Flood Surge"
              : "Simulate Flood Attack (DR-02)"}

          </button>

        </div>


        {/* BATTERY CARD */}

        <div
          className={`p-6 rounded-3xl border-2 border-white flex flex-col justify-between transition-all hover:scale-[1.02] shadow-xl ${
            batteryActive
              ? "bg-[#7f1d1d]"
              : "bg-[#203c62]"
          }`}
        >

          <div>

            <div className="flex items-center justify-between mb-4">

              <div className="flex items-center gap-2">

                <BatteryCharging size={20} />

                <h3 className="text-xl font-black">

                  Battery Anomaly

                </h3>

              </div>


              <span className="px-3 py-1 text-[12px] font-black rounded-lg border-2 border-white bg-white text-[#172f4d]">

                {batteryActive
                  ? "CAUTION"
                  : "SECURE"}

              </span>

            </div>


            <p className="text-[13px] text-blue-100 mb-4 leading-relaxed">

              Monitors electrochemical decay gradients.
              Catches sudden discharge surges, phantom
              capacity reports, and executes automatic
              failsafe Return-to-Home.

            </p>


            <div className="space-y-3 text-[13px] border-t border-white/20 pt-4 mb-5">

              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Critical Threshold
                </span>

                <span className="font-extrabold text-white">
                  15.0% Capacity
                </span>

              </div>


              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Discharge Gradient
                </span>

                <span className="font-extrabold text-white">
                  Linear Check
                </span>

              </div>


              <div className="flex justify-between">

                <span className="font-semibold text-blue-200">
                  Failsafe Action
                </span>

                <span className="font-extrabold text-white">
                  Autonomous RTH
                </span>

              </div>

            </div>

          </div>


          <button
            onClick={() =>
              triggerAttack("battery")
            }
            className="w-full py-3 px-4 rounded-xl text-[13px] font-extrabold uppercase transition-all hover:scale-105 border-2 border-white shadow-md bg-[#142844] hover:bg-white text-white hover:text-[#172f4d]"
          >

            {batteryActive
              ? "Re-Inject Battery Drain"
              : "Simulate Battery Drain (DR-05)"}

          </button>

        </div>

      </div>


      {/* AUDIT LOG */}

      <div className="bg-[#203c62] border-2 border-white rounded-3xl p-6 shadow-2xl">

        <div className="flex items-center justify-between mb-4 border-b-2 border-white/20 pb-3">

          <div className="flex items-center gap-2.5">

            <Terminal
              size={20}
              className="text-blue-200"
            />

            <h3 className="text-xl sm:text-2xl font-black text-white">

              Security Audit Stream Log

            </h3>

          </div>


          <div className="text-[13px] font-bold text-blue-200">

            50 Hz Real-Time Telemetry Stream

          </div>

        </div>


        <div className="h-56 overflow-y-auto text-[13px] space-y-2.5 pr-2">

          {logs.map(
            (log, index) => (

              <div
                key={index}
                className={`p-3 rounded-2xl border-2 ${
                  log.includes("CAUTION")
                    ? "bg-[#7f1d1d] border-white text-white font-bold"
                    : "bg-[#0f243d] border-white/30 text-blue-100"
                }`}
              >

                {log}

              </div>

            )
          )}

        </div>

      </div>

    </div>

  )
}
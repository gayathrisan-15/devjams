export default function MapPage() {
  return (
    <main className="min-h-screen bg-[#0f243d] text-white p-6 sm:p-10">

      <div className="max-w-7xl mx-auto">

        <div className="border-b-2 border-white/20 pb-5 mb-8">

          <p className="text-sm uppercase tracking-widest text-blue-200 font-bold">
            Swarm Intelligence
          </p>

          <h1 className="text-4xl font-black mt-1">
            Live Drone Map
          </h1>

          <p className="text-blue-200 mt-2">
            View drones, relay nodes and detected threat zones.
          </p>

        </div>


        {/* MAP PLACEHOLDER */}

        <div className="bg-[#203c62] border-2 border-white rounded-3xl p-6">

          <div className="h-[550px] bg-[#142844] border-2 border-white/30 rounded-2xl relative overflow-hidden">

            {/* GRID */}

            <div
              className="absolute inset-0 opacity-20"
              style={{
                backgroundImage:
                  "linear-gradient(#ffffff 1px, transparent 1px), linear-gradient(90deg, #ffffff 1px, transparent 1px)",
                backgroundSize: "50px 50px",
              }}
            />

            {/* DRONES */}

            <div className="absolute top-24 left-32">
              <div className="w-5 h-5 bg-white rounded-full" />
              <p className="text-xs mt-1">DR-01</p>
            </div>


            <div className="absolute top-40 right-40">
              <div className="w-5 h-5 bg-white rounded-full" />
              <p className="text-xs mt-1">DR-02</p>
            </div>


            <div className="absolute bottom-32 left-52">
              <div className="w-5 h-5 bg-[#7f1d1d] rounded-full border-2 border-white" />
              <p className="text-xs mt-1">DR-03 ⚠️</p>
            </div>


            <div className="absolute bottom-24 right-60">
              <div className="w-5 h-5 bg-white rounded-full" />
              <p className="text-xs mt-1">DR-04</p>
            </div>


            {/* CENTER */}

            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">

              <div className="w-20 h-20 rounded-full border-2 border-white flex items-center justify-center mx-auto">
                📡
              </div>

              <p className="font-bold mt-2">
                RELAY NODE
              </p>

            </div>


            {/* MAP LABEL */}

            <div className="absolute bottom-5 left-5 bg-[#0f243d] border border-white/40 rounded-lg px-4 py-2">

              <p className="text-xs text-blue-200">
                LIVE TELEMETRY
              </p>

              <p className="font-bold">
                4 drones connected
              </p>

            </div>

          </div>

        </div>

      </div>

    </main>
  )
}
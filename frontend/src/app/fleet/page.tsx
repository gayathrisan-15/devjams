import Menu from "../components/Menu"

export default function FleetPage() {
  const drones = [
    {
      id: "DR-01",
      status: "ONLINE",
      battery: 92,
      location: "Zone A",
    },
    {
      id: "DR-02",
      status: "ONLINE",
      battery: 78,
      location: "Zone B",
    },
    {
      id: "DR-03",
      status: "WARNING",
      battery: 41,
      location: "Zone C",
    },
    {
      id: "DR-04",
      status: "ONLINE",
      battery: 86,
      location: "Zone D",
    },
  ]

  return (
    <main className="min-h-screen bg-[#0f243d] text-white p-6 sm:p-10 relative">

      {/* TOP LEFT - AEROMESH + MENU */}
      <div className="absolute top-6 left-8 z-50 flex items-center gap-4">

        {/* AEROMESH */}
        <div className="text-white text-2xl font-black tracking-wide">
          AEROMESH
        </div>

        {/* MENU */}
        <Menu />

      </div>


      <div className="max-w-7xl mx-auto pt-20">

        {/* PAGE TITLE */}
        <div className="border-b-2 border-white/20 pb-5 mb-8">

          <p className="text-sm uppercase tracking-widest text-blue-200 font-bold">
            Swarm Operations
          </p>

          <h1 className="text-4xl font-black mt-1">
            Drone Fleet
          </h1>

          <p className="text-blue-200 mt-2">
            Monitor the health and connection status of all drones.
          </p>

        </div>


        {/* SUMMARY CARDS */}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">

          <div className="bg-[#203c62] border-2 border-white rounded-2xl p-5">
            <p className="text-blue-200 text-sm">
              Total Drones
            </p>

            <h2 className="text-4xl font-black mt-2">
              4
            </h2>
          </div>


          <div className="bg-[#203c62] border-2 border-white rounded-2xl p-5">
            <p className="text-blue-200 text-sm">
              Online
            </p>

            <h2 className="text-4xl font-black mt-2">
              3
            </h2>
          </div>


          <div className="bg-[#203c62] border-2 border-white rounded-2xl p-5">
            <p className="text-blue-200 text-sm">
              Warnings
            </p>

            <h2 className="text-4xl font-black mt-2">
              1
            </h2>
          </div>


          <div className="bg-[#203c62] border-2 border-white rounded-2xl p-5">
            <p className="text-blue-200 text-sm">
              Fleet Health
            </p>

            <h2 className="text-4xl font-black mt-2">
              89%
            </h2>
          </div>

        </div>


        {/* DRONE LIST */}

        <div className="bg-[#203c62] border-2 border-white rounded-3xl p-6">

          <h2 className="text-2xl font-black mb-6">
            Active Drone Fleet
          </h2>


          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

            {drones.map((drone) => (

              <div
                key={drone.id}
                className="bg-[#142844] border-2 border-white/40 rounded-2xl p-5"
              >

                <div className="flex items-center justify-between mb-4">

                  <div>
                    <h3 className="text-xl font-black">
                      {drone.id}
                    </h3>

                    <p className="text-blue-200 text-sm">
                      {drone.location}
                    </p>
                  </div>

                  <span
                    className={`px-3 py-1 rounded-lg border-2 border-white text-xs font-black ${
                      drone.status === "WARNING"
                        ? "bg-[#7f1d1d]"
                        : "bg-[#203c62]"
                    }`}
                  >
                    {drone.status}
                  </span>

                </div>


                <div className="mb-3">

                  <div className="flex justify-between text-sm mb-1">

                    <span className="text-blue-200">
                      Battery
                    </span>

                    <span className="font-bold">
                      {drone.battery}%
                    </span>

                  </div>

                  <div className="w-full h-3 bg-[#0f243d] rounded-full overflow-hidden">

                    <div
                      className="h-full bg-white"
                      style={{
                        width: `${drone.battery}%`,
                      }}
                    />

                  </div>

                </div>


                <div className="flex justify-between text-sm mt-4">

                  <span className="text-blue-200">
                    Connection
                  </span>

                  <span className="font-bold">
                    Secure Mesh
                  </span>

                </div>

              </div>

            ))}

          </div>

        </div>

      </div>

    </main>
  )
}
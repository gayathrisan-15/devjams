export default function SecurityPage() {
  const threats = [
    {
      name: "GPS Spoofing",
      status: "SECURE",
      description: "Monitors suspicious changes in drone position.",
    },
    {
      name: "Flood / DoS",
      status: "SECURE",
      description: "Monitors abnormal network traffic and packet surges.",
    },
    {
      name: "Battery Anomaly",
      status: "SECURE",
      description: "Detects abnormal battery discharge behaviour.",
    },
  ]

  return (
    <main className="min-h-screen bg-[#0f243d] text-white p-6 sm:p-10">

      <div className="max-w-7xl mx-auto">

        <div className="border-b-2 border-white/20 pb-5 mb-8">

          <p className="text-sm uppercase tracking-widest text-blue-200 font-bold">
            Cyber Defense
          </p>

          <h1 className="text-4xl font-black mt-1">
            Security Center
          </h1>

          <p className="text-blue-200 mt-2">
            Monitor threats affecting the drone communication network.
          </p>

        </div>


        {/* SECURITY STATUS */}

        <div className="bg-[#203c62] border-2 border-white rounded-2xl p-6 mb-8">

          <div className="flex items-center justify-between">

            <div>
              <p className="text-blue-200 text-sm">
                Overall Security Status
              </p>

              <h2 className="text-3xl font-black mt-1">
                SECURE
              </h2>
            </div>

            <div className="text-4xl">
              🛡️
            </div>

          </div>

        </div>


        {/* THREATS */}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          {threats.map((threat) => (

            <div
              key={threat.name}
              className="bg-[#203c62] border-2 border-white rounded-3xl p-6"
            >

              <div className="flex justify-between items-center mb-5">

                <h2 className="text-xl font-black">
                  {threat.name}
                </h2>

                <span className="px-3 py-1 bg-[#142844] border-2 border-white rounded-lg text-xs font-black">
                  {threat.status}
                </span>

              </div>

              <p className="text-blue-100 text-sm leading-relaxed">
                {threat.description}
              </p>

            </div>

          ))}

        </div>

      </div>

    </main>
  )
}
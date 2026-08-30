export default function LogsPage() {
  const logs = [
    {
      time: "09:41:22",
      level: "INFO",
      source: "DR-01",
      message: "Telemetry packet received.",
    },
    {
      time: "09:41:20",
      level: "DEFENSE",
      source: "MESH",
      message: "Secure communication channel verified.",
    },
    {
      time: "09:40:58",
      level: "INFO",
      source: "DR-02",
      message: "Battery telemetry updated.",
    },
    {
      time: "09:40:31",
      level: "CAUTION",
      source: "DR-03",
      message: "Unusual positional movement detected.",
    },
    {
      time: "09:40:12",
      level: "INFO",
      source: "RELAY",
      message: "Mesh relay heartbeat received.",
    },
  ]

  return (
    <main className="min-h-screen bg-[#0f243d] text-white p-6 sm:p-10">

      <div className="max-w-7xl mx-auto">

        <div className="border-b-2 border-white/20 pb-5 mb-8">

          <p className="text-sm uppercase tracking-widest text-blue-200 font-bold">
            System Monitoring
          </p>

          <h1 className="text-4xl font-black mt-1">
            Security Audit Logs
          </h1>

          <p className="text-blue-200 mt-2">
            History of security and drone communication events.
          </p>

        </div>


        <div className="bg-[#203c62] border-2 border-white rounded-3xl p-6">

          <div className="flex justify-between items-center mb-5">

            <h2 className="text-2xl font-black">
              Event Stream
            </h2>

            <span className="text-blue-200 text-sm font-bold">
              REAL-TIME
            </span>

          </div>


          <div className="space-y-3">

            {logs.map((log, index) => (

              <div
                key={index}
                className={`p-4 rounded-2xl border-2 ${
                  log.level === "CAUTION"
                    ? "bg-[#7f1d1d] border-white"
                    : "bg-[#142844] border-white/30"
                }`}
              >

                <div className="flex flex-col md:flex-row md:items-center gap-3">

                  <span className="text-blue-200 text-sm">
                    [{log.time}]
                  </span>

                  <span className="px-2 py-1 bg-white text-[#172f4d] rounded-md text-xs font-black">
                    {log.level}
                  </span>

                  <span className="font-black">
                    [{log.source}]
                  </span>

                  <span>
                    {log.message}
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
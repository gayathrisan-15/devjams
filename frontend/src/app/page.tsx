import Image from "next/image"
import Menu from "./components/Menu"

export default function Home() {
  return (
    <main className="min-h-screen bg-white text-[#173d7a] relative overflow-hidden">

      {/* TOP LEFT - AEROMESH TEXT + MENU */}
      <div className="absolute top-6 left-8 z-50 flex items-center gap-4">

        {/* AEROMESH TEXT */}
        <div className="text-[#173d7a] text-2xl font-black tracking-wide">
          AEROMESH
        </div>

        {/* MENU */}
        <Menu />

      </div>


      {/* MAIN CONTENT */}
      <section className="min-h-screen relative flex items-center">

        {/* MAIN DRONE IMAGE */}
     
<div className="absolute top-[8%] right-[-2%] w-[720px] h-[520px]">

  <Image
    src="/drone.png"
    alt="AeroMesh drone"
    fill
    priority
    className="object-contain"
  />

</div>


        {/* TEXT */}
        <div className="absolute left-8 bottom-24 max-w-2xl">

          <p className="text-sm font-bold tracking-widest uppercase mb-6">
            ● Beyond-Line-of-Sight Drone Comms • 2026
          </p>

          <h1 className="text-6xl md:text-7xl font-black leading-[0.95] tracking-tight">
            One Network,
            <br />
            Zero Blind Spots.
            <br />
            <span>Airborne.</span>
          </h1>

        </div>

      </section>

    </main>
  )
}
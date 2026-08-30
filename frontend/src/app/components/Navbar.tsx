"use client"

import Link from "next/link"

export default function Navbar() {
  return (
    <nav className="w-full bg-[#142844] border-b-2 border-white/20 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">

        {/* Logo */}
        <Link
          href="/"
          className="text-white font-bold text-lg"
        >
          🛡️ DRONE CYBER DEFENSE
        </Link>

        {/* Navigation */}
        <div className="flex flex-wrap gap-2">

          <Link
            href="/"
            className="px-4 py-2 rounded-lg text-white hover:bg-white hover:text-[#142844]"
          >
            Dashboard
          </Link>

          <Link
            href="/fleet"
            className="px-4 py-2 rounded-lg text-white hover:bg-white hover:text-[#142844]"
          >
            Fleet
          </Link>

          <Link
            href="/map"
            className="px-4 py-2 rounded-lg text-white hover:bg-white hover:text-[#142844]"
          >
            Live Map
          </Link>

          <Link
            href="/security"
            className="px-4 py-2 rounded-lg text-white hover:bg-white hover:text-[#142844]"
          >
            Security
          </Link>

          <Link
            href="/logs"
            className="px-4 py-2 rounded-lg text-white hover:bg-white hover:text-[#142844]"
          >
            Audit Logs
          </Link>

        </div>
      </div>
    </nav>
  )
}
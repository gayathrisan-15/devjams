"use client"

import { useState } from "react"
import Link from "next/link"

export default function Menu() {
  const [open, setOpen] = useState(false)

  const items = [
    {
      name: "Dashboard",
      description: "Main dashboard",
      href: "/",
    },
    {
      name: "Drone Fleet",
      description: "Manage your drones",
      href: "/fleet",
    },
    {
      name: "Live Map",
      description: "Track drones",
      href: "/map",
    },
    {
      name: "Security Center",
      description: "Monitor threats",
      href: "/security",
    },
    {
      name: "Audit Logs",
      description: "System events",
      href: "/logs",
    },
  ]

  return (
    <div className="relative">

      {/* MENU BUTTON */}
      <button
        onClick={() => setOpen(!open)}
        className="bg-[#173d7a] text-white px-6 py-3 rounded-full font-bold flex items-center gap-2 hover:bg-[#123365] transition-colors"
      >
        <span className="text-lg">☰</span>
        <span>MENU</span>
      </button>


      {/* DROPDOWN MENU */}
      {open && (
        <div className="absolute left-0 top-full mt-3 w-96 bg-white rounded-3xl shadow-2xl border border-gray-200 p-4 z-50">

          {items.map((item, index) => (
            <div key={item.name}>

              <Link
                href={item.href}
                onClick={() => setOpen(false)}
                className="block px-6 py-5 rounded-xl hover:bg-gray-50 transition-colors"
              >

                <h3 className="text-xl font-bold text-[#173d7a]">
                  {item.name}
                </h3>

                <p className="text-gray-500 mt-1">
                  {item.description}
                </p>

              </Link>


              {/* THIN DIVIDER */}
              {index < items.length - 1 && (
                <div className="mx-6 border-b border-[#173d7a]/15" />
              )}

            </div>
          ))}

        </div>
      )}

    </div>
  )
}
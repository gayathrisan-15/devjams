import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "AeroMesh",
  description: "Beyond-Line-of-Sight Drone Communication Network",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
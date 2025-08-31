import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Apex - Your Confidential Companion',
  description: 'An Agentic AI Companion for Empowering Women in Indian Science & Technology',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}

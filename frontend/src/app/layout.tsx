import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'InfraFlow AI - Infrastructure Finance Intelligence Platform',
  description: 'Accelerate Energy Transition Financing with AI - The intelligent platform connecting climate finance with bankable infrastructure projects.',
  keywords: ['infrastructure finance', 'DFI', 'energy transition', 'project finance', 'AI'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}

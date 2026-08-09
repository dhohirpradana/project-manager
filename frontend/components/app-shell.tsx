"use client"

import * as React from "react"
import { usePathname } from "next/navigation"
import { Sidebar } from "@/components/sidebar"

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const isAuthPage = pathname === "/" || pathname === "/login" || pathname === "/register"

  return (
    <div className="flex min-h-screen bg-zinc-50 dark:bg-zinc-900">
      {!isAuthPage && <Sidebar />}
      <main className="flex-1">{children}</main>
    </div>
  )
}
"use client"

import * as React from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { KanbanSquare } from "lucide-react"

export default function HomePage() {
  const router = useRouter()

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 p-8">
      <div className="flex flex-col items-center gap-4 text-center">
        <KanbanSquare className="h-16 w-16" />
        <h1 className="text-4xl font-bold tracking-tight">ProjectManager</h1>
        <p className="max-w-md text-muted-foreground">
          Plan, track, and manage your projects, tasks, and timelines in one place.
        </p>
      </div>
      <div className="flex gap-4">
        <Button onClick={() => router.push("/login")}>Login</Button>
        <Button variant="outline" onClick={() => router.push("/register")}>
          Register
        </Button>
      </div>
    </div>
  )
}
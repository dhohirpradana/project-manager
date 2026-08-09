"use client"

import * as React from "react"
import { Card, CardContent } from "@/components/ui/card"

const events = [
  { date: "2024-08-12", title: "Project kickoff", project: "Website Redesign" },
  { date: "2024-08-15", title: "Design phase complete", project: "Website Redesign" },
  { date: "2024-08-20", title: "Development started", project: "Mobile App" },
  { date: "2024-08-25", title: "API integration complete", project: "API Integration" },
  { date: "2024-09-01", title: "Testing phase", project: "Mobile App" },
]

export default function TimelinePage() {
  return (
    <div className="flex flex-col gap-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Timeline</h1>
        <p className="text-muted-foreground">Project timeline and milestones</p>
      </div>
      <div className="space-y-4">
        {events.map((event, i) => (
          <div key={i} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className="flex h-10 w-10 items-center justify-center rounded-full border-2 border-zinc-900 bg-white dark:border-zinc-50 dark:bg-zinc-950">
                <div className="h-3 w-3 rounded-full bg-zinc-900 dark:bg-zinc-50" />
              </div>
              {i < events.length - 1 && <div className="w-0.5 flex-1 bg-zinc-200 dark:bg-zinc-800" />}
            </div>
            <Card className="flex-1">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">{event.title}</p>
                    <p className="text-sm text-muted-foreground">{event.project}</p>
                  </div>
                  <span className="text-sm text-muted-foreground">{event.date}</span>
                </div>
              </CardContent>
            </Card>
          </div>
        ))}
      </div>
    </div>
  )
}
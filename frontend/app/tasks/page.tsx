"use client"

import * as React from "react"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus, CheckCircle2, Circle } from "lucide-react"

const tasks = [
  { id: 1, title: "Design mockups review", status: "todo", project: "Website Redesign" },
  { id: 2, title: "Implement authentication", status: "in-progress", project: "Mobile App" },
  { id: 3, title: "Deploy staging environment", status: "todo", project: "API Integration" },
  { id: 4, title: "Write unit tests", status: "done", project: "Mobile App" },
  { id: 5, title: "Client presentation", status: "todo", project: "Website Redesign" },
]

export default function TasksPage() {
  return (
    <div className="flex flex-col gap-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Tasks</h1>
          <p className="text-muted-foreground">Manage your tasks</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Task
        </Button>
      </div>
      <div className="space-y-4">
        {tasks.map((task) => (
          <Card key={task.id}>
            <CardContent className="flex items-center justify-between p-6">
              <div className="flex items-center gap-4">
                {task.status === "done" ? (
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                ) : (
                  <Circle className="h-5 w-5 text-muted-foreground" />
                )}
                <div>
                  <p className="font-medium">{task.title}</p>
                  <p className="text-sm text-muted-foreground">{task.project}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${
                    task.status === "done"
                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100"
                      : task.status === "in-progress"
                      ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-100"
                      : "bg-zinc-100 text-zinc-800 dark:bg-zinc-800 dark:text-zinc-100"
                  }`}
                >
                  {task.status}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
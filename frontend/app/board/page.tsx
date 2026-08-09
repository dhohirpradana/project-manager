"use client"

import * as React from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"

const columns = [
  { id: "todo", title: "To Do", tasks: ["Design mockups review", "Deploy staging environment", "Client presentation"] },
  { id: "in-progress", title: "In Progress", tasks: ["Implement authentication", "API documentation"] },
  { id: "done", title: "Done", tasks: ["Write unit tests", "Setup CI/CD"] },
]

export default function BoardPage() {
  return (
    <div className="flex flex-col gap-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Board</h1>
        <p className="text-muted-foreground">Kanban board view</p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {columns.map((column) => (
          <div key={column.id} className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <h2 className="font-semibold">{column.title}</h2>
              <span className="text-sm text-muted-foreground">{column.tasks.length}</span>
            </div>
            <div className="space-y-3">
              {column.tasks.map((task, i) => (
                <Card key={i}>
                  <CardContent className="p-4">
                    <p className="text-sm">{task}</p>
                  </CardContent>
                </Card>
              ))}
              <Button variant="outline" className="w-full">
                <Plus className="mr-2 h-4 w-4" />
                Add task
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
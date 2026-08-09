"use client"

import * as React from "react"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Search as SearchIcon } from "lucide-react"

export default function SearchPage() {
  const [query, setQuery] = React.useState("")

  return (
    <div className="flex flex-col gap-6 p-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Search</h1>
        <p className="text-muted-foreground">Find projects, tasks, and more</p>
      </div>
      <div className="relative">
        <SearchIcon className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="pl-10"
        />
      </div>
      {query && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Results for "{query}"</h2>
          <Card>
            <CardContent className="p-4">
              <p className="text-sm text-muted-foreground">No results found</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
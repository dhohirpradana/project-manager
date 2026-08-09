"use client";

import { Select } from "@/components/ui/dialog";
import type { TaskStatus } from "@/lib/types";
import { setTaskStatus } from "@/lib/store";

const STATUSES: TaskStatus[] = [
  "BACKLOG",
  "TODO",
  "IN_PROGRESS",
  "BLOCKED",
  "REVIEW",
  "DONE",
  "CANCELLED",
];

export function TaskStatusSelect({
  taskId,
  value,
}: {
  taskId: number;
  value: TaskStatus;
}) {
  return (
    <Select
      value={value}
      onChange={(e) => setTaskStatus(taskId, e.target.value as TaskStatus)}
      className="h-8 w-auto text-xs"
    >
      {STATUSES.map((s) => (
        <option key={s} value={s}>
          {s}
        </option>
      ))}
    </Select>
  );
}
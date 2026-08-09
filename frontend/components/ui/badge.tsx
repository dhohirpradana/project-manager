import { cn } from "@/lib/utils";
import type { Priority, TaskStatus } from "@/lib/types";
import { getPriorityColor, getStatusColor } from "@/lib/utils";

export function Badge({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        className
      )}
    >
      {children}
    </span>
  );
}

export function StatusBadge({ status }: { status: TaskStatus }) {
  return <Badge className={getStatusColor(status)}>{status}</Badge>;
}

export function PriorityBadge({ priority }: { priority: Priority }) {
  const dot: Record<Priority, string> = {
    LOW: "bg-gray-400",
    MEDIUM: "bg-blue-500",
    HIGH: "bg-orange-500",
    URGENT: "bg-red-600",
  };
  return (
    <span className="inline-flex items-center gap-1.5 text-xs font-medium">
      <span className={cn("h-2 w-2 rounded-full", dot[priority])} />
      <span className={getPriorityColor(priority)}>{priority}</span>
    </span>
  );
}

export function ProgressBar({
  value,
  className,
}: {
  value: number;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "h-2 w-full overflow-hidden rounded-full bg-zinc-200 dark:bg-zinc-800",
        className
      )}
    >
      <div
        className="h-full rounded-full bg-zinc-900 transition-all dark:bg-zinc-100"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}
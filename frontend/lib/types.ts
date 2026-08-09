export type TaskStatus =
  | "BACKLOG"
  | "TODO"
  | "IN_PROGRESS"
  | "BLOCKED"
  | "REVIEW"
  | "DONE"
  | "CANCELLED";

export type Priority = "LOW" | "MEDIUM" | "HIGH" | "URGENT";

export type ProjectStatus =
  | "PLANNED"
  | "ACTIVE"
  | "ON_HOLD"
  | "COMPLETED"
  | "CANCELLED"
  | "ARCHIVED";

export interface User {
  id: number;
  username: string;
  full_name: string | null;
}

export interface Project {
  id: number;
  parent_id: number | null;
  name: string;
  description: string | null;
  status: ProjectStatus;
  priority: Priority;
  start_date: string | null;
  due_date: string | null;
  created_by: number;
  created_at: string;
  children: Project[];
  tasks: Task[];
}

export interface Task {
  id: number;
  project_id: number;
  parent_task_id: number | null;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: Priority;
  progress: number;
  environment: string | null;
  assignee_id: number | null;
  created_by: number;
  estimated_minutes: number | null;
  spent_minutes: number;
  start_date: string | null;
  due_date: string | null;
  completed_at: string | null;
  created_at: string;
  subtasks: Task[];
  tags: Tag[];
  // denormalized for UI (not on backend model, filled by mock)
  assignee?: User | null;
  comments?: Comment[];
  time_entries?: TimeEntry[];
  activity?: Activity[];
  attachments?: Attachment[];
}

export interface Tag {
  id: number;
  name: string;
  color: string | null;
}

export interface Comment {
  id: number;
  task_id: number;
  author_id: number;
  author?: User | null;
  content: string;
  created_at: string;
}

export interface TimeEntry {
  id: number;
  task_id: number;
  user_id: number;
  user?: User | null;
  minutes: number;
  description: string | null;
  logged_at: string;
}

export interface Activity {
  id: number;
  task_id: number;
  user_id: number;
  user?: User | null;
  action: string;
  details: string | null;
  created_at: string;
}

export interface Attachment {
  id: number;
  task_id: number;
  filename: string;
  file_size: number | null;
  mime_type: string | null;
  uploaded_at: string;
}
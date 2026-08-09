import type {
  Project,
  Task,
  User,
  Comment,
  TimeEntry,
  Activity,
  Attachment,
  TaskStatus,
} from "./types";

const users: User[] = [
  { id: 1, username: "alice", full_name: "Alice Chen" },
  { id: 2, username: "bob", full_name: "Bob Reyes" },
  { id: 3, username: "carol", full_name: "Carol Nguyen" },
  { id: 4, username: "dave", full_name: "Dave Osei" },
];

const now = Date.now();
const days = (n: number) => new Date(now + n * 86400000).toISOString();

let taskSeq = 100;
let commentSeq = 500;
let timeSeq = 600;
let activitySeq = 700;
let attachSeq = 800;

function makeTask(partial: Partial<Task> & { project_id: number }): Task {
  const id = partial.id ?? taskSeq++;
  const status = partial.status ?? "TODO";
  const canComplete = status === "DONE";
  const task: Task = {
    id,
    project_id: partial.project_id,
    parent_task_id: partial.parent_task_id ?? null,
    title: partial.title ?? "Untitled task",
    description: partial.description ?? null,
    status,
    priority: partial.priority ?? "MEDIUM",
    progress: partial.progress ?? (canComplete ? 100 : 0),
    environment: partial.environment ?? null,
    assignee_id: partial.assignee_id ?? null,
    created_by: partial.created_by ?? 1,
    estimated_minutes: partial.estimated_minutes ?? null,
    spent_minutes: partial.spent_minutes ?? 0,
    start_date: partial.start_date ?? null,
    due_date: partial.due_date ?? null,
    completed_at: canComplete ? days(0) : null,
    created_at: days(-10),
    subtasks: partial.subtasks ?? [],
    tags: partial.tags ?? [],
  };
  task.assignee = users.find((u) => u.id === task.assignee_id) ?? null;
  task.comments = partial.comments ?? [];
  task.time_entries = partial.time_entries ?? [];
  task.activity = partial.activity ?? [];
  task.attachments = partial.attachments ?? [];
  return task;
}

function comment(task_id: number, author_id: number, content: string): Comment {
  const id = commentSeq++;
  return {
    id,
    task_id,
    author_id,
    author: users.find((u) => u.id === author_id) ?? null,
    content,
    created_at: days(-2),
  };
}
function timeEntry(
  task_id: number,
  user_id: number,
  minutes: number,
  description: string
): TimeEntry {
  const id = timeSeq++;
  return {
    id,
    task_id,
    user_id,
    user: users.find((u) => u.id === user_id) ?? null,
    minutes,
    description,
    logged_at: days(-1),
  };
}
function activity(
  task_id: number,
  user_id: number,
  action: string,
  details: string | null
): Activity {
  const id = activitySeq++;
  return {
    id,
    task_id,
    user_id,
    user: users.find((u) => u.id === user_id) ?? null,
    action,
    details,
    created_at: days(-1),
  };
}
function attachment(task_id: number, filename: string, size: number): Attachment {
  const id = attachSeq++;
  return {
    id,
    task_id,
    filename,
    file_size: size,
    mime_type: filename.endsWith(".png")
      ? "image/png"
      : "application/pdf",
    uploaded_at: days(-3),
  };
}

// Subtask builders
const t101 = makeTask({
  id: 101,
  project_id: 1,
  title: "Design database schema",
  status: "DONE",
  priority: "HIGH",
  assignee_id: 1,
  estimated_minutes: 480,
  spent_minutes: 520,
  tags: [{ id: 1, name: "design", color: "#8b5cf6" }],
});
const t102 = makeTask({
  id: 102,
  project_id: 1,
  title: "Set up REST API routes",
  status: "IN_PROGRESS",
  priority: "HIGH",
  assignee_id: 2,
  estimated_minutes: 600,
  spent_minutes: 240,
  start_date: days(-3),
  due_date: days(4),
  tags: [{ id: 2, name: "backend", color: "#10b981" }],
});
const t103 = makeTask({
  id: 103,
  project_id: 1,
  title: "Implement auth flow",
  status: "BLOCKED",
  priority: "URGENT",
  assignee_id: 3,
  estimated_minutes: 300,
  spent_minutes: 90,
  due_date: days(2),
  tags: [{ id: 3, name: "security", color: "#f43f5e" }],
});
const t104 = makeTask({
  id: 104,
  project_id: 1,
  title: "Write unit tests",
  status: "BACKLOG",
  priority: "MEDIUM",
  assignee_id: 4,
  estimated_minutes: 240,
  due_date: days(10),
  tags: [{ id: 4, name: "qa", color: "#f59e0b" }],
});
const t105 = makeTask({
  id: 105,
  project_id: 1,
  title: "Deploy staging environment",
  status: "REVIEW",
  priority: "HIGH",
  assignee_id: 1,
  estimated_minutes: 120,
  spent_minutes: 45,
  due_date: days(1),
  tags: [{ id: 5, name: "devops", color: "#06b6d4" }],
});

// Wire nested data on task 102
t102.comments = [
  comment(102, 1, "Routes mostly done, need to finalize pagination."),
  comment(102, 3, "Sent review; check the error handling middleware."),
];
t102.time_entries = [
  timeEntry(102, 2, 120, "API scaffolding"),
  timeEntry(102, 2, 120, "Pagination + filters"),
];
t102.activity = [
  activity(102, 2, "STATUS_CHANGED", "TODO -> IN_PROGRESS"),
  activity(102, 3, "COMMENTED", "Sent review"),
];
t102.attachments = [
  attachment(102, "api-design.png", 204800),
  attachment(102, "endpoints.pdf", 102400),
];

// Task 101 subtask demo
const t101a = makeTask({
  id: 106,
  project_id: 1,
  parent_task_id: 101,
  title: "Normalize entities",
  status: "DONE",
  assignee_id: 1,
  estimated_minutes: 180,
  spent_minutes: 200,
});
const t101b = makeTask({
  id: 107,
  project_id: 1,
  parent_task_id: 101,
  title: "Add indexes",
  status: "DONE",
  assignee_id: 1,
  estimated_minutes: 120,
  spent_minutes: 110,
});
t101.subtasks = [t101a, t101b];

const tasks: Task[] = [t101, t102, t103, t104, t105, t101a, t101b];

const projects: Project[] = [
  {
    id: 1,
    parent_id: null,
    name: "Project Manager",
    description: "Internal project management platform.",
    status: "ACTIVE",
    priority: "HIGH",
    start_date: days(-15),
    due_date: days(20),
    created_by: 1,
    created_at: days(-20),
    children: [],
    tasks: [t101, t102, t103, t104, t105],
  },
  {
    id: 2,
    parent_id: null,
    name: "Mobile App",
    description: "iOS and Android companion app.",
    status: "ACTIVE",
    priority: "MEDIUM",
    start_date: days(-8),
    due_date: days(40),
    created_by: 2,
    created_at: days(-10),
    children: [],
    tasks: [],
  },
  {
    id: 3,
    parent_id: null,
    name: "Marketing Site",
    description: "Public marketing pages.",
    status: "PLANNED",
    priority: "LOW",
    start_date: null,
    due_date: days(60),
    created_by: 3,
    created_at: days(-5),
    children: [],
    tasks: [],
  },
];

// child project demo
const childProject: Project = {
  id: 4,
  parent_id: 2,
  name: "Android Build",
  description: "Android-specific release work.",
  status: "ON_HOLD",
  priority: "MEDIUM",
  start_date: days(-5),
  due_date: days(30),
  created_by: 2,
  created_at: days(-6),
  children: [],
  tasks: [],
};
projects[1].children = [childProject];

// Find a task helper
export function findTask(id: number): Task | undefined {
  return tasks.find((t) => t.id === id);
}

export function findProject(id: number): Project | undefined {
  return projects.find((p) => p.id === id);
}

export function collectTasks(projectList: Project[] = projects): Task[] {
  const out: Task[] = [];
  const walk = (p: Project) => {
    out.push(...p.tasks);
    p.children.forEach(walk);
  };
  projectList.forEach(walk);
  return out;
}

export function allTasks(): Task[] {
  return tasks;
}

export function allProjects(): Project[] {
  return projects;
}

export function allUsers(): User[] {
  return users;
}

export function getUser(id: number | null): User | null {
  if (!id) return null;
  return users.find((u) => u.id === id) ?? null;
}

export function isOverdue(task: Task): boolean {
  return (
    !!task.due_date &&
    task.status !== "DONE" &&
    task.status !== "CANCELLED" &&
    new Date(task.due_date).getTime() < now
  );
}

export function addComment(taskId: number, authorId: number, content: string) {
  const task = findTask(taskId);
  if (!task) return;
  task.comments = task.comments ?? [];
  task.comments.push(comment(taskId, authorId, content));
}

// Project aggregate stats
export function projectStats(p: Project) {
  const all = collectTasks([p]);
  return {
    total: all.length,
    done: all.filter((t) => t.status === "DONE").length,
    blocked: all.filter((t) => t.status === "BLOCKED").length,
    overdue: all.filter(isOverdue).length,
    inProgress: all.filter((t) => t.status === "IN_PROGRESS").length,
  };
}

export function updateTaskStatus(id: number, status: TaskStatus) {
  const task = findTask(id);
  if (!task) return;
  task.status = status;
  if (status === "DONE") {
    task.progress = 100;
    task.completed_at = new Date().toISOString();
  }
}
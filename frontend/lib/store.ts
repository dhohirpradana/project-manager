"use client";

import { useSyncExternalStore } from "react";
import type { Task, TaskStatus } from "./types";
import {
  allTasks,
  findTask,
  updateTaskStatus,
  addComment,
  allProjects,
} from "./mock-data";

let version = 0;
const listeners = new Set<() => void>();

function emit() {
  version++;
  listeners.forEach((l) => l());
}

function subscribe(l: () => void) {
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
}

function getSnapshot() {
  return version;
}

export function refresh() {
  emit();
}

export function setTaskStatus(id: number, status: TaskStatus) {
  updateTaskStatus(id, status);
  emit();
}

export function postComment(taskId: number, authorId: number, content: string) {
  addComment(taskId, authorId, content);
  emit();
}

export function useTasks(): Task[] {
  useSyncExternalStore(subscribe, getSnapshot);
  return allTasks();
}

export function useTask(id: number): Task | undefined {
  useSyncExternalStore(subscribe, getSnapshot);
  return findTask(id);
}

export function useProjects() {
  useSyncExternalStore(subscribe, getSnapshot);
  return allProjects();
}
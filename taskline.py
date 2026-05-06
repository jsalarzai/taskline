#!/usr/bin/env python3
"""Taskline: a simple CLI task manager."""

# Imports & Constants

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

TASKS_FILE = Path.home() / ".taskline.json"

# File I/O Helpers

def get_tasks_path() -> Path: # -> Path is the return type annotation that returns a `Path` object.
    """Return the path to the JSON storage file."""
    return TASKS_FILE

def load_tasks() -> List[Dict]:
    """Load tasks from file, return empty list if missing or corrupted."""
    path = get_tasks_path()
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []

def save_tasks(tasks: List[Dict]) -> None:
    """Write the task list to the JSON file."""
    path = get_tasks_path()
    # Ensure parent directory exists (though it's home)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, default=str)

# Core Task Operations
def add_task(title: str) -> None:
    """Add a new task with status 'todo' and current timestamp."""
    tasks = load_tasks()
    # Generate new ID
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1 # Generator expression
    else:
        new_id = 1

    new_task = {
        "id": new_id,
        "title": title,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added: [{new_id}] {title}")

def list_tasks() -> None:
    """Print all tasks in a simple table."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    print(f"{'ID':<5} {'Status':<8} {'Created':<20} Title")
    print("-" * 60)
    for task in tasks:
        print(
            f"{task['id']:<5} {task['status']:<8} "
            f"{task['created_at'][:19]:<20} {task['title']}"
        )

def done_task(task_id: int) -> None:
    """Mark a task as done."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["status"] == "done":
                print(f"Task {task_id} is already marked as done.")
                return
            task["status"] = "done"
            save_tasks(tasks)
            print(f"Marked task {task_id} as done.")
            return
    print(f"Error: Task with id {task_id} not found.")

def remove_task(task_id: int) -> None:
    """Remove a task by its ID."""
    tasks = load_tasks()
    initial_length = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == initial_length:
        print(f"Error: Task with id {task_id} not found.")
        return
    save_tasks(tasks)
    print(f"Removed task {task_id}.")

def clear_tasks() -> None:
    """Delete all tasks after confirmation."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks to clear.")
        return
    confirm = input("Are you sure you want to clear all tasks? (y/N): ")
    if confirm.strip().lower() in ("y", "yes"):
        save_tasks([])
        print("All tasks cleared.")
    else:
        print("Clear cancelled.")

main():

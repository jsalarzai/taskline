#!/usr/bin/env python3
"""Taskline: a simple CLI task manager."""

# Imports & Constants

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path.home() / ".taskline.json"

# File I/O Helpers


def load_tasks() -> list[dict]:
    """Load tasks from file, return empty list if missing or corrupted."""
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: Could not read tasks from {TASKS_FILE}: {e}", file=sys.stderr)
        print(
            "To prevent data loss, no changes will be saved. Please fix the file manually.",
            file=sys.stderr,
        )
        sys.exit(1)  # stops the program before any save happens
        # return []


def save_tasks(tasks: list[dict]) -> None:
    """Write the task list to the JSON file."""
    # Ensure parent directory exists (though it's home)
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


# Core Task Operations
def add_task(title: str) -> None:
    """Add a new task with status 'todo' and current timestamp."""
    tasks = load_tasks()
    # Generate new ID
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1  # Generator expression
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
    print(f"Error: Task with id {task_id} not found.", file=sys.stderr)
    sys.exit(1)


def remove_task(task_id: int) -> None:
    """Remove a task by its ID."""
    tasks = load_tasks()
    initial_length = len(tasks)
    tasks = [t for t in tasks if t["id"] != task_id]
    if len(tasks) == initial_length:
        print(f"Error: Task with id {task_id} not found.", file=sys.stderr)
        sys.exit(1)
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


def main() -> None:
    """Parse command-line arguments and run the appropriate function."""
    parser = argparse.ArgumentParser(
        description="Taskline – A simple CLI task manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("title", nargs="+", help="Title of the task")

    # list
    subparsers.add_parser("list", help="List all tasks")

    # done
    parser_done = subparsers.add_parser("done", help="Mark a task as done")
    parser_done.add_argument("id", type=int, help="Task ID to mark as done")

    # remove
    parser_remove = subparsers.add_parser("remove", help="Remove a task")
    parser_remove.add_argument("id", type=int, help="Task ID to remove")

    # clear
    subparsers.add_parser("clear", help="Clear all tasks")

    args = parser.parse_args()

    if args.command == "add":
        title = " ".join(args.title)  # re-join multi-word title
        add_task(title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        done_task(args.id)
    elif args.command == "remove":
        remove_task(args.id)
    elif args.command == "clear":
        clear_tasks()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

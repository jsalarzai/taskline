import sys
from datetime import UTC, datetime

from taskline.models import Status, Task
from taskline.storage import load_tasks, save_tasks


def add_task(title: str) -> None:
    """Add a new task with status 'todo' and current timestamp."""
    tasks = load_tasks()
    # Generate new ID

    new_id = max((t.id for t in tasks), default=0) + 1

    new_task = Task(
        id=new_id,
        title=title,
        status=Status.TODO,
        created_at=datetime.now(UTC).isoformat(),  # Timezone-aware UTC!
    )
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
            f"{task.id:<5} {task.status.value:<8} {task.created_at[:19]:<20} {task.title}"
        )


def done_task(task_id: int) -> None:
    """Mark a task as done."""
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            if task.status == Status.DONE:
                print(f"Task {task_id} is already marked as done.")
                return
            task.status = Status.DONE
            save_tasks(tasks)
            print(f"Marked task {task_id} as done.")
            return
    print(f"Error: Task with id {task_id} not found.", file=sys.stderr)
    sys.exit(1)


def remove_task(task_id: int) -> None:
    """Remove a task by its ID."""
    tasks = load_tasks()
    initial_length = len(tasks)
    tasks = [t for t in tasks if t.id != task_id]
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

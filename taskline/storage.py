import json
import sys
from pathlib import Path

from taskline.models import Task

TASKS_FILE = Path.home() / ".taskline.json"


def load_tasks() -> list[Task]:
    """Load tasks from file, return empty list if missing or corrupted."""
    if not TASKS_FILE.exists():
        return []
    try:
        with open(TASKS_FILE, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [Task.from_dict(item) for item in data]
            return []
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: Could not read tasks from {TASKS_FILE}: {e}", file=sys.stderr)
        print(
            "To prevent data loss, no changes will be saved. Please fix the file manually.",
            file=sys.stderr,
        )
        sys.exit(1)  # stops the program before any save happens


def save_tasks(tasks: list[Task]) -> None:
    """Write the task list to the JSON file."""
    # Ensure parent directory exists (though it's home)
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=2)

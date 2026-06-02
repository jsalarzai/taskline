import argparse
import sys

from taskline.api import TodoFetchError
from taskline.commands import (
    TaskNotFoundError,
    add_task,
    clear_tasks,
    done_task,
    import_todos,
    list_tasks,
    remove_task,
)


def main() -> None:
    """Parse command-line arguments and run the appropriate function."""
    parser = argparse.ArgumentParser(
        description="Taskline – A simple CLI task manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    parser_add = subparsers.add_parser("add", help="Add a new task")
    parser_add.add_argument("title", nargs="+", help="Title of the task")
    parser_add.set_defaults(func=lambda args: add_task(" ".join(args.title)))

    # list
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=lambda args: list_tasks())

    # done
    parser_done = subparsers.add_parser("done", help="Mark a task as done")
    parser_done.add_argument("id", type=int, help="Task ID to mark as done")
    parser_done.set_defaults(func=lambda args: done_task(args.id))

    # remove
    parser_remove = subparsers.add_parser("remove", help="Remove a task")
    parser_remove.add_argument("id", type=int, help="Task ID to remove")
    parser_remove.set_defaults(func=lambda args: remove_task(args.id))

    # clear
    clear_parser = subparsers.add_parser("clear", help="Clear all tasks")
    clear_parser.set_defaults(func=lambda args: clear_tasks())

    # import
    parser_import = subparsers.add_parser(
        "import", help="Import todos from JSONPlaceholder"
    )
    parser_import.add_argument(
        "--limit", type=int, default=5, help="Number of todos to import"
    )
    parser_import.set_defaults(func=lambda args: import_todos(args.limit))

    args = parser.parse_args()
    try:
        args.func(args)
    except TodoFetchError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except TaskNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

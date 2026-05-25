import argparse

from taskline.commands import add_task, clear_tasks, done_task, list_tasks, remove_task


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

    args = parser.parse_args()

    args.func(args)

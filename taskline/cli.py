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

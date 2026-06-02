import pytest

from taskline.commands import TaskNotFoundError, add_task, done_task, remove_task
from taskline.storage import load_tasks


def test_add_task_adds_task_with_id_1(task_file):
    add_task("Buy milk")

    tasks = load_tasks()

    assert len(tasks) == 1
    assert tasks[0].id == 1
    assert tasks[0].title == "Buy milk"


def test_add_task_twice_produces_ids_1_and_2(task_file):
    add_task("Buy milk")
    add_task("Walk the dog")

    tasks = load_tasks()

    assert len(tasks) == 2
    assert tasks[0].id == 1
    assert tasks[1].id == 2


def test_done_task_raises_when_task_not_found(task_file):
    with pytest.raises(TaskNotFoundError, match="not found"):
        done_task(999)


def test_remove_task_removes_existing_task(task_file):
    add_task("Buy milk")

    remove_task(1)

    assert load_tasks() == []

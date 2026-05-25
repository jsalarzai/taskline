import json

import pytest

from taskline import storage
from taskline.models import Status, Task


def test_load_returns_empty_list_when_file_missing(task_file):
    assert storage.load_tasks() == []


def test_round_trip_save_and_load(task_file):
    # arrange — create a task
    task = Task(
        id=1,
        title="Buy milk",
        status=Status.TODO,
        created_at="2026-05-21T10:00:00+00:00",
    )

    # act — save then load
    storage.save_tasks([task])
    result = storage.load_tasks()

    # assert — what came back equals what went in
    assert result == [task]


def test_save_tasks_writes_valid_json(task_file):

    task = Task(
        id=1,
        title="Buy milk",
        status=Status.TODO,
        created_at="2026-05-21T10:00:00+00:00",
    )

    storage.save_tasks([task])

    with open(task_file) as f:
        data = json.load(f)

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Buy milk"


def test_load_tasks_exits_on_invalid_json(task_file):
    task_file.write_text("not json")

    with pytest.raises(SystemExit) as exc_info:
        storage.load_tasks()

    assert exc_info.value.code == 1


@pytest.mark.parametrize("content", ["null", "{}"])
def test_load_tasks_returns_empty_list_for_non_list_json(task_file, content):
    task_file.write_text(content)
    assert storage.load_tasks() == []

import pytest

from taskline.models import Status, Task


def test_from_dict_creates_task_with_correct_fields():
    data = {
        "id": 1,
        "title": "Buy milk",
        "status": "todo",
        "created_at": "2026-05-21T10:00:00+00:00",
    }

    task = Task.from_dict(data)

    assert task.id == 1
    assert task.title == "Buy milk"
    assert task.status == Status.TODO
    assert task.created_at == "2026-05-21T10:00:00+00:00"


def test_from_dict_converts_done_string_to_status_done():
    data = {
        "id": 1,
        "title": "Buy milk",
        "status": "done",
        "created_at": "2026-05-21T10:00:00+00:00",
    }

    task = Task.from_dict(data)

    assert task.status == Status.DONE


def test_to_dict_returns_all_expected_keys():
    task = Task(
        id=1,
        title="Buy milk",
        status=Status.TODO,
        created_at="2026-05-21T10:00:00+00:00",
    )
    result = task.to_dict()
    assert set(result.keys()) == {"id", "title", "status", "created_at"}


def test_to_dict_returns_status_as_string():
    task = Task(
        id=1,
        title="Buy milk",
        status=Status.TODO,
        created_at="2026-05-21T10:00:00+00:00",
    )
    result = task.to_dict()
    assert result["status"] == "todo"


def test_round_trip_from_dict_and_to_dict():
    original = Task(
        id=1,
        title="Buy milk",
        status=Status.TODO,
        created_at="2026-05-21T10:00:00+00:00",
    )
    assert Task.from_dict(original.to_dict()) == original


def test_from_dict_raises_value_error_for_invalid_status():
    data = {
        "id": 1,
        "title": "Buy milk",
        "status": "invalid",
        "created_at": "2026-05-21T10:00:00+00:00",
    }

    with pytest.raises(ValueError):
        Task.from_dict(data)

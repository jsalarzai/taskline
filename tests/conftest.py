import pytest

from taskline import storage


@pytest.fixture
def task_file(tmp_path, monkeypatch):
    path = tmp_path / "tasks.json"
    monkeypatch.setattr(storage, "TASKS_FILE", path)
    return path

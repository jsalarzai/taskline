import pytest
import requests
import requests_mock

from taskline.api import BASE_URL, TodoFetchError, fetch_todo, fetch_todos


def test_fetch_todo_success():
    """fetch_todo returns parsed dict on 200."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://jsonplaceholder.typicode.com/todos/1",
            json={"userId": 1, "id": 1, "title": "Test todo", "completed": False},
            status_code=200,
        )
        session = requests.Session()
        result = fetch_todo(session, 1)
        assert result["id"] == 1
        assert result["title"] == "Test todo"


def test_fetch_todo_404():
    """fetch_todo raises TodoFetchError on 404."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://jsonplaceholder.typicode.com/todos/999",
            status_code=404,
        )
        session = requests.Session()
        with pytest.raises(TodoFetchError):
            fetch_todo(session, 999)


def test_fetch_todo_timeout():
    """fetch_todo raises TodoFetchError on timeout."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://jsonplaceholder.typicode.com/todos/1",
            exc=requests.Timeout,
        )
        session = requests.Session()
        with pytest.raises(TodoFetchError):
            fetch_todo(session, 1)


def test_fetch_todos_limit():
    """fetch_todos returns only limit number of items."""
    with requests_mock.Mocker() as m:
        m.get(
            f"{BASE_URL}/todos",
            json=[
                {"id": i, "title": f"Todo {i}", "userId": 1, "completed": False}
                for i in range(1, 21)
            ],
        )
        session = requests.Session()
        result = fetch_todos(session, 5)
        assert len(result) == 5

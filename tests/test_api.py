import pytest
import requests
import requests_mock as requests_mock_lib

from taskline.api import TodoFetchError, fetch_todo


def test_fetch_todo_success():
    """fetch_todo returns parsed dict on 200."""
    with requests_mock_lib.Mocker() as m:
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
    with requests_mock_lib.Mocker() as m:
        m.get(
            "https://jsonplaceholder.typicode.com/todos/999",
            status_code=404,
        )
        session = requests.Session()
        with pytest.raises(TodoFetchError):
            fetch_todo(session, 999)


def test_fetch_todo_timeout():
    """fetch_todo raises TodoFetchError on timeout."""
    with requests_mock_lib.Mocker() as m:
        m.get(
            "https://jsonplaceholder.typicode.com/todos/1",
            exc=requests.Timeout,
        )
        session = requests.Session()
        with pytest.raises(TodoFetchError):
            fetch_todo(session, 1)

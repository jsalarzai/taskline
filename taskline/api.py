from typing import Any

import requests

from taskline.errors import TodoFetchError

BASE_URL = "https://jsonplaceholder.typicode.com"


def _get_json(session: requests.Session, url: str, context: str) -> Any:
    """GET url, return parsed JSON, wrap network errors as TodoFetchError."""
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as e:
        raise TodoFetchError(f"Timeout {context}") from e
    except requests.ConnectionError as e:
        raise TodoFetchError(f"Connection error {context}") from e
    except requests.HTTPError as e:
        raise TodoFetchError(f"Bad response {context}: {e}") from e
    except requests.RequestException as e:
        raise TodoFetchError(f"Request error {context}: {e}") from e


def fetch_todo(session: requests.Session, todo_id: int) -> dict[str, Any]:
    return _get_json(
        session,
        f"{BASE_URL}/todos/{todo_id}",
        f"fetching todo {todo_id}",
    )


def fetch_todos(session: requests.Session, limit: int) -> list[dict[str, Any]]:
    data = _get_json(session, f"{BASE_URL}/todos", "fetching todos")
    return data[:limit]

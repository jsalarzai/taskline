import requests


class TodoFetchError(Exception):
    pass


def fetch_todo(session: requests.Session, todo_id: int) -> dict:
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.Timeout as e:
        raise TodoFetchError(f"Request timed out for todo {todo_id}") from e
    except requests.ConnectionError as e:
        raise TodoFetchError(f"Could not reach server for todo {todo_id}") from e
    except requests.HTTPError as e:
        raise TodoFetchError(f"Bad response for todo {todo_id}: {e}") from e
    except requests.RequestException as e:
        raise TodoFetchError(f"Unexpected request error: {e}") from e


def fetch_todos(session: requests.Session, limit: int) -> list[dict]:
    url = "https://jsonplaceholder.typicode.com/todos"
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()[:limit]  # slice to limit
    except requests.Timeout as e:
        raise TodoFetchError("Request timed out fetching todos") from e
    except requests.ConnectionError as e:
        raise TodoFetchError("Could not reach server") from e
    except requests.HTTPError as e:
        raise TodoFetchError(f"Bad response: {e}") from e
    except requests.RequestException as e:
        raise TodoFetchError(f"Unexpected error: {e}") from e

from dataclasses import dataclass
from enum import StrEnum


class Status(StrEnum):
    TODO = "todo"
    DONE = "done"


# Models
@dataclass
class Task:
    id: int
    title: str
    status: Status
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            status=Status(data["status"]),
            created_at=data["created_at"],
        )

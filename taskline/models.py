from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class Status(StrEnum):
    TODO = "todo"
    DONE = "done"


@dataclass
class Task:
    id: int
    title: str
    status: Status
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            status=Status(data["status"]),
            created_at=data["created_at"],
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

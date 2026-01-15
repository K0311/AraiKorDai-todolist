"""Data models for the to-do list application."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class Priority(str, Enum):
    """Priority levels for todo items."""

    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(str, Enum):
    """Status of todo items."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    """Represents a single todo item."""

    title: str
    details: str
    priority: Priority
    status: Status
    owner: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert TodoItem to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority.value,
            "status": self.status.value,
            "owner": self.owner,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create a TodoItem from a dictionary (e.g., from JSON)."""
        return cls(
            id=data["id"],
            title=data["title"],
            details=data["details"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            owner=data["owner"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

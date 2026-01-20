"""Unit tests for the models module."""

import pytest
from datetime import datetime
from src.models import TodoItem, Priority, Status


class TestPriority:
    """Test the Priority enum."""

    def test_priority_high(self):
        """Test that Priority.HIGH is correctly defined."""
        assert Priority.HIGH.value == "HIGH"

    def test_priority_mid(self):
        """Test that Priority.MID is correctly defined."""
        assert Priority.MID.value == "MID"

    def test_priority_low(self):
        """Test that Priority.LOW is correctly defined."""
        assert Priority.LOW.value == "LOW"

    def test_priority_from_string(self):
        """Test creating Priority enum from string values."""
        assert Priority("HIGH") == Priority.HIGH
        assert Priority("MID") == Priority.MID
        assert Priority("LOW") == Priority.LOW

    def test_priority_invalid_value(self):
        """Test that invalid priority values raise ValueError."""
        with pytest.raises(ValueError):
            Priority("INVALID")

    def test_priority_is_string_enum(self):
        """Test that Priority is a string enum."""
        assert isinstance(Priority.HIGH, str)
        assert Priority.HIGH == "HIGH"


class TestStatus:
    """Test the Status enum."""

    def test_status_pending(self):
        """Test that Status.PENDING is correctly defined."""
        assert Status.PENDING.value == "PENDING"

    def test_status_completed(self):
        """Test that Status.COMPLETED is correctly defined."""
        assert Status.COMPLETED.value == "COMPLETED"

    def test_status_from_string(self):
        """Test creating Status enum from string values."""
        assert Status("PENDING") == Status.PENDING
        assert Status("COMPLETED") == Status.COMPLETED

    def test_status_invalid_value(self):
        """Test that invalid status values raise ValueError."""
        with pytest.raises(ValueError):
            Status("INVALID")

    def test_status_is_string_enum(self):
        """Test that Status is a string enum."""
        assert isinstance(Status.PENDING, str)
        assert Status.PENDING == "PENDING"


class TestTodoItem:
    """Test the TodoItem dataclass."""

    @pytest.fixture
    def sample_todo(self):
        """Create a sample TodoItem for testing."""
        return TodoItem(
            title="Test Task",
            details="This is a test task",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )

    def test_todo_item_creation(self, sample_todo):
        """Test creating a TodoItem with all fields."""
        assert sample_todo.title == "Test Task"
        assert sample_todo.details == "This is a test task"
        assert sample_todo.priority == Priority.HIGH
        assert sample_todo.status == Status.PENDING
        assert sample_todo.owner == "testuser"

    def test_todo_item_auto_generated_fields(self, sample_todo):
        """Test that id and timestamps are auto-generated."""
        assert sample_todo.id is not None
        assert len(sample_todo.id) == 36  # UUID4 format with hyphens
        assert sample_todo.created_at is not None
        assert sample_todo.updated_at is not None

    def test_todo_item_created_updated_timestamps(self, sample_todo):
        """Test that created_at and updated_at are ISO format strings."""
        # Verify ISO format
        assert "T" in sample_todo.created_at
        assert "T" in sample_todo.updated_at

    def test_todo_item_due_date_optional(self):
        """Test that due_date is optional and defaults to None."""
        todo = TodoItem(
            title="Test",
            details="Test",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="testuser",
        )
        assert todo.due_date is None

    def test_todo_item_with_due_date(self):
        """Test creating a TodoItem with a due date."""
        due_date = "2025-12-31T23:59:59"
        todo = TodoItem(
            title="Test",
            details="Test",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
            due_date=due_date,
        )
        assert todo.due_date == due_date

    def test_todo_item_with_custom_id(self):
        """Test creating a TodoItem with a custom ID."""
        custom_id = "custom-id-12345"
        todo = TodoItem(
            id=custom_id,
            title="Test",
            details="Test",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )
        assert todo.id == custom_id

    def test_todo_item_to_dict(self, sample_todo):
        """Test converting TodoItem to dictionary."""
        todo_dict = sample_todo.to_dict()
        assert isinstance(todo_dict, dict)
        assert todo_dict["title"] == "Test Task"
        assert todo_dict["details"] == "This is a test task"
        assert todo_dict["priority"] == "HIGH"
        assert todo_dict["status"] == "PENDING"
        assert todo_dict["owner"] == "testuser"
        assert todo_dict["id"] == sample_todo.id
        assert todo_dict["created_at"] == sample_todo.created_at
        assert todo_dict["updated_at"] == sample_todo.updated_at

    def test_todo_item_to_dict_with_due_date(self):
        """Test converting TodoItem with due_date to dictionary."""
        todo = TodoItem(
            title="Test",
            details="Test",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="testuser",
            due_date="2025-12-31",
        )
        todo_dict = todo.to_dict()
        assert todo_dict["due_date"] == "2025-12-31"

    def test_todo_item_from_dict(self):
        """Test creating TodoItem from dictionary."""
        data = {
            "id": "test-id-123",
            "title": "Test Task",
            "details": "Test details",
            "priority": "HIGH",
            "status": "PENDING",
            "owner": "testuser",
            "created_at": "2025-01-20T10:00:00",
            "updated_at": "2025-01-20T10:00:00",
            "due_date": "2025-12-31",
        }
        todo = TodoItem.from_dict(data)
        assert todo.id == "test-id-123"
        assert todo.title == "Test Task"
        assert todo.details == "Test details"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.PENDING
        assert todo.owner == "testuser"
        assert todo.created_at == "2025-01-20T10:00:00"
        assert todo.updated_at == "2025-01-20T10:00:00"
        assert todo.due_date == "2025-12-31"

    def test_todo_item_from_dict_without_due_date(self):
        """Test creating TodoItem from dictionary without due_date."""
        data = {
            "id": "test-id-123",
            "title": "Test Task",
            "details": "Test details",
            "priority": "MID",
            "status": "COMPLETED",
            "owner": "testuser",
            "created_at": "2025-01-20T10:00:00",
            "updated_at": "2025-01-20T10:00:00",
        }
        todo = TodoItem.from_dict(data)
        assert todo.due_date is None

    def test_todo_item_round_trip_serialization(self, sample_todo):
        """Test that TodoItem can be converted to dict and back without losing data."""
        todo_dict = sample_todo.to_dict()
        restored_todo = TodoItem.from_dict(todo_dict)
        assert restored_todo.id == sample_todo.id
        assert restored_todo.title == sample_todo.title
        assert restored_todo.details == sample_todo.details
        assert restored_todo.priority == sample_todo.priority
        assert restored_todo.status == sample_todo.status
        assert restored_todo.owner == sample_todo.owner
        assert restored_todo.created_at == sample_todo.created_at
        assert restored_todo.updated_at == sample_todo.updated_at

    def test_todo_item_all_priority_levels(self):
        """Test TodoItem creation with all priority levels."""
        for priority in [Priority.HIGH, Priority.MID, Priority.LOW]:
            todo = TodoItem(
                title="Test",
                details="Test",
                priority=priority,
                status=Status.PENDING,
                owner="testuser",
            )
            assert todo.priority == priority

    def test_todo_item_all_status_levels(self):
        """Test TodoItem creation with all status levels."""
        for status in [Status.PENDING, Status.COMPLETED]:
            todo = TodoItem(
                title="Test",
                details="Test",
                priority=Priority.HIGH,
                status=status,
                owner="testuser",
            )
            assert todo.status == status

    def test_todo_item_unique_ids(self):
        """Test that auto-generated IDs are unique."""
        todo1 = TodoItem(
            title="Test1",
            details="Test",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="user1",
        )
        todo2 = TodoItem(
            title="Test2",
            details="Test",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="user2",
        )
        assert todo1.id != todo2.id

    def test_todo_item_from_dict_with_enum_conversion(self):
        """Test that from_dict properly converts string enums to Enum objects."""
        data = {
            "id": "test-id",
            "title": "Test",
            "details": "Test",
            "priority": "LOW",
            "status": "COMPLETED",
            "owner": "user",
            "created_at": "2025-01-20T10:00:00",
            "updated_at": "2025-01-20T10:00:00",
        }
        todo = TodoItem.from_dict(data)
        assert isinstance(todo.priority, Priority)
        assert isinstance(todo.status, Status)
        assert todo.priority == Priority.LOW
        assert todo.status == Status.COMPLETED

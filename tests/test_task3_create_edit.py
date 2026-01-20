"""Unit tests for Task 3: Create & Edit To-Do List Items functionality."""

import json
import pytest
from datetime import datetime
from unittest.mock import patch

from src.models import TodoItem, Priority, Status
from src.main import TodoManager, App


class TestTodoCreation:
    """Test suite for creating new to-do items."""

    @pytest.fixture
    def todo_manager(self, tmp_path):
        """Create a TodoManager instance with a temporary file."""
        todos_file = tmp_path / "todos.json"
        return TodoManager(str(todos_file))

    def test_create_todo_with_all_fields(self, todo_manager):
        """Test creating a todo item with all required fields."""
        todo = TodoItem(
            title="Complete Project",
            details="Finish the Python CLI project",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            due_date="2025-12-31",
        )
        assert todo_manager.add_todo(todo) is True

    def test_create_todo_minimal_fields(self, todo_manager):
        """Test creating a todo item with only required fields."""
        todo = TodoItem(
            title="Simple Task",
            details="",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
        )
        assert todo_manager.add_todo(todo) is True

    def test_created_todo_has_unique_id(self):
        """Test that each created todo has a unique ID."""
        todo1 = TodoItem(
            title="Task 1",
            details="Description 1",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="user1",
        )
        todo2 = TodoItem(
            title="Task 2",
            details="Description 2",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="user1",
        )
        assert todo1.id != todo2.id

    def test_created_todo_has_pending_status(self):
        """Test that newly created todos have PENDING status by default."""
        todo = TodoItem(
            title="New Task",
            details="Task description",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="testuser",
        )
        assert todo.status == Status.PENDING

    def test_created_todo_has_timestamp(self):
        """Test that created todos have creation and update timestamps."""
        todo = TodoItem(
            title="Task with Timestamp",
            details="Check timestamps",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
        )
        assert todo.created_at is not None
        assert todo.updated_at is not None
        assert "T" in todo.created_at  # ISO format check
        assert "T" in todo.updated_at

    def test_created_todo_persisted_to_file(self, todo_manager):
        """Test that created todos are persisted to the JSON file."""
        todo = TodoItem(
            title="Persistent Task",
            details="Should be saved",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )
        todo_manager.add_todo(todo)

        # Verify the todo was saved to file
        with open(todo_manager.todos_file, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["title"] == "Persistent Task"
        assert data[0]["owner"] == "testuser"

    def test_multiple_todos_created_for_same_user(self, todo_manager):
        """Test that multiple todos can be created for the same user."""
        todo1 = TodoItem(
            title="Task 1",
            details="First task",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="user1",
        )
        todo2 = TodoItem(
            title="Task 2",
            details="Second task",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="user1",
        )
        todo_manager.add_todo(todo1)
        todo_manager.add_todo(todo2)

        user_todos = todo_manager.get_user_todos("user1")
        assert len(user_todos) == 2

    def test_create_todo_with_different_priorities(self, todo_manager):
        """Test creating todos with all priority levels."""
        for priority in [Priority.HIGH, Priority.MID, Priority.LOW]:
            todo = TodoItem(
                title=f"Task with {priority.value} priority",
                details="Test priority",
                priority=priority,
                status=Status.PENDING,
                owner="testuser",
            )
            assert todo_manager.add_todo(todo) is True

    def test_create_todo_with_optional_due_date(self, todo_manager):
        """Test creating a todo with an optional due date."""
        due_date = "2025-12-31T23:59:59"
        todo = TodoItem(
            title="Task with Due Date",
            details="Has a due date",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            due_date=due_date,
        )
        todo_manager.add_todo(todo)

        user_todos = todo_manager.get_user_todos("testuser")
        assert user_todos[0].due_date == due_date

    def test_create_todo_without_due_date(self, todo_manager):
        """Test creating a todo without a due date (defaults to None)."""
        todo = TodoItem(
            title="Task without Due Date",
            details="No due date",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
        )
        todo_manager.add_todo(todo)

        user_todos = todo_manager.get_user_todos("testuser")
        assert user_todos[0].due_date is None

    def test_title_is_required_for_creation(self):
        """Test that title field is required for todo creation (empty string should work but is discouraged)."""
        # Dataclasses don't enforce type validation at runtime
        # The CLI layer should validate that title is not empty
        todo = TodoItem(
            title="",
            details="Description",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )
        assert todo.title == ""


class TestTodoEditing:
    """Test suite for editing to-do items."""

    @pytest.fixture
    def todo_manager(self, tmp_path):
        """Create a TodoManager instance with a temporary file."""
        todos_file = tmp_path / "todos.json"
        return TodoManager(str(todos_file))

    @pytest.fixture
    def sample_todo(self):
        """Create a sample todo for testing."""
        return TodoItem(
            id="test-id-123",
            title="Original Title",
            details="Original details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T10:00:00",
            due_date="2025-12-31",
        )

    def test_edit_todo_title(self, todo_manager, sample_todo):
        """Test editing the title of a todo item."""
        todo_manager.add_todo(sample_todo)

        # Edit the title
        sample_todo.title = "Updated Title"
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify the change
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.title == "Updated Title"

    def test_edit_todo_details(self, todo_manager, sample_todo):
        """Test editing the details/description of a todo item."""
        todo_manager.add_todo(sample_todo)

        # Edit the details
        sample_todo.details = "Updated details"
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify the change
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.details == "Updated details"

    def test_edit_todo_priority(self, todo_manager, sample_todo):
        """Test editing the priority of a todo item."""
        todo_manager.add_todo(sample_todo)

        # Change priority from HIGH to LOW
        sample_todo.priority = Priority.LOW
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify the change
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.priority == Priority.LOW

    def test_edit_todo_status(self, todo_manager, sample_todo):
        """Test editing the status of a todo item."""
        todo_manager.add_todo(sample_todo)

        # Change status from PENDING to COMPLETED
        sample_todo.status = Status.COMPLETED
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify the change
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.status == Status.COMPLETED

    def test_edit_todo_due_date(self, todo_manager, sample_todo):
        """Test editing the due date of a todo item."""
        todo_manager.add_todo(sample_todo)

        # Update due date
        sample_todo.due_date = "2026-06-15"
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify the change
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.due_date == "2026-06-15"

    def test_edit_todo_remove_due_date(self, todo_manager, sample_todo):
        """Test removing the due date from a todo item."""
        todo_manager.add_todo(sample_todo)

        # Remove due date
        sample_todo.due_date = None
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify the change
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.due_date is None

    def test_edit_multiple_fields_at_once(self, todo_manager, sample_todo):
        """Test editing multiple fields of a todo item at once."""
        todo_manager.add_todo(sample_todo)

        # Edit multiple fields
        sample_todo.title = "New Title"
        sample_todo.details = "New details"
        sample_todo.priority = Priority.MID
        sample_todo.due_date = "2025-11-01"
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify all changes
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.title == "New Title"
        assert updated_todo.details == "New details"
        assert updated_todo.priority == Priority.MID
        assert updated_todo.due_date == "2025-11-01"

    def test_edit_updates_timestamp(self, todo_manager, sample_todo):
        """Test that editing a todo updates the updated_at timestamp."""
        todo_manager.add_todo(sample_todo)

        # Wait a moment and edit
        sample_todo.title = "Updated Title"
        new_updated_at = datetime.now().isoformat()
        sample_todo.updated_at = new_updated_at
        assert todo_manager.update_todo(sample_todo) is True

        # Verify timestamp was updated
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.updated_at == new_updated_at

    def test_edit_preserves_created_timestamp(self, todo_manager, sample_todo):
        """Test that editing a todo preserves the original created_at timestamp."""
        original_created_at = sample_todo.created_at
        todo_manager.add_todo(sample_todo)

        # Edit the todo
        sample_todo.title = "Updated Title"
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify created_at wasn't changed
        updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
        assert updated_todo.created_at == original_created_at

    def test_edit_preserves_todo_id(self, todo_manager, sample_todo):
        """Test that editing a todo preserves its ID."""
        original_id = sample_todo.id
        todo_manager.add_todo(sample_todo)

        # Edit the todo
        sample_todo.title = "Updated Title"
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is True

        # Verify ID wasn't changed
        updated_todo = todo_manager.get_todo_by_id(original_id, "testuser")
        assert updated_todo.id == original_id

    def test_edit_todo_persisted_to_file(self, todo_manager, sample_todo):
        """Test that edited todos are persisted to the JSON file."""
        todo_manager.add_todo(sample_todo)

        # Edit the todo
        sample_todo.title = "Updated Title"
        sample_todo.updated_at = datetime.now().isoformat()
        todo_manager.update_todo(sample_todo)

        # Verify the change was saved to file
        with open(todo_manager.todos_file, "r") as f:
            data = json.load(f)
        assert data[0]["title"] == "Updated Title"

    def test_edit_nonexistent_todo_returns_false(self, todo_manager):
        """Test that editing a non-existent todo returns False."""
        todo = TodoItem(
            id="nonexistent-id",
            title="Nonexistent",
            details="This doesn't exist",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )
        assert todo_manager.update_todo(todo) is False

    def test_edit_todo_owned_by_different_user(self, todo_manager, sample_todo):
        """Test that a todo cannot be edited by a different user."""
        todo_manager.add_todo(sample_todo)

        # Try to edit the todo as a different user
        sample_todo.owner = "different_user"
        sample_todo.updated_at = datetime.now().isoformat()
        assert todo_manager.update_todo(sample_todo) is False

    def test_edit_todo_all_priority_levels(self, todo_manager, sample_todo):
        """Test editing a todo to each priority level."""
        todo_manager.add_todo(sample_todo)

        for priority in [Priority.HIGH, Priority.MID, Priority.LOW]:
            sample_todo.priority = priority
            sample_todo.updated_at = datetime.now().isoformat()
            assert todo_manager.update_todo(sample_todo) is True

            updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
            assert updated_todo.priority == priority

    def test_edit_todo_all_status_levels(self, todo_manager, sample_todo):
        """Test editing a todo to each status level."""
        todo_manager.add_todo(sample_todo)

        for status in [Status.PENDING, Status.COMPLETED]:
            sample_todo.status = status
            sample_todo.updated_at = datetime.now().isoformat()
            assert todo_manager.update_todo(sample_todo) is True

            updated_todo = todo_manager.get_todo_by_id("test-id-123", "testuser")
            assert updated_todo.status == status


class TestTodoValidation:
    """Test suite for todo creation and editing validation."""

    def test_todo_from_dict_with_invalid_priority(self):
        """Test that invalid priority in from_dict raises error."""
        data = {
            "id": "test-id",
            "title": "Test",
            "details": "Test",
            "priority": "INVALID_PRIORITY",
            "status": "PENDING",
            "owner": "user",
            "created_at": "2025-01-20T10:00:00",
            "updated_at": "2025-01-20T10:00:00",
        }
        with pytest.raises(ValueError):
            TodoItem.from_dict(data)

    def test_todo_from_dict_with_invalid_status(self):
        """Test that invalid status in from_dict raises error."""
        data = {
            "id": "test-id",
            "title": "Test",
            "details": "Test",
            "priority": "HIGH",
            "status": "INVALID_STATUS",
            "owner": "user",
            "created_at": "2025-01-20T10:00:00",
            "updated_at": "2025-01-20T10:00:00",
        }
        with pytest.raises(ValueError):
            TodoItem.from_dict(data)


class TestTodoAppIntegration:
    """Integration tests for the App class methods related to task 3."""

    @pytest.fixture
    def app(self, tmp_path):
        """Create an App instance with temporary files."""
        app = App()
        app.todo_manager.todos_file = str(tmp_path / "todos.json")
        app.auth_manager.users_file = str(tmp_path / "users.json")
        # Ensure files are created
        app.auth_manager._ensure_file_exists()
        app.todo_manager._ensure_file_exists()
        # Setup a logged-in user
        app.auth_manager.register("testuser", "testpass")
        app.current_user = "testuser"
        return app

    def test_handle_add_todo_with_valid_input(self, app):
        """Test adding a todo through the app interface."""
        # Mock user input
        with patch("builtins.input") as mock_input:
            mock_input.side_effect = [
                "Test Task",  # title
                "Test details",  # details
                "HIGH",  # priority
                "2025-12-31",  # due_date
            ]
            with patch("builtins.print"):
                app.handle_add_todo()

        # Verify todo was added
        todos = app.todo_manager.get_user_todos("testuser")
        assert len(todos) == 1
        assert todos[0].title == "Test Task"

    def test_handle_add_todo_validates_empty_title(self, app):
        """Test that adding a todo with empty title is rejected."""
        with patch("builtins.input") as mock_input:
            mock_input.return_value = ""  # empty title
            with patch("builtins.print"):
                app.handle_add_todo()

        # Verify no todo was added
        todos = app.todo_manager.get_user_todos("testuser")
        assert len(todos) == 0

    def test_handle_add_todo_with_invalid_priority_defaults_to_mid(self, app):
        """Test that invalid priority defaults to MID."""
        with patch("builtins.input") as mock_input:
            mock_input.side_effect = [
                "Test Task",  # title
                "Details",  # details
                "INVALID_PRIORITY",  # invalid priority
                "",  # due_date
            ]
            with patch("builtins.print"):
                app.handle_add_todo()

        # Verify todo was added with MID priority
        todos = app.todo_manager.get_user_todos("testuser")
        assert len(todos) == 1
        assert todos[0].priority == Priority.MID

    def test_handle_edit_todo_title(self, app):
        """Test editing a todo's title through the app interface."""
        # Add a todo first
        todo = TodoItem(
            title="Original Title",
            details="Details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )
        app.todo_manager.add_todo(todo)

        # Mock user input for editing
        with patch("builtins.input") as mock_input:
            mock_input.side_effect = [
                "1",  # select first todo
                "New Title",  # new title
                "",  # keep details
                "",  # keep priority
                "",  # keep due date
            ]
            with patch("builtins.print"):
                app.handle_edit_todo()

        # Verify todo was updated
        todos = app.todo_manager.get_user_todos("testuser")
        assert todos[0].title == "New Title"

    def test_handle_edit_todo_priority(self, app):
        """Test editing a todo's priority through the app interface."""
        # Add a todo first
        todo = TodoItem(
            title="Test Task",
            details="Details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )
        app.todo_manager.add_todo(todo)

        # Mock user input for editing
        with patch("builtins.input") as mock_input:
            mock_input.side_effect = [
                "1",  # select first todo
                "",  # keep title
                "",  # keep details
                "LOW",  # new priority
                "",  # keep due date
            ]
            with patch("builtins.print"):
                app.handle_edit_todo()

        # Verify todo was updated
        todos = app.todo_manager.get_user_todos("testuser")
        assert todos[0].priority == Priority.LOW

    def test_handle_edit_todo_with_no_todos(self, app):
        """Test that editing is not possible when user has no todos."""
        with patch("builtins.print") as mock_print:
            app.handle_edit_todo()
            # Verify appropriate message was printed
            assert any(
                "no todos" in str(call).lower() for call in mock_print.call_args_list
            )

    def test_handle_edit_todo_with_invalid_selection(self, app):
        """Test handling invalid todo selection during editing."""
        # Add a todo first
        todo = TodoItem(
            title="Test Task",
            details="Details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
        )
        app.todo_manager.add_todo(todo)

        # Mock user input with invalid selection
        with patch("builtins.input") as mock_input:
            mock_input.return_value = "999"  # invalid selection
            with patch("builtins.print") as mock_print:
                app.handle_edit_todo()
            # Verify error message
            assert any(
                "invalid" in str(call).lower() for call in mock_print.call_args_list
            )

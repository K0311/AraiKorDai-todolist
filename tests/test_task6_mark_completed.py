"""Unit tests for Task 6: Mark a To-Do List Item as Completed functionality."""

from unittest.mock import patch, MagicMock

from src.models import TodoItem, Priority, Status
from src.main import App


class TestMarkCompleted:
    """Test suite for marking to-do items as completed."""

    def setup_method(self):
        """Set up test fixtures."""
        self.app = App()
        self.app.current_user = "testuser"
        # Mock the todo_manager
        self.app.todo_manager = MagicMock()

    @patch("builtins.print")
    def test_no_todos_to_mark_completed(self, mock_print):
        """Test marking completed when user has no todos."""
        # Mock empty todos list
        self.app.todo_manager.get_user_todos.return_value = []

        # Call the method
        self.app.handle_mark_completed()

        # Check that get_user_todos was called
        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")

        # Check message printed
        mock_print.assert_called_once_with("You have no todos yet.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_mark_pending_todo_as_completed(self, mock_print, mock_input):
        """Test successfully marking a pending todo as completed."""
        # Create a pending todo
        pending_todo = TodoItem(
            id="test-id-123",
            title="Test Task",
            details="Test details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T10:00:00",
        )

        # Mock todos list with one pending todo
        self.app.todo_manager.get_user_todos.return_value = [pending_todo]
        self.app.todo_manager.update_todo.return_value = True

        # Simulate user selecting the first todo
        mock_input.return_value = "1"

        # Call the method
        self.app.handle_mark_completed()

        # Check that get_user_todos was called
        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")

        # Check that update_todo was called
        self.app.todo_manager.update_todo.assert_called_once()

        # Get the todo that was passed to update_todo
        updated_todo = self.app.todo_manager.update_todo.call_args[0][0]

        # Check that status was changed to COMPLETED
        assert updated_todo.status == Status.COMPLETED

        # Check that updated_at was updated (should be recent)
        assert updated_todo.updated_at != "2025-01-20T10:00:00"

        # Check success message
        mock_print.assert_any_call("Todo marked as completed!")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_attempt_to_mark_already_completed_todo(self, mock_print, mock_input):
        """Test attempting to mark an already completed todo."""
        # Create a completed todo
        completed_todo = TodoItem(
            id="test-id-456",
            title="Completed Task",
            details="Already done",
            priority=Priority.MID,
            status=Status.COMPLETED,
            owner="testuser",
            created_at="2025-01-19T10:00:00",
            updated_at="2025-01-19T11:00:00",
        )

        # Mock todos list with one completed todo
        self.app.todo_manager.get_user_todos.return_value = [completed_todo]

        # Simulate user selecting the first todo
        mock_input.return_value = "1"

        # Call the method
        self.app.handle_mark_completed()

        # Check that get_user_todos was called
        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")

        # Check that update_todo was NOT called
        self.app.todo_manager.update_todo.assert_not_called()

        # Check message about already completed
        mock_print.assert_any_call("This todo is already completed.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_selection_number(self, mock_print, mock_input):
        """Test selecting an invalid todo number."""
        # Create a todo
        todo = TodoItem(
            id="test-id-789",
            title="Test Task",
            details="Test details",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T10:00:00",
        )

        # Mock todos list with one todo
        self.app.todo_manager.get_user_todos.return_value = [todo]

        # Simulate user selecting invalid number (2 when only 1 todo exists)
        mock_input.return_value = "2"

        # Call the method
        self.app.handle_mark_completed()

        # Check that update_todo was NOT called
        self.app.todo_manager.update_todo.assert_not_called()

        # Check invalid selection message
        mock_print.assert_any_call("Invalid selection.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_non_numeric_input(self, mock_print, mock_input):
        """Test entering non-numeric input for selection."""
        # Create a todo
        todo = TodoItem(
            id="test-id-101",
            title="Test Task",
            details="Test details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T10:00:00",
        )

        # Mock todos list with one todo
        self.app.todo_manager.get_user_todos.return_value = [todo]

        # Simulate user entering non-numeric input
        mock_input.return_value = "abc"

        # Call the method
        self.app.handle_mark_completed()

        # Check that update_todo was NOT called
        self.app.todo_manager.update_todo.assert_not_called()

        # Check error message for invalid number
        mock_print.assert_any_call("Please enter a valid number.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_display_pending_and_completed_todos(self, mock_print, mock_input):
        """Test that both pending and completed todos are displayed correctly."""
        # Create one pending and one completed todo
        pending_todo = TodoItem(
            id="pending-id",
            title="Pending Task",
            details="Not done yet",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T09:00:00",
            updated_at="2025-01-20T09:00:00",
        )
        completed_todo = TodoItem(
            id="completed-id",
            title="Completed Task",
            details="Already done",
            priority=Priority.MID,
            status=Status.COMPLETED,
            owner="testuser",
            created_at="2025-01-19T10:00:00",
            updated_at="2025-01-19T11:00:00",
        )

        # Mock todos list with both todos
        self.app.todo_manager.get_user_todos.return_value = [
            pending_todo,
            completed_todo,
        ]

        # Simulate user selecting the first (pending) todo
        mock_input.return_value = "1"

        # Call the method
        self.app.handle_mark_completed()

        # Check that both todos are displayed in the list
        mock_print.assert_any_call("1. Pending Task")
        mock_print.assert_any_call("2. Completed Task (Already completed)")

        # Check that update_todo was called (for the pending one)
        self.app.todo_manager.update_todo.assert_called_once()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_update_todo_failure(self, mock_print, mock_input):
        """Test when update_todo returns False (failure)."""
        # Create a pending todo
        pending_todo = TodoItem(
            id="test-id-999",
            title="Test Task",
            details="Test details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T10:00:00",
        )

        # Mock todos list with one pending todo
        self.app.todo_manager.get_user_todos.return_value = [pending_todo]
        self.app.todo_manager.update_todo.return_value = False  # Simulate failure

        # Simulate user selecting the first todo
        mock_input.return_value = "1"

        # Call the method
        self.app.handle_mark_completed()

        # Check that update_todo was called
        self.app.todo_manager.update_todo.assert_called_once()

        # Check failure message
        mock_print.assert_any_call("Failed to update todo.")

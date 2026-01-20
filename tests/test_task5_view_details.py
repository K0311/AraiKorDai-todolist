"""Unit tests for Task 5: View To-Do List Item Details functionality."""

from unittest.mock import patch, MagicMock

from src.models import TodoItem, Priority, Status
from src.main import App


class TestViewTodoDetails:
    """Test suite for viewing todo details."""

    def setup_method(self):
        self.app = App()
        self.app.current_user = "testuser"
        # Replace the todo_manager with a mock
        self.app.todo_manager = MagicMock()

    @patch("builtins.print")
    def test_no_todos(self, mock_print):
        """When the user has no todos, an appropriate message is shown."""
        self.app.todo_manager.get_user_todos.return_value = []

        self.app.handle_view_todo_details()

        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")
        mock_print.assert_called_once_with("You have no todos yet.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_view_todo_details_with_due_date(self, mock_print, mock_input):
        """Successful display of todo details including due date."""
        todo = TodoItem(
            id="detail-id-1",
            title="Detail Task",
            details="Some details",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T11:00:00",
            due_date="2025-12-31",
        )

        self.app.todo_manager.get_user_todos.return_value = [todo]
        mock_input.return_value = "1"

        self.app.handle_view_todo_details()

        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")

        # Verify key detail lines were printed
        mock_print.assert_any_call(f"ID: {todo.id}")
        mock_print.assert_any_call(f"Title: {todo.title}")
        mock_print.assert_any_call(f"Details: {todo.details}")
        mock_print.assert_any_call(f"Priority: {todo.priority.value}")
        mock_print.assert_any_call(f"Status: {todo.status.value}")
        mock_print.assert_any_call(f"Owner: {todo.owner}")
        mock_print.assert_any_call(f"Created: {todo.created_at}")
        mock_print.assert_any_call(f"Updated: {todo.updated_at}")
        mock_print.assert_any_call(f"Due Date: {todo.due_date}")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_view_todo_details_without_due_date(self, mock_print, mock_input):
        """Display todo details when no due date is present (no Due Date line)."""
        todo = TodoItem(
            id="detail-id-2",
            title="No Due",
            details="No due date here",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-02-01T10:00:00",
            updated_at="2025-02-01T11:00:00",
            due_date=None,
        )

        self.app.todo_manager.get_user_todos.return_value = [todo]
        mock_input.return_value = "1"

        self.app.handle_view_todo_details()

        # Ensure Due Date line was not printed
        mock_print.assert_any_call(f"ID: {todo.id}")
        # Build the Due Date string and ensure it was not present in any calls
        due_call = (f"Due Date: {todo.due_date}")
        for call in mock_print.call_args_list:
            assert due_call not in call.args

    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_selection_number(self, mock_print, mock_input):
        """Selecting a number outside the available range yields an invalid message."""
        todo = TodoItem(
            id="detail-id-3",
            title="Only Task",
            details="",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-03-01T10:00:00",
            updated_at="2025-03-01T11:00:00",
        )

        self.app.todo_manager.get_user_todos.return_value = [todo]
        mock_input.return_value = "2"  # invalid selection

        self.app.handle_view_todo_details()

        mock_print.assert_any_call("Invalid selection.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_non_numeric_input(self, mock_print, mock_input):
        """Non-numeric selection input is handled gracefully."""
        todo = TodoItem(
            id="detail-id-4",
            title="Task",
            details="",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-04-01T10:00:00",
            updated_at="2025-04-01T11:00:00",
        )

        self.app.todo_manager.get_user_todos.return_value = [todo]
        mock_input.return_value = "abc"  # non-numeric

        self.app.handle_view_todo_details()

        mock_print.assert_any_call("Please enter a valid number.")

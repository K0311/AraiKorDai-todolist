"""Unit tests for Task 4: View All To-Do List Items functionality."""

from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

from src.models import TodoItem, Priority, Status
from src.main import App


class TestViewAllTodos:
    """Test suite for viewing all to-do items."""

    def setup_method(self):
        """Set up test fixtures."""
        self.app = App()
        self.app.current_user = "testuser"
        # Mock the todo_manager
        self.app.todo_manager = MagicMock()

    @patch("builtins.print")
    def test_no_todos_message(self, mock_print):
        """Test viewing todos when user has no todos."""
        # Mock empty todos list
        self.app.todo_manager.get_user_todos.return_value = []

        # Call the method
        self.app.handle_view_todos()

        # Check that get_user_todos was called with the current user
        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")

        # Check that appropriate message is printed
        mock_print.assert_called_once_with("You have no todos yet.")

    @patch("builtins.print")
    def test_single_todo_display(self, mock_print):
        """Test viewing todos with a single todo item."""
        # Create a single todo
        todo = TodoItem(
            id="test-id-001",
            title="Buy groceries",
            details="Milk, bread, eggs",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T08:00:00",
            updated_at="2025-01-20T08:00:00",
            due_date="2025-01-21",
        )

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = [todo]

        # Call the method
        self.app.handle_view_todos()

        # Check that get_user_todos was called
        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")

        # Check that header is printed
        mock_print.assert_any_call("\n=== YOUR TODOS ===")

        # Check that todo title is printed
        mock_print.assert_any_call("\n1. Buy groceries (Due: 2025-01-21)")

        # Check that status is printed
        mock_print.assert_any_call("   Status: PENDING")

        # Check that priority is printed
        mock_print.assert_any_call("   Priority: MID")

        # Check that details are printed
        mock_print.assert_any_call("   Details: Milk, bread, eggs")

        # Check that created date is printed
        mock_print.assert_any_call("   Created: 2025-01-20T08:00:00")

    @patch("builtins.print")
    def test_todo_without_details(self, mock_print):
        """Test viewing a todo without details field."""
        # Create a todo without details
        todo = TodoItem(
            id="test-id-002",
            title="Call dentist",
            details="",  # Empty details
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T09:00:00",
            updated_at="2025-01-20T09:00:00",
        )

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = [todo]

        # Call the method
        self.app.handle_view_todos()

        # Check that the details line is NOT printed when empty
        calls = [str(call) for call in mock_print.call_args_list]
        details_printed = any("Details:" in str(call) for call in calls)
        assert not details_printed

    @patch("builtins.print")
    def test_todo_without_due_date(self, mock_print):
        """Test viewing a todo without a due date."""
        # Create a todo without due_date
        todo = TodoItem(
            id="test-id-003",
            title="Read a book",
            details="Fiction novel",
            priority=Priority.LOW,
            status=Status.COMPLETED,
            owner="testuser",
            created_at="2025-01-19T10:00:00",
            updated_at="2025-01-20T15:30:00",
            due_date=None,
        )

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = [todo]

        # Call the method
        self.app.handle_view_todos()

        # Check that todo title is printed without due date suffix
        mock_print.assert_any_call("\n1. Read a book")

    @patch("builtins.print")
    def test_multiple_todos_sorted_by_creation_time(self, mock_print):
        """Test viewing multiple todos sorted by creation time (newest first)."""
        # Create todos with different creation times
        old_todo = TodoItem(
            id="test-id-old",
            title="Old task",
            details="Created earlier",
            priority=Priority.LOW,
            status=Status.COMPLETED,
            owner="testuser",
            created_at="2025-01-18T08:00:00",
            updated_at="2025-01-18T08:00:00",
        )

        new_todo = TodoItem(
            id="test-id-new",
            title="New task",
            details="Created recently",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T15:00:00",
            updated_at="2025-01-20T15:00:00",
        )

        mid_todo = TodoItem(
            id="test-id-mid",
            title="Middle task",
            details="Created in between",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-19T12:00:00",
            updated_at="2025-01-19T12:00:00",
        )

        # Return todos in non-sorted order
        self.app.todo_manager.get_user_todos.return_value = [
            old_todo,
            mid_todo,
            new_todo,
        ]

        # Call the method
        self.app.handle_view_todos()

        # Get all the print calls
        print_calls = [str(call) for call in mock_print.call_args_list]

        # Find the indices of each todo title in the output
        new_task_index = next(
            i
            for i, call in enumerate(print_calls)
            if "New task" in str(call)
        )
        mid_task_index = next(
            i
            for i, call in enumerate(print_calls)
            if "Middle task" in str(call)
        )
        old_task_index = next(
            i
            for i, call in enumerate(print_calls)
            if "Old task" in str(call)
        )

        # Verify they're in the correct order (newest first)
        assert new_task_index < mid_task_index < old_task_index

    @patch("builtins.print")
    def test_all_priority_levels_displayed(self, mock_print):
        """Test that all priority levels are correctly displayed."""
        # Create todos with different priorities
        high_priority_todo = TodoItem(
            id="test-high",
            title="Urgent task",
            details="",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T10:00:00",
        )

        mid_priority_todo = TodoItem(
            id="test-mid",
            title="Normal task",
            details="",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:05:00",
            updated_at="2025-01-20T10:05:00",
        )

        low_priority_todo = TodoItem(
            id="test-low",
            title="Low priority task",
            details="",
            priority=Priority.LOW,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:10:00",
            updated_at="2025-01-20T10:10:00",
        )

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = [
            high_priority_todo,
            mid_priority_todo,
            low_priority_todo,
        ]

        # Call the method
        self.app.handle_view_todos()

        # Check that all priorities are displayed
        mock_print.assert_any_call("   Priority: HIGH")
        mock_print.assert_any_call("   Priority: MID")
        mock_print.assert_any_call("   Priority: LOW")

    @patch("builtins.print")
    def test_all_status_levels_displayed(self, mock_print):
        """Test that all status levels are correctly displayed."""
        # Create todos with different statuses
        pending_todo = TodoItem(
            id="test-pending",
            title="Pending task",
            details="",
            priority=Priority.MID,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-20T10:00:00",
            updated_at="2025-01-20T10:00:00",
        )

        completed_todo = TodoItem(
            id="test-completed",
            title="Completed task",
            details="",
            priority=Priority.MID,
            status=Status.COMPLETED,
            owner="testuser",
            created_at="2025-01-19T10:00:00",
            updated_at="2025-01-20T10:00:00",
        )

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = [
            pending_todo,
            completed_todo,
        ]

        # Call the method
        self.app.handle_view_todos()

        # Check that both statuses are displayed
        mock_print.assert_any_call("   Status: PENDING")
        mock_print.assert_any_call("   Status: COMPLETED")

    @patch("builtins.print")
    def test_multiple_todos_with_various_combinations(self, mock_print):
        """Test viewing multiple todos with various field combinations."""
        todos = [
            TodoItem(
                id="id-1",
                title="Task with all fields",
                details="Complete information",
                priority=Priority.HIGH,
                status=Status.PENDING,
                owner="testuser",
                created_at="2025-01-20T10:00:00",
                updated_at="2025-01-20T10:00:00",
                due_date="2025-01-22",
            ),
            TodoItem(
                id="id-2",
                title="Task with minimal fields",
                details="",
                priority=Priority.LOW,
                status=Status.COMPLETED,
                owner="testuser",
                created_at="2025-01-19T10:00:00",
                updated_at="2025-01-19T10:00:00",
                due_date=None,
            ),
            TodoItem(
                id="id-3",
                title="Task without due date",
                details="Some details here",
                priority=Priority.MID,
                status=Status.PENDING,
                owner="testuser",
                created_at="2025-01-18T10:00:00",
                updated_at="2025-01-18T10:00:00",
                due_date=None,
            ),
        ]

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = todos

        # Call the method
        self.app.handle_view_todos()

        # Get all print calls
        all_calls = mock_print.call_args_list
        call_strings = [str(call) for call in all_calls]

        # Check that all three todos are displayed
        assert any("Task with all fields" in str(call) for call in call_strings)
        assert any("Task with minimal fields" in str(call) for call in call_strings)
        assert any("Task without due date" in str(call) for call in call_strings)

        # Check that all todos have correct status and priority
        assert any("HIGH" in str(call) for call in call_strings)
        assert any("LOW" in str(call) for call in call_strings)
        assert any("MID" in str(call) for call in call_strings)

    @patch("builtins.print")
    def test_todos_numbered_correctly(self, mock_print):
        """Test that todos are numbered sequentially starting from 1."""
        todos = [
            TodoItem(
                id="id-1",
                title="First task",
                details="",
                priority=Priority.MID,
                status=Status.PENDING,
                owner="testuser",
                created_at="2025-01-20T10:00:00",
                updated_at="2025-01-20T10:00:00",
            ),
            TodoItem(
                id="id-2",
                title="Second task",
                details="",
                priority=Priority.MID,
                status=Status.PENDING,
                owner="testuser",
                created_at="2025-01-20T11:00:00",
                updated_at="2025-01-20T11:00:00",
            ),
            TodoItem(
                id="id-3",
                title="Third task",
                details="",
                priority=Priority.MID,
                status=Status.PENDING,
                owner="testuser",
                created_at="2025-01-20T12:00:00",
                updated_at="2025-01-20T12:00:00",
            ),
        ]

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = todos

        # Call the method
        self.app.handle_view_todos()

        # Check that todos are numbered (they are sorted by creation time - newest first)
        # So the order should be: Third task (1), Second task (2), First task (3)
        mock_print.assert_any_call("\n1. Third task")
        mock_print.assert_any_call("\n2. Second task")
        mock_print.assert_any_call("\n3. First task")

    @patch("builtins.print")
    def test_formatting_with_due_dates(self, mock_print):
        """Test that due dates are formatted correctly in the display."""
        todo = TodoItem(
            id="test-id",
            title="Important deadline",
            details="Project completion",
            priority=Priority.HIGH,
            status=Status.PENDING,
            owner="testuser",
            created_at="2025-01-15T09:00:00",
            updated_at="2025-01-15T09:00:00",
            due_date="2025-02-15",
        )

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = [todo]

        # Call the method
        self.app.handle_view_todos()

        # Check that due date is formatted correctly as "(Due: YYYY-MM-DD)"
        mock_print.assert_any_call("\n1. Important deadline (Due: 2025-02-15)")

    @patch("builtins.print")
    def test_todos_retrieved_for_correct_user(self, mock_print):
        """Test that todos are retrieved only for the current user."""
        # Create app with specific user
        self.app.current_user = "specific_user"

        todos = [
            TodoItem(
                id="id-1",
                title="User task",
                details="",
                priority=Priority.MID,
                status=Status.PENDING,
                owner="specific_user",
                created_at="2025-01-20T10:00:00",
                updated_at="2025-01-20T10:00:00",
            ),
        ]

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = todos

        # Call the method
        self.app.handle_view_todos()

        # Verify that get_user_todos was called with the correct username
        self.app.todo_manager.get_user_todos.assert_called_once_with("specific_user")

    @patch("builtins.print")
    def test_created_date_always_displayed(self, mock_print):
        """Test that created date is always displayed for all todos."""
        todos = [
            TodoItem(
                id="id-1",
                title="Task 1",
                details="",
                priority=Priority.MID,
                status=Status.PENDING,
                owner="testuser",
                created_at="2025-01-20T08:30:00",
                updated_at="2025-01-20T08:30:00",
            ),
            TodoItem(
                id="id-2",
                title="Task 2",
                details="",
                priority=Priority.MID,
                status=Status.PENDING,
                owner="testuser",
                created_at="2025-01-19T14:45:00",
                updated_at="2025-01-19T14:45:00",
            ),
        ]

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = todos

        # Call the method
        self.app.handle_view_todos()

        # Check that created dates are displayed
        mock_print.assert_any_call("   Created: 2025-01-20T08:30:00")
        mock_print.assert_any_call("   Created: 2025-01-19T14:45:00")

    @patch("builtins.print")
    def test_large_number_of_todos(self, mock_print):
        """Test viewing a large number of todos."""
        # Create 50 todos
        todos = [
            TodoItem(
                id=f"id-{i}",
                title=f"Task {i}",
                details=f"Details for task {i}",
                priority=Priority.MID,
                status=Status.PENDING if i % 2 == 0 else Status.COMPLETED,
                owner="testuser",
                created_at=f"2025-01-{(i % 31) + 1:02d}T10:00:00",
                updated_at=f"2025-01-{(i % 31) + 1:02d}T10:00:00",
                due_date=None,
            )
            for i in range(1, 51)
        ]

        # Mock todos list
        self.app.todo_manager.get_user_todos.return_value = todos

        # Call the method
        self.app.handle_view_todos()

        # Get the print calls
        all_calls = [str(call) for call in mock_print.call_args_list]

        # Verify get_user_todos was called
        self.app.todo_manager.get_user_todos.assert_called_once_with("testuser")

        # Verify that the method completes without error
        # and that the header was printed
        assert any("YOUR TODOS" in call for call in all_calls)

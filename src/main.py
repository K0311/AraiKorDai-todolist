"""Main entry point for the to-do list CLI application."""

import json
import os
from typing import Optional

from models import TodoItem, Priority, Status


class AuthManager:
    """Handles user authentication and registration."""

    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create users file if it doesn't exist."""
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump([], f)

    def _load_users(self) -> list:
        """Load all users from file."""
        with open(self.users_file, "r") as f:
            return json.load(f)

    def _save_users(self, users: list) -> None:
        """Save users to file."""
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)

    def register(self, username: str, password: str) -> bool:
        """Register a new user. Returns True if successful, False if user exists."""
        users = self._load_users()
        if any(user["username"] == username for user in users):
            return False
        users.append({"username": username, "password": password})
        self._save_users(users)
        return True

    def login(self, username: str, password: str) -> bool:
        """Authenticate a user. Returns True if credentials are correct."""
        users = self._load_users()
        return any(
            user["username"] == username and user["password"] == password
            for user in users
        )


class TodoManager:
    """Manages to-do items."""

    def __init__(self, todos_file: str = "todos.json"):
        self.todos_file = todos_file
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Create todos file if it doesn't exist."""
        if not os.path.exists(self.todos_file):
            with open(self.todos_file, "w") as f:
                json.dump([], f)

    def _load_todos(self) -> list:
        """Load all todos from file."""
        with open(self.todos_file, "r") as f:
            return json.load(f)

    def _save_todos(self, todos: list) -> None:
        """Save todos to file."""
        with open(self.todos_file, "w") as f:
            json.dump(todos, f, indent=2)

    def add_todo(self, todo: TodoItem) -> bool:
        """Add a new todo item."""
        todos = self._load_todos()
        todos.append(todo.to_dict())
        self._save_todos(todos)
        return True

    def get_user_todos(self, username: str) -> list:
        """Get all todos for a user."""
        todos = self._load_todos()
        return [TodoItem.from_dict(todo) for todo in todos if todo["owner"] == username]

    def get_todo_by_id(self, todo_id: str, username: str) -> Optional[TodoItem]:
        """Get a specific todo by ID for the user."""
        todos = self._load_todos()
        for todo_data in todos:
            if todo_data["id"] == todo_id and todo_data["owner"] == username:
                return TodoItem.from_dict(todo_data)
        return None

    def update_todo(self, todo: TodoItem) -> bool:
        """Update an existing todo item."""
        todos = self._load_todos()
        for i, todo_data in enumerate(todos):
            if todo_data["id"] == todo.id and todo_data["owner"] == todo.owner:
                todos[i] = todo.to_dict()
                self._save_todos(todos)
                return True
        return False


class App:
    """Main CLI application."""

    def __init__(self):
        self.auth_manager = AuthManager()
        self.todo_manager = TodoManager()
        self.current_user: Optional[str] = None

    def show_pre_login_menu(self) -> None:
        """Display the pre-login menu."""
        while not self.current_user:
            print("\n=== TO-DO LIST APPLICATION ===")
            print("[1] Login")
            print("[2] Sign Up")
            print("[3] Exit")
            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_signup()
            elif choice == "3":
                print("Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")

    def handle_login(self) -> None:
        """Handle user login."""
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if self.auth_manager.login(username, password):
            self.current_user = username
            print(f"\nWelcome, {username}!")
        else:
            print("Invalid username or password.")

    def handle_signup(self) -> None:
        """Handle user registration."""
        username = input("Enter a new username: ").strip()
        password = input("Enter a password: ").strip()

        if not username or not password:
            print("Username and password cannot be empty.")
            return

        if self.auth_manager.register(username, password):
            print(f"Account created successfully for {username}!")
        else:
            print("Username already exists.")

    def show_main_menu(self) -> None:
        """Display the main menu after login."""
        print("\n=== MAIN MENU ===")
        print("[1] Add Todo")
        print("[2] View All Todos")
        print("[3] View Todo Details")
        print("[4] Edit Todo")
        print("[5] Mark Todo as Completed")
        print("[6] Logout")
        print("[7] Exit")

    def run(self) -> None:
        """Main application loop."""
        self.show_pre_login_menu()

        while self.current_user:
            self.show_main_menu()
            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                self.handle_add_todo()
            elif choice == "2":
                self.handle_view_todos()
            elif choice == "3":
                self.handle_view_todo_details()
            elif choice == "4":
                self.handle_edit_todo()
            elif choice == "5":
                self.handle_mark_completed()
            elif choice == "6":
                self.current_user = None
                print("Logged out successfully.")
                self.show_pre_login_menu()
            elif choice == "7":
                print("Goodbye!")
                exit()
            else:
                print("Invalid choice. Please try again.")

    def handle_add_todo(self) -> None:
        """Handle adding a new todo item."""
        title = input("Enter todo title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
        details = input("Enter todo details (optional): ").strip()
        priority_str = input("Enter priority (HIGH/MID/LOW): ").strip().upper()

        try:
            priority = Priority(priority_str)
        except ValueError:
            print("Invalid priority. Defaulting to MID.")
            priority = Priority.MID

        due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip()
        if not due_date:
            due_date = None

        todo = TodoItem(
            title=title,
            details=details,
            priority=priority,
            status=Status.PENDING,
            owner=self.current_user,
            due_date=due_date,
        )

        if self.todo_manager.add_todo(todo):
            print("Todo added successfully!")

    def handle_view_todos(self) -> None:
        """Handle viewing user's todos."""
        todos = self.todo_manager.get_user_todos(self.current_user)

        if not todos:
            print("You have no todos yet.")
            return

        # Sort by creation time (newest first)
        todos.sort(key=lambda x: x.created_at, reverse=True)

        print("\n=== YOUR TODOS ===")
        for i, todo in enumerate(todos, 1):
            due_info = f" (Due: {todo.due_date})" if todo.due_date else ""
            print(f"\n{i}. {todo.title}{due_info}")
            print(f"   Status: {todo.status.value}")
            print(f"   Priority: {todo.priority.value}")
            if todo.details:
                print(f"   Details: {todo.details}")
            print(f"   Created: {todo.created_at}")

    def handle_view_todo_details(self) -> None:
        """Handle viewing detailed information of a specific todo."""
        todos = self.todo_manager.get_user_todos(self.current_user)

        if not todos:
            print("You have no todos yet.")
            return

        print("\n=== SELECT TODO TO VIEW DETAILS ===")
        for i, todo in enumerate(todos, 1):
            print(f"{i}. {todo.title}")

        try:
            choice = int(input("\nEnter the number of the todo to view: ").strip())
            if 1 <= choice <= len(todos):
                todo = todos[choice - 1]
                print("\n=== TODO DETAILS ===")
                print(f"ID: {todo.id}")
                print(f"Title: {todo.title}")
                print(f"Details: {todo.details}")
                print(f"Priority: {todo.priority.value}")
                print(f"Status: {todo.status.value}")
                print(f"Owner: {todo.owner}")
                print(f"Created: {todo.created_at}")
                print(f"Updated: {todo.updated_at}")
                if todo.due_date:
                    print(f"Due Date: {todo.due_date}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

    def handle_edit_todo(self) -> None:
        """Handle editing a todo item."""
        todos = self.todo_manager.get_user_todos(self.current_user)

        if not todos:
            print("You have no todos yet.")
            return

        print("\n=== SELECT TODO TO EDIT ===")
        for i, todo in enumerate(todos, 1):
            print(f"{i}. {todo.title}")

        try:
            choice = int(input("\nEnter the number of the todo to edit: ").strip())
            if 1 <= choice <= len(todos):
                todo = todos[choice - 1]
                print(f"\nEditing: {todo.title}")

                # Edit title
                new_title = input(f"Title [{todo.title}]: ").strip()
                if new_title:
                    todo.title = new_title

                # Edit details
                new_details = input(f"Details [{todo.details}]: ").strip()
                if new_details or new_details == "":
                    todo.details = new_details

                # Edit priority
                new_priority_str = (
                    input(f"Priority [{todo.priority.value}]: ").strip().upper()
                )
                if new_priority_str:
                    try:
                        todo.priority = Priority(new_priority_str)
                    except ValueError:
                        print("Invalid priority. Keeping current.")

                # Edit due date
                new_due_date = input(f"Due Date [{todo.due_date or 'None'}]: ").strip()
                if new_due_date or new_due_date == "":
                    todo.due_date = new_due_date if new_due_date else None

                # Update timestamp
                from datetime import datetime

                todo.updated_at = datetime.now().isoformat()

                if self.todo_manager.update_todo(todo):
                    print("Todo updated successfully!")
                else:
                    print("Failed to update todo.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")

    def handle_mark_completed(self) -> None:
        """Handle marking a todo as completed."""
        todos = self.todo_manager.get_user_todos(self.current_user)

        if not todos:
            print("You have no todos yet.")
            return

        print("\n=== SELECT TODO TO MARK AS COMPLETED ===")
        for i, todo in enumerate(todos, 1):
            if todo.status == Status.PENDING:
                print(f"{i}. {todo.title}")
            else:
                print(f"{i}. {todo.title} (Already completed)")

        try:
            choice = int(
                input("\nEnter the number of the todo to mark as completed: ").strip()
            )
            if 1 <= choice <= len(todos):
                todo = todos[choice - 1]
                if todo.status == Status.COMPLETED:
                    print("This todo is already completed.")
                else:
                    todo.status = Status.COMPLETED
                    from datetime import datetime

                    todo.updated_at = datetime.now().isoformat()
                    if self.todo_manager.update_todo(todo):
                        print("Todo marked as completed!")
                    else:
                        print("Failed to update todo.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.")


def main() -> None:
    """Entry point for the application."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()

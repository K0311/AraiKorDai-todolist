"""Unit tests for the CLI application, focusing on task 2: pre-login menu."""

import pytest
from unittest.mock import patch, MagicMock
from src.main import App


class TestPreLoginMenu:
    """Test cases for the pre-login menu functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.app = App()
        # Mock the auth_manager to control behavior
        self.app.auth_manager = MagicMock()

    @patch("builtins.input")
    @patch("builtins.print")
    def test_successful_login(self, mock_print, mock_input):
        """Test successful login through the menu."""
        # Simulate user choosing 1 (login), entering username and password
        mock_input.side_effect = ["1", "testuser", "testpass"]

        # Mock successful login
        self.app.auth_manager.login.return_value = True

        # Run the pre-login menu
        self.app.show_pre_login_menu()

        # Check that login was called with correct args
        self.app.auth_manager.login.assert_called_once_with("testuser", "testpass")

        # Check that current_user is set
        assert self.app.current_user == "testuser"

        # Check that welcome message was printed
        mock_print.assert_any_call("\nWelcome, testuser!")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_failed_login(self, mock_print, mock_input):
        """Test failed login through the menu."""
        # Simulate user choosing 1 (login), entering username and password, then invalid choice to loop
        mock_input.side_effect = ["1", "testuser", "wrongpass", "3"]

        # Mock failed login
        self.app.auth_manager.login.return_value = False

        # Run the pre-login menu, expect SystemExit on exit
        with pytest.raises(SystemExit):
            self.app.show_pre_login_menu()

        # Check that login was called
        self.app.auth_manager.login.assert_called_once_with("testuser", "wrongpass")

        # Check error message
        mock_print.assert_any_call("Invalid username or password.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_successful_signup(self, mock_print, mock_input):
        """Test successful signup through the menu."""
        # Simulate user choosing 2 (signup), entering username and password, then exit
        mock_input.side_effect = ["2", "newuser", "newpass", "3"]

        # Mock successful registration
        self.app.auth_manager.register.return_value = True

        # Run the pre-login menu, expect SystemExit
        with pytest.raises(SystemExit):
            self.app.show_pre_login_menu()

        # Check that register was called
        self.app.auth_manager.register.assert_called_once_with("newuser", "newpass")

        # Check success message
        mock_print.assert_any_call("Account created successfully for newuser!")

        # Since not logged in yet, current_user should still be None
        assert self.app.current_user is None

    @patch("builtins.input")
    @patch("builtins.print")
    def test_failed_signup_existing_user(self, mock_print, mock_input):
        """Test failed signup due to existing user."""
        # Simulate user choosing 2 (signup), entering username and password, then exit
        mock_input.side_effect = ["2", "existinguser", "pass", "3"]

        # Mock failed registration
        self.app.auth_manager.register.return_value = False

        # Run the pre-login menu, expect SystemExit
        with pytest.raises(SystemExit):
            self.app.show_pre_login_menu()

        # Check that register was called
        self.app.auth_manager.register.assert_called_once_with("existinguser", "pass")

        # Check error message
        mock_print.assert_any_call("Username already exists.")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_exit_option(self, mock_print, mock_input):
        """Test choosing exit option."""
        # Simulate user choosing 3 (exit)
        mock_input.side_effect = ["3"]

        # Run the pre-login menu, expect SystemExit
        with pytest.raises(SystemExit):
            self.app.show_pre_login_menu()

        # Check goodbye message
        mock_print.assert_any_call("Goodbye!")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_invalid_choice_then_exit(self, mock_print, mock_input):
        """Test invalid choice followed by exit."""
        # Simulate invalid choice, then exit
        mock_input.side_effect = ["invalid", "3"]

        # Run the pre-login menu, expect SystemExit
        with pytest.raises(SystemExit):
            self.app.show_pre_login_menu()

        # Check invalid message
        mock_print.assert_any_call("Invalid choice. Please try again.")

        # Check goodbye
        mock_print.assert_any_call("Goodbye!")

    @patch("builtins.input")
    @patch("builtins.print")
    def test_empty_credentials_signup(self, mock_print, mock_input):
        """Test signup with empty username or password."""
        # Simulate choosing 2, empty username, then exit
        mock_input.side_effect = ["2", "", "pass", "3"]

        # Run the pre-login menu, expect SystemExit
        with pytest.raises(SystemExit):
            self.app.show_pre_login_menu()

        # Check error message
        mock_print.assert_any_call("Username and password cannot be empty.")

        # Register should not be called
        self.app.auth_manager.register.assert_not_called()

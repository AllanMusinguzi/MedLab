import unittest
from unittest.mock import MagicMock, patch
import bcrypt
from loginPage import Login  # Replace with the actual module name

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.master = MagicMock()
        self.db = MagicMock()
        self.on_login_success = MagicMock()
        self.on_switch_to_signup = MagicMock()
        self.login = Login(self.master, self.db, self.on_login_success, self.on_switch_to_signup)

    def test_create_login_form(self):
        # Check if the login form is created correctly
        self.assertIsNotNone(self.login.login_username)
        self.assertIsNotNone(self.login.login_password)

    def test_login_success(self):
        # Mock the database cursor and its behavior
        mock_cursor = MagicMock()
        self.db.cursor.return_value = mock_cursor

        # Prepare the mock user data
        username = "allan"
        password = "allan40"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        mock_cursor.fetchone.return_value = (1, hashed_password, "test@example.com", "1234567890", username, "user")

        # Set the entry fields
        self.login.login_username.insert(0, username)
        self.login.login_password.insert(0, password)

        # Call the login method
        self.login.login()

        # Check if the login callback was called
        self.on_login_success.assert_called_once_with(username, "user")
        mock_cursor.execute.assert_called_with("""
                INSERT INTO login_logs 
                (username, success, role, timestamp)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            """, (username, True, "user"))
        self.db.commit.assert_called_once()

    def test_login_invalid_password(self):
        # Mock the database cursor and its behavior
        mock_cursor = MagicMock()
        self.db.cursor.return_value = mock_cursor

        # Prepare the mock user data
        username = "test_user"
        password = "wrong_password"
        hashed_password = bcrypt.hashpw("test_password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        mock_cursor.fetchone.return_value = (1, hashed_password, "test@example.com", "1234567890", username, "user")

        # Set the entry fields
        self.login.login_username.insert(0, username)
        self.login.login_password.insert(0, password)

        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.login.login()
            mock_showerror.assert_called_once_with("Error", "Invalid username or password.")

    def test_login_empty_fields(self):
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.login.login()
            mock_showerror.assert_called_once_with("Error", "Please enter both username and password.")

    def test_switch_to_signup(self):
        # Simulate clicking the signup button
        self.login.switch_to_signup_callback()
        self.on_switch_to_signup.assert_called_once()

    def test_clear_fields(self):
        # Set some values in the fields
        self.login.login_username.insert(0, "test_user")
        self.login.login_password.insert(0, "test_password")
        self.login.remember_me.select()

        # Clear the fields
        self.login.clear_fields()

        # Check that the fields are cleared
        self.assertEqual(self.login.login_username.get(), "")
        self.assertEqual(self.login.login_password.get(), "")
        self.assertFalse(self.login.remember_me.var.get())  # Assuming remember_me uses a variable

if __name__ == '__main__':
    unittest.main()
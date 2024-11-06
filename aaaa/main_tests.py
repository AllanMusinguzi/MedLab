import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from mysql.connector import Error
from main import MedicalLabSystem

class TestMedicalLabSystem(unittest.TestCase):

    def setUp(self):
        self.master_mock = MagicMock()
        self.app = MedicalLabSystem(self.master_mock)

    @patch('connect_to_database.mysql.connector.connect')
    def test_connect_to_database_success(self, mock_connect):
        mock_connect.return_value = MagicMock()
        self.app.connect_to_database()
        self.assertIsNotNone(self.app.db)
        self.master_mock.after.assert_called_with(0, self.app.initialize_app)

    @patch('connect_to_database.mysql.connector.connect')
    def test_connect_to_database_failure(self, mock_connect):
        mock_connect.side_effect = Error("Connection failed")
        self.app.connect_to_database()
        self.master_mock.after.assert_called_with(0, self.app.show_connection_error, "Connection failed")

    @patch('os.path.exists')
    @patch('load_config.configparser.ConfigParser.read')
    def test_load_config_success(self, mock_read, mock_exists):
        mock_exists.return_value = True
        self.app.load_config()
        mock_read.assert_called_once()

    @patch('os.path.exists')
    def test_load_config_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(SystemExit):
            self.app.load_config()

    def test_show_loading_screen(self):
        self.app.show_loading_screen()
        self.assertIsNotNone(self.app.loading_screen)

    def test_hide_loading_screen(self):
        self.app.show_loading_screen()
        self.app.hide_loading_screen()
        self.assertIsNone(self.app.loading_screen)

    @patch('show_login.Login')
    def test_show_login(self, mock_login):
        self.app.show_login()
        mock_login.assert_called_once()

    @patch('show_signup.Signup')
    def test_show_signup(self, mock_signup):
        self.app.show_signup()
        mock_signup.assert_called_once()

    @patch('show_user_page.UserPage')
    def test_show_user_page(self, mock_user_page):
        self.app.show_user_page(1, 'testuser', 'password', '1234567890')
        mock_user_page.assert_called_once()

    @patch('show_admin_page.AdminDashboard')
    def test_show_admin_page(self, mock_admin_page):
        self.app.show_admin_page(1, 'testuser', 'password', '1234567890')
        mock_admin_page.assert_called_once()

    @patch('show_superadmin_page.SuperAdminPage')
    def test_show_superadmin_page(self, mock_superadmin_page):
        self.app.show_superadmin_page(1, 'testuser', 'password', '1234567890')
        mock_superadmin_page.assert_called_once()

    def test_clear_current_frame(self):
        self.app.current_frame = MagicMock()
        self.app.clear_current_frame()
        self.app.current_frame.destroy.assert_called_once()

    @patch('login_callback.messagebox.showerror')
    def test_login_callback_success(self, mock_showerror):
        self.app.db.cursor = MagicMock()
        self.app.db.cursor.return_value.fetchone.return_value = (1, '1234567890', 'password')
        self.app.login_callback('testuser', 'user')
        self.assertIsNotNone(self.app.current_session)

    @patch('login_callback.messagebox.showerror')
    def test_login_callback_user_not_found(self, mock_showerror):
        self.app.db.cursor = MagicMock()
        self.app.db.cursor.return_value.fetchone.return_value = None
        self.app.login_callback('testuser', 'user')
        mock_showerror.assert_called_with("Error", "User details not found.")

    @patch('login_callback.messagebox.showerror')
    def test_login_callback_invalid_role(self, mock_showerror):
        self.app.db.cursor = MagicMock()
        self.app.db.cursor.return_value.fetchone.return_value = (1, '1234567890', 'password')
        self.app.login_callback('testuser', 'invalid_role')
        mock_showerror.assert_called_with("Error", "Invalid user role.")

    @patch('logout_callback.messagebox.showerror')
    def test_logout_callback(self, mock_showerror):
        self.app.logout_callback()
        self.assertIsNotNone(self.app.login_frame)

if __name__ == '__main__':
    unittest.main()
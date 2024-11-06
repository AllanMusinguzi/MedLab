import customtkinter as ctk
from tkinter import messagebox, filedialog
import mysql.connector
import bcrypt
import json
import psutil
import os
import csv
import subprocess
import configparser
from datetime import datetime
import configparser
import mysql.connector

class SuperAdminDashboard:
    def __init__(self, db, user_id, username, password, phone_number, logout_callback):
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.logout_callback = logout_callback

        # Configure default theme
        ctk.set_appearance_mode("dark")  # Default theme
        ctk.set_default_color_theme("blue")

        # Create main window
        self.window = ctk.CTk()
        self.window.title("Super Administrator Dashboard")
        self.window.geometry("1200x800")

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Create main layout
        self.create_header()
        self.create_sidebar()
        self.create_main_content()

    def create_header(self):
        # Header frame
        self.header = ctk.CTkFrame(self.window, height=60)
        self.header.pack(fill="x", padx=20, pady=(10, 0))

        # Title
        ctk.CTkLabel(
            self.header, 
            text=f"Super Administrator Dashboard - {self.username}",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=10)

        # Theme switcher
        theme_options = ["Light", "Dark", "System"]
        self.theme_var = ctk.StringVar(value="Dark")
        theme_menu = ctk.CTkOptionMenu(
            self.header,
            values=theme_options,
            variable=self.theme_var,
            command=self.change_theme
        )
        theme_menu.pack(side="right", padx=10)

        # Logout button
        ctk.CTkButton(
            self.header,
            text="Logout",
            command=self.logout_callback
        ).pack(side="right", padx=10)

    def create_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.window, width=200)
        self.sidebar.pack(side="left", fill="y", padx=(20, 10), pady=10)

        # Navigation buttons
        buttons = [
            ("User Management", self.show_user_management),
            ("System Settings", self.show_system_settings),
            ("Audit Logs", self.show_audit_logs),
            ("Login Logs", self.show_login_logs)
        ]

        for text, command in buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=40
            ).pack(padx=10, pady=5, fill="x")

    def create_main_content(self):
        # Main content frame
        self.main_content = ctk.CTkFrame(self.window)
        self.main_content.pack(side="right", fill="both", expand=True, padx=(10, 20), pady=10)

        # Initialize content frames (hidden initially)
        self.user_management_frame = self.create_user_management_frame()
        self.system_settings_frame = self.create_system_settings_frame()
        self.audit_logs_frame = self.create_audit_logs_frame()
        self.login_logs_frame = self.create_login_logs_frame()

        # Show default view
        self.show_user_management()

    def create_user_management_frame(self):
        frame = ctk.CTkFrame(self.main_content)

        # Controls
        controls = ctk.CTkFrame(frame)
        controls.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Add New User",
            command=self.show_add_user
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls,
            text="Modify Selected",
            command=self.modify_user
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls,
            text="Delete Selected",
            command=self.delete_user
        ).pack(side="left", padx=5)

        # User table
        columns = ("ID", "Username", "Role", "Phone", "Status")
        self.user_tree = self.create_treeview(frame, columns)
        self.user_tree.pack(fill="both", expand=True, padx=10, pady=5)

        return frame

    def create_system_settings_frame(self):
        frame = ctk.CTkFrame(self.main_content)

        # Database controls
        db_frame = ctk.CTkFrame(frame)
        db_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            db_frame,
            text="Database Management",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)

        ctk.CTkButton(
            db_frame,
            text="Backup Database",
            command=self.backup_database
        ).pack(side="left", padx=5, pady=5)

        ctk.CTkButton(
            db_frame,
            text="Restore Database",
            command=self.restore_database
        ).pack(side="left", padx=5, pady=5)

        # System maintenance
        maint_frame = ctk.CTkFrame(frame)
        maint_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            maint_frame,
            text="System Maintenance",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)

        ctk.CTkButton(
            maint_frame,
            text="Clear Audit Logs",
            command=self.clear_audit_logs
        ).pack(side="left", padx=5, pady=5)

        ctk.CTkButton(
            maint_frame,
            text="System Health Check",
            command=self.system_health_check
        ).pack(side="left", padx=5, pady=5)

        return frame

    def create_audit_logs_frame(self):
        frame = ctk.CTkFrame(self.main_content)

        # Controls
        controls = ctk.CTkFrame(frame)
        controls.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Export Logs",
            command=self.export_audit_logs
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            controls,
            text="Refresh",
            command=self.refresh_audit_logs
        ).pack(side="left", padx=5)

        # Audit logs table
        columns = ("Timestamp", "User", "Action", "Details")
        self.audit_tree = self.create_treeview(frame, columns)
        self.audit_tree.pack(fill="both", expand=True, padx=10, pady=5)

        return frame

    def create_login_logs_frame(self):
        frame = ctk.CTkFrame(self.main_content)

        # Login logs table
        columns = ("ID", "Username", "Success", "Role", "Timestamp")
        self.login_tree = self.create_treeview(frame, columns)
        self.login_tree.pack(fill="both", expand=True, padx=10, pady=5)

        return frame

    def create_treeview(self, parent, columns):
        tree = ctk.CTkTable(
            parent,
            column=len(columns),
            header=columns,
            values=[[""]*len(columns)]*10  # Empty rows initially
        )
        return tree

    def change_theme(self, new_theme):
        if new_theme == "System":
            ctk.set_appearance_mode("system")
        else:
            ctk.set_appearance_mode(new_theme.lower())

    def show_user_management(self):
        self.hide_all_frames()
        self.user_management_frame.pack(fill="both", expand=True)

    def show_system_settings(self):
        self.hide_all_frames()
        self.system_settings_frame.pack(fill="both", expand=True)

    def show_audit_logs(self):
        self.hide_all_frames()
        self.audit_logs_frame.pack(fill="both", expand=True)

    def show_login_logs(self):
        self.hide_all_frames()
        self.login_logs_frame.pack(fill="both", expand=True)

    def hide_all_frames(self):
        for frame in [self.user_management_frame, self.system_settings_frame,
                     self.audit_logs_frame, self.login_logs_frame]:
            frame.pack_forget()

    # The rest of the methods (database operations, user management, etc.) remain
    # largely the same as in your original code, just updated to use CustomTkinter
    # widgets where appropriate. I'll show a few key ones:

    def show_add_user(self):
        dialog = ctk.CTkToplevel(self.window)
        dialog.title("Add New User")
        dialog.geometry("500x600")

        # Create form fields
        fields = [
            ("Full Name:", "full_name"),
            ("Email:", "email"),
            ("Phone Number:", "phone"),
            ("Username:", "username"),
            ("Password:", "password", True),
            ("Confirm Password:", "confirm_password", True),
            ("Address:", "address")
        ]

        entries = {}
        for i, field in enumerate(fields):
            label_text = field[0]
            field_name = field[1]
            is_password = len(field) > 2 and field[2]

            ctk.CTkLabel(dialog, text=label_text).pack(padx=20, pady=(10, 0))
            entry = ctk.CTkEntry(dialog, show="*" if is_password else "")
            entry.pack(padx=20, pady=(0, 10), fill="x")
            entries[field_name] = entry

        # Role selector
        ctk.CTkLabel(dialog, text="Role:").pack(padx=20, pady=(10, 0))
        role_var = ctk.StringVar(value="User")
        role_menu = ctk.CTkOptionMenu(
            dialog,
            values=["User", "Admin", "SuperAdmin"],
            variable=role_var
        )
        role_menu.pack(padx=20, pady=(0, 10), fill="x")

        # Preferences
        pref_frame = ctk.CTkFrame(dialog)
        pref_frame.pack(padx=20, pady=10, fill="x")

        ctk.CTkLabel(
            pref_frame,
            text="Preferences",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=5)

        prefs = {}
        for pref in ["Notifications", "Newsletter", "Dark Mode"]:
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(
                pref_frame,
                text=pref,
                variable=var
            ).pack(pady=2)
            prefs[pref.lower().replace(" ", "_")] = var

        def save_user():
            # Collect all the data
            data = {
                field[1]: entries[field[1]].get()
                for field in fields
            }
            
            # Validate
            if not all(data.values()):
                messagebox.showerror("Error", "Please fill in all fields")
                return

            if data["password"] != data["confirm_password"]:
                messagebox.showerror("Error", "Passwords do not match")
                return

            # Hash password
            hashed_pw = bcrypt.hashpw(
                data["password"].encode('utf-8'),
                bcrypt.gensalt()
            )

            # Collect preferences
            preferences = {
                k: v.get() for k, v in prefs.items()
            }

            try:
                cursor = self.db.cursor()
                cursor.execute("""
                    INSERT INTO users (
                        full_name, email, phone_number, username,
                        password, address, role, preferences
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    data["full_name"], data["email"], data["phone"],
                    data["username"], hashed_pw.decode('utf-8'),
                    data["address"], role_var.get(),
                    json.dumps(preferences)
                ))
                self.db.commit()
                messagebox.showinfo("Success", "User added successfully")
                dialog.destroy()
                self.load_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.db.rollback()

        ctk.CTkButton(
            dialog,
            text="Save User",
            command=save_user
        ).pack(pady=20)

    def run(self):
        self.window.mainloop()

'''

if __name__ == "__main__":
    # Read configuration
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Setup database connection using config
    db = mysql.connector.connect(
        host=config['DATABASE']['host'],
        user=config['DATABASE']['user'],
        password=config['DATABASE']['password'],
        database=config['DATABASE']['database']
    )

    # Get user data from config
    user_data = {
        "user_id": config['user'].getint('user_id'),
        "username": config['user']['username'],
        "password": config['user']['password'],
        "phone_number": config['user']['phone_number']
    }

    # Create and run the dashboard
    app = SuperAdminDashboard(
        db=db,
        user_id=user_data["user_id"],
        username=user_data["username"],
        password=user_data["password"],
        phone_number=user_data["phone_number"],
        logout_callback=lambda: print("Logout clicked")
    )
    app.run()


'''    
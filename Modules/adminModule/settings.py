import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox


class AdminSettings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = None
        self.create_settings_frame()

    def create_settings_frame(self):
        # Title Frame
        settings_frame = tk.LabelFrame(self, text="Admin Settings")
        settings_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        settings_frame.columnconfigure(0, weight=1)

        # Change Admin Password
        self.add_password_section(settings_frame)

        # Application Theme
        self.add_theme_section(settings_frame)

        # Database Settings
        self.add_database_section(settings_frame)

    def add_password_section(self, frame):
        # Password Section
        password_frame = ctk.CTkFrame(frame)
        password_frame.grid(row=1, column=0, padx=10, pady=(10, 20), sticky="ew")
        password_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(password_frame, text="New Password:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.new_password_entry = ctk.CTkEntry(password_frame, show="*")
        self.new_password_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(password_frame, text="Update Password", command=self.update_password).grid(row=0, column=2, padx=5)

    def add_theme_section(self, frame):
        # Theme Section
        theme_frame = ctk.CTkFrame(frame)
        theme_frame.grid(row=2, column=0, padx=10, pady=(10, 20), sticky="ew")
        theme_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(theme_frame, text="Select Theme:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.theme_option = ctk.CTkOptionMenu(theme_frame, values=["Light", "Dark", "System"], command=self.change_theme)
        self.theme_option.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def add_database_section(self, frame):
        # Database Section
        db_frame = ctk.CTkFrame(frame)
        db_frame.grid(row=3, column=0, padx=10, pady=(10, 20), sticky="ew")
        db_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(db_frame, text="Host:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.db_host_entry = ctk.CTkEntry(db_frame)
        self.db_host_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(db_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.db_port_entry = ctk.CTkEntry(db_frame)
        self.db_port_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(db_frame, text="User:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.db_user_entry = ctk.CTkEntry(db_frame)
        self.db_user_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(db_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.db_password_entry = ctk.CTkEntry(db_frame, show="*")
        self.db_password_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkButton(db_frame, text="Save Database Settings", command=self.save_database_settings).grid(row=4, column=1, pady=10)

    def update_password(self):
        new_password = self.new_password_entry.get()
        if new_password:
            cursor = self.db.cursor()
            try:
                cursor.execute("UPDATE admin SET password = %s WHERE admin_id = 1", (new_password,))
                self.db.commit()
                messagebox.showinfo("Success", "Password updated successfully.")
                self.new_password_entry.delete(0, 'end')
            except Exception as e:
                self.db.rollback()
                messagebox.showerror("Error", f"Failed to update password: {str(e)}")
            finally:
                cursor.close()
        else:
            messagebox.showwarning("Input Required", "Please enter a new password.")

    def change_theme(self, choice):
        theme = choice.lower()
        if theme == "light":
            ctk.set_appearance_mode("light")
        elif theme == "dark":
            ctk.set_appearance_mode("dark")
        elif theme == "system":
            ctk.set_appearance_mode("system")

    def save_database_settings(self):
        host = self.db_host_entry.get()
        port = self.db_port_entry.get()
        user = self.db_user_entry.get()
        password = self.db_password_entry.get()

        if all([host, port, user, password]):
            # Simulate saving to a config or db
            # e.g., save these values to a config file or settings table
            try:
                # Here you would typically update the db connection config
                messagebox.showinfo("Success", "Database settings saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save database settings: {str(e)}")
        else:
            messagebox.showwarning("Incomplete Data", "Please fill in all database fields.")

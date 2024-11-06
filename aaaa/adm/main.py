# main.py
import customtkinter as ctk
import tkinter as tk
from modules.dashboard_view import DashboardView
from modules.patients_view import PatientsView
from modules.tests_view import TestsView
from modules.results_view import ResultsView
from modules.settings_view import SettingsView
from utils.theme_manager import ThemeManager
from utils.database import Database

class AdminDashboard:
    def __init__(self):
        # Initialize database connection
        self.db = Database()
        
        # Set theme and color scheme
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme("dark")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Healthcare Admin Dashboard")
        self.root.geometry("1200x700")

        # Create main grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Initialize views
        self.views = {
            'dashboard': DashboardView,
            'patients': PatientsView,
            'tests': TestsView,
            'results': ResultsView,
            'settings': SettingsView
        }
        
        self.current_view = None
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()

        # Initialize default view
        self.show_view('dashboard')

    def create_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        # Logo label
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="Healthcare Admin", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Navigation buttons with icons (you'll need to add actual icons)
        nav_buttons = [
            ("Dashboard", "dashboard", "📊"),
            ("Patients", "patients", "👥"),
            ("Tests", "tests", "🔬"),
            ("Results", "results", "📋"),
            ("Settings", "settings", "⚙️")
        ]
        
        for idx, (text, view_name, icon) in enumerate(nav_buttons):
            button = ctk.CTkButton(
                self.sidebar,
                text=f"{icon} {text}",
                command=lambda v=view_name: self.show_view(v),
                anchor="w",
                height=40
            )
            button.grid(row=idx + 1, column=0, padx=20, pady=10, sticky="ew")

    def create_main_content(self):
        self.main_content = ctk.CTkFrame(self.root)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)

    def show_view(self, view_name):
        # Clear current view
        if self.current_view:
            self.current_view.destroy()

        # Create new view
        view_class = self.views[view_name]
        self.current_view = view_class(self.main_content, self.db)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdminDashboard()
    app.run()
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import random

class AdminDashboard:
    def __init__(self):
        # Set theme and color scheme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Healthcare Admin Dashboard")
        self.root.geometry("1200x700")

        # Create main grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()

        # Initialize default view
        self.show_dashboard()

    def create_sidebar(self):
        # Sidebar frame
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)

        # Logo label
        self.logo_label = ctk.CTkLabel(self.sidebar, text="Healthcare Admin", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=20)

        # Navigation buttons
        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Patients", self.show_patients),
            ("Tests", self.show_tests),
            ("Results", self.show_results),
            ("Settings", self.show_settings)
        ]
        for idx, (text, command) in enumerate(nav_buttons):
            button = ctk.CTkButton(self.sidebar, text=text, command=command)
            button.grid(row=idx + 1, column=0, padx=20, pady=10)

    def create_main_content(self):
        # Main content frame
        self.main_content = ctk.CTkFrame(self.root)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_content.grid_columnconfigure(0, weight=1)

    def show_dashboard(self):
        # Clear main content
        self.clear_main_content()

        # Header
        header = ctk.CTkLabel(self.main_content, text="Dashboard Overview", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Stats summary
        stats_frame = ctk.CTkFrame(self.main_content)
        stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Statistics cards
        self.create_stat_card(stats_frame, "Total Patients", "1,235", 0)
        self.create_stat_card(stats_frame, "Pending Tests", "54", 1)
        self.create_stat_card(stats_frame, "Completed Tests", "789", 2)
        self.create_stat_card(stats_frame, "Positive Cases", "312", 3)

        # Visualization frame (for graphs)
        viz_frame = ctk.CTkFrame(self.main_content)
        viz_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        viz_frame.grid_columnconfigure((0,1), weight=1)

        # Placeholder for graphs (replace with actual graph integration)
        self.create_viz_placeholder(viz_frame, "Monthly Active Users", 0)
        self.create_viz_placeholder(viz_frame, "Test Results Distribution", 1)

    def create_viz_placeholder(self, parent, title, col):
        viz_card = ctk.CTkFrame(parent, height=200)
        viz_card.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        title_label = ctk.CTkLabel(viz_card, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=20)
        # Insert graph creation code here (e.g., using matplotlib)

    def show_patients(self):
        self.clear_main_content()
        header = ctk.CTkLabel(self.main_content, text="Patients Overview", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Patients Table
        columns = ('ID', 'Name', 'Age', 'Contact', 'Status')
        self.create_table(self.main_content, columns, "patients")

    def show_tests(self):
        self.clear_main_content()
        header = ctk.CTkLabel(self.main_content, text="Tests Overview", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Tests Table
        columns = ('Test ID', 'Patient ID', 'Type', 'Date', 'Status')
        self.create_table(self.main_content, columns, "tests")

    def show_results(self):
        self.clear_main_content()
        header = ctk.CTkLabel(self.main_content, text="Test Results", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Results Table
        columns = ('Result ID', 'Patient ID', 'Test Type', 'Result', 'Date')
        self.create_table(self.main_content, columns, "results")

    def show_settings(self):
        self.clear_main_content()
        header = ctk.CTkLabel(self.main_content, text="Settings", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Settings form
        settings_frame = ctk.CTkFrame(self.main_content)
        settings_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Theme selection
        theme_label = ctk.CTkLabel(settings_frame, text="Theme Mode:")
        theme_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        theme_menu = ctk.CTkOptionMenu(settings_frame, values=["Dark", "Light"])
        theme_menu.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    def create_stat_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
        title_label = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14))
        title_label.grid(row=0, column=0, padx=20, pady=5)
        value_label = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=20, weight="bold"))
        value_label.grid(row=1, column=0, padx=20, pady=5)

    def create_table(self, parent, columns, data_type):
        tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add sample data based on type
        data_samples = {
            "patients": [('1', 'Alice Brown', '29', '555-1234', 'Active')],
            "tests": [('101', '1', 'Blood Test', '2023-10-01', 'Pending')],
            "results": [('1001', '1', 'Blood Test', 'Negative', '2023-10-02')]
        }
        for row in data_samples.get(data_type, []):
            tree.insert('', tk.END, values=row)
        tree.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AdminDashboard()
    app.run()

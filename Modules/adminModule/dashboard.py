import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import mysql.connector

from Modules.adminModule.patients import PatientManagement
from Modules.adminModule.results import ResultsFrame
from Modules.adminModule.settings import AdminSettings
from Modules.adminModule.tests import TestManagement
from Modules.adminModule.analytics import AnalyticsView

class AdminDashboard:
    def __init__(self, master, db, user_id, username, password, phone_number, logout_callback=None):
        self.master = master
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.email, self.role, self.profile_picture = self.get_user_details(user_id)
        self.logout_callback = logout_callback
        
        # Configure the main window
        if isinstance(self.master, (ctk.CTk, ctk.CTkToplevel)):
            self.master.title("Admin Dashboard")
            self.master.geometry("1400x800")
            
        # Set the color theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # main layout frames
        self.create_layout()
        
        self.show_dashboard_content()

    def create_layout(self):
        self.main_container = ctk.CTkFrame(self.master, fg_color="#f0f0f0")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left sidebar for navigation
        self.sidebar = ctk.CTkFrame(self.main_container, width=280, bg_color="#2C3E50")
        self.sidebar.pack(side="left", fill="y", padx=(0, 20))
        self.sidebar.pack_propagate(False)
        
        self.create_profile_section()
        
        self.create_navigation()
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self.main_container)
        self.main_frame.pack(side="right", fill="both", expand=True)

    def get_user_details(self, user_id):
        try:
            cursor = self.db.cursor()
            query = "SELECT email, role, profile_picture FROM users WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                email, role, profile_picture = result
                if os.path.exists(profile_picture):
                    return email, role, profile_picture
                else:
                    return email, role, None
            else:
                return "admin@example.com", "Administrator", None
        except mysql.connector.Error as err:
            print(f"Error fetching user details: {err}")
            return "admin@example.com", "Administrator", None

    def create_profile_section(self):
        
        self.profile_frame = ctk.CTkFrame(self.sidebar, fg_color="#3d5667")
        self.profile_frame.pack(fill="x", padx=20, pady=20)
        
        # Load and display profile picture
        if self.profile_picture:
            profile_image = Image.open(self.profile_picture)
            profile_image = profile_image.resize((100, 100), resample=Image.LANCZOS)
            self.profile_image = ImageTk.PhotoImage(profile_image)
        else:
            self.profile_image = ctk.CTkImage(size=(100, 100))
        
        self.profile_pic = ctk.CTkButton(
            self.profile_frame,
            image=self.profile_image,
            text="",
            width=50,
            height=50,
            corner_radius=50,
            fg_color="#2b2b2b",
            hover_color="#404040",
            command=self.toggle_profile_details
        )
        self.profile_pic.pack(pady=(10, 10))
        
        # Profile details (initially hidden)
        self.profile_details = ctk.CTkFrame(self.profile_frame, fg_color="#f0f0f0")
        self.profile_details_visible = False
        
        # labels for user details
        details = [
            ("Name", self.username),
            ("Email", self.email),
            ("Contact", self.phone_number),
            ("Role", self.role),
            ("ID", self.user_id)
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(self.profile_details, fg_color="transparent")
            detail_frame.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(
                detail_frame,
                text=f"{label}:",
                font=("Ubuntu", 12, "bold"),
                anchor="w",
                text_color="#2C3E50"
            ).pack(side="left")
            
            ctk.CTkLabel(
                detail_frame,
                text=value,
                font=("Ubuntu", 12),
                anchor="e",
                text_color="#2C3E50"
            ).pack(side="right")
            
    def toggle_profile_details(self):
        if self.profile_details_visible:
            self.profile_details.pack_forget()
        else:
            self.profile_details.pack(fill="x", pady=(10, 0))
        self.profile_details_visible = not self.profile_details_visible
        
    def create_navigation(self):
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="#e0e0e0")
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        nav_items = [
            ("Dashboard", "home.png", self.show_dashboard_content),
            ("Patients", "patients.png", self.show_patients_content),
            ("Tests", "tests.png", self.show_tests_content),
            ("Results", "results.png", self.show_results_content),
            ("Analytics", "analytics.png", self.show_analytics_content),
            ("Settings", "settings.png", self.show_settings_content)
        ]
        
        for text, icon_name, command in nav_items:
            # Get the path to the current file (e.g., dashboard.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Construct the relative path to the icon file
            icon_path = os.path.join(current_dir, '..', '..', 'icons', icon_name)
            
            # Load and resize the icon image
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((30, 30), resample=Image.LANCZOS)
            nav_icon = ctk.CTkImage(light_image=icon_image, dark_image=icon_image)
            
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                image=nav_icon,
                font=("Ubuntu", 16),
                height=45,
                anchor="w",
                fg_color="#2C3E50",
                text_color="#f0f0f0",
                hover_color="#3d5667",
                corner_radius=0,
                command=command
            )
            btn.pack(fill="x", pady=5, padx=10)
        
        # Logout button at the bottom
        logout_button = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            height=45,
            font=("Ubuntu", 14),
            fg_color="#FF5252",
            hover_color="#FF1A1A",
            corner_radius=0,
            command=self.handle_logout
        )
        logout_button.pack(side="bottom", fill="x", padx=20, pady=20)
        
    def show_dashboard_content(self):
        self.clear_main_frame()
        
        # Header with refresh timestamp
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 20))
        
        header_left = ctk.CTkFrame(header, fg_color="transparent")
        header_left.pack(side="left", fill="y")
        
        ctk.CTkLabel(
            header_left,
            text="Dashboard Overview",
            font=("Ubuntu", 24, "bold"),
            text_color="#2C3E50"
        ).pack(side="top")
        
        self.update_label = ctk.CTkLabel(
            header_left,
            text=f"Last updated: {datetime.now().strftime('%H:%M:%S')}",
            font=("Ubuntu", 12),
            text_color="#7F8C8D"
        )
        self.update_label.pack(side="top")

        # Statistics cards frame
        stats_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30)
        
        # Fetch current statistics
        with self.db.cursor() as cursor:
            # Total Patients
            cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = cursor.fetchone()[0]
            
            # Active Tests
            cursor.execute("SELECT COUNT(*) FROM tests")
            total_tests = cursor.fetchone()[0]
            

            cursor.execute("SELECT COUNT(*) FROM patient_tests")
            completed_tests = cursor.fetchone()[0]
            
            # Pending Results
            cursor.execute(" SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

        stats = [
            ("Total Patients", f"{total_patients:,}", "#4CAF50"),
            ("Available Tests", f"{total_tests:,}", "#2196F3"),
            ("Completed Tests", f"{completed_tests:,}", "#FF9800"),
            ("Total Users", f"{total_users:,}", "#F44336")
        ]

        # Generate stat cards with hover effect
        for title, value, color in stats:
            stat_card = ctk.CTkFrame(stats_frame, fg_color="#f0f0f0", corner_radius=10)
            stat_card.pack(side="left", fill="both", expand=True, padx=5)
            
            # Add hover effect
            stat_card.bind("<Enter>", lambda e, card=stat_card: card.configure(fg_color="#e8e8e8"))
            stat_card.bind("<Leave>", lambda e, card=stat_card: card.configure(fg_color="#f0f0f0"))
            
            # Title with icon (you can add icons based on the stat type)
            title_frame = ctk.CTkFrame(stat_card, fg_color="transparent")
            title_frame.pack(pady=(15, 5))
            
            ctk.CTkLabel(
                title_frame,
                text=title,
                font=("Ubuntu", 14),
                text_color="#2C3E50"
            ).pack()
            
            # Value with trend indicator
            value_frame = ctk.CTkFrame(stat_card, fg_color="transparent")
            value_frame.pack(pady=(0, 15))
            
            ctk.CTkLabel(
                value_frame,
                text=value,
                font=("Ubuntu", 24, "bold"),
                text_color=color
            ).pack()
            
        # Charts section
        charts_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Left chart
        left_chart = self.create_line_chart(charts_frame, "Patient Visits Trend")
        left_chart.pack(side="left", fill="both", expand=True, padx=5)
        
        # Right chart
        right_chart = self.create_pie_chart(charts_frame, "Test Results Distribution")
        right_chart.pack(side="left", fill="both", expand=True, padx=5)

    def create_line_chart(self, frame, title=""):
        chart_frame = ctk.CTkFrame(frame, fg_color="#f0f0f0", corner_radius=10)
        
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        visits = np.random.randint(10, 50, size=30)
        
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(dates, visits, color="#2196F3")
        ax.set_title(title, pad=20, color="#2C3E50")
        ax.set_xlabel("Date", color="#2C3E50")
        ax.set_ylabel("Number of Visits", color="#2C3E50")
        fig.autofmt_xdate()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        return chart_frame
        
    def create_pie_chart(self, frame, title=""):
        chart_frame = ctk.CTkFrame(frame, fg_color="#f0f0f0", corner_radius=10)
        
        labels = ['Normal', 'Abnormal', 'Inconclusive']
        sizes = [65, 25, 10]
        colors = ['#4CAF50', '#F44336', '#9E9E9E']
        
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title(title, pad=20, color="#2C3E50")
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        return chart_frame
        
    def show_patients_content(self):
        self.clear_main_frame()
        patient_management = PatientManagement(self.main_frame)
        patient_management.db = self.db
        patient_management.pack(fill="both", expand=True)
        
    def show_tests_content(self):
        self.clear_main_frame()
        test_management = TestManagement(self.main_frame)
        test_management.db = self.db
        test_frame = test_management.create_test_management_frame()
        test_frame.pack(fill="both", expand=True)
        
    def show_results_content(self):
        self.clear_main_frame()
        results_management = ResultsFrame(self.main_frame)
        results_management.db = self.db
        results_management.pack(fill="both", expand=True)
        
    def show_analytics_content(self):
        self.clear_main_frame()
        analytics_management = AnalyticsView(self.main_frame)
        analytics_management.db = self.db
        analytics_frame = analytics_management.create_analytics_management_frame()
        analytics_frame.pack(fill="both", expand=True)
        
    def show_settings_content(self):
        self.clear_main_frame()
        settings_management = AdminSettings(self.main_frame)
        settings_management.db = self.db
        settings_management.pack(fill="both", expand=True)
        
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
    def handle_logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            if self.logout_callback:
                self.logout_callback()
            self.master.destroy()
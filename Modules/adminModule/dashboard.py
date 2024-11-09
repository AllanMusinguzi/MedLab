import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime, timedelta
from tkinter import (
    Frame,
    Button,
    Label,
    Checkbutton,
    BooleanVar,
    Toplevel,
    LEFT, RIGHT, TOP, BOTH, X, Y,  # Constants for positioning
    RAISED, FLAT,  # Constants for relief/border style
)
import os

from Modules.adminModule.patients import PatientManagement
from Modules.adminModule.results import ResultsFrame
from Modules.adminModule.settings import AdminSettings
from Modules.adminModule.tests import TestManagement
from Modules.adminModule.analytics import AnalyticsView

class AdminDashboard:
    def __init__(self, master, db, user_id, username, password, phone_number, logout_callback):
        self.master = master
        self.db = db
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.logout_callback = logout_callback

        # Configure the main window
        if isinstance(self.master, (tk.Tk, tk.Toplevel)):
            self.master.title("Admin Dashboard")
            self.master.geometry("1200x800")

        try:
            # Create a top-level menu without tearoff
            self.menubar = tk.Menu(master)
            
            # Create File menu (disable tearoff)
            self.file_menu = tk.Menu(self.menubar, tearoff=0)
            self.file_menu.add_command(label="Export", command=self.export_data)
            self.file_menu.add_separator()
            self.file_menu.add_command(label="Exit", command=self.handle_logout)
            
            # Create Settings menu (disable tearoff)
            self.settings_menu = tk.Menu(self.menubar, tearoff=0)
            self.settings_menu.add_command(label="Preferences", command=self.show_settings_content)
            
            # Add cascading menus to the menubar
            self.menubar.add_cascade(label="File", menu=self.file_menu)
            self.menubar.add_cascade(label="Settings", menu=self.settings_menu)
            
            # Configure the root window to use the menubar
            self.master.configure(menu=self.menubar)
        except Exception as e:
            print(f"Menu creation error: {e}")
            # Continue without menu if there's an error
            self.create_toolbar()

        # Navigation frame
        self.nav_frame = Frame(self.master, bg="#2c3e50", width=200)
        self.nav_frame.pack(side=LEFT, fill=Y)
        self.nav_frame.pack_propagate(False)

        # Main content frame
        self.main_frame = Frame(self.master, bg="white")
        self.main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        # Create layout and start with dashboard
        self.create_navigation()
        self.show_dashboard_content()

    def create_toolbar(self):
        """Create a toolbar as an alternative to menu"""
        toolbar = Frame(self.master, bd=1, relief=RAISED)
        toolbar.pack(side=TOP, fill=X)

        # Add toolbar buttons
        btn_export = Button(toolbar, text="Export", command=self.export_data)
        btn_export.pack(side=LEFT, padx=2, pady=2)
        
        btn_settings = Button(toolbar, text="Settings", command=self.show_settings_content)
        btn_settings.pack(side=LEFT, padx=2, pady=2)
        

    def create_navigation(self):
        nav_style = {
            "font": ("Ubuntu", 12),
            "bg": "#2c3e50",
            "fg": "white",
            "bd": 0,
            "relief": FLAT,
            "activebackground": "#34495e",
            "activeforeground": "white",
            "width": 25,
            "cursor": "hand2"
        }

        nav_items = [
            ("Dashboard", self.show_dashboard_content),
            ("Patients", self.show_patients_content),
            ("Tests", self.show_tests_content),
            ("Results", self.show_results_content),
            ("Analytics", self.show_analytics_content),
            ("Settings", self.show_settings_content),
            ("Logout", self.handle_logout)
        ]

        for text, command in nav_items:
            btn = Button(self.nav_frame, text=text, command=command, **nav_style)
            btn.pack(pady=5, padx=5)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#34495e"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#2c3e50"))

    def create_chart_frame(self):
        chart_frame = Frame(self.main_frame, bg="white")
        chart_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        return chart_frame

    def create_line_chart(self, frame, title=""):
        # Sample data for patient visits over time
        dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
        visits = np.random.randint(10, 50, size=30)

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.plot(dates, visits)
        ax.set_title(title)
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Visits")
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        return canvas.get_tk_widget()

    def create_pie_chart(self, frame, title=""):
        labels = ['Normal', 'Abnormal', 'Inconclusive']
        sizes = [65, 25, 10]
        colors = ['#2ecc71', '#e74c3c', '#95a5a6']

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        return canvas.get_tk_widget()

    def show_dashboard_content(self):
        self.clear_main_frame()
        
        # Header
        Label(self.main_frame, text="Dashboard Overview", font=("Ubuntu", 20, "bold"), bg="white").pack(pady=20)

        # Statistics Row
        stats_frame = Frame(self.main_frame, bg="white")
        stats_frame.pack(fill=X, padx=20)

        stats = [
            ("Total Patients", "1,234"),
            ("Active Tests", "156"),
            ("Completed Today", "45"),
            ("Pending Results", "23")
        ]

        for title, value in stats:
            stat_box = Frame(stats_frame, bg="#f0f0f0", padx=20, pady=15)
            stat_box.pack(side=LEFT, expand=True, fill=BOTH, padx=5)
            Label(stat_box, text=title, font=("Ubuntu", 12), bg="#f0f0f0").pack()
            Label(stat_box, text=value, font=("Ubuntu", 20, "bold"), bg="#f0f0f0").pack()

        # Charts Row
        charts_frame = Frame(self.main_frame, bg="white")
        charts_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Left chart
        left_chart = self.create_line_chart(charts_frame, "Patient Visits Trend")
        left_chart.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        # Right chart
        right_chart = self.create_pie_chart(charts_frame, "Test Results Distribution")
        right_chart.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

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

    def export_data(self):
        from tkinter import filedialog, messagebox
        import csv
        from datetime import datetime

        # Create export options
        export_options = [
            ("Patients", "patients"),
            ("Test Results", "results"),
            ("Analytics Data", "analytics")
        ]

        try:
            # Create export dialog window
            export_window = Toplevel(self.master)
            export_window.title("Export Data")
            export_window.geometry("300x400")
            export_window.transient(self.master)
            
            # Add export options
            Label(export_window, text="Select data to export:", font=("Ubuntu", 12)).pack(pady=10)
            
            selected_items = {}
            for label, key in export_options:
                var = BooleanVar()
                cb = Checkbutton(export_window, text=label, variable=var)
                cb.pack(pady=5, padx=20, anchor="w")
                selected_items[key] = var

            def perform_export():
                # Get selected items
                to_export = [k for k, v in selected_items.items() if v.get()]
                
                if not to_export:
                    messagebox.showwarning("Export", "Please select at least one item to export")
                    return
                    
                # Ask for export directory
                export_dir = filedialog.askdirectory()
                if not export_dir:
                    return
                    
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                for item in to_export:
                    try:
                        if item == "patients":
                            data = self.db.get_all_patients()  # Assuming this method exists
                            filename = f"patients_{timestamp}.csv"
                            headers = ["ID", "Name", "DOB", "Gender", "Contact"]
                            
                        elif item == "results":
                            data = self.db.get_all_test_results()  # Assuming this method exists
                            filename = f"test_results_{timestamp}.csv"
                            headers = ["Test ID", "Patient ID", "Test Date", "Test Type", "Result"]
                            
                        elif item == "analytics":
                            data = self.db.get_analytics_data()  # Assuming this method exists
                            filename = f"analytics_{timestamp}.csv"
                            headers = ["Metric", "Value", "Date"]
                        
                        # Write to CSV
                        filepath = os.path.join(export_dir, filename)
                        with open(filepath, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(headers)
                            writer.writerows(data)
                            
                    except Exception as e:
                        messagebox.showerror("Export Error", f"Error exporting {item}: {str(e)}")
                        continue
                
                messagebox.showinfo("Export Complete", 
                                f"Successfully exported {len(to_export)} file(s) to {export_dir}")
                export_window.destroy()

            # Add export button
            Button(export_window, text="Export Selected", 
                command=perform_export).pack(pady=20)
            
            # Add cancel button
            Button(export_window, text="Cancel", 
                command=export_window.destroy).pack(pady=5)

        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {str(e)}")

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def handle_logout(self):
        if self.logout_callback:
            self.logout_callback()
        self.master.destroy()


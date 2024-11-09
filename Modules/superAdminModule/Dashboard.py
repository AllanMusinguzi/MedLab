import customtkinter as ctk
from datetime import datetime, timedelta
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from fpdf import FPDF
import pandas as pd
from tkcalendar import DateEntry

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side="top", fill="both", expand=True, padx=20, pady=20)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        
        # Initialize state
        self.real_time_updates_enabled = True
        self.selected_date_range = ("7d", "Last 7 Days")
        self.metric_labels = {}  # Store metric labels for updates
        self.charts = {}  # Store chart references
        
        self.initialize_data()
        self.create_dashboard()
        self.start_real_time_updates()
        
    def initialize_data(self):
        """Initialize dashboard data with sample values"""
        self.metrics = {
            "Total Users": random.randint(1000, 5000),
            "Active Users": random.randint(500, 2000),
            "New Users (Today)": random.randint(10, 100),
            "Total Revenue": f"${random.randint(10000, 50000):,}"
        }
        
        # Generate realistic time series data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        self.user_growth_data = {}
        current_users = random.randint(1000, 2000)
        
        for i in range(31):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            growth = random.randint(-50, 100)
            current_users += growth
            self.user_growth_data[date] = max(current_users, 0)
        
        self.user_distribution = {
            "Admin": random.randint(10, 30),
            "Doctor": random.randint(50, 100),
            "Staff": random.randint(100, 200),
            "Patient": random.randint(500, 1000)
        }
        
        # Sample activity data
        self.activities = [
            self.generate_activity() for _ in range(10)
        ]
        
    def generate_activity(self):
        """Generate a realistic activity entry"""
        actions = ["logged in", "updated profile", "submitted report", "viewed dashboard", "exported data"]
        users = ["John D.", "Sarah M.", "Alex K.", "Maria R.", "James L."]
        
        return {
            "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 60)),
            "user": random.choice(users),
            "action": random.choice(actions),
            "details": f"Session ID: {random.randint(1000, 9999)}"
        }
        
    def create_dashboard(self):
        """Create main dashboard layout"""
        # Create header
        self.create_header()
        
        # Create main content frame with grid layout
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # Create dashboard sections using grid
        self.create_metrics_section()
        self.create_charts_section()
        self.create_activity_section()
        
    def create_header(self):
        """Create dashboard header with controls"""
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10, pady=(0, 20))
        
        # Title and date range
        left_frame = ctk.CTkFrame(header)
        left_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            left_frame,
            text="Dashboard Overview",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left", padx=10)
        
        # Date range selector
        self.date_range = ctk.CTkComboBox(
            left_frame,
            values=["Last 7 Days", "Last 30 Days", "Last 90 Days", "Custom"],
            command=self.handle_date_range_change
        )
        self.date_range.pack(side="left", padx=10)
        self.date_range.set("Last 7 Days")
        
        # Controls
        right_frame = ctk.CTkFrame(header)
        right_frame.pack(side="right")
        
        # Real-time toggle
        self.real_time_var = ctk.BooleanVar(value=True)
        ctk.CTkSwitch(
            right_frame,
            text="Real-time Updates",
            variable=self.real_time_var,
            command=self.toggle_real_time_updates
        ).pack(side="right", padx=10)
        
        # Refresh button
        ctk.CTkButton(
            right_frame,
            text="Refresh",
            command=self.refresh_dashboard
        ).pack(side="right", padx=10)
        
        # Export button
        ctk.CTkButton(
            right_frame,
            text="Export Data",
            command=self.show_export_menu
        ).pack(side="right", padx=10)
        
    def create_metrics_section(self):
        """Create metrics cards section"""
        metrics_frame = ctk.CTkFrame(self.main_frame)
        metrics_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        for i, (metric, value) in enumerate(self.metrics.items()):
            card = ctk.CTkFrame(metrics_frame)
            card.grid(row=0, column=i, sticky="ew", padx=5, pady=5)
            metrics_frame.grid_columnconfigure(i, weight=1)
            
            title_label = ctk.CTkLabel(
                card,
                text=metric,
                font=ctk.CTkFont(size=14)
            )
            title_label.pack(pady=(10, 5))
            
            value_label = ctk.CTkLabel(
                card,
                text=str(value),
                font=ctk.CTkFont(size=20, weight="bold")
            )
            value_label.pack(pady=(0, 10))
            
            self.metric_labels[metric] = value_label
            
    def create_charts_section(self):
        """Create charts section with tabs"""
        charts_frame = ctk.CTkFrame(self.main_frame)
        charts_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        tab_view = ctk.CTkTabview(charts_frame)
        tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # User Growth Chart
        growth_tab = tab_view.add("User Growth")
        self.charts['growth'] = self.create_growth_chart(growth_tab)
        
        # Distribution Chart
        dist_tab = tab_view.add("Distribution")
        self.charts['distribution'] = self.create_distribution_chart(dist_tab)
        
    def create_growth_chart(self, parent):
        """Create user growth line chart"""
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        dates = list(self.user_growth_data.keys())[-7:]  # Last 7 days by default
        values = list(self.user_growth_data.values())[-7:]
        
        line, = ax.plot(dates, values, marker='o', color='#1f77b4')
        ax.set_title("User Growth")
        ax.set_xlabel("Date")
        ax.set_ylabel("Total Users")
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        return {'figure': fig, 'ax': ax, 'line': line, 'canvas': canvas}
        
    def create_distribution_chart(self, parent):
        """Create user distribution pie chart"""
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        labels = list(self.user_distribution.keys())
        sizes = list(self.user_distribution.values())
        
        patches, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            explode=[0.05] * len(labels),
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        )
        ax.set_title("User Distribution")
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        return {'figure': fig, 'ax': ax, 'patches': patches, 'canvas': canvas}
        
    def create_activity_section(self):
        """Create recent activity section"""
        activity_frame = ctk.CTkFrame(self.main_frame)
        activity_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        # Activity header
        ctk.CTkLabel(
            activity_frame,
            text="Recent Activity",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        # Activity list with scrollbar
        tree_frame = ctk.CTkFrame(activity_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Configure treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)
        
        columns = ("Timestamp", "User", "Action", "Details")
        self.activity_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=6,
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.activity_tree.yview)
        
        # Configure columns
        for col in columns:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, width=150)
            
        self.activity_tree.pack(fill="both", expand=True)
        self.update_activity_list()
        
    def handle_date_range_change(self, choice):
        """Handle date range selection change"""
        if choice == "Custom":
            self.show_custom_date_picker()
        else:
            self.selected_date_range = choice
            self.refresh_dashboard()
            
    def show_custom_date_picker(self):
        """Show custom date range picker dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Select Date Range")
        dialog.geometry("300x200")
        
        # Start date picker
        ctk.CTkLabel(dialog, text="Start Date:").pack(pady=5)
        start_date = DateEntry(dialog)
        start_date.pack(pady=5)
        
        # End date picker
        ctk.CTkLabel(dialog, text="End Date:").pack(pady=5)
        end_date = DateEntry(dialog)
        end_date.pack(pady=5)
        
        # Apply button
        ctk.CTkButton(
            dialog,
            text="Apply",
            command=lambda: self.apply_custom_date_range(
                start_date.get_date(),
                end_date.get_date(),
                dialog
            )
        ).pack(pady=20)
        
    def apply_custom_date_range(self, start_date, end_date, dialog):
        """Apply selected custom date range"""
        if start_date > end_date:
            messagebox.showerror("Invalid Date Range", "Start date must be before end date")
            return
            
        self.selected_date_range = (start_date, end_date)
        self.refresh_dashboard()
        dialog.destroy()
        
    def refresh_dashboard(self):
        """Refresh all dashboard components"""
        self.initialize_data()
        self.update_metrics()
        self.update_charts()
        self.update_activity_list()
        
    def update_metrics(self):
        """Update metric values"""
        for metric, value in self.metrics.items():
            if metric in self.metric_labels:
                self.metric_labels[metric].configure(text=str(value))
                
    def update_charts(self):
        """Update all charts with new data"""
        # Update growth chart
        growth_chart = self.charts['growth']
        dates = list(self.user_growth_data.keys())
        values = list(self.user_growth_data.values())
        
        growth_chart['line'].set_data(dates, values)
        growth_chart['ax'].relim()
        growth_chart['ax'].autoscale_view()
        growth_chart['canvas'].draw()
        
        # Update distribution chart
        dist_chart = self.charts['distribution']
        dist_chart['ax'].clear()
        labels = list(self.user_distribution.keys())
        sizes = list(self.user_distribution.values())
        
        dist_chart['ax'].pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%', 
            explode=[0.05] * len(labels),
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        )
        dist_chart['canvas'].draw()
        
    def update_activity_list(self):
        """Update activity list with new data"""
        # Clear existing items
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
            
        # Add new activities
        for activity in self.activities:
            self.activity_tree.insert(
                "",
                "end",
                values=(
                    activity['timestamp'].strftime("%Y-%m-%d %H:%M"),
                    activity['user'],
                    activity['action'],
                    activity['details']
                )
            )
            
    def toggle_real_time_updates(self):
        """Toggle real-time updates"""
        self.real_time_updates_enabled = self.real_time_var.get()
        
    def show_export_menu(self):
        """Show export options dialog"""
        export_menu = ctk.CTkToplevel(self)
        export_menu.title("Export Data")
        export_menu.geometry("300x320")

        # Export section header
        ctk.CTkLabel(
            export_menu,
            text="Export Dashboard Data",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        # Date range for export
        ctk.CTkLabel(
            export_menu,
            text="Select Date Range:"
        ).pack(pady=5)
        
        start_date = DateEntry(export_menu)
        start_date.pack(pady=5)
        
        end_date = DateEntry(export_menu)
        end_date.pack(pady=5)
        
        # Format selection
        formats = [
            ("CSV", "csv"),
            ("Excel", "excel"),
            ("PDF", "pdf")
        ]
        
        format_var = ctk.StringVar(value="csv")
        
        for label, format_type in formats:
            ctk.CTkRadioButton(
                export_menu,
                text=label,
                variable=format_var,
                value=format_type
            ).pack(pady=5)
            
        # Export button
        ctk.CTkButton(
            export_menu,
            text="Export",
            command=lambda: self.export_data(
                format_var.get(),
                start_date.get_date(),
                end_date.get_date()
            )
        ).pack(pady=20)
            
    def export_data(self, format_type, start_date, end_date):
        """Export dashboard data in specified format"""
        try:
            # Prepare export data
            export_data = {
                'metrics': self.metrics,
                'user_growth': {
                    k: v for k, v in self.user_growth_data.items()
                    if start_date <= datetime.strptime(k, "%Y-%m-%d").date() <= end_date
                },
                'user_distribution': self.user_distribution,
                'activities': [
                    activity for activity in self.activities
                    if start_date <= activity['timestamp'].date() <= end_date
                ]
            }
            
            # Create DataFrame for metrics
            metrics_df = pd.DataFrame(self.metrics.items(), columns=['Metric', 'Value'])
            
            # Create DataFrame for user growth
            growth_df = pd.DataFrame(
                list(export_data['user_growth'].items()),
                columns=['Date', 'Users']
            )
            
            # Create DataFrame for user distribution
            distribution_df = pd.DataFrame(
                list(self.user_distribution.items()),
                columns=['Role', 'Count']
            )
            
            # Create DataFrame for activities
            activities_df = pd.DataFrame(export_data['activities'])
            
            if format_type == "csv":
                with pd.ExcelWriter('dashboard_export.csv', engine='openpyxl') as writer:
                    metrics_df.to_excel(writer, sheet_name='Metrics', index=False)
                    growth_df.to_excel(writer, sheet_name='User Growth', index=False)
                    distribution_df.to_excel(writer, sheet_name='Distribution', index=False)
                    activities_df.to_excel(writer, sheet_name='Activities', index=False)
                    
            elif format_type == "excel":
                with pd.ExcelWriter('dashboard_export.xlsx', engine='openpyxl') as writer:
                    metrics_df.to_excel(writer, sheet_name='Metrics', index=False)
                    growth_df.to_excel(writer, sheet_name='User Growth', index=False)
                    distribution_df.to_excel(writer, sheet_name='Distribution', index=False)
                    activities_df.to_excel(writer, sheet_name='Activities', index=False)
                    
            elif format_type == "pdf":
                pdf = FPDF()
                
                # Add metrics page
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, "Dashboard Metrics", ln=True, align='C')
                pdf.set_font("Arial", size=12)
                
                for metric, value in self.metrics.items():
                    pdf.cell(200, 10, f"{metric}: {value}", ln=True)
                    
                # Add user growth page
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, "User Growth", ln=True, align='C')
                pdf.set_font("Arial", size=12)
                
                for date, users in export_data['user_growth'].items():
                    pdf.cell(200, 10, f"{date}: {users} users", ln=True)
                    
                # Add distribution page
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, "User Distribution", ln=True, align='C')
                pdf.set_font("Arial", size=12)
                
                for role, count in self.user_distribution.items():
                    pdf.cell(200, 10, f"{role}: {count} users", ln=True)
                    
                pdf.output("dashboard_export.pdf")
                
            messagebox.showinfo(
                "Export Success",
                f"Data exported successfully as {format_type.upper()}"
            )
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")
            
    def start_real_time_updates(self):
        """Start real-time update loop"""
        if self.real_time_updates_enabled:
            self.simulate_real_time_updates()
        self.after(5000, self.start_real_time_updates)
        
    def simulate_real_time_updates(self):
        """Simulate real-time data updates"""
        # Update metrics with small changes
        self.metrics["Active Users"] = max(
            0,
            int(float(self.metrics["Active Users"]) * (1 + random.uniform(-0.05, 0.05)))
        )
        self.metrics["New Users (Today)"] = max(
            0,
            int(float(self.metrics["New Users (Today)"]) + random.randint(-5, 10))
        )
        revenue = int(self.metrics["Total Revenue"].replace("$", "").replace(",", ""))
        revenue = int(revenue * (1 + random.uniform(-0.02, 0.05)))
        self.metrics["Total Revenue"] = f"${revenue:,}"
        
        # Update user growth data
        latest_date = max(self.user_growth_data.keys())
        latest_users = self.user_growth_data[latest_date]
        new_users = max(0, latest_users + random.randint(-50, 100))
        self.user_growth_data[latest_date] = new_users
        
        # Add new activity
        new_activity = self.generate_activity()
        self.activities.insert(0, new_activity)
        self.activities = self.activities[:10]  # Keep only last 10 activities
        
        # Update UI
        self.update_metrics()
        self.update_charts()
        self.update_activity_list()
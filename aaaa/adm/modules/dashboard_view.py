# modules/dashboard_view.py
import customtkinter as ctk
from utils.charts import create_line_chart, create_pie_chart

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkLabel(
            self, 
            text="Dashboard Overview", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Stats summary
        self.create_stats_summary()
        
        # Charts
        self.create_charts()
        
        # Recent activity
        self.create_recent_activity()

    def create_stats_summary(self):
        stats_frame = ctk.CTkFrame(self)
        stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure((0,1,2,3), weight=1)

        # Get actual stats from database
        stats = self.db.get_dashboard_stats()
        
        stats_cards = [
            ("Total Patients", stats['total_patients'], "👥"),
            ("Pending Tests", stats['pending_tests'], "⏳"),
            ("Completed Tests", stats['completed_tests'], "✅"),
            ("Critical Cases", stats['critical_cases'], "⚠️")
        ]

        for i, (title, value, icon) in enumerate(stats_cards):
            self.create_stat_card(stats_frame, title, value, icon, i)

    def create_stat_card(self, parent, title, value, icon, col):
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=col, padx=10, pady=10, sticky="ew")
        
        icon_label = ctk.CTkLabel(
            card, 
            text=icon, 
            font=ctk.CTkFont(size=24)
        )
        icon_label.grid(row=0, column=0, padx=20, pady=5)
        
        title_label = ctk.CTkLabel(
            card, 
            text=title, 
            font=ctk.CTkFont(size=14)
        )
        title_label.grid(row=1, column=0, padx=20, pady=5)
        
        value_label = ctk.CTkLabel(
            card, 
            text=str(value), 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        value_label.grid(row=2, column=0, padx=20, pady=5)

    def create_charts(self):
        charts_frame = ctk.CTkFrame(self)
        charts_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        charts_frame.grid_columnconfigure((0,1), weight=1)

        # Monthly patients chart
        monthly_data = self.db.get_monthly_patients_data()
        create_line_chart(
            charts_frame, 
            "Monthly Patient Admissions", 
            monthly_data,
            0
        )

        # Test results distribution
        results_data = self.db.get_test_results_distribution()
        create_pie_chart(
            charts_frame, 
            "Test Results Distribution", 
            results_data,
            1
        )

    def create_recent_activity(self):
        activity_frame = ctk.CTkFrame(self)
        activity_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        
        header = ctk.CTkLabel(
            activity_frame, 
            text="Recent Activity", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header.pack(pady=10, padx=10, anchor="w")
        
        # Get recent activities from database
        activities = self.db.get_recent_activities(limit=5)
        
        for activity in activities:
            activity_item = ctk.CTkLabel(
                activity_frame,
                text=f"{activity['timestamp']} - {activity['description']}",
                anchor="w"
            )
            activity_item.pack(pady=5, padx=10, fill="x")
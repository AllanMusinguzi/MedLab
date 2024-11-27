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
        
        # Initialize state
        self.real_time_updates_enabled = True
        self.selected_date_range = ("7d", "Last 7 Days")
        self.metric_labels = {}
        self.charts = {}
        
        self.initialize_data()
        self.create_dashboard()
        self.start_real_time_updates()
        
    def initialize_data(self):
        """Initialize dashboard data with sample values"""
        self.metrics = {
            "Sales": {"value": "59,467", "change": "High 311↑", "color": "#8B5CF6"},
            "Returns": {"value": "28,085", "change": "High 2.98↑", "color": "#06B6D4"},
            "Purchases": {"value": "39,645", "change": "Low 0.21↓", "color": "#3B82F6"},
            "Downloads": {"value": "44,148", "change": "Low 1.12↓", "color": "#4B5563"}
        }
        
        self.secondary_metrics = {
            "Customers": {"value": "92,556", "change": "1.35↑ More than last month"},
            "Conversion": {"value": "53,812", "change": "0.17↓ Less than last month"},
            "Revenue": {"value": "40,008", "change": "0.06↓ Less than last month"}
        }
        
        # Revenue data for charts
        self.revenue_data = {
            'online': [600, 620, 580, 600, 550, 780, 700, 800],
            'offline': [800, 780, 650, 900, 780, 1080, 800, 900],
            'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
        }
        
        self.sales_distribution = {
            'Sales total': 12,
            'Sales total 2': 20,
            'Sales total 3': 67
        }
        
        self.market_data = [
            {
                'id': 'WMQ96921',
                'date': '18 Sep 2019',
                'type': '#ABU81275',
                'sku': '931',
                'quantity': '8',
                'amount': '14689',
                'status': 'Completed'
            },
            {
                'id': 'WMQ60538',
                'date': '29 May 2019',
                'type': '#HGA55521',
                'sku': '828',
                'quantity': '37',
                'amount': '19888',
                'status': 'Cancelled'
            }
        ]
        
    def create_dashboard(self):
        """Create main dashboard layout"""
        # Create header
        self.create_header()
        
        # Create main content
        main_content = ctk.CTkFrame(self)
        main_content.pack(fill="both", expand=True, pady=20)
        
        # Create metric cards section
        self.create_metric_cards(main_content)
        
        # Create middle section with three panels
        self.create_middle_section(main_content)
        
        # Create bottom section with charts
        self.create_bottom_section(main_content)
        
    def create_header(self):
        """Create dashboard header"""
        header = ctk.CTkFrame(self)
        header.pack(fill="x", pady=(0, 20))
        
        # Left side - Navigation
        nav_frame = ctk.CTkFrame(header)
        nav_frame.pack(side="left")
        
        path_items = ["Dashboard", "App", "Dashboard", "Analytics"]
        for item in path_items:
            ctk.CTkLabel(nav_frame, text=item).pack(side="left", padx=5)
            if item != path_items[-1]:
                ctk.CTkLabel(nav_frame, text=">").pack(side="left", padx=5)
        
        # Right side - Controls
        controls_frame = ctk.CTkFrame(header)
        controls_frame.pack(side="right")
        
        # Date picker
        date_btn = ctk.CTkButton(
            controls_frame,
            text="02 Aug 2019",
            fg_color="#8B5CF6",
            hover_color="#7C3AED"
        )
        date_btn.pack(side="left", padx=10)
        
        # Download button
        download_btn = ctk.CTkButton(
            controls_frame,
            text="Download Report",
            fg_color="#F3F4F6",
            text_color="#374151",
            hover_color="#E5E7EB"
        )
        download_btn.pack(side="left")
        
    def create_metric_cards(self, parent):
        """Create top metric cards"""
        cards_frame = ctk.CTkFrame(parent)
        cards_frame.pack(fill="x", pady=(0, 20))
        
        # Configure grid columns with equal weight
        for i in range(4):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Create metric cards
        for i, (metric, data) in enumerate(self.metrics.items()):
            card = ctk.CTkFrame(cards_frame)
            card.grid(row=0, column=i, padx=10, sticky="ew")
            
            # Icon frame (placeholder for now)
            icon_frame = ctk.CTkFrame(card, width=40, height=40)
            icon_frame.pack(anchor="w", padx=15, pady=10)
            
            # Metric name
            ctk.CTkLabel(
                card,
                text=metric,
                font=("Ubuntu", 14)
            ).pack(anchor="w", padx=15)
            
            # Value
            ctk.CTkLabel(
                card,
                text=data["value"],
                font=("Ubuntu", 24, "bold")
            ).pack(anchor="w", padx=15)
            
            # Change indicator
            change_label = ctk.CTkLabel(
                card,
                text=data["change"],
                font=("Ubuntu", 12)
            )
            change_label.pack(anchor="w", padx=15, pady=(0, 10))
            
            # Store reference
            self.metric_labels[metric] = {
                'value': change_label
            }
            
    def create_middle_section(self, parent):
        """Create middle section with three panels"""
        middle_frame = ctk.CTkFrame(parent)
        middle_frame.pack(fill="x", pady=(0, 20))
        
        # Configure columns
        for i in range(3):
            middle_frame.grid_columnconfigure(i, weight=1)
        
        # Create three panels
        for i, (metric, data) in enumerate(self.secondary_metrics.items()):
            panel = ctk.CTkFrame(middle_frame)
            panel.grid(row=0, column=i, padx=10, sticky="nsew")
            
            # Header
            header_frame = ctk.CTkFrame(panel)
            header_frame.pack(fill="x", padx=15, pady=10)
            
            ctk.CTkLabel(
                header_frame,
                text=metric,
                font=("Ubuntu", 16)
            ).pack(side="left")
            
            # More options button
            ctk.CTkButton(
                header_frame,
                text="•••",
                width=30,
                fg_color="transparent",
                hover_color="#F3F4F6"
            ).pack(side="right")
            
            # Value
            ctk.CTkLabel(
                panel,
                text=data["value"],
                font=("Ubuntu", 32, "bold")
            ).pack(anchor="w", padx=15)
            
            # Change indicator
            ctk.CTkLabel(
                panel,
                text=data["change"],
                font=("Ubuntu", 14)
            ).pack(anchor="w", padx=15, pady=(0, 10))
            
            # Placeholder for charts
            chart_frame = ctk.CTkFrame(panel, height=100)
            chart_frame.pack(fill="x", padx=15, pady=(0, 15))
            
    def create_bottom_section(self, parent):
        """Create bottom section with revenue chart and sales distribution"""
        bottom_frame = ctk.CTkFrame(parent)
        bottom_frame.pack(fill="both", expand=True)
        
        # Configure columns
        bottom_frame.grid_columnconfigure(0, weight=2)
        bottom_frame.grid_columnconfigure(1, weight=1)
        
        # Revenue chart
        self.create_revenue_chart(bottom_frame)
        
        # Sales distribution
        self.create_sales_distribution(bottom_frame)
        
    def create_revenue_chart(self, parent):
        """Create revenue chart panel"""
        chart_frame = ctk.CTkFrame(parent)
        chart_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        # Header
        header_frame = ctk.CTkFrame(chart_frame)
        header_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="Revenue For Last 30 Days",
            font=("Ubuntu", 16)
        ).pack(side="left")
        
        # More options button
        ctk.CTkButton(
            header_frame,
            text="•••",
            width=30,
            fg_color="transparent",
            hover_color="#F3F4F6"
        ).pack(side="right")
        
        # Create matplotlib figure
        fig = Figure(figsize=(10, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot data
        ax.plot(self.revenue_data['months'], self.revenue_data['online'], 
                color='#06B6D4', label='Online revenue')
        ax.plot(self.revenue_data['months'], self.revenue_data['offline'], 
                color='#8B5CF6', label='Offline revenue')
        
        ax.fill_between(self.revenue_data['months'], self.revenue_data['online'], 
                       alpha=0.1, color='#06B6D4')
        ax.fill_between(self.revenue_data['months'], self.revenue_data['offline'], 
                       alpha=0.1, color='#8B5CF6')
        
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
    def create_sales_distribution(self, parent):
        """Create sales distribution panel"""
        dist_frame = ctk.CTkFrame(parent)
        dist_frame.grid(row=0, column=1, sticky="nsew")
        
        # Header
        header_frame = ctk.CTkFrame(dist_frame)
        header_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            header_frame,
            text="All Online Sales",
            font=("Ubuntu", 16)
        ).pack(side="left")
        
        # More options button
        ctk.CTkButton(
            header_frame,
            text="•••",
            width=30,
            fg_color="transparent",
            hover_color="#F3F4F6"
        ).pack(side="right")
        
        # Create matplotlib figure for donut chart
        fig = Figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(111)
        
        # Plot donut chart
        values = list(self.sales_distribution.values())
        labels = list(self.sales_distribution.keys())
        colors = ['#06B6D4', '#8B5CF6', '#3B82F6']
        
        ax.pie(values, labels=labels, colors=colors, autopct='%1.0f%%',
               pctdistance=0.85, wedgeprops=dict(width=0.5))
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=dist_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def start_real_time_updates(self):
        """Start real-time update loop"""
        if self.real_time_updates_enabled:
            self.simulate_real_time_updates()
        self.after(5000, self.start_real_time_updates)
        
    def simulate_real_time_updates(self):
        """Simulate real-time data updates"""
        # Update metrics with small random changes
        for metric in self.metrics:
            current_value = int(self.metrics[metric]["value"].replace(",", ""))
            change = random.uniform(-0.02, 0.02)
            new_value = int(current_value * (1 + change))
            self.metrics[metric]["value"] = f"{new_value:,}"
            
            # Update change indicator
            direction = "↑" if change > 0 else "↓"
            magnitude = "High" if abs(change) > 0.01 else "Low"
            self.metrics[metric]["change"] = f"{magnitude} {abs(change)*100:.2f}{direction}"
            
        self.update_metrics()
        
    def update_metrics(self):
        """Update metric values in the UI"""
        for metric, labels in self.metric_labels.items():
            if 'value' in labels:
                labels['value'].configure(text=self.metrics[metric]["change"])
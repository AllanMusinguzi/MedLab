# pages/adminModule/analytics.py
import tkinter as tk
from tkinter import ttk
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsView:
    """Main entry point for the analytics module with GUI integration."""
    
    def __init__(self, parent_frame):
        """Initialize the analytics view with parent frame.
        
        Args:
            parent_frame: Parent tkinter frame
        """
        self.parent = parent_frame
        self.db = None
        self.last_refresh = None
        self.refresh_interval = timedelta(minutes=5)
        self.analytics_frame = None
        
    def create_analytics_management_frame(self):
        """Create and return the main analytics management frame.
        
        Returns:
            tkinter Frame containing the analytics interface
        """
        self.analytics_frame = ttk.Frame(self.parent)
        
        # Create header
        header_frame = ttk.Frame(self.analytics_frame)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(
            header_frame,
            text="Analytics Dashboard",
            font=('Helvetica', 16, 'bold')
        ).pack(side="left")
        
        refresh_btn = ttk.Button(
            header_frame,
            text="Refresh Data",
            command=self.refresh_analytics
        )
        refresh_btn.pack(side="right")
        
        # Create main content area with tabs
        tab_control = ttk.Notebook(self.analytics_frame)
        
        # Overview tab
        overview_tab = self._create_overview_tab(tab_control)
        tab_control.add(overview_tab, text="Overview")
        
        # Detailed Metrics tab
        metrics_tab = self._create_metrics_tab(tab_control)
        tab_control.add(metrics_tab, text="Detailed Metrics")
        
        # Trends tab
        trends_tab = self._create_trends_tab(tab_control)
        tab_control.add(trends_tab, text="Trends")
        
        tab_control.pack(expand=True, fill="both", padx=10, pady=5)
        
        # Load initial data
        self.refresh_analytics()
        
        return self.analytics_frame
    
    def _create_overview_tab(self, parent):
        """Create the overview tab content."""
        tab = ttk.Frame(parent)
        
        # Key metrics section
        metrics_frame = ttk.LabelFrame(tab, text="Key Metrics")
        metrics_frame.pack(fill="x", padx=5, pady=5)
        
        self.metrics_widgets = {}
        metric_names = ["Total Users", "Active Users", "Revenue", "Conversion Rate"]
        
        for i, metric in enumerate(metric_names):
            frame = ttk.Frame(metrics_frame)
            frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="nsew")
            
            ttk.Label(frame, text=metric).pack()
            value_label = ttk.Label(frame, text="Loading...")
            value_label.pack()
            
            self.metrics_widgets[metric] = value_label
        
        # Recent activity section
        activity_frame = ttk.LabelFrame(tab, text="Recent Activity")
        activity_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.activity_tree = ttk.Treeview(
            activity_frame,
            columns=("timestamp", "type", "details"),
            show="headings"
        )
        self.activity_tree.heading("timestamp", text="Timestamp")
        self.activity_tree.heading("type", text="Type")
        self.activity_tree.heading("details", text="Details")
        
        scrollbar = ttk.Scrollbar(
            activity_frame,
            orient="vertical",
            command=self.activity_tree.yview
        )
        self.activity_tree.configure(yscrollcommand=scrollbar.set)
        
        self.activity_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return tab
    
    def _create_metrics_tab(self, parent):
        """Create the detailed metrics tab content."""
        tab = ttk.Frame(parent)
        
        # Metrics filter section
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Time Range:").pack(side="left")
        time_range = ttk.Combobox(
            filter_frame,
            values=["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom"],
            state="readonly"
        )
        time_range.set("Last 7 Days")
        time_range.pack(side="left", padx=5)
        
        # Metrics display
        metrics_frame = ttk.Frame(tab)
        metrics_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.metrics_tree = ttk.Treeview(
            metrics_frame,
            columns=("metric", "value", "change", "trend"),
            show="headings"
        )
        self.metrics_tree.heading("metric", text="Metric")
        self.metrics_tree.heading("value", text="Value")
        self.metrics_tree.heading("change", text="Change")
        self.metrics_tree.heading("trend", text="Trend")
        
        scrollbar = ttk.Scrollbar(
            metrics_frame,
            orient="vertical",
            command=self.metrics_tree.yview
        )
        self.metrics_tree.configure(yscrollcommand=scrollbar.set)
        
        self.metrics_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return tab
    
    def _create_trends_tab(self, parent):
        """Create the trends tab content."""
        tab = ttk.Frame(parent)
        
        # Trends filter section
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(filter_frame, text="Metric:").pack(side="left")
        metric_selector = ttk.Combobox(
            filter_frame,
            values=["Users", "Revenue", "Conversion", "Engagement"],
            state="readonly"
        )
        metric_selector.set("Users")
        metric_selector.pack(side="left", padx=5)
        
        # Placeholder for chart
        chart_frame = ttk.Frame(tab)
        chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        return tab
    
    def refresh_analytics(self):
        """Refresh all analytics data and update the UI."""
        try:
            if not self.db:
                logger.error("Database connection not initialized")
                return
                
            self._load_metrics_data()
            self._load_activity_data()
            self._load_trends_data()
            
            self.last_refresh = datetime.now()
            logger.info("Analytics data refreshed successfully")
            
        except Exception as e:
            logger.error(f"Error refreshing analytics data: {str(e)}")
    
    def _load_metrics_data(self):
        """Load and display metrics data."""
        try:
            query = """
                SELECT 
                    metric_name,
                    current_value,
                    previous_value,
                    last_updated
                FROM analytics_metrics
                WHERE last_updated >= NOW() - INTERVAL '24 HOURS'
            """
            
            results = self.db.execute(query)
            
            # Update metrics widgets
            for row in results:
                if row['metric_name'] in self.metrics_widgets:
                    value = self._format_metric_value(
                        row['current_value'],
                        row['metric_name']
                    )
                    change = self._calculate_change(
                        row['current_value'],
                        row['previous_value']
                    )
                    
                    self.metrics_widgets[row['metric_name']].configure(
                        text=f"{value} ({change:+.1f}%)"
                    )
                    
        except Exception as e:
            logger.error(f"Error loading metrics data: {str(e)}")
    
    def _load_activity_data(self):
        """Load and display recent activity data."""
        try:
            query = """
                SELECT 
                    timestamp,
                    activity_type,
                    details
                FROM analytics_activity
                WHERE timestamp >= NOW() - INTERVAL '24 HOURS'
                ORDER BY timestamp DESC
                LIMIT 100
            """
            
            results = self.db.execute(query)
            
            # Clear existing items
            for item in self.activity_tree.get_children():
                self.activity_tree.delete(item)
            
            # Add new items
            for row in results:
                self.activity_tree.insert(
                    "",
                    "end",
                    values=(
                        row['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                        row['activity_type'],
                        row['details']
                    )
                )
                
        except Exception as e:
            logger.error(f"Error loading activity data: {str(e)}")
    
    def _load_trends_data(self):
        """Load and display trends data."""
        try:
            query = """
                SELECT 
                    metric_name,
                    timestamp,
                    value
                FROM analytics_trends
                WHERE timestamp >= NOW() - INTERVAL '7 DAYS'
                ORDER BY metric_name, timestamp
            """
            
            results = self.db.execute(query)
            # Update trends visualization (implement based on your charting library)
            
        except Exception as e:
            logger.error(f"Error loading trends data: {str(e)}")
    
    def _format_metric_value(self, value: float, metric_name: str) -> str:
        """Format metric value for display."""
        if 'rate' in metric_name.lower():
            return f"{value:.1f}%"
        elif 'revenue' in metric_name.lower():
            return f"${value:,.2f}"
        elif value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
        return str(value)
    
    def _calculate_change(self, current: float, previous: float) -> float:
        """Calculate percentage change between two values."""
        if not previous:
            return 0.0
        return ((current - previous) / previous) * 100
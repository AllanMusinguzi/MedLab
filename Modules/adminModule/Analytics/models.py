# pages/adminModule/analytics/models.py
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class AnalyticsMetric:
    """Represents a single analytics metric."""
    name: str
    value: float
    timestamp: datetime
    category: str
    unit: Optional[str] = None
    
@dataclass
class TimeSeriesData:
    """Represents time-series analytics data."""
    metric_name: str
    values: List[float]
    timestamps: List[datetime]
    metadata: Dict = None

class AnalyticsDataManager:
    """Handles analytics data operations and transformations."""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.cache = {}
        
    def get_metrics(self, start_date: datetime, end_date: datetime) -> List[AnalyticsMetric]:
        """Fetch metrics for a given date range."""
        query = """
            SELECT metric_name, value, timestamp, category, unit
            FROM analytics_metrics
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp DESC
        """
        results = self.db.execute(query, (start_date, end_date))
        return [AnalyticsMetric(*row) for row in results]
    
    def get_time_series(self, metric_name: str, period: str) -> TimeSeriesData:
        """Fetch time series data for a specific metric."""
        if period not in ['day', 'week', 'month', 'year']:
            raise ValueError("Invalid period specified")
            
        query = """
            SELECT timestamp, value
            FROM analytics_time_series
            WHERE metric_name = %s
            AND period = %s
            ORDER BY timestamp
        """
        results = self.db.execute(query, (metric_name, period))
        timestamps, values = zip(*results)
        return TimeSeriesData(metric_name, values, timestamps)

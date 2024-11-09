# pages/adminModule/analytics/views.py
from typing import List, Dict, Any
from datetime import datetime, timedelta
from .models import AnalyticsDataManager, AnalyticsMetric, TimeSeriesData

class ModernAnalyticsView:
    """Modern analytics view with advanced features and caching."""
    
    def __init__(self, db_connection=None):
        self.data_manager = AnalyticsDataManager(db_connection) if db_connection else None
        self.cache_duration = timedelta(minutes=15)
        self.last_cache_update = None
        self.cached_data = {}
        
    def connect_db(self, db_connection):
        """Set or update the database connection."""
        self.data_manager = AnalyticsDataManager(db_connection)
        
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        if not self.data_manager:
            raise ValueError("Database connection not initialized")
            
        if self._should_refresh_cache():
            self._refresh_cache()
            
        return self.cached_data
    
    def _should_refresh_cache(self) -> bool:
        """Check if cache needs refreshing."""
        if not self.last_cache_update:
            return True
        return datetime.now() - self.last_cache_update > self.cache_duration
    
    def _refresh_cache(self):
        """Refresh cached analytics data."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        self.cached_data = {
            'key_metrics': self._get_key_metrics(),
            'time_series': self._get_time_series_data(start_date, end_date),
            'top_items': self._get_top_items(),
            'last_updated': datetime.now()
        }
        self.last_cache_update = datetime.now()
        
    def _get_key_metrics(self) -> Dict[str, AnalyticsMetric]:
        """Get key performance metrics."""
        metrics = [
            'total_users',
            'active_users',
            'revenue',
            'conversion_rate'
        ]
        return {
            metric: self.data_manager.get_metrics(
                datetime.now() - timedelta(days=1),
                datetime.now()
            )[0]
            for metric in metrics
        }
        
    def _get_time_series_data(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, TimeSeriesData]:
        """Get time series data for key metrics."""
        metrics = [
            'user_growth',
            'revenue_trend',
            'engagement_rate'
        ]
        return {
            metric: self.data_manager.get_time_series(metric, 'day')
            for metric in metrics
        }
        
    def _get_top_items(self) -> Dict[str, List[Dict]]:
        """Get top performing items across different categories."""
        return {
            'products': self._get_top_products(),
            'pages': self._get_top_pages(),
            'referrers': self._get_top_referrers()
        }
        
    def _get_top_products(self) -> List[Dict]:
        """Get top performing products."""
        query = """
            SELECT product_id, name, revenue, units_sold
            FROM product_analytics
            ORDER BY revenue DESC
            LIMIT 10
        """
        return self.data_manager.db.execute(query)
        
    def _get_top_pages(self) -> List[Dict]:
        """Get top performing pages."""
        query = """
            SELECT page_path, views, unique_visitors
            FROM page_analytics
            ORDER BY views DESC
            LIMIT 10
        """
        return self.data_manager.db.execute(query)
        
    def _get_top_referrers(self) -> List[Dict]:
        """Get top traffic referrers."""
        query = """
            SELECT referrer_domain, visits, conversion_rate
            FROM referrer_analytics
            ORDER BY visits DESC
            LIMIT 10
        """
        return self.data_manager.db.execute(query)

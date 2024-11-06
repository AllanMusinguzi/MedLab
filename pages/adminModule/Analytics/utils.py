# pages/adminModule/analytics/utils.py
from typing import List, Dict, Any
from datetime import datetime

def calculate_growth_rate(
    current_value: float,
    previous_value: float
) -> float:
    """Calculate growth rate between two values."""
    if previous_value == 0:
        return 0
    return ((current_value - previous_value) / previous_value) * 100

def format_metric(
    value: float,
    metric_type: str
) -> str:
    """Format metric values for display."""
    if metric_type == 'currency':
        return f"${value:,.2f}"
    elif metric_type == 'percentage':
        return f"{value:.1f}%"
    elif metric_type == 'number':
        if value >= 1000000:
            return f"{value/1000000:.1f}M"
        elif value >= 1000:
            return f"{value/1000:.1f}K"
    return str(value)

def aggregate_time_series(
    data: List[Dict[str, Any]],
    period: str
) -> List[Dict[str, Any]]:
    """Aggregate time series data by specified period."""
    aggregated = {}
    for entry in data:
        timestamp = entry['timestamp']
        if period == 'hour':
            key = timestamp.replace(minute=0, second=0, microsecond=0)
        elif period == 'day':
            key = timestamp.date()
        elif period == 'month':
            key = timestamp.replace(day=1)
        elif period == 'year':
            key = timestamp.replace(month=1, day=1)
        
        if key not in aggregated:
            aggregated[key] = {
                'timestamp': key,
                'value': 0,
                'count': 0
            }
        
        aggregated[key]['value'] += entry['value']
        aggregated[key]['count'] += 1
    
    return [
        {
            'timestamp': k,
            'value': v['value'] / v['count']
        }
        for k, v in sorted(aggregated.items())
    ]
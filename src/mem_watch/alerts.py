"""Alert management for memory thresholds."""

from typing import List, Optional
import psutil


class Alert:
    """Represents a memory threshold alert."""
    
    def __init__(self, pid: int, name: str, current: float, threshold: float, level: str):
        self.pid = pid
        self.name = name
        self.current = current
        self.threshold = threshold
        self.level = level


class AlertManager:
    """Manage memory threshold alerts."""
    
    def __init__(self, threshold: str):
        self.threshold_bytes: Optional[int] = None
        self.threshold_percent: Optional[float] = None
        self._parse_threshold(threshold)
        
    def _parse_threshold(self, threshold: str):
        """Parse threshold string (e.g., '500M', '2G', '80%')."""
        threshold = threshold.strip()
        
        if threshold.endswith('%'):
            self.threshold_percent = float(threshold[:-1])
        else:
            multipliers = {'K': 1024, 'M': 1024**2, 'G': 1024**3}
            value = threshold.upper()
            
            for suffix, multiplier in multipliers.items():
                if value.endswith(suffix):
                    self.threshold_bytes = int(float(value[:-1]) * multiplier)
                    return
            
            self.threshold_bytes = int(threshold)
    
    def check(self, stats: List) -> List[Alert]:
        """Check if any processes exceed thresholds."""
        alerts = []
        
        for stat in stats:
            alert_level = None
            current_value = 0
            threshold_value = 0
            
            if self.threshold_percent is not None:
                current_value = stat.percent
                threshold_value = self.threshold_percent
                
                if stat.percent >= self.threshold_percent * 1.2:
                    alert_level = "critical"
                elif stat.percent >= self.threshold_percent:
                    alert_level = "warning"
            
            elif self.threshold_bytes is not None:
                current_value = stat.rss
                threshold_value = self.threshold_bytes
                
                if stat.rss >= self.threshold_bytes * 1.2:
                    alert_level = "critical"
                elif stat.rss >= self.threshold_bytes:
                    alert_level = "warning"
            
            if alert_level:
                alerts.append(Alert(
                    pid=stat.pid,
                    name=stat.name,
                    current=current_value,
                    threshold=threshold_value,
                    level=alert_level
                ))
        
        return alerts

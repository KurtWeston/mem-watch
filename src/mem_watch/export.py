"""CSV export functionality for memory usage data."""

import csv
import time
from typing import List
from pathlib import Path


class CSVExporter:
    """Export memory statistics to CSV file."""
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.initialized = False
        
    def write(self, stats: List):
        """Write statistics to CSV file."""
        mode = 'a' if self.initialized else 'w'
        
        with open(self.filepath, mode, newline='') as f:
            writer = csv.writer(f)
            
            if not self.initialized:
                writer.writerow([
                    'timestamp',
                    'pid',
                    'name',
                    'rss_bytes',
                    'vms_bytes',
                    'memory_percent'
                ])
                self.initialized = True
            
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            for stat in stats:
                writer.writerow([
                    timestamp,
                    stat.pid,
                    stat.name,
                    stat.rss,
                    stat.vms,
                    f"{stat.percent:.2f}"
                ])

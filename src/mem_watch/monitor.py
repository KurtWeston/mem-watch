"""Core memory monitoring functionality."""

import re
import time
from typing import List, Optional, Dict, Any
import psutil


class ProcessStats:
    """Container for process memory statistics."""
    
    def __init__(self, pid: int, name: str, rss: int, vms: int, percent: float):
        self.pid = pid
        self.name = name
        self.rss = rss
        self.vms = vms
        self.percent = percent
        self.timestamp = time.time()


class MemoryMonitor:
    """Monitor memory usage of processes."""
    
    def __init__(
        self,
        pid: Optional[int] = None,
        name_pattern: Optional[str] = None,
        include_children: bool = False,
        interval: float = 1.0
    ):
        self.pid = pid
        self.name_pattern = re.compile(name_pattern) if name_pattern else None
        self.include_children = include_children
        self.interval = interval
        self.history: List[List[ProcessStats]] = []
        
    def _get_processes(self) -> List[psutil.Process]:
        """Get list of processes to monitor."""
        processes = []
        
        if self.pid:
            try:
                proc = psutil.Process(self.pid)
                processes.append(proc)
                if self.include_children:
                    processes.extend(proc.children(recursive=True))
            except psutil.NoSuchProcess:
                return []
        elif self.name_pattern:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if self.name_pattern.search(proc.info['name']):
                        processes.append(proc)
                        if self.include_children:
                            processes.extend(proc.children(recursive=True))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        return processes
    
    def collect(self) -> List[ProcessStats]:
        """Collect current memory statistics."""
        stats = []
        processes = self._get_processes()
        
        for proc in processes:
            try:
                mem_info = proc.memory_info()
                mem_percent = proc.memory_percent()
                
                stat = ProcessStats(
                    pid=proc.pid,
                    name=proc.name(),
                    rss=mem_info.rss,
                    vms=mem_info.vms,
                    percent=mem_percent
                )
                stats.append(stat)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if stats:
            self.history.append(stats)
            if len(self.history) > 100:
                self.history.pop(0)
        
        return stats
    
    def get_summary(self) -> Dict[str, Any]:
        """Calculate summary statistics from history."""
        if not self.history:
            return {}
        
        all_rss = [stat.rss for snapshot in self.history for stat in snapshot]
        all_percent = [stat.percent for snapshot in self.history for stat in snapshot]
        
        return {
            "min_rss": min(all_rss),
            "max_rss": max(all_rss),
            "avg_rss": sum(all_rss) / len(all_rss),
            "min_percent": min(all_percent),
            "max_percent": max(all_percent),
            "avg_percent": sum(all_percent) / len(all_percent),
            "samples": len(self.history)
        }

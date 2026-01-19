"""Terminal display formatting and output."""

import os
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


class Display:
    """Handle terminal output and formatting."""
    
    def __init__(self, show_graph: bool = True):
        self.console = Console()
        self.show_graph = show_graph
        self.history_size = 50
        self.rss_history: List[int] = []
        
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024:
                return f"{bytes_value:.1f}{unit}"
            bytes_value /= 1024
        return f"{bytes_value:.1f}TB"
    
    def _get_color(self, percent: float, alerts: List = None) -> str:
        """Determine color based on memory percentage and alerts."""
        if alerts:
            for alert in alerts:
                if alert.level == "critical":
                    return "red"
                elif alert.level == "warning":
                    return "yellow"
        
        if percent >= 80:
            return "red"
        elif percent >= 60:
            return "yellow"
        return "green"
    
    def _create_graph(self, values: List[int], width: int = 50) -> str:
        """Create ASCII graph from values."""
        if not values:
            return ""
        
        max_val = max(values)
        min_val = min(values)
        range_val = max_val - min_val if max_val != min_val else 1
        
        bars = "▁▂▃▄▅▆▇█"
        graph = ""
        
        for val in values[-width:]:
            normalized = (val - min_val) / range_val
            bar_idx = min(int(normalized * (len(bars) - 1)), len(bars) - 1)
            graph += bars[bar_idx]
        
        return graph
    
    def show(self, stats: List, alerts: Optional[List] = None):
        """Display current memory statistics."""
        self.console.clear()
        
        table = Table(title="Memory Usage Monitor", show_header=True)
        table.add_column("PID", style="cyan")
        table.add_column("Process", style="cyan")
        table.add_column("RSS", justify="right")
        table.add_column("VMS", justify="right")
        table.add_column("Memory %", justify="right")
        table.add_column("Status")
        
        total_rss = 0
        
        for stat in stats:
            total_rss += stat.rss
            color = self._get_color(stat.percent, alerts)
            
            status = "OK"
            if alerts:
                for alert in alerts:
                    if alert.pid == stat.pid:
                        status = alert.level.upper()
                        break
            
            table.add_row(
                str(stat.pid),
                stat.name,
                Text(self._format_bytes(stat.rss), style=color),
                self._format_bytes(stat.vms),
                Text(f"{stat.percent:.1f}%", style=color),
                Text(status, style=color)
            )
        
        self.console.print(table)
        
        if self.show_graph and stats:
            self.rss_history.append(total_rss)
            if len(self.rss_history) > self.history_size:
                self.rss_history.pop(0)
            
            graph = self._create_graph(self.rss_history)
            graph_panel = Panel(
                f"RSS History: {graph}\n"
                f"Current: {self._format_bytes(total_rss)} | "
                f"Peak: {self._format_bytes(max(self.rss_history))}",
                title="Memory Trend"
            )
            self.console.print(graph_panel)
        
        if alerts:
            alert_text = Text()
            for alert in alerts:
                alert_text.append(
                    f"⚠ {alert.name} (PID {alert.pid}): {alert.level.upper()}\n",
                    style="red" if alert.level == "critical" else "yellow"
                )
            self.console.print(Panel(alert_text, title="Alerts", border_style="red"))

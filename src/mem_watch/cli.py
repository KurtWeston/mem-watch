"""CLI interface for mem-watch."""

import argparse
import sys
import time
from typing import Optional

from .monitor import MemoryMonitor
from .alerts import AlertManager
from .display import Display
from .export import CSVExporter


def parse_memory_value(value: str) -> int:
    """Parse memory value with unit (e.g., '500M', '2G') to bytes."""
    value = value.upper().strip()
    multipliers = {"K": 1024, "M": 1024**2, "G": 1024**3}
    
    for suffix, multiplier in multipliers.items():
        if value.endswith(suffix):
            return int(float(value[:-1]) * multiplier)
    return int(value)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor process memory usage with alerts and history tracking"
    )
    parser.add_argument("-p", "--pid", type=int, help="Process ID to monitor")
    parser.add_argument("-n", "--name", help="Process name pattern (regex)")
    parser.add_argument(
        "-i", "--interval", type=float, default=1.0, help="Sampling interval in seconds"
    )
    parser.add_argument(
        "-t", "--threshold", help="Memory threshold (e.g., '500M', '2G', '80%%')"
    )
    parser.add_argument(
        "-c", "--children", action="store_true", help="Include child processes"
    )
    parser.add_argument(
        "-e", "--export", help="Export data to CSV file"
    )
    parser.add_argument(
        "-d", "--duration", type=int, help="Monitoring duration in seconds"
    )
    parser.add_argument(
        "--no-graph", action="store_true", help="Disable ASCII graph display"
    )

    args = parser.parse_args()

    if not args.pid and not args.name:
        parser.error("Either --pid or --name must be specified")

    try:
        monitor = MemoryMonitor(
            pid=args.pid,
            name_pattern=args.name,
            include_children=args.children,
            interval=args.interval
        )
        
        alert_manager = None
        if args.threshold:
            alert_manager = AlertManager(args.threshold)
        
        display = Display(show_graph=not args.no_graph)
        exporter = CSVExporter(args.export) if args.export else None
        
        start_time = time.time()
        
        while True:
            stats = monitor.collect()
            
            if not stats:
                print("No matching processes found")
                sys.exit(1)
            
            if alert_manager:
                alerts = alert_manager.check(stats)
                display.show(stats, alerts)
            else:
                display.show(stats)
            
            if exporter:
                exporter.write(stats)
            
            if args.duration and (time.time() - start_time) >= args.duration:
                break
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped")
        if exporter:
            print(f"Data exported to {args.export}")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

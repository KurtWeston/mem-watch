"""Memory monitoring tool for tracking process memory usage."""

__version__ = "0.1.0"
__author__ = "mem-watch"

from .monitor import MemoryMonitor
from .alerts import AlertManager

__all__ = ["MemoryMonitor", "AlertManager", "__version__"]

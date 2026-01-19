"""Tests for alert management functionality."""

import pytest
from mem_watch.alerts import AlertManager, Alert
from mem_watch.monitor import ProcessStats


class TestAlert:
    def test_alert_creation(self):
        alert = Alert(pid=1234, name="test", current=90.0, threshold=80.0, level="warning")
        assert alert.pid == 1234
        assert alert.name == "test"
        assert alert.current == 90.0
        assert alert.threshold == 80.0
        assert alert.level == "warning"


class TestAlertManager:
    def test_parse_percentage_threshold(self):
        manager = AlertManager("80%")
        assert manager.threshold_percent == 80.0
        assert manager.threshold_bytes is None

    def test_parse_megabytes_threshold(self):
        manager = AlertManager("500M")
        assert manager.threshold_bytes == 500 * 1024 * 1024
        assert manager.threshold_percent is None

    def test_parse_gigabytes_threshold(self):
        manager = AlertManager("2G")
        assert manager.threshold_bytes == 2 * 1024 * 1024 * 1024
        assert manager.threshold_percent is None

    def test_parse_kilobytes_threshold(self):
        manager = AlertManager("1024K")
        assert manager.threshold_bytes == 1024 * 1024

    def test_parse_bytes_threshold(self):
        manager = AlertManager("1048576")
        assert manager.threshold_bytes == 1048576

    def test_check_percent_warning(self):
        manager = AlertManager("50%")
        stats = [ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=55.0)]
        alerts = manager.check(stats)
        
        assert len(alerts) == 1
        assert alerts[0].level == "warning"
        assert alerts[0].pid == 1234

    def test_check_percent_critical(self):
        manager = AlertManager("50%")
        stats = [ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=65.0)]
        alerts = manager.check(stats)
        
        assert len(alerts) == 1
        assert alerts[0].level == "critical"

    def test_check_bytes_warning(self):
        manager = AlertManager("1M")
        stats = [ProcessStats(pid=1234, name="test", rss=1100000, vms=2048000, percent=5.0)]
        alerts = manager.check(stats)
        
        assert len(alerts) == 1
        assert alerts[0].level == "warning"

    def test_check_bytes_critical(self):
        manager = AlertManager("1M")
        stats = [ProcessStats(pid=1234, name="test", rss=1500000, vms=2048000, percent=5.0)]
        alerts = manager.check(stats)
        
        assert len(alerts) == 1
        assert alerts[0].level == "critical"

    def test_check_no_alerts(self):
        manager = AlertManager("80%")
        stats = [ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=50.0)]
        alerts = manager.check(stats)
        
        assert len(alerts) == 0

    def test_check_multiple_processes(self):
        manager = AlertManager("50%")
        stats = [
            ProcessStats(pid=1234, name="test1", rss=1024000, vms=2048000, percent=60.0),
            ProcessStats(pid=5678, name="test2", rss=512000, vms=1024000, percent=30.0),
            ProcessStats(pid=9012, name="test3", rss=2048000, vms=4096000, percent=70.0)
        ]
        alerts = manager.check(stats)
        
        assert len(alerts) == 2

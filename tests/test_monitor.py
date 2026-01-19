"""Tests for memory monitoring functionality."""

import pytest
import psutil
from unittest.mock import Mock, patch, MagicMock
from mem_watch.monitor import MemoryMonitor, ProcessStats


class TestProcessStats:
    def test_process_stats_creation(self):
        stats = ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=5.5)
        assert stats.pid == 1234
        assert stats.name == "test"
        assert stats.rss == 1024000
        assert stats.vms == 2048000
        assert stats.percent == 5.5
        assert stats.timestamp > 0


class TestMemoryMonitor:
    def test_monitor_by_pid(self):
        with patch('psutil.Process') as mock_process:
            mock_proc = Mock()
            mock_proc.pid = 1234
            mock_proc.name.return_value = "test_process"
            mock_proc.memory_info.return_value = Mock(rss=1024000, vms=2048000)
            mock_proc.memory_percent.return_value = 5.5
            mock_proc.children.return_value = []
            mock_process.return_value = mock_proc
            
            monitor = MemoryMonitor(pid=1234)
            stats = monitor.collect()
            
            assert len(stats) == 1
            assert stats[0].pid == 1234
            assert stats[0].name == "test_process"
            assert stats[0].rss == 1024000

    def test_monitor_by_name_pattern(self):
        with patch('psutil.process_iter') as mock_iter:
            mock_proc = Mock()
            mock_proc.info = {'pid': 1234, 'name': 'python3'}
            mock_proc.pid = 1234
            mock_proc.name.return_value = "python3"
            mock_proc.memory_info.return_value = Mock(rss=1024000, vms=2048000)
            mock_proc.memory_percent.return_value = 5.5
            mock_proc.children.return_value = []
            mock_iter.return_value = [mock_proc]
            
            monitor = MemoryMonitor(name_pattern="python.*")
            stats = monitor.collect()
            
            assert len(stats) == 1
            assert stats[0].name == "python3"

    def test_monitor_with_children(self):
        with patch('psutil.Process') as mock_process:
            child_proc = Mock()
            child_proc.pid = 5678
            child_proc.name.return_value = "child"
            child_proc.memory_info.return_value = Mock(rss=512000, vms=1024000)
            child_proc.memory_percent.return_value = 2.5
            
            parent_proc = Mock()
            parent_proc.pid = 1234
            parent_proc.name.return_value = "parent"
            parent_proc.memory_info.return_value = Mock(rss=1024000, vms=2048000)
            parent_proc.memory_percent.return_value = 5.5
            parent_proc.children.return_value = [child_proc]
            mock_process.return_value = parent_proc
            
            monitor = MemoryMonitor(pid=1234, include_children=True)
            stats = monitor.collect()
            
            assert len(stats) == 2

    def test_monitor_no_such_process(self):
        with patch('psutil.Process') as mock_process:
            mock_process.side_effect = psutil.NoSuchProcess(1234)
            
            monitor = MemoryMonitor(pid=1234)
            stats = monitor.collect()
            
            assert len(stats) == 0

    def test_history_tracking(self):
        with patch('psutil.Process') as mock_process:
            mock_proc = Mock()
            mock_proc.pid = 1234
            mock_proc.name.return_value = "test"
            mock_proc.memory_info.return_value = Mock(rss=1024000, vms=2048000)
            mock_proc.memory_percent.return_value = 5.5
            mock_proc.children.return_value = []
            mock_process.return_value = mock_proc
            
            monitor = MemoryMonitor(pid=1234)
            monitor.collect()
            monitor.collect()
            
            assert len(monitor.history) == 2

    def test_get_summary(self):
        with patch('psutil.Process') as mock_process:
            mock_proc = Mock()
            mock_proc.pid = 1234
            mock_proc.name.return_value = "test"
            mock_proc.memory_info.return_value = Mock(rss=1024000, vms=2048000)
            mock_proc.memory_percent.return_value = 5.5
            mock_proc.children.return_value = []
            mock_process.return_value = mock_proc
            
            monitor = MemoryMonitor(pid=1234)
            monitor.collect()
            summary = monitor.get_summary()
            
            assert 'min_rss' in summary
            assert 'max_rss' in summary
            assert 'avg_rss' in summary

    def test_get_summary_empty_history(self):
        monitor = MemoryMonitor(pid=1234)
        summary = monitor.get_summary()
        assert summary == {}

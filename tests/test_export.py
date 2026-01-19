"""Tests for CSV export functionality."""

import pytest
import csv
from pathlib import Path
from mem_watch.export import CSVExporter
from mem_watch.monitor import ProcessStats


class TestCSVExporter:
    def test_write_creates_file(self, tmp_path):
        filepath = tmp_path / "test.csv"
        exporter = CSVExporter(str(filepath))
        stats = [ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=5.5)]
        
        exporter.write(stats)
        
        assert filepath.exists()

    def test_write_headers(self, tmp_path):
        filepath = tmp_path / "test.csv"
        exporter = CSVExporter(str(filepath))
        stats = [ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=5.5)]
        
        exporter.write(stats)
        
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert headers == ['timestamp', 'pid', 'name', 'rss_bytes', 'vms_bytes', 'memory_percent']

    def test_write_data(self, tmp_path):
        filepath = tmp_path / "test.csv"
        exporter = CSVExporter(str(filepath))
        stats = [ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=5.5)]
        
        exporter.write(stats)
        
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip headers
            row = next(reader)
            assert row[1] == '1234'
            assert row[2] == 'test'
            assert row[3] == '1024000'
            assert row[4] == '2048000'
            assert row[5] == '5.50'

    def test_write_multiple_stats(self, tmp_path):
        filepath = tmp_path / "test.csv"
        exporter = CSVExporter(str(filepath))
        stats = [
            ProcessStats(pid=1234, name="test1", rss=1024000, vms=2048000, percent=5.5),
            ProcessStats(pid=5678, name="test2", rss=512000, vms=1024000, percent=2.5)
        ]
        
        exporter.write(stats)
        
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip headers
            rows = list(reader)
            assert len(rows) == 2

    def test_append_mode(self, tmp_path):
        filepath = tmp_path / "test.csv"
        exporter = CSVExporter(str(filepath))
        stats1 = [ProcessStats(pid=1234, name="test", rss=1024000, vms=2048000, percent=5.5)]
        stats2 = [ProcessStats(pid=5678, name="test2", rss=512000, vms=1024000, percent=2.5)]
        
        exporter.write(stats1)
        exporter.write(stats2)
        
        with open(filepath, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip headers
            rows = list(reader)
            assert len(rows) == 2

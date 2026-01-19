"""Tests for display functionality."""

import pytest
from mem_watch.display import Display
from mem_watch.monitor import ProcessStats
from mem_watch.alerts import Alert


class TestDisplay:
    def test_format_bytes(self):
        display = Display()
        assert display._format_bytes(500) == "500.0B"
        assert display._format_bytes(1024) == "1.0KB"
        assert display._format_bytes(1024 * 1024) == "1.0MB"
        assert display._format_bytes(1024 * 1024 * 1024) == "1.0GB"

    def test_get_color_normal(self):
        display = Display()
        assert display._get_color(50.0) == "green"

    def test_get_color_warning(self):
        display = Display()
        assert display._get_color(65.0) == "yellow"

    def test_get_color_critical(self):
        display = Display()
        assert display._get_color(85.0) == "red"

    def test_get_color_with_alert(self):
        display = Display()
        alerts = [Alert(pid=1234, name="test", current=90.0, threshold=80.0, level="critical")]
        assert display._get_color(50.0, alerts) == "red"

    def test_create_graph(self):
        display = Display()
        values = [100, 200, 300, 200, 100]
        graph = display._create_graph(values)
        assert len(graph) == 5
        assert all(c in "▁▂▃▄▅▆▇█" for c in graph)

    def test_create_graph_empty(self):
        display = Display()
        graph = display._create_graph([])
        assert graph == ""

    def test_create_graph_single_value(self):
        display = Display()
        graph = display._create_graph([100])
        assert len(graph) == 1

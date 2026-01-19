"""Tests for CLI functionality."""

import pytest
from mem_watch.cli import parse_memory_value


class TestParseMemoryValue:
    def test_parse_kilobytes(self):
        assert parse_memory_value("100K") == 100 * 1024
        assert parse_memory_value("100k") == 100 * 1024

    def test_parse_megabytes(self):
        assert parse_memory_value("500M") == 500 * 1024 * 1024
        assert parse_memory_value("500m") == 500 * 1024 * 1024

    def test_parse_gigabytes(self):
        assert parse_memory_value("2G") == 2 * 1024 * 1024 * 1024
        assert parse_memory_value("2g") == 2 * 1024 * 1024 * 1024

    def test_parse_bytes(self):
        assert parse_memory_value("1048576") == 1048576

    def test_parse_decimal_values(self):
        assert parse_memory_value("1.5G") == int(1.5 * 1024 * 1024 * 1024)
        assert parse_memory_value("0.5M") == int(0.5 * 1024 * 1024)

    def test_parse_with_whitespace(self):
        assert parse_memory_value(" 100M ") == 100 * 1024 * 1024

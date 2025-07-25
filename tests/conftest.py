"""Test configuration and fixtures."""

from unittest.mock import Mock, patch

import pytest

# Common test fixtures and utilities


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for testing."""
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_platform_system():
    """Mock platform.system for testing."""
    with patch("platform.system") as mock_system:
        yield mock_system


@pytest.fixture
def mock_psutil():
    """Mock psutil for testing."""
    with (
        patch("psutil.cpu_count") as mock_cpu_count,
        patch("psutil.cpu_percent") as mock_cpu_percent,
        patch("psutil.virtual_memory") as mock_virtual_memory,
        patch("psutil.swap_memory") as mock_swap_memory,
        patch("psutil.disk_partitions") as mock_disk_partitions,
        patch("psutil.disk_usage") as mock_disk_usage,
        patch("psutil.net_if_addrs") as mock_net_if_addrs,
        patch("psutil.net_if_stats") as mock_net_if_stats,
        patch("psutil.boot_time") as mock_boot_time,
    ):

        # Set up default return values
        mock_cpu_count.return_value = 4
        mock_cpu_percent.return_value = 25.0

        memory_mock = Mock()
        memory_mock.total = 8589934592  # 8GB
        memory_mock.available = 4294967296  # 4GB
        memory_mock.used = 4294967296  # 4GB
        memory_mock.free = 4294967296  # 4GB
        memory_mock.percent = 50.0
        mock_virtual_memory.return_value = memory_mock

        swap_mock = Mock()
        swap_mock.total = 2147483648  # 2GB
        swap_mock.used = 0
        swap_mock.free = 2147483648  # 2GB
        swap_mock.percent = 0.0
        mock_swap_memory.return_value = swap_mock

        mock_boot_time.return_value = 1234567890

        yield {
            "cpu_count": mock_cpu_count,
            "cpu_percent": mock_cpu_percent,
            "virtual_memory": mock_virtual_memory,
            "swap_memory": mock_swap_memory,
            "disk_partitions": mock_disk_partitions,
            "disk_usage": mock_disk_usage,
            "net_if_addrs": mock_net_if_addrs,
            "net_if_stats": mock_net_if_stats,
            "boot_time": mock_boot_time,
        }

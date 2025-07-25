"""Tests for system information utilities."""

from unittest.mock import Mock, patch

from nettools.core.sysinfo import SystemInfo


class TestSystemInfo:
    """Test cases for SystemInfo functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.sysinfo = SystemInfo()

    def test_get_platform_info(self):
        """Test getting platform information."""
        with patch("nettools.core.sysinfo.get_platform_info") as mock_get_platform_info:
            mock_get_platform_info.return_value = {
                "platform": "linux",
                "system": "Linux",
                "architecture": "64bit",
                "node": "test-host",
                "release": "5.4.0",
                "version": "#48-Ubuntu",
                "machine": "x86_64",
                "processor": "x86_64",
            }

            result = self.sysinfo.get_platform_info()

            assert result["platform"] == "linux"
            assert result["system"] == "Linux"
            assert result["hostname"] == "test-host"

    def test_get_cpu_info(self, mock_psutil):
        """Test getting CPU information."""
        mock_psutil["cpu_count"].return_value = 8
        mock_psutil["cpu_percent"].return_value = 35.5

        result = self.sysinfo.get_cpu_info()

        assert result["count"] == 8
        assert result["usage"] == 35.5

    def test_get_memory_info(self, mock_psutil):
        """Test getting memory information."""
        memory_mock = mock_psutil["virtual_memory"].return_value
        swap_mock = mock_psutil["swap_memory"].return_value

        result = self.sysinfo.get_memory_info()

        assert result["virtual"]["total"] == memory_mock.total
        assert result["virtual"]["available"] == memory_mock.available
        assert result["virtual"]["used"] == memory_mock.used
        assert result["virtual"]["percent"] == memory_mock.percent
        assert result["swap"]["total"] == swap_mock.total
        assert result["swap"]["used"] == swap_mock.used
        assert result["swap"]["percent"] == swap_mock.percent

    def test_get_disk_info(self, mock_psutil):
        """Test getting disk information."""
        # Mock disk partition
        partition_mock = Mock()
        partition_mock.device = "/dev/sda1"
        partition_mock.mountpoint = "/"
        partition_mock.fstype = "ext4"
        mock_psutil["disk_partitions"].return_value = [partition_mock]

        # Mock disk usage
        usage_mock = Mock()
        usage_mock.total = 1000000000  # 1GB
        usage_mock.used = 500000000  # 500MB
        usage_mock.free = 500000000  # 500MB
        mock_psutil["disk_usage"].return_value = usage_mock

        result = self.sysinfo.get_disk_info()

        assert len(result["partitions"]) == 1
        partition = result["partitions"][0]
        assert partition["device"] == "/dev/sda1"
        assert partition["mountpoint"] == "/"
        assert partition["fstype"] == "ext4"
        assert partition["total"] == 1000000000
        assert partition["used"] == 500000000
        assert partition["free"] == 500000000
        assert partition["percent"] == 50.0

    def test_get_uptime(self, mock_psutil):
        """Test getting system uptime."""
        with patch("time.time") as mock_time:
            mock_time.return_value = 1234567890 + 86400  # 1 day later
            mock_psutil["boot_time"].return_value = 1234567890

            result = self.sysinfo.get_uptime()

            assert "1 day" in result

    @patch("nettools.core.sysinfo.get_platform_info")
    def test_get_all_info(self, mock_get_platform_info, mock_psutil):
        """Test getting all system information."""
        mock_get_platform_info.return_value = {
            "platform": "linux",
            "system": "Linux",
            "architecture": "64bit",
            "node": "test-host",
            "release": "5.4.0",
            "version": "#48-Ubuntu",
            "machine": "x86_64",
            "processor": "x86_64",
        }

        with patch("time.time") as mock_time:
            mock_time.return_value = 1234567890 + 3600  # 1 hour later
            mock_psutil["boot_time"].return_value = 1234567890

            # Mock empty disk partitions to avoid issues
            mock_psutil["disk_partitions"].return_value = []

            result = self.sysinfo.get_all_info()

            assert "platform" in result
            assert "cpu" in result
            assert "memory" in result
            assert "disk" in result
            assert "uptime" in result
            assert "timestamp" in result
            assert result["platform"] == "linux"

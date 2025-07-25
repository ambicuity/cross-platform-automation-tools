"""Tests for iperf3 wrapper functionality."""

import json
import subprocess
from unittest.mock import Mock, patch

from nettools.core.iperf3 import IPerf3Wrapper


class TestIPerf3Wrapper:
    """Test cases for IPerf3Wrapper functionality."""

    def setup_method(self):
        """Set up test environment."""
        with patch.object(IPerf3Wrapper, "_check_iperf3_availability"):
            self.iperf3 = IPerf3Wrapper()

    @patch("subprocess.run")
    def test_check_iperf3_availability_success(self, mock_run):
        """Test successful iperf3 availability check."""
        mock_run.return_value.returncode = 0

        # Should not raise an exception
        wrapper = IPerf3Wrapper()
        assert wrapper is not None

    @patch("subprocess.run")
    def test_check_iperf3_availability_failure(self, mock_run):
        """Test iperf3 availability check failure."""
        mock_run.side_effect = FileNotFoundError()

        try:
            IPerf3Wrapper()
            raise AssertionError("Should have raised RuntimeError")
        except RuntimeError as e:
            assert "iperf3 is not installed" in str(e)

    def test_run_server(self):
        """Test running iperf3 in server mode."""
        with patch("subprocess.Popen") as mock_popen:
            mock_process = Mock()
            mock_process.pid = 12345
            mock_popen.return_value = mock_process

            result = self.iperf3.run_server(port=5201)

            assert result["mode"] == "server"
            assert result["port"] == 5201
            assert result["status"] == "running"
            assert result["pid"] == 12345

    @patch("subprocess.run")
    def test_run_client_success(self, mock_run):
        """Test successful iperf3 client run."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = json.dumps(
            {
                "start": {"connecting_to": {"host": "192.168.1.5", "port": 5201}},
                "end": {
                    "sum_received": {
                        "seconds": 10.0,
                        "bytes": 1000000000,
                        "bits_per_second": 800000000,
                    },
                    "sum_sent": {"retransmits": 0},
                    "cpu_utilization_percent": {"host_total": 5.0, "remote_total": 3.0},
                },
            }
        )
        mock_run.return_value = mock_result

        result = self.iperf3.run_client("192.168.1.5")

        assert result["mode"] == "client"
        assert result["host"] == "192.168.1.5"
        assert result["port"] == 5201
        assert result["duration"] == 10.0
        assert result["bandwidth"] == 800.0  # 800 Mbits/sec

    @patch("subprocess.run")
    def test_run_client_timeout(self, mock_run):
        """Test iperf3 client timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("iperf3", 30)

        try:
            self.iperf3.run_client("192.168.1.5")
            raise AssertionError("Should have raised RuntimeError")
        except RuntimeError as e:
            assert "timed out" in str(e)

    def test_parse_client_result(self):
        """Test parsing iperf3 client results."""
        raw_result = {
            "start": {"connecting_to": {"host": "test.com", "port": 5201}},
            "end": {
                "sum_received": {
                    "seconds": 10.0,
                    "bytes": 1250000000,
                    "bits_per_second": 1000000000,
                },
                "sum_sent": {"retransmits": 2},
                "cpu_utilization_percent": {"host_total": 10.0, "remote_total": 8.0},
            },
        }

        result = self.iperf3._parse_client_result(raw_result)

        assert result["mode"] == "client"
        assert result["host"] == "test.com"
        assert result["port"] == 5201
        assert result["duration"] == 10.0
        assert result["bytes_transferred"] == 1250000000
        assert result["bandwidth"] == 1000.0  # 1000 Mbits/sec
        assert result["retransmits"] == 2

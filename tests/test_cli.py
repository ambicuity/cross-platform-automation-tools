"""Tests for the CLI module."""

import json
from unittest.mock import patch

from typer.testing import CliRunner

from nettools.cli.main import app


class TestCLI:
    """Test cases for CLI functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()

    def test_app_help(self):
        """Test that the app shows help information."""
        result = self.runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "nettools" in result.stdout
        assert "Cross-platform CLI automation suite" in result.stdout

    @patch("nettools.core.ping.PingWrapper.ping")
    def test_ping_host_command(self, mock_ping):
        """Test ping-host command."""
        mock_ping.return_value = {
            "host": "example.com",
            "packets_sent": 4,
            "packets_received": 4,
            "packet_loss": 0.0,
            "avg_time": 20.5,
            "min_time": 18.2,
            "max_time": 23.1,
        }

        result = self.runner.invoke(app, ["ping-host", "example.com"])
        assert result.exit_code == 0
        mock_ping.assert_called_once()

    @patch("nettools.core.ping.PingWrapper.ping")
    def test_ping_host_json_output(self, mock_ping):
        """Test ping-host command with JSON output."""
        expected_result = {
            "host": "example.com",
            "packets_sent": 4,
            "packets_received": 4,
            "packet_loss": 0.0,
            "avg_time": 20.5,
        }
        mock_ping.return_value = expected_result

        result = self.runner.invoke(app, ["ping-host", "example.com", "--json"])
        assert result.exit_code == 0

        # Extract JSON from output (skip any initial lines)
        lines = result.stdout.strip().split("\n")
        json_start = -1
        for i, line in enumerate(lines):
            if line.strip().startswith("{"):
                json_start = i
                break

        assert json_start != -1, "No JSON found in output"
        json_output = "\n".join(lines[json_start:])
        output_data = json.loads(json_output)
        assert output_data == expected_result

    @patch("nettools.core.ports.PortChecker.check_ports")
    def test_check_ports_command(self, mock_check_ports):
        """Test check-ports command."""
        mock_check_ports.return_value = {
            "host": "localhost",
            "total_ports": 2,
            "open_ports": 1,
            "closed_ports": 1,
            "ports": [
                {"port": 80, "open": True, "response_time": 0.001},
                {"port": 443, "open": False, "response_time": 1.0},
            ],
        }

        result = self.runner.invoke(app, ["check-ports", "80,443"])
        assert result.exit_code == 0
        mock_check_ports.assert_called_once()

    @patch("nettools.core.sysinfo.SystemInfo.get_all_info")
    def test_sysinfo_command(self, mock_get_all_info):
        """Test sysinfo command."""
        mock_get_all_info.return_value = {
            "platform": "linux",
            "hostname": "test-host",
            "cpu": {"count": 4, "usage": 25.0},
            "memory": {"total": 8589934592, "available": 4294967296, "percent": 50.0},
        }

        result = self.runner.invoke(app, ["sysinfo"])
        assert result.exit_code == 0
        mock_get_all_info.assert_called_once()

    @patch("nettools.core.iperf3.IPerf3Wrapper._check_iperf3_availability")
    @patch("nettools.core.iperf3.IPerf3Wrapper.run_client")
    def test_iperf3_client_command(self, mock_run_client, mock_check_iperf3):
        """Test iperf3-run command in client mode."""
        mock_check_iperf3.return_value = None  # No exception means iperf3 is available
        mock_run_client.return_value = {
            "mode": "client",
            "host": "192.168.1.5",
            "port": 5201,
            "bandwidth": 95.2,
            "duration": 10,
        }

        result = self.runner.invoke(app, ["iperf3-run", "--client", "192.168.1.5"])
        assert result.exit_code == 0
        mock_run_client.assert_called_once()

    @patch("nettools.core.iperf3.IPerf3Wrapper._check_iperf3_availability")
    def test_iperf3_no_mode_error(self, mock_check_iperf3):
        """Test iperf3-run command without specifying server or client mode."""
        mock_check_iperf3.return_value = None  # No exception means iperf3 is available

        result = self.runner.invoke(app, ["iperf3-run"])
        assert result.exit_code == 1
        assert "Must specify either --server or --client" in result.stdout

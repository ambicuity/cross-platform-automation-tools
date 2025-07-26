"""Tests for port checking functionality."""

from unittest.mock import Mock, patch

from nettools.core.ports import PortChecker


class TestPortChecker:
    """Test cases for PortChecker functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.port_checker = PortChecker()

    @patch("socket.socket")
    def test_check_port_open(self, mock_socket_class):
        """Test checking an open port."""
        mock_socket = Mock()
        mock_socket.connect_ex.return_value = 0  # Success
        mock_socket_class.return_value.__enter__.return_value = mock_socket

        result = self.port_checker.check_port("localhost", 80)

        assert result["port"] == 80
        assert result["open"] is True
        assert result["error"] is None
        assert "response_time" in result

    @patch("socket.socket")
    def test_check_port_closed(self, mock_socket_class):
        """Test checking a closed port."""
        mock_socket = Mock()
        mock_socket.connect_ex.return_value = 111  # Connection refused
        mock_socket_class.return_value.__enter__.return_value = mock_socket

        result = self.port_checker.check_port("localhost", 8080)

        assert result["port"] == 8080
        assert result["open"] is False
        assert "Connection failed" in result["error"]

    @patch("socket.socket")
    def test_check_port_timeout(self, mock_socket_class):
        """Test port check timeout."""
        mock_socket = Mock()
        mock_socket.connect_ex.side_effect = TimeoutError("Connection timeout")
        mock_socket_class.return_value.__enter__.return_value = mock_socket

        result = self.port_checker.check_port("localhost", 443)

        assert result["port"] == 443
        assert result["open"] is False
        assert "timeout" in result["error"].lower()

    @patch("socket.socket")
    def test_check_ports_multiple(self, mock_socket_class):
        """Test checking multiple ports."""
        mock_socket = Mock()
        # Mock responses: 80 open, 443 open, 8080 closed
        mock_socket.connect_ex.side_effect = [0, 0, 111]
        mock_socket_class.return_value.__enter__.return_value = mock_socket

        result = self.port_checker.check_ports("localhost", [80, 443, 8080])

        assert result["host"] == "localhost"
        assert result["total_ports"] == 3
        assert result["open_ports"] == 2
        assert result["closed_ports"] == 1
        assert len(result["ports"]) == 3
        assert 80 in result["summary"]["open"]
        assert 443 in result["summary"]["open"]
        assert 8080 in result["summary"]["closed"]

    def test_check_service_known(self):
        """Test checking a known service."""
        with patch.object(self.port_checker, "check_port") as mock_check:
            mock_check.return_value = {
                "port": 80,
                "open": True,
                "response_time": 0.001,
                "error": None,
            }

            result = self.port_checker.check_service("localhost", "http")

            assert result["service"] == "http"
            assert result["port"] == 80
            assert result["available"] is True
            mock_check.assert_called_once_with("localhost", 80, 5)

    def test_check_service_unknown(self):
        """Test checking an unknown service."""
        result = self.port_checker.check_service("localhost", "unknown_service")

        assert result["service"] == "unknown_service"
        assert "error" in result
        assert "Unknown service" in result["error"]

    def test_scan_common_ports(self):
        """Test scanning common ports."""
        with patch.object(self.port_checker, "check_ports") as mock_check_ports:
            mock_check_ports.return_value = {
                "host": "localhost",
                "total_ports": 20,
                "open_ports": 3,
                "ports": [],
            }

            result = self.port_checker.scan_common_ports("localhost")

            assert result["host"] == "localhost"
            mock_check_ports.assert_called_once()
            # Verify common ports are included
            args = mock_check_ports.call_args[0]
            ports = args[1]
            assert 80 in ports  # HTTP
            assert 443 in ports  # HTTPS
            assert 22 in ports  # SSH

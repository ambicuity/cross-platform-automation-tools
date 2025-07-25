"""Tests for platform detection utilities."""

from unittest.mock import patch

from nettools.utils.platform_detect import (
    PlatformType,
    get_platform,
    get_platform_info,
    get_shell_command_prefix,
    is_linux,
    is_macos,
    is_windows,
)


class TestPlatformDetect:
    """Test cases for platform detection functionality."""

    @patch("platform.system")
    def test_get_platform_linux(self, mock_system):
        """Test platform detection for Linux."""
        mock_system.return_value = "Linux"
        assert get_platform() == PlatformType.LINUX

    @patch("platform.system")
    def test_get_platform_macos(self, mock_system):
        """Test platform detection for macOS."""
        mock_system.return_value = "Darwin"
        assert get_platform() == PlatformType.MACOS

    @patch("platform.system")
    def test_get_platform_windows(self, mock_system):
        """Test platform detection for Windows."""
        mock_system.return_value = "Windows"
        assert get_platform() == PlatformType.WINDOWS

    @patch("platform.system")
    def test_get_platform_unknown(self, mock_system):
        """Test platform detection for unknown system."""
        mock_system.return_value = "UnknownOS"
        assert get_platform() == PlatformType.UNKNOWN

    @patch("platform.system")
    def test_is_windows_true(self, mock_system):
        """Test is_windows returns True on Windows."""
        mock_system.return_value = "Windows"
        assert is_windows() is True
        assert is_linux() is False
        assert is_macos() is False

    @patch("platform.system")
    def test_is_linux_true(self, mock_system):
        """Test is_linux returns True on Linux."""
        mock_system.return_value = "Linux"
        assert is_linux() is True
        assert is_windows() is False
        assert is_macos() is False

    @patch("platform.system")
    def test_is_macos_true(self, mock_system):
        """Test is_macos returns True on macOS."""
        mock_system.return_value = "Darwin"
        assert is_macos() is True
        assert is_windows() is False
        assert is_linux() is False

    @patch("platform.system")
    @patch("platform.release")
    @patch("platform.version")
    @patch("platform.machine")
    @patch("platform.processor")
    @patch("platform.architecture")
    @patch("platform.node")
    def test_get_platform_info(
        self,
        mock_node,
        mock_architecture,
        mock_processor,
        mock_machine,
        mock_version,
        mock_release,
        mock_system,
    ):
        """Test get_platform_info returns comprehensive information."""
        mock_system.return_value = "Linux"
        mock_release.return_value = "5.4.0"
        mock_version.return_value = "#48-Ubuntu"
        mock_machine.return_value = "x86_64"
        mock_processor.return_value = "x86_64"
        mock_architecture.return_value = ("64bit", "ELF")
        mock_node.return_value = "test-host"

        info = get_platform_info()

        assert info["system"] == "Linux"
        assert info["platform"] == "linux"
        assert info["release"] == "5.4.0"
        assert info["version"] == "#48-Ubuntu"
        assert info["machine"] == "x86_64"
        assert info["processor"] == "x86_64"
        assert info["architecture"] == "64bit"
        assert info["node"] == "test-host"

    @patch("platform.system")
    def test_get_shell_command_prefix_windows(self, mock_system):
        """Test shell command prefix for Windows."""
        mock_system.return_value = "Windows"
        prefix = get_shell_command_prefix()
        assert prefix == ("cmd", "/c")

    @patch("platform.system")
    def test_get_shell_command_prefix_unix(self, mock_system):
        """Test shell command prefix for Unix-like systems."""
        mock_system.return_value = "Linux"
        prefix = get_shell_command_prefix()
        assert prefix == ("sh", "-c")

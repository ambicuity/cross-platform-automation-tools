"""Platform detection utilities."""

import platform
from enum import Enum


class PlatformType(Enum):
    """Enumeration of supported platforms."""

    LINUX = "linux"
    MACOS = "macos"
    WINDOWS = "windows"
    UNKNOWN = "unknown"


def get_platform() -> PlatformType:
    """Detect the current platform.

    Returns:
        PlatformType enum value representing the current platform.
    """
    system = platform.system().lower()

    if system == "linux":
        return PlatformType.LINUX
    elif system == "darwin":
        return PlatformType.MACOS
    elif system == "windows":
        return PlatformType.WINDOWS
    else:
        return PlatformType.UNKNOWN


def get_platform_info() -> dict:
    """Get detailed platform information.

    Returns:
        Dictionary containing platform details.
    """
    return {
        "system": platform.system(),
        "platform": get_platform().value,
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0],
        "node": platform.node(),
    }


def is_windows() -> bool:
    """Check if running on Windows."""
    return get_platform() == PlatformType.WINDOWS


def is_linux() -> bool:
    """Check if running on Linux."""
    return get_platform() == PlatformType.LINUX


def is_macos() -> bool:
    """Check if running on macOS."""
    return get_platform() == PlatformType.MACOS


def get_shell_command_prefix() -> tuple[str, ...]:
    """Get the appropriate shell command prefix for the platform.

    Returns:
        Tuple of command prefix parts.
    """
    if is_windows():
        return ("cmd", "/c")
    else:
        return ("sh", "-c")

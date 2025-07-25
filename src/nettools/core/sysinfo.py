"""System information utilities."""

import time
from datetime import datetime, timedelta
from typing import Any

import psutil  # type: ignore[import-untyped]

from nettools.utils.logger import get_logger
from nettools.utils.platform_detect import get_platform_info


class SystemInfo:
    """Utility class for gathering system information."""

    def __init__(self) -> None:
        """Initialize the system info utility."""
        self.logger = get_logger(self.__class__.__name__)

    def get_all_info(self) -> dict:
        """Get comprehensive system information.

        Returns:
            Dictionary with all system information.
        """
        self.logger.debug("Gathering system information")

        return {
            **self.get_platform_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "uptime": self.get_uptime(),
            "timestamp": datetime.now().isoformat(),
        }

    def get_platform_info(self) -> dict:
        """Get platform and OS information.

        Returns:
            Dictionary with platform details.
        """
        platform_info = get_platform_info()

        return {
            "platform": platform_info["platform"],
            "system": platform_info["system"],
            "architecture": platform_info["architecture"],
            "hostname": platform_info["node"],
            "release": platform_info["release"],
            "version": platform_info["version"],
            "machine": platform_info["machine"],
            "processor": platform_info["processor"],
        }

    def get_cpu_info(self) -> dict:
        """Get CPU information and usage statistics.

        Returns:
            Dictionary with CPU details.
        """
        try:
            cpu_info = {
                "count": psutil.cpu_count(logical=True),
                "physical_count": psutil.cpu_count(logical=False),
                "usage": psutil.cpu_percent(interval=1),
                "frequency": None,
                "load_avg": None,
            }

            # Get CPU frequency if available
            try:
                freq = psutil.cpu_freq()
                if freq:
                    cpu_info["frequency"] = {
                        "current": freq.current,
                        "min": freq.min,
                        "max": freq.max,
                    }
            except (AttributeError, NotImplementedError):
                self.logger.debug("CPU frequency information not available")

            # Get load average (Unix-like systems only)
            try:
                if hasattr(psutil, "getloadavg"):
                    load_avg = psutil.getloadavg()
                    cpu_info["load_avg"] = {
                        "1min": load_avg[0],
                        "5min": load_avg[1],
                        "15min": load_avg[2],
                    }
            except (AttributeError, NotImplementedError):
                self.logger.debug("Load average information not available")

            return cpu_info

        except Exception as e:
            self.logger.error(f"Error getting CPU info: {e}")
            return {"error": str(e)}

    def get_memory_info(self) -> dict:
        """Get memory usage information.

        Returns:
            Dictionary with memory details.
        """
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                "virtual": {
                    "total": memory.total,
                    "available": memory.available,
                    "used": memory.used,
                    "free": memory.free,
                    "percent": memory.percent,
                },
                "swap": {
                    "total": swap.total,
                    "used": swap.used,
                    "free": swap.free,
                    "percent": swap.percent,
                },
                # Backward compatibility
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent,
            }

        except Exception as e:
            self.logger.error(f"Error getting memory info: {e}")
            return {"error": str(e)}

    def get_disk_info(self) -> dict:
        """Get disk usage information.

        Returns:
            Dictionary with disk details.
        """
        try:
            disk_info: dict[str, Any] = {"partitions": []}

            # Get all disk partitions
            partitions = psutil.disk_partitions()

            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partition_info = {
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent": (
                            (usage.used / usage.total) * 100 if usage.total > 0 else 0
                        ),
                    }
                    disk_info["partitions"].append(partition_info)
                except (PermissionError, FileNotFoundError, OSError):
                    # Skip partitions that can't be accessed
                    continue

            # Calculate total disk space across all partitions
            if disk_info["partitions"]:
                total_space = sum(p["total"] for p in disk_info["partitions"])
                used_space = sum(p["used"] for p in disk_info["partitions"])
                free_space = sum(p["free"] for p in disk_info["partitions"])

                disk_info["summary"] = {
                    "total": total_space,
                    "used": used_space,
                    "free": free_space,
                    "percent": (
                        (used_space / total_space) * 100 if total_space > 0 else 0
                    ),
                }

            return disk_info

        except Exception as e:
            self.logger.error(f"Error getting disk info: {e}")
            return {"error": str(e)}

    def get_network_info(self) -> dict:
        """Get network interface information.

        Returns:
            Dictionary with network details.
        """
        try:
            network_info: dict[str, Any] = {"interfaces": []}

            # Get network interfaces
            interfaces = psutil.net_if_addrs()
            stats = psutil.net_if_stats()

            for interface_name, addresses in interfaces.items():
                interface_info = {
                    "name": interface_name,
                    "addresses": [],
                    "stats": None,
                }

                # Get addresses for this interface
                for addr in addresses:
                    addr_info = {
                        "family": str(addr.family),
                        "address": addr.address,
                        "netmask": addr.netmask,
                        "broadcast": addr.broadcast,
                    }
                    interface_info["addresses"].append(addr_info)

                # Get interface statistics
                if interface_name in stats:
                    stat = stats[interface_name]
                    interface_info["stats"] = {
                        "is_up": stat.isup,
                        "duplex": str(stat.duplex),
                        "speed": stat.speed,
                        "mtu": stat.mtu,
                    }

                network_info["interfaces"].append(interface_info)

            # Get network I/O statistics
            try:
                io_counters = psutil.net_io_counters()
                network_info["io_counters"] = {
                    "bytes_sent": io_counters.bytes_sent,
                    "bytes_recv": io_counters.bytes_recv,
                    "packets_sent": io_counters.packets_sent,
                    "packets_recv": io_counters.packets_recv,
                    "errin": io_counters.errin,
                    "errout": io_counters.errout,
                    "dropin": io_counters.dropin,
                    "dropout": io_counters.dropout,
                }
            except AttributeError:
                self.logger.debug("Network I/O counters not available")

            return network_info

        except Exception as e:
            self.logger.error(f"Error getting network info: {e}")
            return {"error": str(e)}

    def get_uptime(self) -> str:
        """Get system uptime.

        Returns:
            String representation of system uptime.
        """
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_delta = timedelta(seconds=uptime_seconds)

            # Format uptime as "X days, Y hours, Z minutes"
            days = uptime_delta.days
            hours, remainder = divmod(uptime_delta.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            parts = []
            if days > 0:
                parts.append(f"{days} day{'s' if days != 1 else ''}")
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
            if minutes > 0:
                parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

            return ", ".join(parts) if parts else "less than a minute"

        except Exception as e:
            self.logger.error(f"Error getting uptime: {e}")
            return f"Error: {e}"

    def get_processes(self, limit: int = 10) -> dict:
        """Get information about running processes.

        Args:
            limit: Maximum number of processes to return

        Returns:
            Dictionary with process information.
        """
        try:
            processes = []

            for proc in psutil.process_iter(
                ["pid", "name", "username", "cpu_percent", "memory_percent"]
            ):
                try:
                    process_info = proc.info
                    process_info["cpu_percent"] = proc.cpu_percent()
                    processes.append(process_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Sort by CPU usage
            processes.sort(key=lambda x: x.get("cpu_percent", 0), reverse=True)

            return {
                "total_processes": len(processes),
                "top_processes": processes[:limit],
            }

        except Exception as e:
            self.logger.error(f"Error getting process info: {e}")
            return {"error": str(e)}

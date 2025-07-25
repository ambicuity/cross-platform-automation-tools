"""Ping wrapper for network connectivity testing."""

import re
import statistics
import subprocess

from nettools.utils.logger import get_logger
from nettools.utils.platform_detect import is_windows


class PingWrapper:
    """Wrapper class for ping operations."""

    def __init__(self) -> None:
        """Initialize the ping wrapper."""
        self.logger = get_logger(self.__class__.__name__)

    def ping(
        self,
        host: str,
        count: int = 4,
        timeout: int = 5,
        packet_size: int | None = None,
    ) -> dict:
        """Ping a host and return connectivity results.

        Args:
            host: Hostname or IP address to ping
            count: Number of ping packets to send
            timeout: Timeout in seconds for each ping
            packet_size: Size of ping packets in bytes (optional)

        Returns:
            Dictionary with ping results.
        """
        cmd = self._build_ping_command(host, count, timeout, packet_size)

        self.logger.info(f"Pinging {host} with {count} packets")
        self.logger.debug(f"Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout * count + 10,  # Add buffer time
            )

            return self._parse_ping_output(result.stdout, result.stderr, host, count)

        except subprocess.TimeoutExpired:
            self.logger.error(f"Ping to {host} timed out")
            return {
                "host": host,
                "packets_sent": count,
                "packets_received": 0,
                "packet_loss": 100.0,
                "error": "Timeout expired",
            }
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to ping {host}: {e}")
            return {
                "host": host,
                "packets_sent": count,
                "packets_received": 0,
                "packet_loss": 100.0,
                "error": str(e),
            }

    def _build_ping_command(
        self, host: str, count: int, timeout: int, packet_size: int | None
    ) -> list[str]:
        """Build the appropriate ping command for the current platform.

        Args:
            host: Target host
            count: Number of pings
            timeout: Timeout per ping
            packet_size: Packet size in bytes

        Returns:
            List of command arguments.
        """
        if is_windows():
            cmd = [
                "ping",
                "-n",
                str(count),
                "-w",
                str(timeout * 1000),
            ]  # Windows uses milliseconds
            if packet_size:
                cmd.extend(["-l", str(packet_size)])
        else:
            cmd = ["ping", "-c", str(count), "-W", str(timeout)]
            if packet_size:
                cmd.extend(["-s", str(packet_size)])

        cmd.append(host)
        return cmd

    def _parse_ping_output(
        self, stdout: str, stderr: str, host: str, count: int
    ) -> dict:
        """Parse ping command output into a standardized format.

        Args:
            stdout: Standard output from ping command
            stderr: Standard error from ping command
            host: Target host
            count: Number of pings sent

        Returns:
            Parsed ping results.
        """
        result = {
            "host": host,
            "packets_sent": count,
            "packets_received": 0,
            "packet_loss": 100.0,
            "times": [],
            "min_time": None,
            "max_time": None,
            "avg_time": None,
            "raw_output": stdout,
        }

        if stderr:
            result["error"] = stderr.strip()
            return result

        try:
            if is_windows():
                result.update(self._parse_windows_ping(stdout))
            else:
                result.update(self._parse_unix_ping(stdout))
        except Exception as e:
            self.logger.error(f"Error parsing ping output: {e}")
            result["error"] = f"Failed to parse output: {e}"

        return result

    def _parse_windows_ping(self, output: str) -> dict:
        """Parse Windows ping output.

        Args:
            output: Raw ping output

        Returns:
            Parsed results dictionary.
        """
        lines = output.split("\n")
        times = []
        packets_received = 0

        # Extract round-trip times
        for line in lines:
            # Look for lines like "Reply from 8.8.8.8: bytes=32 time=20ms TTL=56"
            time_match = re.search(r"time[<=](\d+)ms", line)
            if time_match:
                times.append(float(time_match.group(1)))
                packets_received += 1

        # Extract summary statistics
        for line in lines:
            # Look for packet loss info: "Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)"
            loss_match = re.search(r"Lost = \d+ \((\d+)% loss\)", line)
            if loss_match:
                packet_loss = float(loss_match.group(1))
                break
        else:
            packet_loss = (len(times) / 4) * 100 if times else 100.0

        result = {
            "packets_received": packets_received,
            "packet_loss": packet_loss,
            "times": times,
        }

        if times:
            result.update(
                {
                    "min_time": min(times),
                    "max_time": max(times),
                    "avg_time": statistics.mean(times),
                }
            )

        return result

    def _parse_unix_ping(self, output: str) -> dict:
        """Parse Unix/Linux/macOS ping output.

        Args:
            output: Raw ping output

        Returns:
            Parsed results dictionary.
        """
        lines = output.split("\n")
        times = []
        packets_received = 0

        # Extract round-trip times
        for line in lines:
            # Look for lines like "64 bytes from 8.8.8.8: icmp_seq=1 ttl=56 time=19.6 ms"
            time_match = re.search(r"time=(\d+\.?\d*)", line)
            if time_match:
                times.append(float(time_match.group(1)))
                packets_received += 1

        # Extract summary statistics
        for line in lines:
            # Look for packet loss info: "4 packets transmitted, 4 received, 0% packet loss"
            loss_match = re.search(r"(\d+)% packet loss", line)
            if loss_match:
                packet_loss = float(loss_match.group(1))
                break
        else:
            packet_loss = (
                ((len(times) - packets_received) / len(times)) * 100 if times else 100.0
            )

        result = {
            "packets_received": packets_received,
            "packet_loss": packet_loss,
            "times": times,
        }

        if times:
            result.update(
                {
                    "min_time": min(times),
                    "max_time": max(times),
                    "avg_time": statistics.mean(times),
                }
            )

        return result

    def traceroute(self, host: str, max_hops: int = 30) -> dict:
        """Perform a traceroute to the specified host.

        Args:
            host: Target host
            max_hops: Maximum number of hops

        Returns:
            Dictionary with traceroute results.
        """
        if is_windows():
            cmd = ["tracert", "-h", str(max_hops), host]
        else:
            cmd = ["traceroute", "-m", str(max_hops), host]

        self.logger.info(f"Running traceroute to {host}")
        self.logger.debug(f"Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max_hops * 5 + 30,  # Generous timeout
            )

            return {
                "host": host,
                "max_hops": max_hops,
                "success": result.returncode == 0,
                "raw_output": result.stdout,
                "error": result.stderr if result.stderr else None,
            }

        except subprocess.TimeoutExpired:
            self.logger.error(f"Traceroute to {host} timed out")
            return {
                "host": host,
                "max_hops": max_hops,
                "success": False,
                "error": "Timeout expired",
            }
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to run traceroute to {host}: {e}")
            return {
                "host": host,
                "max_hops": max_hops,
                "success": False,
                "error": str(e),
            }

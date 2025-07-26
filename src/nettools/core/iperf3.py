"""iPerf3 wrapper for bandwidth testing."""

import json
import subprocess
from typing import Any

from nettools.utils.logger import get_logger


class IPerf3Wrapper:
    """Wrapper class for iperf3 operations."""

    def __init__(self) -> None:
        """Initialize the iperf3 wrapper."""
        self.logger = get_logger(self.__class__.__name__)
        self._check_iperf3_availability()

    def _check_iperf3_availability(self) -> None:
        """Check if iperf3 is available on the system."""
        try:
            result = subprocess.run(
                ["iperf3", "--version"], capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                raise FileNotFoundError("iperf3 not found or not executable")
            self.logger.debug("iperf3 found and available")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError(
                "iperf3 is not installed or not available in PATH. "
                "Please install iperf3 to use this functionality."
            )

    def run_server(self, port: int = 5201, bind_address: str | None = None) -> dict:
        """Run iperf3 in server mode.

        Args:
            port: Port to listen on (default: 5201)
            bind_address: Address to bind to (default: all interfaces)

        Returns:
            Dictionary with server information.
        """
        cmd = ["iperf3", "--server", "--port", str(port)]

        if bind_address:
            cmd.extend(["--bind", bind_address])

        self.logger.info(f"Starting iperf3 server on port {port}")
        self.logger.debug(f"Command: {' '.join(cmd)}")

        try:
            # For server mode, we need to handle this differently
            # as it runs indefinitely until stopped
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            return {
                "mode": "server",
                "port": port,
                "bind_address": bind_address,
                "status": "running",
                "pid": process.pid,
            }

        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to start iperf3 server: {e}")
            raise RuntimeError(f"Failed to start iperf3 server: {e}")

    def run_client(
        self,
        host: str,
        port: int = 5201,
        duration: int = 10,
        parallel: int = 1,
        reverse: bool = False,
    ) -> dict:
        """Run iperf3 in client mode.

        Args:
            host: Server hostname or IP address
            port: Server port (default: 5201)
            duration: Test duration in seconds (default: 10)
            parallel: Number of parallel streams (default: 1)
            reverse: Run in reverse mode (server sends) (default: False)

        Returns:
            Dictionary with test results.
        """
        cmd = [
            "iperf3",
            "--client",
            host,
            "--port",
            str(port),
            "--time",
            str(duration),
            "--parallel",
            str(parallel),
            "--json",
        ]

        if reverse:
            cmd.append("--reverse")

        self.logger.info(f"Running iperf3 client test to {host}:{port}")
        self.logger.debug(f"Command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=duration + 30,  # Add buffer time
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip() or "Unknown iperf3 error"
                raise RuntimeError(f"iperf3 client failed: {error_msg}")

            # Parse JSON output
            try:
                raw_result = json.loads(result.stdout)
                return self._parse_client_result(raw_result)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse iperf3 JSON output: {e}")
                # Fallback to text parsing
                return self._parse_text_output(result.stdout)

        except subprocess.TimeoutExpired:
            self.logger.error("iperf3 client test timed out")
            raise RuntimeError("iperf3 client test timed out")
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to run iperf3 client: {e}")
            raise RuntimeError(f"Failed to run iperf3 client: {e}")

    def _parse_client_result(self, raw_result: dict) -> dict:
        """Parse iperf3 JSON output into a standardized format.

        Args:
            raw_result: Raw JSON result from iperf3

        Returns:
            Parsed result dictionary.
        """
        try:
            end = raw_result.get("end", {})
            sum_sent = end.get("sum_sent", {})
            sum_received = end.get("sum_received", {})

            # Use received data if available (for normal mode)
            # Use sent data if in reverse mode or if received is not available
            primary_data = sum_received if sum_received else sum_sent

            return {
                "mode": "client",
                "host": raw_result.get("start", {})
                .get("connecting_to", {})
                .get("host"),
                "port": raw_result.get("start", {})
                .get("connecting_to", {})
                .get("port"),
                "duration": primary_data.get("seconds", 0),
                "bytes_transferred": primary_data.get("bytes", 0),
                "bits_per_second": primary_data.get("bits_per_second", 0),
                "bandwidth": primary_data.get("bits_per_second", 0)
                / 1_000_000,  # Convert to Mbits/sec
                "retransmits": sum_sent.get("retransmits", 0),
                "cpu_utilization": {
                    "local": end.get("cpu_utilization_percent", {}).get(
                        "host_total", 0
                    ),
                    "remote": end.get("cpu_utilization_percent", {}).get(
                        "remote_total", 0
                    ),
                },
                "raw_result": raw_result,
            }
        except (KeyError, TypeError) as e:
            self.logger.error(f"Error parsing iperf3 result: {e}")
            return {
                "mode": "client",
                "error": f"Failed to parse result: {e}",
                "raw_result": raw_result,
            }

    def _parse_text_output(self, output: str) -> dict[str, Any]:
        """Parse text output as fallback when JSON parsing fails.

        Args:
            output: Raw text output from iperf3

        Returns:
            Basic result dictionary.
        """
        # This is a simple fallback parser for text output
        lines = output.split("\n")
        result: dict[str, Any] = {
            "mode": "client",
            "error": "JSON parsing failed, using text parsing",
            "raw_output": output,
        }

        # Try to extract basic bandwidth information
        for line in lines:
            if "Mbits/sec" in line and "sender" in line:
                try:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if "Mbits/sec" in part and i > 0:
                            result["bandwidth"] = float(parts[i - 1])
                            break
                except (ValueError, IndexError):
                    pass

        return result

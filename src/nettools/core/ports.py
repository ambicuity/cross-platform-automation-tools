"""Port checking utilities for network connectivity testing."""

import socket
import threading
import time

from nettools.utils.logger import get_logger


class PortChecker:
    """Utility class for checking port connectivity."""

    def __init__(self) -> None:
        """Initialize the port checker."""
        self.logger = get_logger(self.__class__.__name__)

    def check_port(self, host: str, port: int, timeout: int = 5) -> dict:
        """Check if a single port is open on a host.

        Args:
            host: Hostname or IP address
            port: Port number to check
            timeout: Connection timeout in seconds

        Returns:
            Dictionary with port check result.
        """
        start_time = time.time()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                response_time = time.time() - start_time

                if result == 0:
                    self.logger.debug(f"Port {port} is open on {host}")
                    return {
                        "port": port,
                        "open": True,
                        "response_time": response_time,
                        "error": None,
                    }
                else:
                    self.logger.debug(f"Port {port} is closed on {host}")
                    return {
                        "port": port,
                        "open": False,
                        "response_time": response_time,
                        "error": f"Connection failed (error code: {result})",
                    }

        except TimeoutError:
            response_time = time.time() - start_time
            self.logger.debug(f"Port {port} check timed out on {host}")
            return {
                "port": port,
                "open": False,
                "response_time": response_time,
                "error": "Connection timeout",
            }
        except socket.gaierror as e:
            response_time = time.time() - start_time
            self.logger.error(f"DNS resolution failed for {host}: {e}")
            return {
                "port": port,
                "open": False,
                "response_time": response_time,
                "error": f"DNS resolution failed: {e}",
            }
        except Exception as e:
            response_time = time.time() - start_time
            self.logger.error(f"Error checking port {port} on {host}: {e}")
            return {
                "port": port,
                "open": False,
                "response_time": response_time,
                "error": str(e),
            }

    def check_ports(
        self, host: str, ports: list[int], timeout: int = 5, max_threads: int = 50
    ) -> dict:
        """Check multiple ports on a host concurrently.

        Args:
            host: Hostname or IP address
            ports: List of port numbers to check
            timeout: Connection timeout in seconds for each port
            max_threads: Maximum number of concurrent threads

        Returns:
            Dictionary with results for all ports.
        """
        self.logger.info(f"Checking {len(ports)} ports on {host}")

        results = []
        threads = []
        semaphore = threading.Semaphore(max_threads)

        def check_port_worker(port: int) -> None:
            """Worker function for threaded port checking."""
            with semaphore:
                result = self.check_port(host, port, timeout)
                results.append(result)

        start_time = time.time()

        # Start threads for each port
        for port in ports:
            thread = threading.Thread(target=check_port_worker, args=(port,))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        total_time = time.time() - start_time

        # Sort results by port number
        results.sort(key=lambda x: x["port"])

        # Calculate summary statistics
        open_ports = [r for r in results if r["open"]]
        closed_ports = [r for r in results if not r["open"]]

        return {
            "host": host,
            "total_ports": len(ports),
            "open_ports": len(open_ports),
            "closed_ports": len(closed_ports),
            "scan_time": total_time,
            "ports": results,
            "summary": {
                "open": [r["port"] for r in open_ports],
                "closed": [r["port"] for r in closed_ports],
                "errors": [
                    r
                    for r in results
                    if r["error"] and "timeout" not in r["error"].lower()
                ],
            },
        }

    def scan_common_ports(self, host: str, timeout: int = 5) -> dict:
        """Scan commonly used ports on a host.

        Args:
            host: Hostname or IP address
            timeout: Connection timeout in seconds

        Returns:
            Dictionary with scan results.
        """
        common_ports = [
            21,  # FTP
            22,  # SSH
            23,  # Telnet
            25,  # SMTP
            53,  # DNS
            80,  # HTTP
            110,  # POP3
            143,  # IMAP
            443,  # HTTPS
            993,  # IMAPS
            995,  # POP3S
            3389,  # RDP
            5432,  # PostgreSQL
            3306,  # MySQL
            1433,  # MSSQL
            6379,  # Redis
            27017,  # MongoDB
            5672,  # RabbitMQ
            9200,  # Elasticsearch
            8080,  # HTTP Alt
        ]

        self.logger.info(f"Scanning common ports on {host}")
        return self.check_ports(host, common_ports, timeout)

    def check_service(self, host: str, service: str, timeout: int = 5) -> dict:
        """Check if a specific service is running by testing its default port.

        Args:
            host: Hostname or IP address
            service: Service name (http, https, ssh, ftp, etc.)
            timeout: Connection timeout in seconds

        Returns:
            Dictionary with service check result.
        """
        service_ports = {
            "http": 80,
            "https": 443,
            "ssh": 22,
            "ftp": 21,
            "smtp": 25,
            "dns": 53,
            "pop3": 110,
            "imap": 143,
            "telnet": 23,
            "rdp": 3389,
            "mysql": 3306,
            "postgresql": 5432,
            "redis": 6379,
            "mongodb": 27017,
            "rabbitmq": 5672,
            "elasticsearch": 9200,
        }

        service_lower = service.lower()
        if service_lower not in service_ports:
            return {
                "service": service,
                "host": host,
                "error": f"Unknown service: {service}. Known services: {', '.join(service_ports.keys())}",
            }

        port = service_ports[service_lower]
        result = self.check_port(host, port, timeout)

        return {
            "service": service,
            "host": host,
            "port": port,
            "available": result["open"],
            "response_time": result["response_time"],
            "error": result["error"],
        }

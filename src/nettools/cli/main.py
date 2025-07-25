"""Main CLI application entry point."""

import json

import typer
from rich.console import Console
from rich.table import Table

from nettools.core.iperf3 import IPerf3Wrapper
from nettools.core.ping import PingWrapper
from nettools.core.ports import PortChecker
from nettools.core.sysinfo import SystemInfo
from nettools.utils.logger import get_logger

app = typer.Typer(
    name="nettools",
    help="Cross-platform CLI automation suite for network and system tools",
    rich_markup_mode="rich",
)

console = Console()
logger = get_logger()


@app.command("iperf3-run")
def iperf3_run(
    server: bool = typer.Option(False, "--server", "-s", help="Run in server mode"),
    client: str | None = typer.Option(
        None, "--client", "-c", help="Connect to server at address"
    ),
    port: int = typer.Option(5201, "--port", "-p", help="Port to use"),
    duration: int = typer.Option(
        10, "--duration", "-t", help="Test duration in seconds"
    ),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Run iperf3 bandwidth tests in client or server mode."""
    if verbose:
        logger.setLevel("DEBUG")

    iperf3 = IPerf3Wrapper()

    try:
        if server:
            console.print(f"[green]Starting iperf3 server on port {port}[/green]")
            result = iperf3.run_server(port=port)
        elif client:
            console.print(
                f"[green]Running iperf3 client test to {client}:{port}[/green]"
            )
            result = iperf3.run_client(host=client, port=port, duration=duration)
        else:
            console.print("[red]Error: Must specify either --server or --client[/red]")
            raise typer.Exit(1)

        if json_output:
            console.print(json.dumps(result, indent=2))
        else:
            _display_iperf3_result(result)

    except Exception as e:
        logger.error(f"iperf3 error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("ping-host")
def ping_host(
    host: str = typer.Argument(..., help="Host to ping"),
    count: int = typer.Option(4, "--count", "-c", help="Number of pings"),
    timeout: int = typer.Option(5, "--timeout", "-t", help="Timeout in seconds"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Ping a host and show connectivity results."""
    if verbose:
        logger.setLevel("DEBUG")

    ping = PingWrapper()

    try:
        console.print(f"[green]Pinging {host} with {count} packets[/green]")
        result = ping.ping(host=host, count=count, timeout=timeout)

        if json_output:
            console.print(json.dumps(result, indent=2))
        else:
            _display_ping_result(result)

    except Exception as e:
        logger.error(f"Ping error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("check-ports")
def check_ports(
    host: str = typer.Option("localhost", "--host", "-h", help="Host to check"),
    ports: str = typer.Argument(..., help="Comma-separated list of ports"),
    timeout: int = typer.Option(5, "--timeout", "-t", help="Connection timeout"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Check if ports are open on a host."""
    if verbose:
        logger.setLevel("DEBUG")

    port_list = [int(p.strip()) for p in ports.split(",")]
    checker = PortChecker()

    try:
        console.print(f"[green]Checking ports {ports} on {host}[/green]")
        result = checker.check_ports(host=host, ports=port_list, timeout=timeout)

        if json_output:
            console.print(json.dumps(result, indent=2))
        else:
            _display_port_result(result)

    except Exception as e:
        logger.error(f"Port check error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command("sysinfo")
def sysinfo(
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Display system information."""
    if verbose:
        logger.setLevel("DEBUG")

    sysinfo_obj = SystemInfo()

    try:
        result = sysinfo_obj.get_all_info()

        if json_output:
            console.print(json.dumps(result, indent=2))
        else:
            _display_sysinfo_result(result)

    except Exception as e:
        logger.error(f"System info error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def _display_iperf3_result(result: dict) -> None:
    """Display iperf3 results in a formatted table."""
    if result.get("mode") == "server":
        console.print("[yellow]Server running... Press Ctrl+C to stop[/yellow]")
        return

    table = Table(title="iPerf3 Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    if "bandwidth" in result:
        table.add_row("Bandwidth", f"{result['bandwidth']:.2f} Mbits/sec")
    if "duration" in result:
        table.add_row("Duration", f"{result['duration']} seconds")
    if "bytes_transferred" in result:
        table.add_row("Bytes Transferred", f"{result['bytes_transferred']:,}")

    console.print(table)


def _display_ping_result(result: dict) -> None:
    """Display ping results in a formatted table."""
    table = Table(title=f"Ping Results for {result.get('host', 'Unknown')}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Packets Sent", str(result.get("packets_sent", 0)))
    table.add_row("Packets Received", str(result.get("packets_received", 0)))
    table.add_row("Packet Loss", f"{result.get('packet_loss', 0):.1f}%")

    if result.get("avg_time"):
        table.add_row("Average Time", f"{result['avg_time']:.2f} ms")
    if result.get("min_time"):
        table.add_row("Min Time", f"{result['min_time']:.2f} ms")
    if result.get("max_time"):
        table.add_row("Max Time", f"{result['max_time']:.2f} ms")

    console.print(table)


def _display_port_result(result: dict) -> None:
    """Display port check results in a formatted table."""
    table = Table(title=f"Port Check Results for {result.get('host', 'Unknown')}")
    table.add_column("Port", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Response Time", style="yellow")

    for port_info in result.get("ports", []):
        status = "🟢 Open" if port_info["open"] else "🔴 Closed"
        response_time = (
            f"{port_info.get('response_time', 0):.3f}s" if port_info["open"] else "N/A"
        )
        table.add_row(str(port_info["port"]), status, response_time)

    console.print(table)


def _display_sysinfo_result(result: dict) -> None:
    """Display system information in formatted tables."""
    # System overview
    system_table = Table(title="System Information")
    system_table.add_column("Metric", style="cyan")
    system_table.add_column("Value", style="green")

    system_table.add_row("Platform", result.get("platform", "Unknown"))
    system_table.add_row("Architecture", result.get("architecture", "Unknown"))
    system_table.add_row("Hostname", result.get("hostname", "Unknown"))
    system_table.add_row("Uptime", result.get("uptime", "Unknown"))

    console.print(system_table)

    # CPU information
    cpu_info = result.get("cpu", {})
    if cpu_info:
        cpu_table = Table(title="CPU Information")
        cpu_table.add_column("Metric", style="cyan")
        cpu_table.add_column("Value", style="green")

        cpu_table.add_row("CPU Count", str(cpu_info.get("count", 0)))
        cpu_table.add_row("CPU Usage", f"{cpu_info.get('usage', 0):.1f}%")
        cpu_table.add_row("Load Average", str(cpu_info.get("load_avg", "N/A")))

        console.print(cpu_table)

    # Memory information
    memory_info = result.get("memory", {})
    if memory_info:
        memory_table = Table(title="Memory Information")
        memory_table.add_column("Metric", style="cyan")
        memory_table.add_column("Value", style="green")

        memory_table.add_row(
            "Total", f"{memory_info.get('total', 0) / (1024**3):.2f} GB"
        )
        memory_table.add_row(
            "Available", f"{memory_info.get('available', 0) / (1024**3):.2f} GB"
        )
        memory_table.add_row("Used", f"{memory_info.get('used', 0) / (1024**3):.2f} GB")
        memory_table.add_row("Usage", f"{memory_info.get('percent', 0):.1f}%")

        console.print(memory_table)


if __name__ == "__main__":
    app()

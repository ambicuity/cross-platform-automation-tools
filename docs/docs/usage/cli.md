# CLI Reference

NetTools provides a comprehensive command-line interface for network and system automation tasks.

## Global Options

All commands support these global options:

- `--json`: Output results in JSON format
- `--verbose`, `-v`: Enable verbose/debug output  
- `--help`: Show command-specific help

## Commands

### `nettools iperf3-run`

Run iperf3 bandwidth tests in client or server mode.

**Usage:**
```bash
# Server mode
nettools iperf3-run --server [OPTIONS]

# Client mode  
nettools iperf3-run --client HOST [OPTIONS]
```

**Options:**
- `--server`, `-s`: Run in server mode
- `--client HOST`, `-c HOST`: Connect to server at address
- `--port PORT`, `-p PORT`: Port to use (default: 5201)
- `--duration SECONDS`, `-t SECONDS`: Test duration in seconds (default: 10)

**Examples:**
```bash
# Start server
nettools iperf3-run --server --port 5201

# Run client test
nettools iperf3-run --client 192.168.1.5 --duration 30 --json
```

### `nettools ping-host`

Ping a host and show connectivity results.

**Usage:**
```bash
nettools ping-host HOST [OPTIONS]
```

**Options:**
- `--count COUNT`, `-c COUNT`: Number of pings (default: 4)
- `--timeout SECONDS`, `-t SECONDS`: Timeout in seconds (default: 5)

**Examples:**
```bash
# Basic ping
nettools ping-host google.com

# Ping with custom count and JSON output
nettools ping-host 8.8.8.8 --count 10 --json
```

### `nettools check-ports`

Check if ports are open on a host.

**Usage:**
```bash
nettools check-ports PORTS [OPTIONS]
```

**Arguments:**
- `PORTS`: Comma-separated list of ports (e.g., "80,443,8080")

**Options:**
- `--host HOST`, `-h HOST`: Host to check (default: localhost)
- `--timeout SECONDS`, `-t SECONDS`: Connection timeout (default: 5)

**Examples:**
```bash
# Check local ports
nettools check-ports 22,80,443

# Check remote host with JSON output
nettools check-ports 80,443,8080 --host example.com --json
```

### `nettools sysinfo`

Display comprehensive system information.

**Usage:**
```bash
nettools sysinfo [OPTIONS]
```

**Examples:**
```bash
# Display system info
nettools sysinfo

# Get system info as JSON
nettools sysinfo --json --verbose
```

## Exit Codes

- `0`: Success
- `1`: General error (network failure, invalid arguments, etc.)
- `2`: Command line argument error

## JSON Output Format

When using `--json`, all commands output structured JSON data:

```json
{
  "command": "ping-host",
  "host": "example.com",
  "result": { ... },
  "timestamp": "2024-01-01T12:00:00"
}
```
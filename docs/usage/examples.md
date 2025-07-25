# Usage Examples

This page provides practical examples of using NetTools for common automation tasks.

## Network Performance Testing

### Basic Bandwidth Testing

```bash
# Start iperf3 server on default port
nettools iperf3-run --server

# Run bandwidth test from another machine
nettools iperf3-run --client 192.168.1.100 --duration 30

# Get results in JSON format for automation
nettools iperf3-run --client 192.168.1.100 --duration 10 --json
```

### Advanced iperf3 Usage

```bash
# Use custom port
nettools iperf3-run --server --port 8080

# Extended test duration with verbose output
nettools iperf3-run --client server.example.com --duration 60 --verbose
```

## Connectivity Testing

### Basic Ping Tests

```bash
# Quick connectivity check
nettools ping-host google.com

# Extended ping test with more packets
nettools ping-host 8.8.8.8 --count 20

# Ping with timeout and JSON output
nettools ping-host unreliable-host.com --timeout 10 --json
```

### Port Connectivity

```bash
# Check common web ports
nettools check-ports 80,443 --host example.com

# Check database ports on local machine
nettools check-ports 3306,5432,27017 --host localhost

# Quick service availability check
nettools check-ports 22,80,443,8080 --host production-server.com --json
```

## System Monitoring

### System Information

```bash
# Get complete system overview
nettools sysinfo

# System info for monitoring scripts
nettools sysinfo --json | jq '.memory.percent'

# Verbose system diagnostics
nettools sysinfo --verbose
```

## Automation Scripts

### Bash Script Example

```bash
#!/bin/bash
# Network health check script

HOSTS=("google.com" "github.com" "stackoverflow.com")
RESULTS_DIR="/tmp/nettools-results"

mkdir -p "$RESULTS_DIR"

echo "Starting network health check..."

for host in "${HOSTS[@]}"; do
    echo "Testing $host..."
    
    # Ping test
    nettools ping-host "$host" --count 5 --json > "$RESULTS_DIR/ping-$host.json"
    
    # Port test
    nettools check-ports 80,443 --host "$host" --json > "$RESULTS_DIR/ports-$host.json"
done

# System info
nettools sysinfo --json > "$RESULTS_DIR/sysinfo.json"

echo "Health check complete. Results in $RESULTS_DIR"
```

### Python Script Example

```python
#!/usr/bin/env python3
import json
import subprocess
import sys

def run_nettools_command(cmd):
    """Run nettools command and return JSON result."""
    try:
        result = subprocess.run(
            ["nettools"] + cmd + ["--json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return None

def main():
    """Network monitoring example."""
    
    # Check system health
    print("Checking system health...")
    sysinfo = run_nettools_command(["sysinfo"])
    if sysinfo:
        memory_usage = sysinfo["memory"]["percent"]
        print(f"Memory usage: {memory_usage}%")
        
        if memory_usage > 80:
            print("WARNING: High memory usage detected!")
    
    # Check critical services
    print("Checking critical services...")
    services = [
        ("localhost", "22,80,443"),
        ("8.8.8.8", "53"),  # DNS
        ("google.com", "80,443")
    ]
    
    for host, ports in services:
        result = run_nettools_command(["check-ports", ports, "--host", host])
        if result:
            open_ports = result["summary"]["open"]
            closed_ports = result["summary"]["closed"]
            print(f"{host}: {len(open_ports)} open, {len(closed_ports)} closed")
            
            if closed_ports:
                print(f"  WARNING: Closed ports: {closed_ports}")

if __name__ == "__main__":
    main()
```

### PowerShell Script Example

```powershell
# NetTools PowerShell automation example
param(
    [string]$TargetHost = "example.com",
    [string]$OutputDir = "C:\temp\nettools-results"
)

# Create output directory
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

Write-Host "Starting network analysis for $TargetHost..."

# System information
Write-Host "Gathering system information..."
nettools sysinfo --json | Out-File -FilePath "$OutputDir\sysinfo.json"

# Connectivity test
Write-Host "Testing connectivity to $TargetHost..."
nettools ping-host $TargetHost --count 10 --json | Out-File -FilePath "$OutputDir\ping-$TargetHost.json"

# Port scan
Write-Host "Scanning common ports on $TargetHost..."
nettools check-ports "21,22,23,25,53,80,110,143,443,993,995" --host $TargetHost --json | Out-File -FilePath "$OutputDir\ports-$TargetHost.json"

# Parse results
$pingResult = Get-Content "$OutputDir\ping-$TargetHost.json" | ConvertFrom-Json
$portResult = Get-Content "$OutputDir\ports-$TargetHost.json" | ConvertFrom-Json

Write-Host "Results:"
Write-Host "  Ping packet loss: $($pingResult.packet_loss)%"
Write-Host "  Open ports: $($portResult.summary.open -join ', ')"
Write-Host "  Closed ports: $($portResult.summary.closed -join ', ')"

Write-Host "Analysis complete. Results saved to $OutputDir"
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Network Health Check

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    
    steps:
    - name: Install NetTools
      run: pip install nettools
    
    - name: Check system health
      run: |
        nettools sysinfo --json > sysinfo.json
        nettools ping-host google.com --count 5 --json > ping-google.json
        nettools check-ports 80,443 --host github.com --json > ports-github.json
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: health-check-results
        path: "*.json"
```

### Docker Health Check

```dockerfile
FROM python:3.11-slim

RUN pip install nettools

# Health check script
COPY health-check.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/health-check.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD /usr/local/bin/health-check.sh
```

```bash
#!/bin/bash
# health-check.sh

# Check if critical services are responding
nettools check-ports 80,443 --host localhost --timeout 5 > /dev/null
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Health check passed"
    exit 0
else
    echo "Health check failed"
    exit 1
fi
```

## Monitoring and Alerting

### Simple Monitoring Loop

```bash
#!/bin/bash
# continuous-monitor.sh

INTERVAL=60  # seconds
LOG_FILE="/var/log/nettools-monitor.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Get system metrics
    MEMORY_USAGE=$(nettools sysinfo --json | jq -r '.memory.percent')
    
    # Check connectivity
    PING_RESULT=$(nettools ping-host 8.8.8.8 --count 1 --json | jq -r '.packet_loss')
    
    echo "$TIMESTAMP - Memory: ${MEMORY_USAGE}%, Ping Loss: ${PING_RESULT}%" >> "$LOG_FILE"
    
    # Alert on high memory usage
    if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
        echo "ALERT: High memory usage: ${MEMORY_USAGE}%" >> "$LOG_FILE"
        # Send notification (mail, webhook, etc.)
    fi
    
    sleep $INTERVAL
done
```

These examples demonstrate the versatility of NetTools for automation, monitoring, and integration into existing workflows.
# NetTools

Cross-platform CLI automation suite for network and system tools.

## Overview

NetTools is a comprehensive, production-ready CLI automation suite built in Python that provides unified tools for network performance testing, system diagnostics, and connectivity checking across Linux, macOS, and Windows platforms.

## Features

- **Network Performance Testing**
  - iperf3 wrapper for bandwidth testing
  - Ping and traceroute functionality
  - Port connectivity checking

- **System Information**
  - CPU, memory, and disk usage
  - Network interface details
  - System uptime and platform info

- **Cross-Platform Support**
  - Works identically on Linux, macOS, and Windows
  - Platform-aware command execution
  - Consistent output formats

- **Production Quality**
  - Comprehensive testing (unit + integration)
  - Type checking with mypy
  - Code formatting with black and ruff
  - CI/CD with GitHub Actions

## Quick Start

### Installation

```bash
pip install nettools
```

### Basic Usage

```bash
# Test network connectivity
nettools ping-host google.com --count 5

# Check port connectivity
nettools check-ports --host localhost --ports 22,80,443

# Get system information
nettools sysinfo --json

# Run bandwidth test
nettools iperf3-run --client 192.168.1.5 --duration 10
```

## Documentation

- [Installation Guide](installation.md)
- [CLI Reference](usage/cli.md)
- [Usage Examples](usage/examples.md)
- [API Documentation](api/cli.md)
- [Development Guide](development/contributing.md)

## Requirements

- Python 3.10 or higher
- Optional: iperf3 (for bandwidth testing)

## License

MIT License - see LICENSE file for details.

## Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details.
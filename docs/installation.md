# Installation Guide

## Requirements

- Python 3.10 or higher
- Optional: iperf3 (for bandwidth testing)

## Installation Methods

### From PyPI (Recommended)

```bash
pip install nettools
```

### From Source

```bash
git clone https://github.com/ambicuity/cross-platform-automation-tools.git
cd cross-platform-automation-tools
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/ambicuity/cross-platform-automation-tools.git
cd cross-platform-automation-tools
pip install -e ".[dev]"
```

## Installing iperf3 (Optional)

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install iperf3
```

### Linux (RHEL/CentOS/Fedora)
```bash
sudo yum install iperf3
# or
sudo dnf install iperf3
```

### macOS
```bash
brew install iperf3
```

### Windows
Download from [iperf.fr](https://iperf.fr/iperf-download.php) or use Chocolatey:
```bash
choco install iperf3
```

## Verification

Verify the installation:

```bash
nettools --help
```

Test basic functionality:

```bash
nettools sysinfo
nettools ping-host 8.8.8.8 --count 2
nettools check-ports 80,443 --host google.com
```
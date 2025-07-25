# NetTools - Cross-Platform Automation Suite

[![CI/CD Pipeline](https://github.com/ambicuity/cross-platform-automation-tools/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/ambicuity/cross-platform-automation-tools/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A fully modular, production-ready, cross-platform CLI automation suite in Python for network performance testing, system diagnostics, and connectivity checking.

## 🚀 Features

### Network Tools
- **iperf3 Integration**: Client/server bandwidth testing with JSON output
- **Ping & Connectivity**: Cross-platform ping with detailed statistics
- **Port Scanning**: Fast concurrent port checking with timeout handling
- **Service Detection**: Check common services (HTTP, SSH, FTP, etc.)

### System Information
- **CPU Metrics**: Usage, count, frequency, load average
- **Memory Stats**: Virtual memory, swap usage, detailed breakdown
- **Disk Usage**: Partition information, space utilization
- **Network Interfaces**: Interface details, statistics, addresses
- **Uptime & Platform**: System uptime, OS details, architecture

### Cross-Platform Support
- **Linux** (Ubuntu/Debian/Arch/RHEL)
- **macOS** (Intel/Apple Silicon)
- **Windows** (Native/WSL)

## 📦 Installation

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

## 🛠️ Usage

### Network Performance Testing

```bash
# Start iperf3 server
nettools iperf3-run --server --port 5201

# Run iperf3 client test
nettools iperf3-run --client 192.168.1.5 --duration 10 --json

# Test connectivity
nettools ping-host google.com --count 5 --verbose
```

### Port and Service Checking

```bash
# Check specific ports
nettools check-ports --host localhost --ports 22,80,443,8080

# Scan common ports
nettools check-ports --host example.com --ports 21,22,23,25,53,80,110,143,443,993,995

# Check with JSON output
nettools check-ports --host 192.168.1.1 --ports 80,443 --json
```

### System Information

```bash
# Get all system info
nettools sysinfo

# Get system info as JSON
nettools sysinfo --json

# Verbose output with debugging
nettools sysinfo --verbose
```

### Global Options

All commands support:
- `--json`: Output results in JSON format
- `--verbose`: Enable verbose/debug output
- `--help`: Show command-specific help

## 🏗️ Architecture

```
nettools/
├── cli/           # Typer-based CLI interface
│   └── main.py    # Main CLI application with subcommands
├── core/          # Core functionality modules
│   ├── iperf3.py  # iperf3 wrapper with JSON parsing
│   ├── ping.py    # Cross-platform ping implementation
│   ├── ports.py   # Port checking and service detection
│   └── sysinfo.py # System information gathering
└── utils/         # Utility modules
    ├── logger.py  # Structured logging
    └── platform_detect.py  # Platform detection and helpers
```

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nettools --cov-report=term-missing

# Run specific test categories
pytest tests/test_core/        # Core functionality tests
pytest tests/test_cli.py       # CLI interface tests
pytest tests/test_utils/       # Utility function tests
```

### Test Strategy
- **Unit Tests**: Mock external dependencies (subprocess, psutil)
- **Integration Tests**: Real command execution in CI
- **Cross-Platform Tests**: GitHub Actions matrix testing
- **Mocking**: Comprehensive mocking of system calls and external tools

## 🔧 Development

### Prerequisites
- Python 3.10+
- Optional: iperf3 for bandwidth testing

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/ambicuity/cross-platform-automation-tools.git
cd cross-platform-automation-tools

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

### Code Quality Tools

```bash
# Format code
black src tests
isort src tests

# Lint code
ruff check src tests

# Type checking
mypy src

# Security scanning
bandit -r src/
safety check
```

### Building Documentation

```bash
cd docs
mkdocs serve  # Development server
mkdocs build  # Build static site
```

## 🚀 CI/CD

The project uses GitHub Actions for:

- **Linting**: ruff, black, isort, mypy
- **Testing**: pytest across Python 3.10, 3.11, 3.12
- **Cross-Platform**: Ubuntu, macOS, Windows
- **Security**: bandit, safety
- **Documentation**: mkdocs build validation
- **Package Building**: wheel and sdist creation

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/development/contributing.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Run quality checks
5. Submit pull request

### Code Standards

- **Type Hints**: All functions must have type annotations
- **Documentation**: Docstrings for all public functions
- **Testing**: 90%+ test coverage required
- **Formatting**: black, isort, ruff compliance
- **Commits**: Conventional commit messages

## 📋 Roadmap

### v0.2.0
- [ ] Advanced iperf3 features (UDP, bidirectional)
- [ ] Traceroute implementation
- [ ] Configuration file support
- [ ] Plugin system for extensions

### v0.3.0
- [ ] Web dashboard interface
- [ ] Historical data storage
- [ ] Performance monitoring
- [ ] Alert system

### v1.0.0
- [ ] Stable API guarantee
- [ ] Complete documentation
- [ ] Installer packages (Homebrew, Chocolatey)
- [ ] Enterprise features

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ambicuity/cross-platform-automation-tools/issues)
- **Documentation**: [docs/](docs/)
- **Discussions**: [GitHub Discussions](https://github.com/ambicuity/cross-platform-automation-tools/discussions)

## 🙏 Acknowledgments

- [Typer](https://typer.tiangolo.com/) for the excellent CLI framework
- [psutil](https://psutil.readthedocs.io/) for cross-platform system information
- [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- [iperf3](https://iperf.fr/) for network performance testing

---

Made with ❤️ for cross-platform automation
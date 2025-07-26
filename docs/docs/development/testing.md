# Testing

## Overview

NetTools uses a comprehensive testing strategy to ensure reliability across all supported platforms.

## Testing Framework

The project uses **pytest** as the primary testing framework, with additional tools for coverage and mocking:

- `pytest`: Core testing framework
- `pytest-cov`: Coverage reporting
- `pytest-mock`: Mocking capabilities

## Test Structure

Tests are organized in the `tests/` directory with the following structure:

```
tests/
├── conftest.py          # Shared fixtures and configuration
├── test_cli.py          # CLI interface tests
├── test_core/           # Core module tests
│   ├── test_ping.py
│   ├── test_ports.py
│   ├── test_sysinfo.py
│   └── test_iperf3.py
└── test_utils/          # Utility module tests
    ├── test_logger.py
    └── test_platform_detect.py
```

## Running Tests

### Local Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nettools --cov-report=term-missing

# Run specific test file
pytest tests/test_cli.py

# Run specific test
pytest tests/test_cli.py::test_main_help
```

### CI/CD Testing
Tests are automatically run across multiple platforms and Python versions:
- **Platforms**: Ubuntu, Windows, macOS
- **Python Versions**: 3.10, 3.11, 3.12

## Test Types

### Unit Tests
- Test individual functions and methods in isolation
- Use mocking for external dependencies (network calls, system commands)
- Focus on edge cases and error conditions

### Integration Tests
- Test end-to-end CLI functionality
- Verify actual tool execution where possible
- Test JSON output formatting

### Platform-Specific Tests
- Verify cross-platform compatibility
- Handle platform-specific differences in tool behavior
- Mock platform-specific functionality when needed

## Mocking Strategy

External dependencies are mocked to ensure reliable, fast tests:
- Network requests and responses
- System command execution
- File system operations
- Platform-specific system calls

## Coverage Goals

- Maintain minimum 80% code coverage
- Focus on critical paths and error handling
- Exclude trivial code from coverage requirements
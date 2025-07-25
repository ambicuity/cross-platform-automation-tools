# Contributing Guide

We welcome contributions to NetTools! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Optional: iperf3 for testing bandwidth functionality

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cross-platform-automation-tools.git
   cd cross-platform-automation-tools
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install Pre-commit Hooks (Optional)**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Style and Quality

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **ruff**: Linting and code analysis
- **mypy**: Static type checking

Run all checks:
```bash
# Format code
black src tests
isort src tests

# Lint code
ruff check src tests

# Type checking
mypy src
```

### Testing

We use pytest for testing with comprehensive coverage:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nettools --cov-report=term-missing

# Run specific test file
pytest tests/test_core/test_sysinfo.py

# Run with verbose output
pytest -v
```

### Adding New Features

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write Tests First** (TDD)
   - Add tests in appropriate `tests/` subdirectory
   - Ensure tests fail initially
   - Implement feature to make tests pass

3. **Implementation Guidelines**
   - Follow existing code patterns
   - Add type hints to all functions
   - Include comprehensive docstrings
   - Handle cross-platform differences

4. **Documentation**
   - Update relevant documentation
   - Add usage examples if applicable
   - Update CLI help text

## Code Standards

### Python Style

- **PEP 8** compliance (enforced by black and ruff)
- **Type hints** for all function parameters and return values
- **Docstrings** for all public functions (Google style)
- **Error handling** with appropriate exceptions

### Example Function Template

```python
def example_function(param: str, optional_param: int | None = None) -> dict:
    """Brief description of the function.
    
    Args:
        param: Description of the parameter.
        optional_param: Description of optional parameter.
        
    Returns:
        Dictionary containing the result.
        
    Raises:
        ValueError: When param is invalid.
        RuntimeError: When operation fails.
    """
    if not param:
        raise ValueError("param cannot be empty")
    
    try:
        # Implementation here
        result = {"success": True, "data": param}
        return result
    except Exception as e:
        raise RuntimeError(f"Operation failed: {e}")
```

### Testing Standards

- **Unit tests** for all public functions
- **Integration tests** for CLI commands
- **Mock external dependencies** (subprocess, network calls)
- **Cross-platform test coverage**
- **Minimum 80% code coverage** for new features

### Example Test Template

```python
"""Tests for example module."""

from unittest.mock import Mock, patch

import pytest

from nettools.core.example import ExampleClass


class TestExampleClass:
    """Test cases for ExampleClass."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.example = ExampleClass()
    
    def test_basic_functionality(self):
        """Test basic functionality works correctly."""
        result = self.example.basic_method("test")
        assert result == "expected_output"
    
    @patch("external.dependency")
    def test_with_mock(self, mock_dependency):
        """Test functionality with mocked dependencies."""
        mock_dependency.return_value = "mocked_value"
        
        result = self.example.method_with_dependency()
        
        assert result == "expected_result"
        mock_dependency.assert_called_once()
    
    def test_error_handling(self):
        """Test error handling."""
        with pytest.raises(ValueError, match="specific error message"):
            self.example.method_that_should_fail("invalid_input")
```

## Pull Request Process

### Before Submitting

1. **Run all quality checks**
   ```bash
   black src tests
   isort src tests
   ruff check src tests
   mypy src
   pytest --cov=nettools
   ```

2. **Ensure tests pass** on your platform
3. **Update documentation** if needed
4. **Add changelog entry** if applicable

### PR Requirements

- **Clear description** of changes
- **Reference issue number** if applicable
- **All tests passing** in CI
- **Code coverage** maintained or improved
- **Documentation updated** if needed

### PR Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added for new functionality
- [ ] Documentation updated
- [ ] CI checks pass
```

## Project Structure

```
cross-platform-automation-tools/
├── src/nettools/           # Main package
│   ├── cli/               # CLI interface
│   ├── core/              # Core functionality
│   └── utils/             # Utility modules
├── tests/                 # Test suite
│   ├── test_cli.py       # CLI tests
│   ├── test_core/        # Core module tests
│   └── test_utils/       # Utility tests
├── docs/                  # Documentation
├── .github/workflows/     # CI/CD configuration
└── pyproject.toml        # Project configuration
```

## Adding New Commands

To add a new CLI command:

1. **Create core functionality** in `src/nettools/core/`
2. **Add CLI interface** in `src/nettools/cli/main.py`
3. **Write comprehensive tests**
4. **Update documentation**
5. **Add usage examples**

### Example: Adding a New Command

```python
# In src/nettools/core/new_feature.py
class NewFeature:
    """Implementation of new feature."""
    
    def execute(self, param: str) -> dict:
        """Execute the new feature."""
        # Implementation here
        return {"result": "success"}

# In src/nettools/cli/main.py
@app.command("new-command")
def new_command(
    param: str = typer.Argument(..., help="Required parameter"),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
) -> None:
    """Description of the new command."""
    if verbose:
        logger.setLevel("DEBUG")
    
    feature = NewFeature()
    
    try:
        result = feature.execute(param)
        
        if json_output:
            console.print(json.dumps(result, indent=2))
        else:
            # Display formatted output
            console.print(f"Result: {result}")
            
    except Exception as e:
        logger.error(f"Command error: {e}")
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
```

## Release Process

Releases are managed by maintainers:

1. **Version bump** in `pyproject.toml`
2. **Update changelog**
3. **Create release tag**
4. **Publish to PyPI**
5. **Update documentation**

## Getting Help

- **Issues**: Report bugs or request features
- **Discussions**: Ask questions or discuss ideas
- **Documentation**: Check existing docs first
- **Code Review**: Maintainers will review PRs

## Code of Conduct

Please be respectful and inclusive in all interactions. We want this to be a welcoming community for everyone.

Thank you for contributing to NetTools! 🚀
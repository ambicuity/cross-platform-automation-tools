# Architecture

## Overview

NetTools is a cross-platform CLI automation suite designed with modularity and extensibility in mind. The architecture is organized into several key components:

## Component Structure

### CLI Layer (`nettools.cli`)
- **Purpose**: Command-line interface and user interaction
- **Key Components**: 
  - `main.py`: Main CLI application using Typer
  - Command handlers for each tool functionality

### Core Layer (`nettools.core`)
- **Purpose**: Core business logic and tool implementations
- **Key Components**:
  - `ping.py`: Network connectivity testing
  - `ports.py`: Port scanning and checking
  - `sysinfo.py`: System information gathering
  - `iperf3.py`: Network performance testing

### Utilities Layer (`nettools.utils`)
- **Purpose**: Cross-cutting concerns and shared functionality
- **Key Components**:
  - `logger.py`: Centralized logging
  - `platform_detect.py`: Cross-platform compatibility handling

## Design Principles

1. **Cross-Platform Compatibility**: All core functionality works across Windows, macOS, and Linux
2. **Modular Design**: Each tool is implemented as a separate module
3. **Rich Output**: Support for both human-readable and JSON output formats
4. **Error Handling**: Comprehensive error handling with meaningful messages
5. **Testability**: Designed with testing in mind, using dependency injection where appropriate

## Data Flow

1. User invokes CLI command
2. CLI layer validates input and routes to appropriate core module
3. Core module executes the requested functionality
4. Results are formatted and returned to CLI layer
5. CLI layer outputs results in requested format (text or JSON)
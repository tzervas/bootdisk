# Bootdisk - Debian Workstation Setup Automation

Customized Debian workstation setup automation for gaming/inference workloads with GPU serving capabilities and PXE boot support.

## Overview

Bootdisk generates and manages workstation configurations for gaming and inference workloads. It provides:

- **Automated Debian Installation**: Streamlined setup for gaming workstations
- **GPU Configuration**: NVIDIA/AMD driver setup and optimization
- **PXE Boot Support**: Network-based installation and management
- **Multi-Agent Architecture**: AI-powered configuration generation
- **Hybrid Development**: Python + Rust components for optimal performance

## Quick Start

### Using DevContainer (Recommended)

1. Open in VS Code
2. Use Command Palette: `Dev Containers: Reopen in Container`
3. The devcontainer will automatically validate the environment

### Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run bootdisk
python main.py
```

## Development Environment

### DevContainer Features

The included devcontainer provides:

- **Rust Toolchain**: For high-performance components
- **Python Environment**: With ML/AI libraries (LangChain, Ollama, PyTorch)
- **Ollama Integration**: Local LLM serving with pre-loaded models
- **aider-chat**: AI-powered code assistance
- **Development Tools**: Git, Docker, testing frameworks

### Testing the DevContainer

#### Automated Testing
```bash
# Run validation (happens automatically on container creation)
./.devcontainer/test-devcontainer.sh
```

#### Interactive Testing
```bash
# Run interactive validation with shell access
./.devcontainer/test-devcontainer.sh interactive
```

#### VS Code Tasks
- `Ctrl+Shift+P` → `Tasks: Run Task` → `Test DevContainer`
- `Test DevContainer (Interactive)` - For manual exploration
- `Validate Python Environment` - Check ML libraries
- `Validate Rust Environment` - Check Rust toolchain
- `Start Ollama Service` - Launch local LLM server
- `Test aider-chat` - Verify AI coding assistant

## Architecture

### Multi-Agent System

Bootdisk uses a multi-agent architecture with specialized roles:

- **System Administrator**: Debian installation and configuration
- **Hardware Specialist**: GPU setup and performance tuning
- **Network Engineer**: PXE boot and network configuration
- **DevOps Specialist**: Container orchestration and Kubernetes

### Hybrid Python/Rust

- **Python**: High-level orchestration, AI agents, configuration management
- **Rust**: Performance-critical components, system utilities

## Available Tools Integration

Bootdisk integrates with the Python development ecosystem:

### py-devcontainer
Generate optimized devcontainers for Python projects:
```bash
# From py-devcontainer project
python -m devcontainer generate --template python-ml
```

### py-devtools
Project scaffolding and development utilities:
```bash
# From py-devtools project
python -m devtools scaffold new-project
```

### py-rust-bridge
Python-Rust FFI and interop tools for hybrid development.

### py2rust
Convert Python code to Rust for performance optimization.

## Configuration

Bootdisk uses YAML-based configuration:

```yaml
project: gaming-workstation
version: "1.0.0"
debian_version: "12"
gpu: nvidia
features:
  - gaming_optimization
  - cuda_support
  - pxe_boot
```

## Development

### Prerequisites

- VS Code with Dev Containers extension
- Docker
- 8GB+ RAM recommended for devcontainer

### Building

```bash
# Python components
pip install -e .

# Rust components
cargo build --release
```

### Testing

```bash
# Python tests
pytest

# Rust tests
cargo test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with comprehensive tests
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- [py-devcontainer](https://github.com/tzervas/py-devcontainer) - DevContainer generation
- [py-devtools](https://github.com/tzervas/py-devtools) - Development utilities
- [py-rust-bridge](https://github.com/tzervas/py-rust-bridge) - Python-Rust interop
- [py2rust](https://github.com/tzervas/py2rust) - Python to Rust transpiler

# Development Setup

Set up your development environment for contributing to Bootdisk.

## Prerequisites

- **VS Code** with Dev Containers extension
- **Git** for version control
- **Docker** for containerized development
- **8GB+ RAM** recommended

## Quick Setup (Recommended)

### Using DevContainer

1. **Clone the repository**
   ```bash
   git clone https://github.com/tzervas/bootdisk.git
   cd bootdisk
   ```

2. **Open in VS Code**
   ```bash
   code bootdisk.code-workspace
   ```

3. **Reopen in DevContainer**
   - `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`
   - Wait for the container to build (first time takes ~10-15 minutes)

4. **Verify setup**
   ```bash
   # Run the validation script
   ./scripts/devcontainer-manager.sh status
   ```

### Manual Setup

If you prefer not to use DevContainer:

```bash
# Install Python dependencies
pip install -e .[dev]

# Install Rust toolchain
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install additional tools
pip install langchain ollama torch  # For AI features
cargo install cargo-watch cargo-expand  # Development tools
```

## Development Workflow

### Daily Development

1. **Start the DevContainer**
   ```bash
   ./scripts/devcontainer-manager.sh start
   ```

2. **Make changes** with AI assistance from Copilot and agents

3. **Run tests**
   ```bash
   # Python tests
   python -m pytest

   # Rust tests
   cargo test
   ```

4. **Build and validate**
   ```bash
   # Build Rust components
   cargo build --release

   # Validate DevContainer
   ./scripts/devcontainer-manager.sh optimize
   ```

### Agent-Assisted Development

Bootdisk includes AI agents to help with development:

- **SWE Agent**: Code implementation and optimization
- **Test Engineer**: Quality assurance and testing
- **Project Manager**: Coordination and planning
- **Security Agent**: Security reviews
- **Documentation Agent**: Automated documentation

### VS Code Tasks

Common development tasks are available:

- `Ctrl+Shift+P` → `Tasks: Run Task`
- `Test DevContainer` - Validate environment
- `Validate Python Environment` - Check ML libraries
- `Validate Rust Environment` - Check Rust toolchain

## Code Quality

### Linting and Formatting

```bash
# Python
black .                    # Format code
isort .                    # Sort imports
flake8 .                   # Lint code

# Rust
cargo clippy               # Lint code
cargo fmt                  # Format code
```

### Testing

```bash
# Run all tests
python -m pytest --cov=bootdisk

# Run specific test
python -m pytest tests/test_config.py

# Run Rust tests
cargo test

# Run integration tests
python -m pytest tests/integration/
```

### Pre-commit Hooks

Install pre-commit hooks for automated quality checks:

```bash
pip install pre-commit
pre-commit install
```

## Building Documentation

```bash
# Generate API documentation
python -m sphinx docs/ build/html

# Build Rust documentation
cargo doc --open
```

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes following the [contributing guide](../developer/contributing.md)
3. Run tests and quality checks
4. Submit a pull request

## Troubleshooting

### Common Issues

**DevContainer won't start**
- Ensure Docker is running
- Check available disk space (need 10GB+)
- Try: `./scripts/devcontainer-manager.sh destroy` then restart

**AI features not working**
- Check Ollama service: `ollama list`
- Restart services: `./scripts/devcontainer-manager.sh restart`

**Tests failing**
- Update dependencies: `pip install -e .[dev]`
- Check Python/Rust versions
- Run in DevContainer for consistent environment

### Getting Help

- [Issues](https://github.com/tzervas/bootdisk/issues) - Report bugs
- [Discussions](https://github.com/tzervas/bootdisk/discussions) - Ask questions
- [Documentation](README.md) - Comprehensive guides
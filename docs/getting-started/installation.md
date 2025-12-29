# Installation Guide

## Prerequisites

Before installing Bootdisk, ensure you have the following:

- **Operating System**: Linux, macOS, or Windows (with WSL2)
- **Python**: 3.12 or later
- **Rust**: 1.70 or later (optional, for development)
- **Docker**: For containerized development (optional)

## Installation Methods

### Option 1: Direct Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/tzervas/bootdisk.git
cd bootdisk

# Install Python dependencies
pip install -e .

# Optional: Install Rust toolchain for development
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

### Option 2: DevContainer (Full Environment)

For the complete development environment with all tools:

1. Open the project in VS Code
2. Use Command Palette: `Dev Containers: Reopen in Container`
3. The container will automatically set up everything

### Option 3: Docker Installation

```bash
# Build the Docker image
docker build -t bootdisk .

# Run bootdisk
docker run -it --rm bootdisk
```

## Verification

Verify your installation:

```bash
# Check Python components
python -c "import bootdisk; print('Bootdisk installed successfully')"

# Check Rust components (if installed)
cargo --version

# Run basic functionality test
python python/main.py --help
```

## Next Steps

- [Quick Start Guide](quick-start.md) - Create your first configuration
- [Development Setup](dev-setup.md) - Set up for development
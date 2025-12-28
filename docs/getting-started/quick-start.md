# Quick Start Guide

Get up and running with Bootdisk in minutes.

## Basic Usage

### Generate a Workstation Configuration

```bash
# Create a basic gaming workstation configuration
python main.py generate --template gaming-workstation --output my-workstation.yaml

# Customize the configuration
python main.py customize my-workstation.yaml --gpu nvidia --ram 32

# Generate the bootable image
python main.py build my-workstation.yaml --output bootdisk.iso
```

### Using Predefined Templates

Bootdisk comes with several predefined templates:

```bash
# List available templates
python main.py templates list

# Use a template
python main.py generate --template ml-workstation
```

## Configuration Example

Here's a basic configuration file:

```yaml
project: my-workstation
version: "1.0.0"
description: "Custom gaming and ML workstation"

debian_config:
  version: "12"
  desktop: gnome
  packages:
    - build-essential
    - git
    - curl

hardware:
  gpu: nvidia
  drivers: proprietary
  cuda: true

features:
  - gaming_optimization
  - cuda_support
  - development_tools
```

## Advanced Usage

### Multi-Agent Configuration Generation

Bootdisk uses AI agents to optimize configurations:

```bash
# Use AI assistance for configuration
python main.py generate --ai-assisted --requirements "gaming workstation with RTX 4090"

# Review agent recommendations
python main.py review my-workstation.yaml
```

### PXE Boot Setup

For network-based installation:

```bash
# Generate PXE configuration
python main.py pxe-setup --config my-workstation.yaml --network 192.168.1.0/24

# Start PXE server
python main.py pxe-serve --config my-workstation.yaml
```

## Development Workflow

### Using DevContainer

For the best development experience:

1. Open in VS Code
2. `Ctrl+Shift+P` → `Dev Containers: Reopen in Container`
3. Start coding with full AI assistance

### Manual Development

```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest

# Build Rust components
cargo build --release
```

## Next Steps

- [Configuration Guide](../user-guide/configuration.md) - Detailed configuration options
- [DevContainer Guide](../devcontainer/guide.md) - Containerized development
- [Contributing Guide](../developer/contributing.md) - How to contribute
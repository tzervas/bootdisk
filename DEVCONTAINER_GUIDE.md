# DevContainer Development Guide

## What is a DevContainer?

A **DevContainer** is a Docker container specifically configured for development. It provides:

- **Isolated Environment**: All dependencies and tools in a container
- **Consistent Setup**: Same environment across all developers/machines
- **Resource Protection**: Development doesn't affect your host system
- **Easy Sharing**: Environment defined in code (devcontainer.json)

## How DevContainers Work

### Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   VS Code       │────│  DevContainer   │────│  Your Code      │
│   (Host)        │    │  (Docker)       │    │  (Volume Mount) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

- **VS Code**: Runs on your host machine
- **DevContainer**: Docker container with development tools
- **Your Code**: Mounted from host, edited in container

### Key Files
- `devcontainer.json`: Configuration for the container
- `Dockerfile`: How to build the container image
- `.devcontainer/`: Directory containing container setup

## Bootdisk DevContainer Setup

### What's Included
- **Python 3.12** with virtual environment
- **Rust toolchain** for performance components
- **AI/ML libraries**: LangChain, PyTorch, Ollama
- **Development tools**: Git, Docker, testing frameworks
- **Ollama models**: Pre-loaded for coding assistance
- **aider-chat**: AI-powered coding assistant

### Resource Requirements
- **RAM**: 8GB+ recommended
- **Disk**: 10GB+ for models and dependencies
- **Docker**: Must be running on host

## Development Workflow

### Daily Development Cycle

```bash
# 1. Check status
./devcontainer-manager.sh status

# 2. Start container (if needed)
./devcontainer-manager.sh start

# 3. Attach VS Code
./devcontainer-manager.sh attach

# 4. Develop in VS Code
# - Code runs in container
# - Files saved to host
# - All tools available

# 5. Stop when done
./devcontainer-manager.sh stop
```

### First-Time Setup

```bash
# Create and start devcontainer
./devcontainer-manager.sh create

# This will:
# - Build Docker image (~5-10 minutes)
# - Create container
# - Run validation tests
# - Open in VS Code
```

### VS Code Integration

#### Automatic Attachment
When you open the workspace in VS Code:
1. VS Code detects `.devcontainer` directory
2. Prompts: "Reopen in Container?"
3. Builds/starts container automatically
4. Attaches VS Code to container

#### Manual Control
- **Command Palette**: `Dev Containers: Reopen in Container`
- **Status Bar**: Shows container status
- **Terminal**: Runs inside container

## Management Commands

### Quick Reference

| Command | Description |
|---------|-------------|
| `./devcontainer-manager.sh status` | Check container status |
| `./devcontainer-manager.sh start` | Start existing container |
| `./devcontainer-manager.sh create` | Create new container |
| `./devcontainer-manager.sh attach` | Connect VS Code |
| `./devcontainer-manager.sh stop` | Stop container (keep data) |
| `./devcontainer-manager.sh destroy` | Remove container completely |

### Common Scenarios

#### "I want to start developing"
```bash
./devcontainer-manager.sh start
./devcontainer-manager.sh attach
```

#### "Container is broken, start fresh"
```bash
./devcontainer-manager.sh destroy
./devcontainer-manager.sh create
```

#### "Check what's happening"
```bash
./devcontainer-manager.sh status
./devcontainer-manager.sh logs
```

#### "Pause development"
```bash
./devcontainer-manager.sh stop
```

## Understanding Container States

### Running
- Container is active
- VS Code can attach
- All services running (Ollama, etc.)
- **Resource usage**: High (RAM, CPU)

### Stopped
- Container exists but not running
- Data preserved
- Quick to restart
- **Resource usage**: Low (disk only)

### Not Created
- No container exists
- Fresh start required
- Build time needed
- **Resource usage**: None

## VS Code DevContainer Features

### Automatic Features
- **Extensions**: Installed in container
- **Settings**: Container-specific configuration
- **Tasks**: Run in container context
- **Debugging**: Works with container tools

### Manual Control
- **Terminal**: `Ctrl+Shift+` `` ` (runs in container)
- **Tasks**: Via Command Palette → Tasks
- **Debug**: F5 or Run/Debug panel

## Troubleshooting

### Container Won't Start
```bash
# Check Docker
docker info

# Check logs
./devcontainer-manager.sh logs

# Clean restart
./devcontainer-manager.sh destroy
./devcontainer-manager.sh create
```

### VS Code Won't Attach
```bash
# Restart VS Code
# Use Command Palette: "Dev Containers: Reopen in Container"
# Check Dev Containers extension is installed
```

### Performance Issues
```bash
# Check resource usage
docker stats

# Stop unnecessary services
# Close unused terminals
# Restart container
```

### File Permission Issues
- Files are mounted from host
- Permissions should work automatically
- If issues: Check Docker file sharing settings

## Best Practices

### Development
- **Start container**: When beginning work
- **Stop container**: When done for the day
- **Destroy rarely**: Only when environment is broken
- **Commit changes**: Push to git regularly

### Resource Management
- **Monitor usage**: `docker stats`
- **Stop when idle**: Prevents resource waste
- **Clean periodically**: Remove unused containers
- **Update images**: Rebuild for dependency updates

### Team Collaboration
- **Share config**: devcontainer.json in version control
- **Document setup**: Update this guide
- **Test builds**: Ensure clean builds work
- **Update dependencies**: Keep images current

## Advanced Usage

### Custom Configuration
Edit `devcontainer.json` to:
- Add new extensions
- Change settings
- Modify build process
- Add features

### Multiple Containers
Can have different containers for:
- Different projects
- Different tech stacks
- Different team members

### CI/CD Integration
DevContainer configs can be used for:
- CI build environments
- Consistent testing
- Deployment containers

## Getting Help

### Common Issues
1. **"Command not found"**: Run in container terminal, not host
2. **"Permission denied"**: Check file mounting
3. **"Out of memory"**: Increase Docker memory limit
4. **"Build fails"**: Check Dockerfile and dependencies

### Debug Steps
1. Check container status: `./devcontainer-manager.sh status`
2. View logs: `./devcontainer-manager.sh logs`
3. Test manually: `docker run -it <image> bash`
4. Rebuild: `./devcontainer-manager.sh destroy && ./devcontainer-manager.sh create`

## Summary

DevContainers provide **isolated**, **consistent**, **resource-safe** development environments. The management script makes them easy to control, while VS Code provides seamless integration. Start with the basic workflow and explore advanced features as needed.
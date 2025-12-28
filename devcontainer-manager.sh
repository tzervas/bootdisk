#!/bin/bash
# DevContainer Management Script for Bootdisk
# Provides easy start/stop/status commands for devcontainer development

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONTAINER_NAME="bootdisk-dev"
WORKSPACE_NAME="bootdisk"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

check_dependencies() {
    local missing_deps=()

    if ! command -v docker &> /dev/null; then
        missing_deps+=("docker")
    fi

    if ! command -v code &> /dev/null; then
        missing_deps+=("code (VS Code)")
    fi

    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install missing dependencies and try again"
        exit 1
    fi
}

get_container_status() {
    if docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo "running"
    elif docker ps -a --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        echo "stopped"
    else
        echo "not_found"
    fi
}

show_status() {
    log_info "Checking devcontainer status..."

    local status=$(get_container_status)

    case $status in
        "running")
            log_success "DevContainer is RUNNING"
            echo "  Container: $CONTAINER_NAME"
            echo "  Status: Active and attached to VS Code"
            ;;
        "stopped")
            log_warning "DevContainer is STOPPED"
            echo "  Container: $CONTAINER_NAME (exists but not running)"
            echo "  Use '$0 start' to restart"
            ;;
        "not_found")
            log_info "DevContainer is NOT CREATED"
            echo "  No container found for $CONTAINER_NAME"
            echo "  Use '$0 create' to create and start"
            ;;
    esac

    # Check if VS Code is running with devcontainer
    if pgrep -f "code.*--devcontainer" > /dev/null 2>&1; then
        log_success "VS Code is connected to devcontainer"
    else
        log_info "VS Code devcontainer connection not detected"
    fi
}

start_devcontainer() {
    log_info "Starting devcontainer..."

    local status=$(get_container_status)

    case $status in
        "running")
            log_warning "DevContainer is already running"
            log_info "Use '$0 attach' to connect VS Code, or '$0 stop' to restart"
            return 0
            ;;
        "stopped")
            log_info "Restarting existing container..."
            docker start "$CONTAINER_NAME"
            log_success "DevContainer restarted"
            ;;
        "not_found")
            log_info "Creating new devcontainer..."
            create_devcontainer
            return $?
            ;;
    esac

    log_info "DevContainer started. Use '$0 attach' to connect with VS Code"
}

create_devcontainer() {
    log_info "Creating new devcontainer from scratch..."
    log_info "This will build the Docker image and create the container"

    cd "$PROJECT_DIR"

    # Check if devcontainer CLI is available
    if command -v devcontainer &> /dev/null; then
        log_info "Using devcontainer CLI..."
        devcontainer open
    else
        log_warning "devcontainer CLI not found, using VS Code..."
        log_info "Opening in VS Code - use Command Palette > Dev Containers: Reopen in Container"

        # Try to open in VS Code
        if command -v code &> /dev/null; then
            code "$PROJECT_DIR/bootdisk.code-workspace"
            log_info "VS Code opened. Use 'Dev Containers: Reopen in Container' from Command Palette"
        else
            log_error "VS Code not found. Please install VS Code and Dev Containers extension"
            exit 1
        fi
    fi
}

attach_vscode() {
    log_info "Attaching VS Code to devcontainer..."

    local status=$(get_container_status)

    if [ "$status" != "running" ]; then
        log_error "DevContainer is not running. Use '$0 start' first"
        exit 1
    fi

    cd "$PROJECT_DIR"

    if command -v code &> /dev/null; then
        log_info "Opening workspace in VS Code..."
        code "$PROJECT_DIR/bootdisk.code-workspace"
        log_success "VS Code opened. Use 'Dev Containers: Reopen in Container' if not already attached"
    else
        log_error "VS Code not found"
        exit 1
    fi
}

stop_devcontainer() {
    log_info "Stopping devcontainer..."

    local status=$(get_container_status)

    case $status in
        "running")
            log_info "Stopping container..."
            docker stop "$CONTAINER_NAME"
            log_success "DevContainer stopped"
            ;;
        "stopped")
            log_warning "DevContainer is already stopped"
            ;;
        "not_found")
            log_warning "DevContainer doesn't exist"
            ;;
    esac
}

destroy_devcontainer() {
    log_warning "Destroying devcontainer completely..."
    log_warning "This will delete the container and all data inside it"

    read -p "Are you sure? This cannot be undone (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Operation cancelled"
        return 0
    fi

    local status=$(get_container_status)

    if [ "$status" != "not_found" ]; then
        log_info "Removing container..."
        docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
        log_success "DevContainer destroyed"
    else
        log_warning "DevContainer doesn't exist"
    fi
}

show_logs() {
    log_info "Showing devcontainer logs..."

    local status=$(get_container_status)

    if [ "$status" = "not_found" ]; then
        log_error "DevContainer doesn't exist"
        exit 1
    fi

    docker logs "$CONTAINER_NAME"
}

show_usage() {
    cat << EOF
DevContainer Management Script for Bootdisk

USAGE:
  $0 <command> [options]

COMMANDS:
  status      Show current devcontainer status
  start       Start or create devcontainer
  create      Create new devcontainer from scratch
  attach      Attach VS Code to running devcontainer
  stop        Stop devcontainer (keeps data)
  destroy     Completely remove devcontainer
  logs        Show devcontainer logs
  help        Show this help

EXAMPLES:
  $0 status                    # Check if devcontainer is running
  $0 start                     # Start devcontainer
  $0 attach                    # Connect VS Code to running container
  $0 stop                      # Stop container
  $0 destroy                   # Remove container completely

WORKFLOW:
  1. $0 start                  # Start container
  2. $0 attach                 # Connect VS Code
  3. Develop in VS Code
  4. $0 stop                   # Stop when done
  5. $0 start                  # Restart later

NOTES:
  - Requires Docker and VS Code with Dev Containers extension
  - First run will build the container (takes time)
  - Container persists data between starts/stops
  - Use 'destroy' to completely reset

EOF
}

main() {
    check_dependencies

    case "${1:-help}" in
        "status")
            show_status
            ;;
        "start")
            start_devcontainer
            ;;
        "create")
            create_devcontainer
            ;;
        "attach")
            attach_vscode
            ;;
        "stop")
            stop_devcontainer
            ;;
        "destroy")
            destroy_devcontainer
            ;;
        "logs")
            show_logs
            ;;
        "help"|"-h"|"--help")
            show_usage
            ;;
        *)
            log_error "Unknown command: $1"
            echo
            show_usage
            exit 1
            ;;
    esac
}

main "$@"
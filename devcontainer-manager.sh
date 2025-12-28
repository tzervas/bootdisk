#!/bin/bash
# DevContainer Management Script for Bootdisk
# Provides easy start/stop/status commands for devcontainer development
# Includes dynamic resource management and optimization

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONTAINER_NAME="bootdisk-dev"
WORKSPACE_NAME="bootdisk"
CONFIG_FILE="$PROJECT_DIR/.devcontainer/config.json"

# Default configuration
DEFAULT_IDLE_TIMEOUT=1800  # 30 minutes
DEFAULT_CHECK_INTERVAL=60  # 1 minute
DEFAULT_MIN_MEMORY="512m"
DEFAULT_MAX_MEMORY="8g"
DEFAULT_MIN_CPU="0.5"
DEFAULT_MAX_CPU="4.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Resource management state
RESOURCE_STATE_FILE="/tmp/${CONTAINER_NAME}_resources.json"
IDLE_STATE_FILE="/tmp/${CONTAINER_NAME}_idle"
LAST_ACTIVITY_FILE="/tmp/${CONTAINER_NAME}_activity"

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

log_resource() {
    echo -e "${CYAN}🔧 $1${NC}"
}

log_idle() {
    echo -e "${PURPLE}😴 $1${NC}"
}

# Configuration management
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        IDLE_TIMEOUT=$(jq -r '.idle_timeout // 1800' "$CONFIG_FILE")
        CHECK_INTERVAL=$(jq -r '.check_interval // 60' "$CONFIG_FILE")
        MIN_MEMORY=$(jq -r '.min_memory // "512m"' "$CONFIG_FILE")
        MAX_MEMORY=$(jq -r '.max_memory // "8g"' "$CONFIG_FILE")
        MIN_CPU=$(jq -r '.min_cpu // 0.5' "$CONFIG_FILE")
        MAX_CPU=$(jq -r '.max_cpu // 4.0' "$CONFIG_FILE")
        AUTO_OPTIMIZE=$(jq -r '.auto_optimize // true' "$CONFIG_FILE")
    else
        IDLE_TIMEOUT=$DEFAULT_IDLE_TIMEOUT
        CHECK_INTERVAL=$DEFAULT_CHECK_INTERVAL
        MIN_MEMORY=$DEFAULT_MIN_MEMORY
        MAX_MEMORY=$DEFAULT_MAX_MEMORY
        MIN_CPU=$DEFAULT_MIN_CPU
        MAX_CPU=$DEFAULT_MAX_CPU
        AUTO_OPTIMIZE=true
    fi
}

save_config() {
    mkdir -p "$(dirname "$CONFIG_FILE")"
    cat > "$CONFIG_FILE" << EOF
{
  "idle_timeout": $IDLE_TIMEOUT,
  "check_interval": $CHECK_INTERVAL,
  "min_memory": "$MIN_MEMORY",
  "max_memory": "$MAX_MEMORY",
  "min_cpu": $MIN_CPU,
  "max_cpu": $MAX_CPU,
  "auto_optimize": $AUTO_OPTIMIZE
}
EOF
}

# Host resource monitoring
get_host_resources() {
    # Get total memory in MB
    local total_mem_kb=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    local total_mem_mb=$((total_mem_kb / 1024))

    # Get available memory in MB
    local available_mem_kb=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    local available_mem_mb=$((available_mem_kb / 1024))

    # Get CPU cores
    local cpu_cores=$(nproc)

    # Get current CPU usage (percentage)
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

    # Get disk usage for project directory
    local disk_usage=$(df "$PROJECT_DIR" | tail -1 | awk '{print $5}' | sed 's/%//')

    echo "{\"total_mem_mb\": $total_mem_mb, \"available_mem_mb\": $available_mem_mb, \"cpu_cores\": $cpu_cores, \"cpu_usage\": $cpu_usage, \"disk_usage\": $disk_usage}"
}

# Container resource monitoring
get_container_resources() {
    if [ "$(get_container_status)" != "running" ]; then
        echo "{}"
        return
    fi

    # Get container stats
    local stats=$(docker stats --no-stream --format json "$CONTAINER_NAME" 2>/dev/null)
    if [ -z "$stats" ]; then
        echo "{}"
        return
    fi

    # Parse memory usage
    local mem_usage=$(echo "$stats" | jq -r '.MemUsage // "0MiB / 0MiB"')
    local mem_used=$(echo "$mem_usage" | awk -F' / ' '{print $1}' | sed 's/MiB//')
    local mem_limit=$(echo "$mem_usage" | awk -F' / ' '{print $2}' | sed 's/MiB//')

    # Parse CPU usage
    local cpu_usage=$(echo "$stats" | jq -r '.CPUPerc // "0%"' | sed 's/%//')

    # Get network I/O
    local net_io=$(docker exec "$CONTAINER_NAME" cat /proc/net/dev 2>/dev/null | grep eth0 | awk '{print $2,$10}' || echo "0 0")
    local net_rx=$(echo "$net_io" | awk '{print $1}')
    local net_tx=$(echo "$net_io" | awk '{print $2}')

    echo "{\"mem_used_mb\": $mem_used, \"mem_limit_mb\": $mem_limit, \"cpu_usage_pct\": $cpu_usage, \"net_rx_kb\": $((net_rx/1024)), \"net_tx_kb\": $((net_tx/1024))}"
}

# Dynamic resource allocation
calculate_optimal_resources() {
    local host_resources=$(get_host_resources)
    local host_total_mem=$(echo "$host_resources" | jq -r '.total_mem_mb')
    local host_available_mem=$(echo "$host_resources" | jq -r '.available_mem_mb')
    local host_cpu_cores=$(echo "$host_resources" | jq -r '.cpu_cores')
    local host_cpu_usage=$(echo "$host_resources" | jq -r '.cpu_usage')

    # Reserve 20% of host memory for system
    local system_reserved=$((host_total_mem / 5))
    local available_for_containers=$((host_available_mem - system_reserved))

    # Allocate based on available resources
    local allocated_mem_mb
    if [ $available_for_containers -gt 8192 ]; then  # 8GB+
        allocated_mem_mb=8192
    elif [ $available_for_containers -gt 4096 ]; then  # 4GB+
        allocated_mem_mb=4096
    elif [ $available_for_containers -gt 2048 ]; then  # 2GB+
        allocated_mem_mb=2048
    else
        allocated_mem_mb=1024  # Minimum
    fi

    # CPU allocation (cores)
    local allocated_cpu_cores
    if [ $host_cpu_cores -ge 8 ]; then
        allocated_cpu_cores=4
    elif [ $host_cpu_cores -ge 4 ]; then
        allocated_cpu_cores=2
    else
        allocated_cpu_cores=1
    fi

    # Adjust based on current CPU usage
    if (( $(echo "$host_cpu_usage > 80" | bc -l) )); then
        allocated_cpu_cores=$((allocated_cpu_cores / 2))
        [ $allocated_cpu_cores -lt 1 ] && allocated_cpu_cores=1
    fi

    echo "{\"memory_mb\": $allocated_mem_mb, \"cpu_cores\": $allocated_cpu_cores, \"host_available_mb\": $available_for_containers}"
}

# Apply resource limits to container
apply_resource_limits() {
    local resources=$(calculate_optimal_resources)
    local memory_mb=$(echo "$resources" | jq -r '.memory_mb')
    local cpu_cores=$(echo "$resources" | jq -r '.cpu_cores')

    log_resource "Applying resource limits: ${memory_mb}MB RAM, ${cpu_cores} CPU cores"

    # Update container resource limits
    docker update --memory "${memory_mb}m" --cpus "$cpu_cores" "$CONTAINER_NAME" 2>/dev/null || true

    # Save current resource state
    echo "$resources" > "$RESOURCE_STATE_FILE"
}

# Activity monitoring
update_activity() {
    echo "$(date +%s)" > "$LAST_ACTIVITY_FILE"
}

is_idle() {
    if [ ! -f "$LAST_ACTIVITY_FILE" ]; then
        return 1  # Not idle if no activity file
    fi

    local last_activity=$(cat "$LAST_ACTIVITY_FILE")
    local current_time=$(date +%s)
    local time_diff=$((current_time - last_activity))

    [ $time_diff -gt $IDLE_TIMEOUT ]
}

# Idle management
pause_idle_container() {
    if [ "$(get_container_status)" = "running" ] && is_idle; then
        log_idle "Container idle for ${IDLE_TIMEOUT}s, pausing to save resources..."
        docker pause "$CONTAINER_NAME"
        echo "paused" > "$IDLE_STATE_FILE"
        log_idle "Container paused. Will resume on next activity."
    fi
}

resume_container() {
    if [ -f "$IDLE_STATE_FILE" ] && [ "$(cat "$IDLE_STATE_FILE")" = "paused" ]; then
        log_idle "Resuming paused container..."
        docker unpause "$CONTAINER_NAME"
        rm -f "$IDLE_STATE_FILE"
        update_activity
        log_idle "Container resumed and marked active."
    fi
}

# Resource optimization
optimize_resources() {
    local container_status=$(get_container_status)

    if [ "$container_status" = "running" ]; then
        if is_idle; then
            # Idle: minimize resources
            log_resource "Optimizing for idle state - minimizing resources"
            docker update --memory "$MIN_MEMORY" --cpus "$MIN_CPU" "$CONTAINER_NAME" 2>/dev/null || true
        else
            # Active: optimize for performance
            log_resource "Optimizing for active state - maximizing performance"
            apply_resource_limits
        fi
    fi
}

# Background monitoring daemon
start_monitoring() {
    log_info "Starting resource monitoring daemon..."

    # Kill any existing monitoring process
    pkill -f "devcontainer-monitor-$CONTAINER_NAME" 2>/dev/null || true

    # Start monitoring in background
    (
        while true; do
            if [ "$AUTO_OPTIMIZE" = "true" ] && [ "$(get_container_status)" = "running" ]; then
                optimize_resources
                pause_idle_container
            fi
            sleep "$CHECK_INTERVAL"
        done
    ) &
    disown

    echo $! > "/tmp/devcontainer-monitor-$CONTAINER_NAME.pid"
    log_success "Resource monitoring daemon started (PID: $(cat "/tmp/devcontainer-monitor-$CONTAINER_NAME.pid"))"
}

stop_monitoring() {
    if [ -f "/tmp/devcontainer-monitor-$CONTAINER_NAME.pid" ]; then
        local pid=$(cat "/tmp/devcontainer-monitor-$CONTAINER_NAME.pid")
        kill "$pid" 2>/dev/null || true
        rm -f "/tmp/devcontainer-monitor-$CONTAINER_NAME.pid"
        log_info "Resource monitoring daemon stopped"
    fi
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

    # Apply dynamic resource limits
    apply_resource_limits

    # Start resource monitoring daemon
    start_monitoring

    # Mark container as active
    update_activity

    log_info "DevContainer started with dynamic resource management. Use '$0 attach' to connect with VS Code"
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

    # Stop resource monitoring daemon
    stop_monitoring

    # Clean up resource state files
    rm -f "$RESOURCE_STATE_FILE" "$IDLE_STATE_FILE" "$LAST_ACTIVITY_FILE"
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

    # Stop resource monitoring daemon
    stop_monitoring

    # Clean up all resource state files
    rm -f "$RESOURCE_STATE_FILE" "$IDLE_STATE_FILE" "$LAST_ACTIVITY_FILE"
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

optimize_resources_cmd() {
    log_info "Manually optimizing container resources..."

    local status=$(get_container_status)

    if [ "$status" != "running" ]; then
        log_error "DevContainer is not running. Use '$0 start' first"
        exit 1
    fi

    apply_resource_limits
    update_activity
    log_success "Resources optimized and container marked active"
}

show_usage() {
    cat << EOF
DevContainer Management Script for Bootdisk

USAGE:
  $0 <command> [options]

COMMANDS:
  status      Show current devcontainer status
  start       Start or create devcontainer with dynamic resource management
  create      Create new devcontainer from scratch
  attach      Attach VS Code to running devcontainer
  stop        Stop devcontainer and cleanup resources
  destroy     Completely remove devcontainer and cleanup
  logs        Show devcontainer logs
  optimize    Manually optimize container resources
  help        Show this help

EXAMPLES:
  $0 status                    # Check if devcontainer is running
  $0 start                     # Start devcontainer with resource management
  $0 attach                    # Connect VS Code to running container
  $0 optimize                  # Manually optimize resources
  $0 stop                      # Stop container and cleanup
  $0 destroy                   # Remove container completely

WORKFLOW:
  1. $0 start                  # Start container with resource management
  2. $0 attach                 # Connect VS Code
  3. Develop in VS Code
  4. $0 optimize               # Optimize resources manually if needed
  5. $0 stop                   # Stop when done
  6. $0 start                  # Restart later

NOTES:
  - Requires Docker and VS Code with Dev Containers extension
  - First run will build the container (takes time)
  - Container persists data between starts/stops
  - Dynamic resource allocation based on host capacity
  - Automatic idle detection and resource optimization
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
        "optimize")
            optimize_resources_cmd
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
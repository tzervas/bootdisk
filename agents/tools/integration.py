#!/usr/bin/env python3
"""
Bootdisk Tools Integration
Provides integration with Python development ecosystem tools
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional


class ToolsIntegration:
    """Integration manager for Python development tools."""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.tools_root = Path.home() / "Documents" / "projects"

    def run_py_devcontainer(self, template: str = "python-ml", output: Optional[str] = None):
        """Generate a devcontainer using py-devcontainer tool."""
        try:
            cmd = [sys.executable, "-m", "devcontainer.cli", "generate",
                   "--template", template]
            if output:
                cmd.extend(["--output", output])

            result = subprocess.run(cmd, cwd=self.tools_root / "py-devcontainer",
                                  capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except FileNotFoundError:
            return False, "", "py-devcontainer tool not found. Install from py-devcontainer project."

    def run_py_devtools(self, command: str, *args):
        """Run py-devtools commands."""
        try:
            cmd = [sys.executable, "-m", "devtools.cli", command] + list(args)
            result = subprocess.run(cmd, cwd=self.tools_root / "py-devtools",
                                  capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except FileNotFoundError:
            return False, "", "py-devtools not found. Install from py-devtools project."

    def scaffold_bootdisk_extension(self, name: str):
        """Scaffold a new bootdisk extension using py-devtools."""
        return self.run_py_devtools("scaffold", "bootdisk-extension", name)

    def generate_devcontainer(self, config: dict):
        """Generate devcontainer config using py-devcontainer."""
        # This would use py-devcontainer to generate optimized configs
        template = "python-ml" if config.get("ml_enabled") else "python-basic"
        return self.run_py_devcontainer(template)

    def validate_environment(self):
        """Validate that all integrated tools are available."""
        tools_status = {}

        # Check py-devcontainer
        success, _, _ = self.run_py_devcontainer("--help")
        tools_status["py-devcontainer"] = success

        # Check py-devtools
        success, _, _ = self.run_py_devtools("--help")
        tools_status["py-devtools"] = success

        # Check Rust toolchain
        try:
            result = subprocess.run(["cargo", "--version"], capture_output=True, text=True)
            tools_status["rust_toolchain"] = result.returncode == 0
        except FileNotFoundError:
            tools_status["rust_toolchain"] = False

        # Check Python environment
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            tools_status["python_environment"] = result.returncode == 0
        except FileNotFoundError:
            tools_status["python_environment"] = False

        return tools_status

    def run_cargo_command(self, command: str, *args, cwd: Optional[str] = None):
        """Run cargo commands for Rust development."""
        try:
            cmd = ["cargo", command] + list(args)
            working_dir = cwd or self.project_root
            result = subprocess.run(cmd, cwd=working_dir, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except FileNotFoundError:
            return False, "", "Cargo not found. Install Rust toolchain."

    def run_uv_command(self, command: str, *args, cwd: Optional[str] = None):
        """Run uv commands for Python package management."""
        try:
            cmd = ["uv", command] + list(args)
            working_dir = cwd or self.project_root
            result = subprocess.run(cmd, cwd=working_dir, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        except FileNotFoundError:
            return False, "", "uv not found. Install uv package manager."

    def check_devcontainer_status(self):
        """Check if devcontainer is running and get its status."""
        try:
            # Check if container exists and is running
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={self.project_root.name}", "--format", "{{.Status}}"],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                return True, result.stdout.strip(), ""
            else:
                return False, "", "DevContainer not running"
        except FileNotFoundError:
            return False, "", "Docker not found"

    def get_system_resources(self):
        """Get current system resource usage."""
        try:
            # Get memory info
            with open("/proc/meminfo", "r") as f:
                mem_info = f.read()

            total_mem = None
            available_mem = None
            for line in mem_info.split('\n'):
                if line.startswith('MemTotal:'):
                    total_mem = int(line.split()[1]) // 1024  # MB
                elif line.startswith('MemAvailable:'):
                    available_mem = int(line.split()[1]) // 1024  # MB

            # Get CPU cores
            cpu_cores = len([line for line in open("/proc/cpuinfo") if line.startswith("processor")])

            return {
                "memory_total_mb": total_mem,
                "memory_available_mb": available_mem,
                "cpu_cores": cpu_cores,
                "memory_usage_percent": ((total_mem - available_mem) / total_mem * 100) if total_mem else 0
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    """CLI interface for tools integration."""
    import argparse

    parser = argparse.ArgumentParser(description="Bootdisk tools integration")
    parser.add_argument("command", choices=["validate", "scaffold", "devcontainer"],
                       help="Command to run")
    parser.add_argument("--name", help="Name for scaffolding")
    parser.add_argument("--template", default="python-ml",
                       help="DevContainer template")

    args = parser.parse_args()
    integration = ToolsIntegration()

    if args.command == "validate":
        status = integration.validate_environment()
        print("🔍 Tools Integration Status:")
        for tool, available in status.items():
            status_icon = "✅" if available else "❌"
            print(f"  {status_icon} {tool}")
        return 0 if all(status.values()) else 1

    elif args.command == "scaffold":
        if not args.name:
            print("❌ --name required for scaffold command")
            return 1
        success, stdout, stderr = integration.scaffold_bootdisk_extension(args.name)
        if success:
            print(f"✅ Scaffolded bootdisk extension: {args.name}")
            print(stdout)
        else:
            print(f"❌ Failed to scaffold: {stderr}")
        return 0 if success else 1

    elif args.command == "devcontainer":
        success, stdout, stderr = integration.run_py_devcontainer(args.template)
        if success:
            print("✅ DevContainer generated successfully")
            print(stdout)
        else:
            print(f"❌ Failed to generate devcontainer: {stderr}")
        return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
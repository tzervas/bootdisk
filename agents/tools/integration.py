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

        return tools_status


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
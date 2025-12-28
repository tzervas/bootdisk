#!/usr/bin/env python3
"""
Bootdisk - Customized Debian workstation setup automation

Generates and manages workstation configurations for gaming/inference workloads
with GPU serving capabilities and PXE boot support.
"""

import sys
from pathlib import Path
from dev_mem import TmpManager, TmpConfig
from agentic_dev_boilerplate import BoilerplateGenerator

def main():
    print("🚀 Bootdisk - Debian Workstation Setup Automation")
    print("=" * 50)

    # Configure memory management for bootdisk operations
    tmp_config = TmpConfig(
        base_tmp_dir=Path("/tmp/bootdisk"),
        max_age_hours=24,  # Keep temp files for 1 day
        prune_interval_minutes=60,  # Clean up hourly
        max_project_dirs=50,
        max_total_size_gb=2.0,  # Limit temp space for bootdisk
        semantic_weighting_enabled=True
    )

    tmp_manager = TmpManager("bootdisk", tmp_config)
    print(f"📁 Temporary directory manager initialized at: {tmp_manager.config.base_tmp_dir}")

    # Load bootdisk schema
    schema_path = Path(__file__).parent / "bootdisk_schema.yaml"
    if not schema_path.exists():
        print(f"❌ Bootdisk schema not found at: {schema_path}")
        sys.exit(1)

    print(f"📋 Loading schema from: {schema_path}")

    # Generate workstation setup boilerplate
    try:
        generator = BoilerplateGenerator(str(schema_path))
        print("✅ Schema loaded successfully")

        # Create temporary directory for generation
        temp_dir = tmp_manager.get_task_dir("workstation_setup")
        print(f"📂 Created temp directory: {temp_dir}")

        # TODO: Generate the actual workstation setup files
        # This will be implemented in the next phase

        print("🎯 Bootdisk setup generation ready!")
        print("Next steps:")
        print("  - Implement PXE boot configuration")
        print("  - Add NVIDIA GPU driver setup")
        print("  - Configure Docker/Kubernetes for inference")
        print("  - Generate Debian installation scripts")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

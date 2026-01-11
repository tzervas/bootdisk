"""
Bootdisk Multi-Agent System
AI-powered development workflows and automation
"""

from . import core as _core
from . import roles as _roles
from . import tools as _tools

__version__ = "1.0.0"
__description__ = "Multi-agent development system for bootdisk"

__all__ = [
    # Core infrastructure
    *_core.__all__,

    # Agent roles
    *_roles.__all__,

    # Tools and integrations
    *_tools.__all__,
]

# Re-export all names listed in the submodules' __all__ attributes
for _module in (_core, _roles, _tools):
    for _name in getattr(_module, "__all__", []):
        globals()[_name] = getattr(_module, _name)</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/agents/__init__.py
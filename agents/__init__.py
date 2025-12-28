"""
Bootdisk Multi-Agent System
AI-powered development workflows and automation
"""

from .core import *
from .roles import *
from .tools import *

__version__ = "1.0.0"
__description__ = "Multi-agent development system for bootdisk"

__all__ = [
    # Core infrastructure
    *core.__all__,

    # Agent roles
    *roles.__all__,

    # Tools and integrations
    *tools.__all__,
]</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/agents/__init__.py
"""
Bootdisk Agent Core
Core infrastructure for multi-agent development workflows
"""

from .manager import BaseAgent, AgentManager, AgentRole, AgentState, AgentConfig, AgentMessage
from .workflows import WorkflowCoordinator, WorkflowType, WorkflowState, WorkflowStep, WorkflowDefinition, WorkflowExecution

__all__ = [
    # Agent management
    "BaseAgent",
    "AgentManager",
    "AgentRole",
    "AgentState",
    "AgentConfig",
    "AgentMessage",

    # Workflow coordination
    "WorkflowCoordinator",
    "WorkflowType",
    "WorkflowState",
    "WorkflowStep",
    "WorkflowDefinition",
    "WorkflowExecution",
]</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/agents/core/__init__.py
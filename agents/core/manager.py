"""
Bootdisk Agent Core Infrastructure
Provides the foundation for multi-agent development workflows
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Defined agent roles in the bootdisk system"""
    SOFTWARE_ENGINEER = "swe"
    QA_ENGINEER = "qa"
    DEVOPS_ENGINEER = "devops"
    SECURITY_ENGINEER = "security"
    DOCUMENTATION_SPECIALIST = "documentation"
    PROJECT_MANAGER = "project_manager"


class AgentState(Enum):
    """Agent execution states"""
    IDLE = "idle"
    ACTIVE = "active"
    WAITING = "waiting"
    ERROR = "error"


@dataclass
class AgentConfig:
    """Configuration for an agent instance"""
    role: AgentRole
    name: str
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4000
    capabilities: List[str] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []


@dataclass
class AgentMessage:
    """Message structure for agent communication"""
    sender: str
    recipient: str
    content: str
    message_type: str = "task"
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseAgent(ABC):
    """Abstract base class for all bootdisk agents"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.state = AgentState.IDLE
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.logger = logging.getLogger(f"{__name__}.{config.name}")

    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task and return results"""
        pass

    @abstractmethod
    async def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the quality of agent output"""
        pass

    async def send_message(self, message: AgentMessage) -> None:
        """Send a message to another agent"""
        # Implementation would integrate with message bus
        self.logger.info(f"Sending message to {message.recipient}: {message.content[:50]}...")

    async def receive_message(self) -> Optional[AgentMessage]:
        """Receive a message from the queue"""
        try:
            return self.message_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def run(self) -> None:
        """Main agent execution loop"""
        self.state = AgentState.ACTIVE
        self.logger.info(f"Agent {self.config.name} starting")

        try:
            while self.state == AgentState.ACTIVE:
                # Process incoming messages
                message = await self.receive_message()
                if message:
                    await self._handle_message(message)

                # Process pending tasks
                await self._process_pending_tasks()

                # Brief pause to prevent busy waiting
                await asyncio.sleep(0.1)

        except Exception as e:
            self.logger.error(f"Agent {self.config.name} error: {e}")
            self.state = AgentState.ERROR
        finally:
            self.logger.info(f"Agent {self.config.name} stopping")

    async def _handle_message(self, message: AgentMessage) -> None:
        """Handle incoming messages"""
        self.logger.info(f"Received message from {message.sender}: {message.message_type}")

        if message.message_type == "task":
            # Process as task
            result = await self.process_task(message.content)
            # Send response
            response = AgentMessage(
                sender=self.config.name,
                recipient=message.sender,
                content=result,
                message_type="response",
                metadata={"original_task": message.content}
            )
            await self.send_message(response)

    async def _process_pending_tasks(self) -> None:
        """Process any pending tasks in the agent's queue"""
        # Implementation specific to each agent
        pass

    def stop(self) -> None:
        """Stop the agent"""
        self.state = AgentState.IDLE
        self.logger.info(f"Agent {self.config.name} stopped")


class AgentManager:
    """Manages the lifecycle and coordination of multiple agents"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.logger = logging.getLogger(f"{__name__}.AgentManager")

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with the manager"""
        self.agents[agent.config.name] = agent
        self.logger.info(f"Registered agent: {agent.config.name} ({agent.config.role.value})")

    def unregister_agent(self, name: str) -> None:
        """Unregister an agent"""
        if name in self.agents:
            self.agents[name].stop()
            del self.agents[name]
            self.logger.info(f"Unregistered agent: {name}")

    async def execute_workflow(self, workflow_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a predefined workflow"""
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        workflow = self.workflows[workflow_name]
        self.logger.info(f"Executing workflow: {workflow_name}")

        # Workflow execution logic would go here
        # This is a simplified implementation

        results = {}
        for step in workflow.get("steps", []):
            agent_name = step["agent"]
            task = step["task"]

            if agent_name not in self.agents:
                raise ValueError(f"Agent {agent_name} not found")

            agent = self.agents[agent_name]
            result = await agent.process_task({**task, **context})
            results[step["name"]] = result

        return results

    def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered agents"""
        return {
            name: {
                "role": agent.config.role.value,
                "state": agent.state.value,
                "capabilities": agent.config.capabilities
            }
            for name, agent in self.agents.items()
        }

    async def shutdown(self) -> None:
        """Shutdown all agents"""
        self.logger.info("Shutting down agent manager")

        # Stop all agents
        for agent in self.agents.values():
            agent.stop()

        # Agents are expected to terminate their run loops in response to stop().
        # No new run loops should be started here; we simply yield control once.
        await asyncio.sleep(0)

        self.agents.clear()
        self.logger.info("Agent manager shutdown complete")</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/agents/core/manager.py
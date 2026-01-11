"""
Bootdisk Agent Workflows
Defines coordination patterns and workflows for multi-agent development
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)


class WorkflowType(Enum):
    """Types of agent workflows"""
    CODE_IMPLEMENTATION = "code_implementation"
    TESTING_VALIDATION = "testing_validation"
    DOCUMENTATION_GENERATION = "documentation_generation"
    SECURITY_REVIEW = "security_review"
    DEPLOYMENT_PREPARATION = "deployment_preparation"
    BUG_FIX = "bug_fix"


class WorkflowState(Enum):
    """Workflow execution states"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStep:
    """A single step in a workflow"""
    name: str
    agent_role: str
    task: Dict[str, Any]
    dependencies: List[str] = None
    timeout: int = 300  # 5 minutes default
    retry_count: int = 0

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class WorkflowDefinition:
    """Complete workflow definition"""
    name: str
    type: WorkflowType
    description: str
    steps: List[WorkflowStep]
    max_duration: int = 1800  # 30 minutes default
    required_capabilities: List[str] = None

    def __post_init__(self):
        if self.required_capabilities is None:
            self.required_capabilities = []


@dataclass
class WorkflowExecution:
    """Runtime state of a workflow execution"""
    workflow_id: str
    definition: WorkflowDefinition
    state: WorkflowState = WorkflowState.PENDING
    current_step: Optional[str] = None
    results: Dict[str, Any] = None
    errors: List[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def __post_init__(self):
        if self.results is None:
            self.results = {}
        if self.errors is None:
            self.errors = []


class WorkflowCoordinator:
    """Coordinates execution of multi-agent workflows"""

    def __init__(self):
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.logger = logging.getLogger(f"{__name__}.WorkflowCoordinator")

    def register_workflow(self, workflow: WorkflowDefinition) -> None:
        """Register a workflow definition"""
        self.workflows[workflow.name] = workflow
        self.logger.info(f"Registered workflow: {workflow.name} ({workflow.type.value})")

    def unregister_workflow(self, name: str) -> None:
        """Unregister a workflow"""
        if name in self.workflows:
            del self.workflows[name]
            self.logger.info(f"Unregistered workflow: {name}")

    async def execute_workflow(self, name: str, context: Dict[str, Any] = None) -> str:
        """Start execution of a workflow"""
        if name not in self.workflows:
            raise ValueError(f"Unknown workflow: {name}")

        if context is None:
            context = {}

        loop = asyncio.get_running_loop()
        workflow_id = f"{name}_{int(loop.time())}"

        execution = WorkflowExecution(
            workflow_id=workflow_id,
            definition=self.workflows[name],
            start_time=loop.time()
        )

        self.executions[workflow_id] = execution
        self.logger.info(f"Started workflow execution: {workflow_id}")

        # Start execution in background
        asyncio.create_task(self._execute_workflow_async(execution, context))

        return workflow_id

    async def _execute_workflow_async(self, execution: WorkflowExecution, context: Dict[str, Any]) -> None:
        """Execute a workflow asynchronously"""
        try:
            execution.state = WorkflowState.RUNNING

            # Execute steps in dependency order
            completed_steps = set()
            pending_steps = {step.name: step for step in execution.definition.steps}

            while pending_steps:
                # Find steps with satisfied dependencies
                executable_steps = []
                for step_name, step in pending_steps.items():
                    if all(dep in completed_steps for dep in step.dependencies):
                        executable_steps.append(step)

                if not executable_steps:
                    # Circular dependency or unsatisfied dependencies
                    execution.state = WorkflowState.FAILED
                    execution.errors.append("Circular dependency detected or unsatisfied dependencies")
                    break

                # Execute steps concurrently if no dependencies between them
                tasks = []
                for step in executable_steps:
                    task = asyncio.create_task(self._execute_step(step, context))
                    tasks.append((step.name, task))

                # Wait for all executable steps to complete
                results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)

                for (step_name, _), result in zip(tasks, results):
                    if isinstance(result, Exception):
                        execution.errors.append(f"Step {step_name} failed: {result}")
                        execution.state = WorkflowState.FAILED
                        break

                    execution.results[step_name] = result
                    completed_steps.add(step_name)
                    del pending_steps[step_name]

                if execution.state == WorkflowState.FAILED:
                    break

            if execution.state != WorkflowState.FAILED:
                execution.state = WorkflowState.COMPLETED

        except Exception as e:
            execution.state = WorkflowState.FAILED
            execution.errors.append(f"Workflow execution failed: {e}")
            self.logger.error(f"Workflow {execution.workflow_id} failed: {e}")

        finally:
            execution.end_time = asyncio.get_event_loop().time()
            duration = execution.end_time - (execution.start_time or 0)
            self.logger.info(f"Workflow {execution.workflow_id} completed in {duration:.2f}s")

    async def _execute_step(self, step: WorkflowStep, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        self.logger.info(f"Executing step: {step.name}")

        # This would integrate with the AgentManager to execute the step
        # For now, return a mock result
        await asyncio.sleep(0.1)  # Simulate processing time

        return {
            "step": step.name,
            "agent": step.agent_role,
            "result": f"Completed {step.name}",
            "context": context
        }

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a workflow execution"""
        execution = self.executions.get(workflow_id)
        if not execution:
            return None

        return {
            "workflow_id": execution.workflow_id,
            "name": execution.definition.name,
            "state": execution.state.value,
            "current_step": execution.current_step,
            "progress": len(execution.results) / len(execution.definition.steps) if execution.definition.steps else 0,
            "errors": execution.errors,
            "duration": (asyncio.get_event_loop().time() - (execution.start_time or 0)) if execution.start_time else 0
        }

    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow"""
        execution = self.executions.get(workflow_id)
        if not execution or execution.state not in [WorkflowState.PENDING, WorkflowState.RUNNING]:
            return False

        execution.state = WorkflowState.CANCELLED
        self.logger.info(f"Cancelled workflow: {workflow_id}")
        return True

    def get_available_workflows(self) -> List[Dict[str, Any]]:
        """Get list of available workflows"""
        return [
            {
                "name": workflow.name,
                "type": workflow.type.value,
                "description": workflow.description,
                "steps": len(workflow.steps),
                "capabilities": workflow.required_capabilities
            }
            for workflow in self.workflows.values()
        ]


# Predefined workflow definitions
def create_code_implementation_workflow() -> WorkflowDefinition:
    """Create the code implementation workflow"""
    return WorkflowDefinition(
        name="code_implementation",
        type=WorkflowType.CODE_IMPLEMENTATION,
        description="Complete code implementation with testing and documentation",
        steps=[
            WorkflowStep(
                name="analyze_requirements",
                agent_role="project_manager",
                task={"action": "analyze", "type": "requirements"}
            ),
            WorkflowStep(
                name="design_solution",
                agent_role="software_engineer",
                task={"action": "design", "type": "architecture"},
                dependencies=["analyze_requirements"]
            ),
            WorkflowStep(
                name="implement_code",
                agent_role="software_engineer",
                task={"action": "implement", "type": "code"},
                dependencies=["design_solution"]
            ),
            WorkflowStep(
                name="write_tests",
                agent_role="qa_engineer",
                task={"action": "write", "type": "tests"},
                dependencies=["implement_code"]
            ),
            WorkflowStep(
                name="run_tests",
                agent_role="qa_engineer",
                task={"action": "run", "type": "tests"},
                dependencies=["write_tests"]
            ),
            WorkflowStep(
                name="generate_docs",
                agent_role="documentation_specialist",
                task={"action": "generate", "type": "documentation"},
                dependencies=["implement_code"]
            ),
            WorkflowStep(
                name="security_review",
                agent_role="security_engineer",
                task={"action": "review", "type": "security"},
                dependencies=["implement_code", "run_tests"]
            )
        ],
        required_capabilities=["code_generation", "testing", "documentation"]
    )


def create_testing_validation_workflow() -> WorkflowDefinition:
    """Create the testing and validation workflow"""
    return WorkflowDefinition(
        name="testing_validation",
        type=WorkflowType.TESTING_VALIDATION,
        description="Comprehensive testing and validation of code changes",
        steps=[
            WorkflowStep(
                name="analyze_codebase",
                agent_role="qa_engineer",
                task={"action": "analyze", "type": "codebase"}
            ),
            WorkflowStep(
                name="generate_test_plan",
                agent_role="qa_engineer",
                task={"action": "generate", "type": "test_plan"},
                dependencies=["analyze_codebase"]
            ),
            WorkflowStep(
                name="write_unit_tests",
                agent_role="qa_engineer",
                task={"action": "write", "type": "unit_tests"},
                dependencies=["generate_test_plan"]
            ),
            WorkflowStep(
                name="write_integration_tests",
                agent_role="qa_engineer",
                task={"action": "write", "type": "integration_tests"},
                dependencies=["generate_test_plan"]
            ),
            WorkflowStep(
                name="run_unit_tests",
                agent_role="qa_engineer",
                task={"action": "run", "type": "unit_tests"},
                dependencies=["write_unit_tests"]
            ),
            WorkflowStep(
                name="run_integration_tests",
                agent_role="qa_engineer",
                task={"action": "run", "type": "integration_tests"},
                dependencies=["write_integration_tests"]
            ),
            WorkflowStep(
                name="generate_test_report",
                agent_role="qa_engineer",
                task={"action": "generate", "type": "test_report"},
                dependencies=["run_unit_tests", "run_integration_tests"]
            )
        ],
        required_capabilities=["testing", "validation", "reporting"]
    )</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/agents/core/workflows.py
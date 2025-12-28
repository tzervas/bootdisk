# Agents Module

A sophisticated multi-agent system designed for agentic development workflows, providing coordinated AI-driven automation for software development tasks.

## Overview

The `agents` module implements a scalable, async-first multi-agent architecture that enables complex development workflows through specialized AI agents, tool integrations, and workflow orchestration. Built with Python's asyncio for high concurrency and reliability.

### Key Features

- **Multi-Agent Coordination**: Concurrent agent execution with message passing
- **Workflow Orchestration**: Dependency-based task execution with timeout management
- **Tool Integration**: Native integration with development tools (Cargo, UV, DevContainers)
- **API Abstractions**: Standardized clients for OpenAI, Ollama, GitHub, and HuggingFace
- **Error Resilience**: Comprehensive error handling and recovery mechanisms
- **Type Safety**: Full type hints and structured data classes
- **Observable**: Extensive logging and state tracking throughout

## Architecture

```
agents/
├── __init__.py          # Module exports and metadata
├── core/                # Core infrastructure
│   ├── __init__.py
│   ├── manager.py       # BaseAgent, AgentManager, message handling
│   └── workflows.py     # WorkflowCoordinator, execution logic
├── roles/               # Specialized agent implementations
│   ├── __init__.py
│   └── swe.py          # SoftwareEngineerAgent
└── tools/               # External integrations
    ├── __init__.py
    ├── integration.py   # Development tool integrations
    └── api.py          # External API clients
```

### Design Principles

1. **Async-First**: All operations use asyncio for scalability and non-blocking I/O
2. **Modular Architecture**: Clear separation between core infrastructure, roles, and tools
3. **Error Resilience**: Comprehensive exception handling with graceful degradation
4. **Extensible**: Plugin architecture for adding new agents, tools, and workflows
5. **Observable**: Structured logging and state tracking for debugging and monitoring
6. **Type Safe**: Full type annotations and runtime validation

## Core Components

### Agent Infrastructure (`core/manager.py`)

#### BaseAgent

Abstract base class defining the agent interface and lifecycle.

```python
from agents.core.manager import BaseAgent, AgentRole, AgentState, AgentConfig

class MyAgent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Implement task processing logic
        return {"result": "processed"}

    def validate_output(self, output: Dict[str, Any]) -> bool:
        # Implement output validation
        return True
```

**AgentRole Enum:**
- `SWE`: Software Engineer - code implementation and refactoring
- `ARCHITECT`: System Architect - design and architecture decisions
- `REVIEWER`: Code Reviewer - quality assurance and validation
- `TEST_ENGINEER`: Test Engineer - testing and quality assurance
- `DEVOPS`: DevOps Engineer - deployment and infrastructure

**AgentState Enum:**
- `IDLE`: Agent is waiting for tasks
- `RUNNING`: Agent is actively processing
- `COMPLETED`: Task completed successfully
- `ERROR`: Task failed with error

**AgentConfig Dataclass:**
```python
@dataclass
class AgentConfig:
    role: AgentRole
    capabilities: List[str]
    max_concurrent_tasks: int = 1
    timeout_seconds: int = 300
    retry_attempts: int = 3
```

#### AgentManager

Coordinates multiple agents and handles inter-agent communication.

```python
from agents.core.manager import AgentManager, AgentMessage

async with AgentManager() as manager:
    # Register agents
    await manager.register_agent("swe_agent", swe_agent)
    await manager.register_agent("reviewer_agent", reviewer_agent)

    # Send messages between agents
    message = AgentMessage(
        sender="swe_agent",
        recipient="reviewer_agent",
        content={"task": "review_code", "files": ["main.py"]},
        metadata={"priority": "high"}
    )
    await manager.send_message(message)
```

**AgentMessage Dataclass:**
```python
@dataclass
class AgentMessage:
    sender: str
    recipient: str
    content: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
```

### Workflow Coordination (`core/workflows.py`)

#### WorkflowCoordinator

Orchestrates complex multi-step processes with dependency management.

```python
from agents.core.workflows import WorkflowCoordinator, WorkflowDefinition

coordinator = WorkflowCoordinator()

# Define a workflow
workflow_def = WorkflowDefinition(
    name="feature_development",
    steps=[
        {
            "name": "analyze_requirements",
            "agent": "architect",
            "timeout": 300,
            "inputs": {"requirements": "..."}
        },
        {
            "name": "implement_feature",
            "agent": "swe",
            "depends_on": ["analyze_requirements"],
            "timeout": 600
        },
        {
            "name": "code_review",
            "agent": "reviewer",
            "depends_on": ["implement_feature"],
            "timeout": 300
        }
    ]
)

# Execute workflow
execution = await coordinator.create_workflow(workflow_def)
result = await coordinator.execute_workflow(execution)
```

**WorkflowDefinition Dataclass:**
```python
@dataclass
class WorkflowDefinition:
    name: str
    steps: List[Dict[str, Any]]
    description: Optional[str] = None
    timeout: int = 3600
```

**WorkflowExecution Dataclass:**
```python
@dataclass
class WorkflowExecution:
    workflow_id: str
    definition: WorkflowDefinition
    status: WorkflowStatus
    results: Dict[str, Any]
    errors: List[str]
    start_time: datetime
    end_time: Optional[datetime] = None
```

### Specialized Agents (`roles/`)

#### SoftwareEngineerAgent (`roles/swe.py`)

Specialized agent for software engineering tasks.

```python
from agents.roles.swe import SoftwareEngineerAgent

agent = SoftwareEngineerAgent(AgentConfig(
    role=AgentRole.SWE,
    capabilities=["python", "rust", "typescript", "refactoring"]
))

# Process different task types
result = await agent.process_task({
    "type": "implement_feature",
    "description": "Add user authentication",
    "language": "python",
    "files": ["auth.py"]
})

result = await agent.process_task({
    "type": "refactor_code",
    "description": "Extract common functionality",
    "files": ["utils.py", "main.py"]
})
```

**Supported Task Types:**
- `implement_feature`: New feature development
- `refactor_code`: Code restructuring and optimization
- `design_architecture`: System design and planning
- `review_code`: Code quality assessment

### Tool Integrations (`tools/`)

#### Development Tools (`tools/integration.py`)

Subprocess-based integration with development tools.

```python
from agents.tools.integration import ToolsIntegration

tools = ToolsIntegration()

# Rust/Cargo operations
result = await tools.run_cargo_command(
    ["build", "--release"],
    cwd="/path/to/rust/project"
)

# Python/UV operations
result = await tools.run_uv_command(
    ["add", "requests"],
    cwd="/path/to/python/project"
)

# DevContainer operations
result = await tools.run_py_devcontainer(
    ["build"],
    config_path=".devcontainer/devcontainer.json"
)
```

**ToolsIntegration Methods:**
- `run_cargo_command(args, cwd, env)`: Execute Cargo commands
- `run_uv_command(args, cwd, env)`: Execute UV package manager commands
- `run_py_devcontainer(args, config_path)`: DevContainer operations
- `run_py_devtools(args, cwd)`: Python development tools
- `validate_environment()`: Check tool availability

#### API Clients (`tools/api.py`)

Standardized HTTP clients for external API services.

```python
from agents.tools.api import (
    OpenAIClient, OllamaClient, GitHubClient,
    HuggingFaceClient, APIClientManager
)

# OpenAI integration
async with OpenAIClient(api_key="your-key") as client:
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "Hello!"}],
        model="gpt-4",
        temperature=0.7
    )

# Ollama integration
async with OllamaClient() as client:
    response = await client.generate(
        model="llama2",
        prompt="Explain quantum computing"
    )

# GitHub integration
async with GitHubClient(token="your-token") as client:
    # Create issue
    issue = await client.create_issue(
        owner="myorg",
        repo="myrepo",
        title="Bug report",
        body="Found a critical bug"
    )

    # Create PR
    pr = await client.create_pull_request(
        owner="myorg",
        repo="myrepo",
        title="Feature implementation",
        head="feature-branch",
        base="main",
        body="Implements new feature"
    )

# HuggingFace integration
async with HuggingFaceClient(api_key="your-key") as client:
    response = await client.text_generation(
        model="gpt2",
        inputs="The future of AI is",
        parameters={"max_length": 50}
    )
```

**APIResponse Dataclass:**
```python
@dataclass
class APIResponse:
    success: bool
    data: Any
    error: Optional[str] = None
    status_code: Optional[int] = None
    headers: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**APIClientManager:**
```python
# Manage multiple clients
async with APIClientManager() as manager:
    manager.register_client("openai", OpenAIClient(api_key))
    manager.register_client("github", GitHubClient(token))

    # Use registered clients
    openai_client = manager.get_client("openai")
    response = await openai_client.chat_completion(...)
```

## Usage Examples

### Basic Agent Setup

```python
import asyncio
from agents.core.manager import AgentManager, AgentConfig, AgentRole
from agents.roles.swe import SoftwareEngineerAgent

async def main():
    # Create agent configuration
    config = AgentConfig(
        role=AgentRole.SWE,
        capabilities=["python", "testing", "refactoring"],
        max_concurrent_tasks=2,
        timeout_seconds=300
    )

    # Create and configure agent
    swe_agent = SoftwareEngineerAgent(config)

    # Set up agent manager
    async with AgentManager() as manager:
        await manager.register_agent("swe", swe_agent)

        # Process a task
        task = {
            "type": "implement_feature",
            "description": "Add logging to the application",
            "language": "python",
            "files": ["app.py"]
        }

        result = await manager.process_task("swe", task)
        print(f"Task completed: {result}")

asyncio.run(main())
```

### Workflow Execution

```python
import asyncio
from agents.core.workflows import WorkflowCoordinator, WorkflowDefinition
from agents.core.manager import AgentManager, AgentConfig, AgentRole
from agents.roles.swe import SoftwareEngineerAgent

async def run_feature_workflow():
    # Set up agents
    swe_config = AgentConfig(role=AgentRole.SWE, capabilities=["python"])
    swe_agent = SoftwareEngineerAgent(swe_config)

    async with AgentManager() as manager:
        await manager.register_agent("swe", swe_agent)

        # Create workflow coordinator
        coordinator = WorkflowCoordinator(manager)

        # Define feature development workflow
        workflow = WorkflowDefinition(
            name="user_auth_feature",
            steps=[
                {
                    "name": "design_auth",
                    "agent": "swe",
                    "task": {
                        "type": "design_architecture",
                        "description": "Design user authentication system"
                    },
                    "timeout": 300
                },
                {
                    "name": "implement_auth",
                    "agent": "swe",
                    "task": {
                        "type": "implement_feature",
                        "description": "Implement authentication endpoints",
                        "files": ["auth.py", "models.py"]
                    },
                    "depends_on": ["design_auth"],
                    "timeout": 600
                }
            ]
        )

        # Execute workflow
        execution = await coordinator.create_workflow(workflow)
        result = await coordinator.execute_workflow(execution)

        print(f"Workflow completed: {result['status']}")

asyncio.run(run_feature_workflow())
```

### Tool Integration Example

```python
import asyncio
from agents.tools.integration import ToolsIntegration
from agents.tools.api import APIClientManager, OpenAIClient, GitHubClient

async def integrated_development():
    tools = ToolsIntegration()
    api_manager = APIClientManager()

    # Register API clients
    api_manager.register_client("openai", OpenAIClient("your-openai-key"))
    api_manager.register_client("github", GitHubClient("your-github-token"))

    async with api_manager:
        # Use tools to set up project
        await tools.run_uv_command(["init", "myproject"])
        await tools.run_uv_command(["add", "fastapi", "uvicorn"], cwd="myproject")

        # Generate code with AI
        openai = api_manager.get_client("openai")
        code_response = await openai.chat_completion(
            messages=[{
                "role": "user",
                "content": "Create a FastAPI hello world endpoint"
            }],
            model="gpt-4"
        )

        # Write code to file
        with open("myproject/main.py", "w") as f:
            f.write(code_response.data["choices"][0]["message"]["content"])

        # Create GitHub repository
        github = api_manager.get_client("github")
        await github.create_repo("myorg", "myproject", "AI-generated FastAPI app")

asyncio.run(integrated_development())
```

## Configuration

### Environment Variables

```bash
# OpenAI API
OPENAI_API_KEY=your_openai_key

# GitHub API
GITHUB_TOKEN=your_github_token

# Ollama (local LLM)
OLLAMA_BASE_URL=http://localhost:11434

# HuggingFace API
HUGGINGFACE_API_KEY=your_huggingface_key

# Agent Configuration
AGENT_TIMEOUT_SECONDS=300
AGENT_MAX_CONCURRENT_TASKS=2
AGENT_RETRY_ATTEMPTS=3
```

### Agent Configuration

```python
from agents.core.manager import AgentConfig, AgentRole

# Basic SWE agent
swe_config = AgentConfig(
    role=AgentRole.SWE,
    capabilities=["python", "typescript", "testing"],
    max_concurrent_tasks=2,
    timeout_seconds=300,
    retry_attempts=3
)

# Specialized architect agent
architect_config = AgentConfig(
    role=AgentRole.ARCHITECT,
    capabilities=["system_design", "scalability", "security"],
    max_concurrent_tasks=1,
    timeout_seconds=600,
    retry_attempts=2
)
```

## Error Handling

The agents module implements comprehensive error handling:

### Agent-Level Errors

```python
try:
    result = await agent.process_task(task)
except AgentTimeoutError:
    logger.error("Task timed out")
except AgentValidationError:
    logger.error("Output validation failed")
except AgentExecutionError:
    logger.error("Task execution failed")
```

### Workflow-Level Errors

```python
try:
    result = await coordinator.execute_workflow(workflow)
except WorkflowDependencyError:
    logger.error("Workflow dependency resolution failed")
except WorkflowTimeoutError:
    logger.error("Workflow execution timed out")
except WorkflowExecutionError:
    logger.error("Workflow execution failed")
```

### API-Level Errors

```python
try:
    response = await client.chat_completion(messages, model)
    if not response.success:
        logger.error(f"API call failed: {response.error}")
except APIConnectionError:
    logger.error("Failed to connect to API")
except APIRateLimitError:
    logger.error("API rate limit exceeded")
```

## Testing

### Unit Tests

```python
import pytest
from agents.core.manager import BaseAgent, AgentConfig, AgentRole

class TestAgent(BaseAgent):
    async def process_task(self, task):
        return {"result": "test"}

    def validate_output(self, output):
        return output.get("result") == "test"

@pytest.mark.asyncio
async def test_agent_lifecycle():
    config = AgentConfig(role=AgentRole.SWE, capabilities=["test"])
    agent = TestAgent(config)

    # Test task processing
    result = await agent.process_task({"type": "test"})
    assert result["result"] == "test"

    # Test validation
    assert agent.validate_output(result)
```

### Integration Tests

```python
import pytest
from agents.tools.integration import ToolsIntegration

@pytest.mark.asyncio
async def test_tool_integration():
    tools = ToolsIntegration()

    # Test environment validation
    is_valid = await tools.validate_environment()
    assert is_valid

    # Test command execution
    result = await tools.run_uv_command(["--version"])
    assert result.returncode == 0
```

## Performance Considerations

### Concurrency Management

- **Agent Pooling**: Limit concurrent agents to prevent resource exhaustion
- **Task Queuing**: Queue tasks when agents are busy
- **Timeout Management**: Prevent hanging operations with configurable timeouts

### Memory Optimization

- **Streaming Responses**: Use streaming for large API responses
- **Cleanup**: Properly close connections and clean up resources
- **Caching**: Cache frequently used data and API responses

### Monitoring

```python
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Performance monitoring
start_time = time.time()
result = await agent.process_task(task)
duration = time.time() - start_time

logger.info(f"Task completed in {duration:.2f}s")
```

## Contributing

### Adding New Agents

1. Create new agent class inheriting from `BaseAgent`
2. Implement required methods: `process_task()`, `validate_output()`
3. Add agent to `roles/__init__.py`
4. Update module exports in `__init__.py`

```python
# agents/roles/new_agent.py
from agents.core.manager import BaseAgent, AgentConfig

class NewAgent(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        # Implement task processing
        return {"result": "processed"}

    def validate_output(self, output: Dict[str, Any]) -> bool:
        # Implement validation
        return True
```

### Adding New Tools

1. Add tool integration to `tools/integration.py`
2. Implement async methods with proper error handling
3. Add environment validation
4. Update method documentation

### Adding New API Clients

1. Create client class inheriting from `BaseAPIClient`
2. Implement service-specific methods
3. Add to `APIClientManager` if needed
4. Update convenience functions

## License

This module is part of the bootdisk project and follows the same licensing terms.

## Changelog

### Version 1.0.0
- Initial release with core agent infrastructure
- Workflow coordination system
- Tool integrations (Cargo, UV, DevContainers)
- API clients (OpenAI, Ollama, GitHub, HuggingFace)
- Software Engineer agent implementation
- Comprehensive error handling and logging
- Full type safety and async-first design</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/agents/README.md
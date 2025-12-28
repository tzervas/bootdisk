# Bootdisk Project Directory Structure Specification

## Overview

This document defines the opinionated directory structure for Bootdisk and similar AI-assisted development projects. The structure is optimized for:

- **GitHub Copilot Integration**: Proper placement of instruction files and prompts
- **Agentic Development**: Clear separation of AI agent components and workflows
- **Documentation Management**: Centralized, discoverable documentation
- **DevContainer Optimization**: Streamlined containerized development
- **Maintainability**: Logical organization for long-term project health

## Core Principles

1. **Separation of Concerns**: Each directory has a single, clear responsibility
2. **Copilot Optimization**: Files are placed where Copilot expects them
3. **Agent Modularity**: AI components are reusable and configurable
4. **Documentation First**: Docs are central to the development experience
5. **Tool Integration**: VS Code, GitHub Actions, and DevContainer integration

## Directory Structure

```
bootdisk/
├── .devcontainer/                    # DevContainer configuration
│   ├── devcontainer.json            # Container definition and extensions
│   ├── Dockerfile                   # Container build instructions
│   ├── test-devcontainer.sh         # Environment validation script
│   └── agents/                      # DevContainer-specific agent configs
├── .github/                         # GitHub integration and automation
│   ├── copilot-instructions/        # GitHub Copilot custom instructions
│   │   ├── global.md               # Project-wide context and conventions
│   │   ├── swe.md                  # Software Engineer instructions
│   │   ├── test-engineer.md        # Test Engineer instructions
│   │   ├── project-manager.md      # Project Manager instructions
│   │   ├── qa-evaluator.md         # QA Evaluator instructions
│   │   ├── communicator.md         # Communicator instructions
│   │   ├── devops.md               # DevOps instructions
│   │   ├── security.md             # Security instructions
│   │   └── documentation.md        # Documentation instructions
│   ├── prompts/                     # Dynamic prompt templates
│   │   ├── code-implementation.md
│   │   ├── testing-validation.md
│   │   ├── project-management.md
│   │   ├── quality-assurance.md
│   │   ├── communication.md
│   │   ├── devops.md
│   │   ├── security.md
│   │   └── workflow-coordination.md
│   └── workflows/                   # GitHub Actions CI/CD
│       ├── ci.yml                  # Continuous integration
│       ├── release.yml             # Automated releases
│       └── agent-validation.yml    # Agent workflow validation
├── .vscode/                         # VS Code workspace configuration
│   ├── settings.json               # Workspace settings
│   ├── tasks.json                  # Custom tasks
│   ├── launch.json                 # Debug configurations
│   └── extensions.json             # Recommended extensions
├── agents/                          # AI agent implementations
│   ├── __init__.py                 # Package initialization
│   ├── core/                       # Core agent infrastructure
│   │   ├── manager.py              # Agent orchestration
│   │   ├── workflows.py            # Workflow coordination
│   │   └── prompts.py              # Dynamic prompt loading
│   ├── roles/                      # Specialized agent roles
│   │   ├── swe.py                  # Software Engineer agent
│   │   ├── test_engineer.py        # Test Engineer agent
│   │   ├── project_manager.py      # Project Manager agent
│   │   ├── qa_evaluator.py         # QA Evaluator agent
│   │   ├── communicator.py         # Communicator agent
│   │   ├── devops.py               # DevOps agent
│   │   ├── security.py             # Security agent
│   │   └── documentation.py        # Documentation agent
│   ├── tools/                      # Agent tools and integrations
│   │   ├── integration.py          # External service integration
│   │   ├── devcontainer.py         # DevContainer management
│   │   └── validation.py           # Agent output validation
│   └── config/                     # Agent configuration
│       ├── secrets.md              # Security and secrets management
│       └── settings.yaml           # Agent settings and parameters
├── config/                          # Project configuration
│   ├── bootdisk_schema.yaml        # Main project schema
│   ├── docs-config.yaml            # Documentation configuration
│   └── environment.yaml            # Environment-specific settings
├── docs/                           # Documentation
│   ├── README.md                   # Documentation index
│   ├── getting-started/            # Onboarding documentation
│   │   ├── installation.md         # Installation instructions
│   │   ├── quick-start.md          # Basic usage guide
│   │   └── dev-setup.md            # Development environment setup
│   ├── user-guide/                 # User documentation
│   │   ├── configuration.md        # Configuration options
│   │   ├── customization.md        # Advanced customization
│   │   └── troubleshooting.md      # Common issues and solutions
│   ├── developer/                  # Developer documentation
│   │   ├── architecture.md         # System architecture
│   │   ├── api-reference.md        # API documentation
│   │   └── contributing.md         # Contribution guidelines
│   ├── agents/                     # Agent-specific documentation
│   │   ├── overview.md             # Agent architecture overview
│   │   ├── workflows.md            # Agent coordination workflows
│   │   └── integration.md          # Integrating agents into workflows
│   └── devcontainer/               # DevContainer documentation
│       ├── guide.md                # DevContainer usage guide
│       └── customization.md        # Customizing DevContainer setup
├── scripts/                        # Utility scripts
│   ├── devcontainer-manager.sh     # DevContainer lifecycle management
│   ├── build.sh                    # Build automation
│   ├── test.sh                     # Testing automation
│   └── deploy.sh                   # Deployment scripts
├── src/                            # Source code
│   ├── lib.rs                      # Rust library root
│   ├── main.rs                     # Rust binary entry point
│   ├── schema.rs                   # Configuration schema handling
│   ├── config.rs                   # Configuration management
│   ├── generator.rs                # Bootdisk generation logic
│   └── tests.rs                    # Unit tests
├── tests/                          # Test suites
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── fixtures/                   # Test data and fixtures
├── output/                         # Build artifacts and outputs
│   ├── dist/                       # Distribution packages
│   ├── images/                     # Generated bootdisk images
│   └── logs/                       # Build and runtime logs
├── target/                         # Rust build artifacts
├── pyproject.toml                  # Python project configuration
├── Cargo.toml                      # Rust project configuration
├── bootdisk.code-workspace         # VS Code workspace file
├── README.md                       # Project README
├── LICENSE                         # Project license
└── .gitignore                      # Git ignore patterns
```

## Directory Responsibilities

### .devcontainer/
**Purpose**: Containerized development environment
**Contents**: Docker configuration, validation scripts, VS Code extensions
**Maintenance**: Update when adding new tools or dependencies

### .github/copilot-instructions/
**Purpose**: GitHub Copilot custom instructions
**Contents**: Agent-specific instruction files with `applyTo` headers
**Maintenance**: Update when agent roles or coding standards change

### .github/prompts/
**Purpose**: Dynamic prompt templates for Copilot interactions
**Contents**: Context-aware prompt templates with variable substitution
**Maintenance**: Evolve based on common development patterns

### .github/workflows/
**Purpose**: CI/CD automation and agent workflow validation
**Contents**: GitHub Actions for testing, building, releasing
**Maintenance**: Update with new quality gates or deployment targets

### agents/
**Purpose**: AI agent implementations and orchestration
**Contents**: Modular agent roles, workflow coordination, tool integrations
**Maintenance**: Extend with new agent capabilities or workflow optimizations

### config/
**Purpose**: Project and environment configuration
**Contents**: Schemas, settings, environment-specific configurations
**Maintenance**: Update when adding new features or deployment environments

### docs/
**Purpose**: Comprehensive project documentation
**Contents**: User guides, API docs, development guides, agent documentation
**Maintenance**: Keep synchronized with code changes

### scripts/
**Purpose**: Automation and utility scripts
**Contents**: Build scripts, deployment tools, DevContainer management
**Maintenance**: Update when processes or tooling change

### src/
**Purpose**: Core source code
**Contents**: Rust implementations, Python orchestration, core business logic
**Maintenance**: Follow established patterns and coding standards

### tests/
**Purpose**: Quality assurance and validation
**Contents**: Unit tests, integration tests, test fixtures
**Maintenance**: Maintain high coverage and update with new features

## File Naming Conventions

- **Directories**: lowercase-with-hyphens (e.g., `getting-started`)
- **Files**: lowercase-with-hyphens (e.g., `quick-start.md`)
- **Code files**: snake_case for Python, snake_case for Rust functions/variables
- **Constants**: SCREAMING_SNAKE_CASE
- **Types/Structs**: PascalCase

## Version Control Guidelines

- **Branching**: `feature/`, `bugfix/`, `hotfix/` prefixes
- **Commits**: Conventional commits with type/scope/description
- **Tags**: Semantic versioning (v1.2.3)
- **Releases**: GitHub releases with changelogs

## Tool Integration Points

### VS Code
- `.vscode/settings.json`: Workspace-specific settings
- `.vscode/tasks.json`: Custom development tasks
- `.vscode/launch.json`: Debug configurations
- `bootdisk.code-workspace`: Multi-root workspace definition

### GitHub
- `.github/copilot-instructions/`: Copilot customization
- `.github/prompts/`: Dynamic prompt templates
- `.github/workflows/`: CI/CD pipelines

### DevContainer
- `.devcontainer/devcontainer.json`: Environment definition
- `.devcontainer/Dockerfile`: Container build
- `scripts/devcontainer-manager.sh`: Lifecycle management

## Migration Guide

### From Legacy Structure
1. Move `.github/instructions/*` → `.github/copilot-instructions/`
2. Move `tools/*` → `agents/tools/` or `scripts/`
3. Move config files → `config/`
4. Move docs → `docs/` with proper structure
5. Update all import paths and references

### Validation Checklist
- [ ] Copilot instructions load correctly
- [ ] DevContainer builds and validates
- [ ] All imports resolve correctly
- [ ] Documentation links work
- [ ] Tests pass in new structure
- [ ] Agent workflows function properly

## Extension Points

### Adding New Agent Roles
1. Create `agents/roles/new_agent.py`
2. Add `.github/copilot-instructions/new-agent.md`
3. Update `agents/core/workflows.py`
4. Add to `.github/prompts/`

### Adding New Documentation Sections
1. Create `docs/new-section/`
2. Add to `docs/README.md`
3. Update navigation links
4. Add to CI documentation validation

### Adding New Tools/Integrations
1. Add to `agents/tools/` or `scripts/`
2. Update DevContainer if needed
3. Add documentation
4. Update CI/CD pipelines

This structure provides a solid foundation for AI-assisted development while maintaining clarity, maintainability, and scalability.
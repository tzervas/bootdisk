# Bootdisk Project Structure Mapping

## Opinionated Directory Structure

This document defines the canonical directory structure for the bootdisk project, optimized for GitHub Copilot for VS Code integration, maintainability, and development efficiency.

```
bootdisk/
├── .devcontainer/                    # Dev container configurations
│   ├── devcontainer.json            # Main devcontainer config
│   ├── Dockerfile                   # Custom devcontainer image
│   └── config.json                  # Resource allocation settings
├── .github/
│   ├── copilot-instructions/        # GitHub Copilot role instructions
│   │   ├── global.md               # Global project instructions
│   │   ├── swe.md                  # Software Engineer instructions
│   │   ├── qa.md                   # QA Engineer instructions
│   │   ├── devops.md               # DevOps instructions
│   │   └── README.md               # Instructions overview
│   ├── prompts/                     # Workflow-specific prompts
│   │   ├── code-implementation.md  # Code implementation prompts
│   │   ├── testing-validation.md   # Testing prompts
│   │   ├── documentation.md        # Documentation prompts
│   │   └── README.md               # Prompts overview
│   └── workflows/                   # GitHub Actions CI/CD
│       ├── ci.yml                  # Continuous integration
│       ├── release.yml             # Release automation
│       └── pr-automation.yml       # PR management
├── .vscode/                         # VS Code workspace configuration
│   ├── settings.json               # Workspace settings
│   ├── tasks.json                  # Build/test tasks
│   ├── launch.json                 # Debug configurations
│   └── extensions.json             # Recommended extensions
├── agents/                          # Agentic development components
│   ├── config/                     # Agent configurations
│   │   ├── roles.yaml              # Agent role definitions
│   │   └── workflows.yaml          # Agent workflow configs
│   ├── core/                       # Core agent infrastructure
│   │   ├── manager.py              # Agent orchestration
│   │   ├── workflows.py            # Workflow coordination
│   │   └── __init__.py
│   ├── roles/                      # Specialized agent roles
│   │   ├── swe.py                  # Software Engineer agent
│   │   ├── qa.py                   # QA Engineer agent
│   │   ├── devops.py               # DevOps agent
│   │   └── __init__.py
│   ├── tools/                      # Agent tools and integrations
│   │   ├── integration.py          # Tool integrations
│   │   ├── api.py                  # API clients
│   │   └── __init__.py
│   └── __init__.py
├── config/                          # Project configuration
│   ├── bootdisk_schema.yaml        # Main project schema
│   ├── docs-config.yaml            # Documentation config
│   └── secrets.md                  # Secret management guide
├── docs/                            # Documentation
│   ├── README.md                   # Documentation index
│   ├── getting-started/            # Getting started guides
│   │   ├── installation.md
│   │   ├── quick-start.md
│   │   └── dev-setup.md
│   ├── user-guide/                 # User documentation
│   │   ├── configuration.md
│   │   ├── customization.md
│   │   └── troubleshooting.md
│   ├── developer/                  # Developer documentation
│   │   ├── architecture.md
│   │   ├── api-reference.md
│   │   ├── contributing.md
│   │   └── testing.md
│   ├── agents/                     # Agent documentation
│   │   ├── overview.md
│   │   ├── workflows.md
│   │   └── integration.md
│   └── devcontainer/               # DevContainer docs
│       └── guide.md
├── scripts/                         # Utility scripts
│   ├── devcontainer-manager.sh     # DevContainer management
│   ├── setup.sh                    # Project setup
│   └── validate.sh                 # Validation scripts
├── src/                             # Source code
│   ├── lib.rs                      # Rust library
│   ├── main.rs                     # Rust binary
│   ├── schema.rs                   # Schema definitions
│   └── tests.rs                    # Rust tests
├── tests/                           # Test suites
│   ├── integration/                # Integration tests
│   ├── unit/                       # Unit tests
│   └── fixtures/                   # Test fixtures
├── python/                          # Python components
│   ├── main.py                     # Python entry point
│   ├── agents/                     # Python agent code
│   ├── config/                     # Python configurations
│   └── requirements.txt            # Python dependencies
├── target/                          # Build artifacts (Rust)
├── output/                          # Generated outputs
├── pyproject.toml                   # Python project config
├── uv.lock                          # UV dependency lock
├── Cargo.toml                       # Rust project config
├── Cargo.lock                       # Rust dependency lock
├── README.md                        # Project README
├── LICENSE                          # License file
└── .gitignore                       # Git ignore rules
```

## Directory Purposes

### Development Environment
- **.devcontainer/**: Containerized development environment
- **.vscode/**: VS Code workspace configuration and tasks
- **scripts/**: Development and deployment utilities

### GitHub Integration
- **.github/copilot-instructions/**: AI assistant role definitions
- **.github/prompts/**: Workflow-specific AI prompts
- **.github/workflows/**: CI/CD automation

### Agentic Architecture
- **agents/**: Multi-agent development system components
- **config/**: Configuration files and schemas
- **docs/**: Comprehensive documentation

### Code Organization
- **src/**: Rust source code (performance-critical)
- **python/**: Python components (AI/ML orchestration)
- **tests/**: Test suites and fixtures

### Build & Dependencies
- **target/**: Rust build artifacts
- **output/**: Generated configurations and artifacts
- **pyproject.toml/uv.lock**: Python dependency management
- **Cargo.toml/Cargo.lock**: Rust dependency management

## File Naming Conventions

- **Directories**: lowercase-with-hyphens (e.g., `getting-started`)
- **Files**: lowercase-with-hyphens (e.g., `api-reference.md`)
- **Code files**: snake_case for Python, snake_case for Rust
- **Config files**: kebab-case or CamelCase as appropriate

## GitHub Copilot Integration

### Instructions Hierarchy
1. **global.md**: Project-wide conventions and standards
2. **Role-specific**: Specialized instructions for each agent role
3. **README.md**: Overview and usage guide

### Prompts Organization
- **code-implementation.md**: Code generation and refactoring
- **testing-validation.md**: Test creation and validation
- **documentation.md**: Documentation generation
- **README.md**: Prompt usage guide

## Maintenance Guidelines

### Adding New Components
1. Check if component fits existing directory structure
2. Update this mapping document
3. Ensure GitHub Copilot instructions cover new patterns
4. Add appropriate tests and documentation

### Directory Structure Changes
1. Update this mapping document first
2. Move files systematically
3. Update all references (imports, paths, documentation)
4. Test all functionality after changes
5. Update CI/CD if build paths change

### Agentic Components
- Keep agent logic in `agents/` directory
- Configuration in `config/` directory
- Documentation in `docs/agents/` directory
- Integration tests in `tests/integration/`

This structure ensures optimal GitHub Copilot integration, clear separation of concerns, and maintainable project organization.</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/docs/PROJECT_STRUCTURE.md
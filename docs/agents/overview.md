# Agentic DevContainer Boilerplate

This directory contains a reusable multi-agentic development environment setup that can be extracted as a standalone sister project for any development workflow.

## Overview

A pre-built, optimized devcontainer for secure multi-agentic software development with specialized AI agents, GitHub Copilot integration, and structured workflow coordination.

## Key Features

- **7 Specialized AI Agents**: SWE, Test Engineer, Project Manager, QA Evaluator, Communicator, DevOps, Security
- **GitHub Copilot Integration**: Custom instruction files with `applyTo` targeting
- **Handoff Protocols**: Structured agent-to-agent communication and escalation
- **Dynamic Prompts**: Context-aware prompt templates in `.github/prompts/`
- **Secure Multi-Agentic Workflow**: 5-phase development process with quality gates
- **RAG-Optimized**: Intelligent context management and information flow

## Project Structure

```
.github/
├── agents/
│   ├── cohort-workflow.md      # Main workflow coordination with handoffs
│   ├── README.md               # This file - extraction and usage guide
│   └── SECRETS.md              # Security and secret management
├── instructions/               # Agent-specific instruction files with applyTo headers
│   ├── swe.md                  # Software Engineer
│   ├── test-engineer.md        # Test Engineer
│   ├── project-manager.md      # Project Manager
│   ├── qa-evaluator.md         # QA Evaluator
│   ├── communicator.md         # Communicator
│   ├── devops.md               # DevOps
│   └── security.md             # Security
└── prompts/                    # Dynamic prompt templates
    ├── code-implementation.md
    ├── testing-validation.md
    ├── project-management.md
    ├── quality-assurance.md
    ├── communication.md
    ├── devops.md
    ├── security.md
    └── workflow-coordination.md
```

## Extraction as Sister Project

### Step 1: Copy Structure
```bash
# From any project, copy the agentic setup
cp -r /path/to/bootdisk/.github /path/to/new-project/
```

### Step 2: Update Context
Modify `applyTo` headers in `.github/instructions/*.md` for your project:
```yaml
---
applyTo: 'src/**/*.js,tests/**/*.js,package.json'
---
```

### Step 3: Customize Prompts
Adapt `.github/prompts/*.md` templates for project-specific needs:
- Update technology references
- Modify coding standards
- Adjust workflow requirements

### Step 4: Configure Agents
Update agent roles in instruction files:
- Modify responsibilities for your tech stack
- Update handoffs for your workflow
- Adjust collaboration patterns

### Step 5: DevContainer Integration
Copy and modify `.devcontainer/` configuration:
- Update base image for your tech stack
- Modify installed tools and extensions
- Configure environment variables

## Quick Start

1. **Prerequisites**
   ```bash
   # Install VS Code with Dev Containers extension
   code --install-extension ms-vscode-remote.remote-containers
   ```

2. **Launch Environment**
   ```bash
   git clone <your-repo>
   cd your-project
   code .
   # Use "Dev Containers: Reopen in Container" command
   ```

3. **Configure Secrets**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start Development**
   ```bash
   # Agents auto-initialize via Copilot instructions
   # Use GitHub Copilot with enhanced context
   ```

## Agent Roles & Handoffs

### Core Development Agents
- **SWE**: Code implementation with handoffs to Test Engineer and Security
- **Test Engineer**: Validation with handoffs to QA Evaluator and DevOps
- **Project Manager**: Coordination with handoffs to all agents for updates

### Quality & Security Agents
- **QA Evaluator**: Quality gates with handoffs to Project Manager
- **Security**: Security reviews with handoffs to SWE and DevOps
- **DevOps**: Infrastructure with handoffs to QA and Project Manager

### Communication & Documentation Agents
- **Communicator**: Context management with handoffs to all agents for information
- **Documentation**: Technical writing with handoffs to DocSnap, DocuGen, APIDocGen, DocSite

## Sister Projects

The Documentation Agent integrates with specialized sister projects for comprehensive documentation automation:

### DocSnap - Screenshot Automation
**Location**: `~/Documents/projects/docsnap/`
- Automated screenshot generation for visual documentation
- Supports web apps, terminals, configuration files
- CI/CD integration for automated visual content

### DocuGen - Documentation Generation
**Location**: `~/Documents/projects/docugen/`
- General documentation generation from code and configs
- Template-based documentation creation
- Multi-format output (Markdown, HTML, PDF)

### APIDocGen - API Documentation
**Location**: `~/Documents/projects/apidocgen/`
- Specialized API documentation generator
- Interactive API testing interfaces
- Multi-language framework support

### DocSite - Documentation Sites
**Location**: `~/Documents/projects/docsite/`
- Automated documentation website generation
- Multiple framework support (MkDocs, Sphinx, Docusaurus)
- Automated deployment to GitHub Pages, Netlify, Vercel

## Workflow Process

### 5-Phase Development Cycle
1. **Task Intake & Planning**: Communicator + Project Manager
2. **Individual Agent Work**: Specialized agent execution
3. **Cohort Collaboration**: Complex task coordination
4. **Review & Approval**: Quality gates and security review
5. **Deployment & Monitoring**: DevOps execution and monitoring

### Handoff Triggers
- **Completion**: Task finished per acceptance criteria
- **Blockers**: Issues requiring other agent expertise
- **Quality Gates**: Mandatory reviews before proceeding
- **Milestones**: Scheduled checkpoints and deliverables

## Security Features

- **Container Isolation**: Host protection with secure execution
- **Secret Management**: Environment-based credential injection
- **Access Controls**: Role-based agent permissions
- **Audit Trails**: Comprehensive logging of agent actions
- **Compliance**: Built-in security and compliance checks

## Performance Optimization

- **Context Targeting**: `applyTo` headers prevent context overload
- **Caching**: Result caching for repeated operations
- **Async Processing**: Concurrent agent operations
- **Resource Monitoring**: Performance tracking and optimization

## Customization Examples

### Adding New Agents
1. Create `.github/instructions/new-agent.md`
2. Add `applyTo` header with file patterns
3. Define role, handoffs, and prompts
4. Update `cohort-workflow.md`

### Technology Stack Updates
1. Modify instruction files for new languages
2. Update prompt templates with tech-specific guidance
3. Adjust devcontainer for new tools
4. Test agent integration

## Troubleshooting

### Common Issues
- **Agent Context Missing**: Check `applyTo` patterns match file types
- **Copilot Not Responding**: Verify VS Code extension and API keys
- **Container Build Failures**: Check devcontainer configuration

### Logs & Debugging
```bash
# View container logs
docker logs <container_id>

# Check agent file targeting
grep "applyTo" .github/instructions/*.md
```

## Contributing

1. Follow cohort workflow for all changes
2. Use appropriate agent for task type
3. Ensure security review by Security agent
4. Update documentation for modifications

## License

MIT License - Extract and modify freely for your projects.
### Specialist Agents
- **DevOps**: Container and infrastructure management
- **Security**: Security assessment and implementation

## Security

- **Host Protection**: All development isolated in container
- **Secret Management**: Secure injection via .env files
- **Access Controls**: Role-based agent permissions
- **Audit Trails**: All agent actions logged

## Customization

### Adding New Agents
1. Create `.github/copilot-instructions/[agent].md`
2. Define role, responsibilities, and prompts
3. Update workflow.md for integration

### Environment Variables
```bash
# Required (optional for basic functionality)
OPENAI_API_KEY=your_key
HUGGINGFACE_TOKEN=your_token

# Optional
OLLAMA_BASE_URL=http://localhost:11434
DEBUG=true
```

## Workflow

The cohort follows a structured 5-phase process:
1. Task intake and planning
2. Individual agent work
3. Cohort collaboration (complex tasks)
4. Review and approval
5. Deployment and monitoring

See `workflow.md` for detailed process documentation.

## Performance

- **CPU-Optimized**: Lightweight models for coding tasks
- **Memory Efficient**: Rust-based with minimal Python footprint
- **Fast Startup**: Pre-built container with cached dependencies
- **Scalable**: Horizontal agent scaling support

## Troubleshooting

### Common Issues
- **Agent not responding**: Check Ollama service status
- **Copilot not working**: Verify VS Code extensions
- **Container slow**: Ensure adequate host resources

### Logs
```bash
# View agent logs
docker logs <container_id>

# Ollama service status
curl http://localhost:11434/api/tags
```

## Contributing

1. Follow the cohort workflow for all changes
2. Use appropriate agent for task type
3. Ensure security review by Security agent
4. Update documentation for new features

## License

MIT License - See LICENSE file for details.
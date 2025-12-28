---
applyTo: '**/*.{rs,py,toml,json,yaml,md,sh}'
---
# Global Bootdisk Project Instructions

## Project Overview
Bootdisk is a hybrid Rust/Python tool for generating customized Debian workstation configurations with GPU serving capabilities and PXE boot support. It features multi-agent AI-powered configuration generation and secure containerized development environments.

## Core Architecture
- **Rust Components**: High-performance system utilities, memory-safe implementations in `src/`
- **Python Components**: AI/ML orchestration, agent workflows, configuration management
- **Hybrid Integration**: Python-Rust FFI for optimal performance and safety
- **Multi-Agent System**: 7 specialized AI agents for collaborative development

## Key Conventions

### Code Style
- **Rust**: Follow `clippy` recommendations, use `Result<T, E>` for error handling, prefer `&str` over `String` for read-only strings
- **Python**: Follow PEP 8, use type hints, prefer dataclasses over dicts for structured data
- **Naming**: Use snake_case for variables/functions, PascalCase for types/structs, SCREAMING_SNAKE_CASE for constants

### Security First
- Never hardcode secrets or credentials
- Use environment variables for configuration
- Implement input validation and sanitization
- Follow principle of least privilege
- Log security events appropriately

### Error Handling
- Rust: Use `Result<T, E>` and `Option<T>` types, avoid `unwrap()` in production code
- Python: Use custom exception classes, provide meaningful error messages
- Always handle errors gracefully, don't let them crash the system

### Configuration Management
- Use YAML for human-editable configuration files
- Validate configuration schemas at startup
- Provide sensible defaults
- Support environment variable overrides

### Testing Strategy
- Unit tests for all public functions
- Integration tests for component interactions
- Property-based testing where applicable
- Mock external dependencies
- Aim for 70%+ code coverage

### Documentation Standards
- All public APIs must have docstrings/doc comments
- Include usage examples in documentation
- Document security considerations
- Keep README and docs synchronized

## Development Workflow
1. **Planning**: Project Manager agent coordinates task breakdown
2. **Implementation**: SWE agent writes code following security and performance guidelines
3. **Testing**: Test Engineer validates functionality and coverage
4. **Security Review**: Security agent checks for vulnerabilities
5. **Quality Gate**: QA Evaluator ensures standards are met
6. **Documentation**: Documentation agent updates guides and API docs

## File Organization
- `src/`: Rust source code and modules
- `agents/`: Python agent implementations and workflows
- `docs/`: Documentation and guides
- `config/`: Configuration files and schemas
- `scripts/`: Build and utility scripts
- `.github/copilot-instructions/`: AI agent instructions for Copilot
- `.github/prompts/`: Dynamic prompt templates
- `.devcontainer/`: Containerized development environment

## Performance Considerations
- Rust components handle performance-critical operations
- Python orchestrates high-level logic and AI workflows
- Minimize allocations and copies in hot paths
- Use async/await for I/O-bound operations
- Profile and optimize bottlenecks

## AI/ML Integration
- Use LangChain for agent orchestration
- Ollama for local LLM serving
- PyTorch for ML workloads
- Validate AI-generated code for security and correctness
- Cache expensive computations appropriately

Remember: This is a security-critical system for generating bootable workstation images. Always prioritize correctness, security, and performance over convenience.
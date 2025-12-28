# Code Implementation Prompt

## Purpose
Guide the Software Engineer agent in implementing new features and functionality with focus on Rust memory safety and Python best practices.

## Context
- **Apply to**: `src/**/*.rs`, `src/**/*.py`, `tests/**/*.rs`, `tests/**/*.py`
- **When to use**: New feature development, code refactoring, API integration

## Template
```
Implement [FEATURE/FUNCTION] in [LANGUAGE] following these requirements:

**Functional Requirements:**
- [List specific functionality needed]
- [Input/output specifications]
- [Error handling requirements]

**Technical Requirements:**
- [Performance constraints]
- [Memory safety requirements (Rust)]
- [Security considerations]
- [Integration points]

**Quality Standards:**
- [Test coverage minimum]
- [Documentation requirements]
- [Code style guidelines]

**Implementation Steps:**
1. [Step-by-step approach]
2. [Testing strategy]
3. [Validation criteria]

**Deliverables:**
- [Source code]
- [Unit tests]
- [Documentation]
- [Integration examples]
```

## Examples

### Rust Function Implementation
```
Implement a secure file parsing function in Rust following these requirements:

**Functional Requirements:**
- Parse YAML configuration files
- Validate schema compliance
- Return structured data or detailed errors

**Technical Requirements:**
- Zero-copy parsing where possible
- Memory-safe error handling
- No panics in production code

**Quality Standards:**
- 90% test coverage
- Comprehensive documentation
- Clippy clean code

**Implementation Steps:**
1. Define error types with thiserror
2. Implement parser with serde_yaml
3. Add validation logic
4. Write comprehensive tests
5. Add documentation and examples
```

### Python AI Integration
```
Implement LangChain agent integration in Python following these requirements:

**Functional Requirements:**
- Connect to Ollama models
- Handle secure credential management
- Provide agent coordination interface

**Technical Requirements:**
- Async/await for concurrent operations
- Proper error handling and logging
- Secure API key management via environment

**Quality Standards:**
- Type hints throughout
- PEP 8 compliance
- Comprehensive error handling
```

## Success Criteria
- Code compiles without warnings
- All tests pass (unit + integration)
- Security review passed
- Documentation complete
- Performance benchmarks met
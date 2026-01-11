# GitHub Copilot Prompts

This directory contains workflow-specific prompts to guide GitHub Copilot in generating high-quality code and documentation for specific development tasks.

## Available Prompts

- **code-implementation.md** - Code generation and implementation guidance
- **testing-validation.md** - Test creation and validation strategies
- **documentation.md** - Technical documentation generation
- **communication.md** - Communication and collaboration guidance
- **devops.md** - Infrastructure and deployment automation
- **security.md** - Security analysis and implementation
- **project-management.md** - Project planning and coordination

## Usage

These prompts are designed to be used with GitHub Copilot Chat or as context for code generation. Each prompt includes:

- **Purpose**: What the prompt is designed to accomplish
- **Context**: When and where to apply the prompt
- **Template**: Structured format for consistent results
- **Examples**: Concrete usage examples

## Prompt Structure

Each prompt file follows a consistent structure:

```markdown
# [Prompt Name]

## Purpose
[Clear description of what this prompt achieves]

## Context
- **Apply to**: [File patterns or contexts]
- **When to use**: [Specific scenarios]

## Template
[Structured prompt template with placeholders]

## Examples
[Concrete examples of usage]
```

## Best Practices

1. **Be Specific**: Include concrete requirements and constraints
2. **Provide Context**: Reference existing code patterns and architecture
3. **Define Scope**: Clearly state what's in and out of scope
4. **Include Examples**: Show expected input/output formats
5. **Test Iteratively**: Refine prompts based on results

## Integration with Instructions

These prompts work alongside the role-specific instructions in `copilot-instructions/` to provide comprehensive AI assistance across the development lifecycle.</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/.github/prompts/README.md
# GitHub Copilot Instructions

This directory contains role-specific instructions for GitHub Copilot to provide context-aware assistance for the bootdisk project.

## Instruction Hierarchy

1. **global.md** - Project-wide conventions, architecture, and standards
2. **Role-specific files** - Specialized instructions for each development role
3. **README.md** - This overview and usage guide

## Available Roles

- **swe.md** - Software Engineer: Code implementation and refactoring
- **qa.md** - QA Engineer: Testing and validation
- **devops.md** - DevOps Engineer: Infrastructure and deployment
- **security.md** - Security Engineer: Security analysis and hardening
- **documentation.md** - Documentation Specialist: Technical writing
- **project-manager.md** - Project Manager: Planning and coordination

## Usage

GitHub Copilot automatically applies these instructions based on:
- File types and paths
- Code context and patterns
- Development workflow stage

## Customization

To add new role instructions:
1. Create a new `.md` file with the role name
2. Follow the established format with frontmatter and sections
3. Update this README
4. Test the instructions in relevant contexts

## File Format

Each instruction file should include:
- Frontmatter with `applyTo` patterns
- Clear role definition and scope
- Code style and conventions
- Best practices and patterns
- Examples and anti-patterns</content>
<parameter name="filePath">/home/spooky/Documents/projects/bootdisk/.github/copilot-instructions/README.md
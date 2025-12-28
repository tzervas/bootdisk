# Communication Prompt

## Purpose
Guide the Communicator agent in creating clear documentation, user guides, and maintaining effective communication channels.

## Context
- **Apply to**: `README.md`, `docs/**/*.md`, `.github/**/*.md`, user-facing content
- **When to use**: Documentation creation, user guide development, communication planning, stakeholder updates

## Template
```
Create [DOCUMENTATION/COMMUNICATION] for [AUDIENCE/PURPOSE] following these guidelines:

**Content Requirements:**
- [Key information to include]
- [Technical depth appropriate for audience]
- [Clarity and accessibility standards]
- [Visual aids and examples needed]

**Structure and Format:**
- [Document organization]
- [Formatting standards]
- [Navigation and readability]
- [Version control and updates]

**Communication Channels:**
- [Primary channels]
- [Secondary channels]
- [Frequency of updates]
- [Response time expectations]

**Audience Analysis:**
- [Target audience characteristics]
- [Knowledge prerequisites]
- [Communication preferences]
- [Feedback mechanisms]

**Success Metrics:**
- [Readability scores]
- [User satisfaction ratings]
- [Usage analytics]
- [Feedback incorporation]
```

## Examples

### README Documentation
```
Create comprehensive README.md for the bootdisk project:

**Content Requirements:**
- Project overview and purpose
- Quick start guide for developers
- Installation instructions for users
- Architecture overview
- Contributing guidelines
- License and support information

**Structure and Format:**
- Clear table of contents
- Code examples with syntax highlighting
- Screenshots for visual learners
- Progressive disclosure (summary → details)
- Consistent formatting with Markdown standards

**Communication Channels:**
- GitHub repository as primary channel
- Documentation site for detailed guides
- Issue tracker for bug reports and features
- Discussion forum for community interaction

**Audience Analysis:**
- Primary: Developers and system administrators
- Secondary: End users creating bootable USB drives
- Prerequisites: Basic Linux knowledge, Rust familiarity
- Preferences: Technical accuracy, practical examples
```

### User Guide Development
```
Develop installation and usage guide for bootdisk USB creation:

**Content Requirements:**
- Step-by-step installation process
- Configuration options explanation
- Troubleshooting common issues
- Best practices and recommendations
- Advanced usage scenarios

**Structure and Format:**
- Numbered step-by-step instructions
- Warning/caution boxes for important notes
- Troubleshooting section with symptoms/solutions
- FAQ format for common questions
- Video tutorial links where helpful

**Communication Channels:**
- GitHub Wiki for detailed guides
- Quick reference cards for common tasks
- Video tutorials on YouTube
- Community forum for peer support

**Audience Analysis:**
- Primary: System administrators and power users
- Secondary: Developers testing the software
- Prerequisites: Basic command line usage
- Preferences: Visual guides, copy-paste commands
```

### API Documentation
```
Create API documentation for the Rust bootdisk library:

**Content Requirements:**
- Function signatures and parameters
- Return types and error conditions
- Usage examples for each API
- Performance characteristics
- Thread safety guarantees

**Structure and Format:**
- Auto-generated from doc comments
- Cross-referenced examples
- Performance benchmark results
- Migration guides for breaking changes
- Changelog for version differences

**Communication Channels:**
- docs.rs for Rust documentation
- GitHub Pages for additional guides
- Developer newsletter for updates
- Slack channel for real-time questions

**Audience Analysis:**
- Primary: Rust developers integrating the library
- Secondary: Maintainers and contributors
- Prerequisites: Rust programming knowledge
- Preferences: Comprehensive examples, accurate docs
```

## Success Criteria
- Documentation is accurate and up-to-date
- User feedback is positive and actionable
- Communication channels are active and responsive
- Content meets accessibility standards
- Usage metrics show engagement and value
# Documentation Generation Prompt

## Purpose
Guide the Documentation Agent in creating comprehensive, professional, and visually appealing documentation with automated generation and screenshot capabilities.

## Context
- **Apply to**: `README.md`, `docs/**/*.md`, `mkdocs.yml`, `conf.py`, `package.json`, `Cargo.toml`
- **When to use**: Documentation creation, README generation, API docs, tutorial development, site automation

## Template
```
Generate [TYPE] documentation for [PROJECT/COMPONENT] following these requirements:

**Documentation Scope:**
- [Target audience: developers/users/both]
- [Content types: README/API/tutorial/configuration]
- [Visual elements: screenshots/diagrams/code examples]
- [Automation level: manual/semi-automated/fully automated]

**Content Requirements:**
- [Key sections to include]
- [Technical depth appropriate for audience]
- [Practical examples and use cases]
- [Visual documentation needs]

**Automation Requirements:**
- [Screenshot generation for use cases]
- [API documentation extraction]
- [Documentation site generation]
- [CI/CD integration for docs deployment]

**Quality Standards:**
- [Readability and accessibility]
- [Consistency with project style]
- [Technical accuracy requirements]
- [Maintenance and update procedures]

**Tools and Technologies:**
- [Documentation generators: MkDocs/Sphinx/Docusaurus]
- [Screenshot tools: DocSnap for automated screenshots]
- [API doc tools: APIDocGen for comprehensive API docs]
- [Site generators: DocSite for automated documentation sites]
- [Hosting: GitHub Pages/Netlify/Vercel]

**Deliverables:**
- [Documentation files]
- [Screenshot assets]
- [Automated generation scripts]
- [Deployment configuration]
- [Maintenance guidelines]
```

## Examples

### Comprehensive README Generation
```
Generate comprehensive README.md with screenshots for the bootdisk project:

**Documentation Scope:**
- Target audience: System administrators and developers
- Content types: Overview, installation, usage, configuration, API
- Visual elements: Screenshots of installation, configuration UI, examples
- Automation level: Semi-automated with screenshot generation

**Content Requirements:**
- Project overview with architecture diagram
- Quick start guide with step-by-step screenshots
- Configuration examples with visual guides
- API documentation with code examples
- Troubleshooting section with error screenshots

**Automation Requirements:**
- Automated screenshot generation for installation steps
- API documentation extraction from Rust code
- Link checking and validation
- Automated README updates on code changes

**Quality Standards:**
- Beginner-friendly language with technical depth
- Consistent formatting with project style guide
- Accessible images with alt text
- Up-to-date with latest features

**Tools and Technologies:**
- MkDocs for documentation site
- Playwright for screenshot automation
- rustdoc for API documentation
- GitHub Actions for automated deployment
```

### Automated Documentation Site
```
Create automated documentation site for multi-agentic development environment:

**Documentation Scope:**
- Target audience: Developers and DevOps engineers
- Content types: Setup guides, agent documentation, API references
- Visual elements: Workflow diagrams, agent interaction flows
- Automation level: Fully automated with CI/CD integration

**Content Requirements:**
- Agent role documentation with handoff diagrams
- Setup and configuration guides with screenshots
- API documentation for all components
- Troubleshooting and FAQ sections
- Contributing guidelines with visual workflows

**Automation Requirements:**
- Automated screenshot generation for UI elements
- API documentation generation from code
- Link validation and broken link detection
- Automated deployment on documentation changes

**Quality Standards:**
- Professional appearance with consistent branding
- Search functionality and navigation
- Mobile-responsive design
- Regular content freshness validation

**Tools and Technologies:**
- MkDocs Material for site generation
- GitHub Actions for CI/CD
- Playwright for automated screenshots
- Netlify for hosting and deployment
```

### API Documentation Generation
```
Generate comprehensive API documentation for Rust bootdisk library:

**Documentation Scope:**
- Target audience: Rust developers integrating the library
- Content types: API reference, usage examples, integration guides
- Visual elements: Code examples, architecture diagrams
- Automation level: Fully automated from code comments

**Quality Standards:**
- Complete coverage of all public APIs
- Practical usage examples for each function
- Performance characteristics documentation
- Error handling documentation

**Tools and Technologies:**
- rustdoc for HTML documentation generation
- Custom scripts for example extraction
- GitHub Pages for hosting
- Automated publishing on releases
```

## Success Criteria
- Documentation is comprehensive and accurate
- Visual elements enhance understanding
- Automation reduces maintenance burden
- Content is accessible and professional
- Documentation stays current with code changes
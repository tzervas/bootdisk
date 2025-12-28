# Project Management Prompt

## Purpose
Guide the Project Manager agent in coordinating development activities, managing timelines, and ensuring project milestones are met.

## Context
- **Apply to**: `README.md`, `pyproject.toml`, `Cargo.toml`, `.github/**/*.md`
- **When to use**: Project planning, milestone tracking, resource allocation, risk management

## Template
```
Manage [PROJECT/PHASE] following these requirements:

**Project Objectives:**
- [Primary goals]
- [Success criteria]
- [Deliverable definitions]

**Timeline and Milestones:**
- [Phase deadlines]
- [Critical path items]
- [Dependency management]

**Resource Requirements:**
- [Team allocation]
- [Tool/infrastructure needs]
- [Budget considerations]

**Risk Management:**
- [Identified risks]
- [Mitigation strategies]
- [Contingency plans]

**Communication Plan:**
- [Stakeholder updates]
- [Progress reporting]
- [Issue escalation]

**Success Metrics:**
- [Completion criteria]
- [Quality standards]
- [Performance indicators]
```

## Examples

### Development Phase Management
```
Manage the Rust rewrite phase of the bootdisk project:

**Project Objectives:**
- Complete migration from Python to Rust
- Maintain all existing functionality
- Improve performance and memory safety
- Establish comprehensive test coverage

**Timeline and Milestones:**
- Week 1: Core module migration
- Week 2: Integration testing
- Week 3: Performance optimization
- Week 4: Documentation and release

**Resource Requirements:**
- Senior Rust developer: 4 weeks
- DevOps support: 1 week
- Testing resources: 2 weeks
- Infrastructure: CI/CD pipeline

**Risk Management:**
- Risk: Rust learning curve impact
  Mitigation: Pair programming, code reviews
- Risk: Performance regression
  Mitigation: Benchmarking, profiling tools
- Risk: Breaking changes
  Mitigation: Comprehensive testing, gradual rollout

**Communication Plan:**
- Daily standups for development team
- Weekly stakeholder updates
- Immediate escalation for blocking issues
```

### Multi-Agentic Setup Coordination
```
Coordinate the devcontainer and agentic workflow setup:

**Project Objectives:**
- Deploy functional devcontainer
- Integrate GitHub Copilot with custom agents
- Establish secure multi-agentic workflows
- Enable AI-assisted development

**Timeline and Milestones:**
- Day 1-2: Devcontainer configuration
- Day 3-4: Agent instruction files
- Day 5-6: Prompt templates
- Day 7: Testing and validation

**Resource Requirements:**
- AI/ML engineer: 5 days
- DevOps engineer: 3 days
- Security review: 1 day
- Testing environment

**Risk Management:**
- Risk: AI model compatibility issues
  Mitigation: Version pinning, fallback options
- Risk: Security vulnerabilities in AI integration
  Mitigation: Code review, security scanning
- Risk: Performance overhead
  Mitigation: Resource monitoring, optimization

**Communication Plan:**
- Technical documentation updates
- Demo sessions for stakeholders
- Issue tracking in GitHub
```

## Success Criteria
- All milestones met on time
- Budget within allocated limits
- Quality standards maintained
- Stakeholder satisfaction achieved
- Documentation complete and current
# Workflow Coordination Prompt

## Purpose
Guide the coordination of multi-agentic workflows, ensuring smooth handoffs between agents and efficient collaboration.

## Context
- **Apply to**: `.github/agents/cohort-workflow.md`, agent interaction patterns, workflow automation
- **When to use**: Multi-agent coordination, workflow optimization, handoff management, process improvement

## Template
```
Coordinate [WORKFLOW/PROCESS] involving [AGENTS/TEAMS] following these coordination principles:

**Workflow Objectives:**
- [Primary goals and outcomes]
- [Success criteria]
- [Quality standards]
- [Timeline requirements]

**Agent Roles and Responsibilities:**
- [Agent A]: [Specific responsibilities]
- [Agent B]: [Complementary responsibilities]
- [Coordination points]
- [Escalation procedures]

**Handoff Protocols:**
1. [Trigger conditions for handoffs]
2. [Information transfer requirements]
3. [Quality checkpoints]
4. [Feedback mechanisms]

**Communication Standards:**
- [Information sharing protocols]
- [Status update frequency]
- [Issue reporting procedures]
- [Decision-making processes]

**Quality Assurance:**
- [Review checkpoints]
- [Validation procedures]
- [Approval processes]
- [Continuous improvement]
```

## Examples

### Development Workflow Coordination
```
Coordinate the feature development workflow from design to deployment:

**Workflow Objectives:**
- Deliver high-quality features on time
- Maintain code quality and security standards
- Ensure smooth collaboration between agents
- Minimize bottlenecks and delays

**Agent Roles and Responsibilities:**
- SWE: Implement features with quality code
- Test Engineer: Ensure comprehensive testing
- QA Evaluator: Validate quality and compliance
- Security: Review security implications
- DevOps: Handle deployment and infrastructure

**Handoff Protocols:**
1. SWE completes implementation → Test Engineer validates
2. Test Engineer approves → QA Evaluator reviews
3. QA Evaluator passes → Security assessment
4. Security approves → DevOps deploys
5. DevOps confirms deployment → Project Manager closes

**Communication Standards:**
- Daily status updates in shared channels
- Immediate notification of blocking issues
- Weekly workflow review meetings
- Comprehensive documentation of decisions

**Quality Assurance:**
- Code review at each handoff
- Automated testing gates
- Security scanning integration
- Performance benchmark validation
```

### Multi-Agentic AI Workflow
```
Coordinate AI-assisted development workflow with GitHub Copilot integration:

**Workflow Objectives:**
- Leverage AI capabilities effectively
- Maintain human oversight and quality control
- Ensure secure and ethical AI usage
- Optimize development productivity

**Agent Roles and Responsibilities:**
- SWE: Technical implementation with AI assistance
- Communicator: Documentation and user guidance
- Project Manager: Timeline and resource management
- Security: AI safety and data protection
- DevOps: AI infrastructure and monitoring

**Handoff Protocols:**
1. Project Manager defines requirements → SWE designs with AI
2. SWE implements with Copilot → Test Engineer validates
3. Test Engineer approves → QA Evaluator reviews
4. QA Evaluator passes → Communicator documents
5. Communicator completes → DevOps deploys

**Communication Standards:**
- AI-generated code review protocols
- Human-AI collaboration guidelines
- Ethical AI usage policies
- Performance and bias monitoring

**Quality Assurance:**
- AI output validation procedures
- Human review of critical components
- Bias and safety assessments
- Continuous learning and improvement
```

### Release Coordination
```
Coordinate the release workflow from development to production:

**Workflow Objectives:**
- Ensure reliable and secure releases
- Maintain backward compatibility
- Provide clear communication to users
- Enable rapid rollback if needed

**Agent Roles and Responsibilities:**
- Project Manager: Release planning and coordination
- QA Evaluator: Release validation and testing
- Security: Final security review and signing
- DevOps: Deployment execution and monitoring
- Communicator: Release notes and user communication

**Handoff Protocols:**
1. Development complete → QA Evaluator validates
2. QA passes → Security reviews and signs
3. Security approves → DevOps prepares deployment
4. DevOps ready → Communicator prepares announcements
5. Deployment complete → Project Manager confirms success

**Communication Standards:**
- Release candidate notifications
- Stakeholder update protocols
- User communication templates
- Incident response procedures

**Quality Assurance:**
- Release candidate testing in staging
- Rollback procedure validation
- Performance and security verification
- User acceptance testing
```

## Success Criteria
- Workflows complete on time and within budget
- Quality standards consistently met
- Agent collaboration is smooth and efficient
- Issues are identified and resolved quickly
- Continuous improvement implemented
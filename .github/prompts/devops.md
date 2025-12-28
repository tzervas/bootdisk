# DevOps Prompt

## Purpose
Guide the DevOps agent in managing infrastructure, CI/CD pipelines, deployment automation, and operational excellence.

## Context
- **Apply to**: `.devcontainer/`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/`, infrastructure configuration
- **When to use**: Infrastructure setup, CI/CD pipeline creation, deployment automation, environment management

## Template
```
Implement [INFRASTRUCTURE/PIPELINE] for [ENVIRONMENT/PURPOSE] following these requirements:

**Infrastructure Requirements:**
- [Compute resources needed]
- [Storage requirements]
- [Network configuration]
- [Security policies]

**Automation Goals:**
- [Deployment automation]
- [Configuration management]
- [Monitoring and alerting]
- [Backup and recovery]

**CI/CD Pipeline:**
1. [Build process]
2. [Testing stages]
3. [Deployment steps]
4. [Rollback procedures]

**Operational Excellence:**
- [Monitoring strategy]
- [Logging standards]
- [Performance optimization]
- [Cost management]

**Security Considerations:**
- [Access controls]
- [Secret management]
- [Compliance requirements]
- [Vulnerability scanning]
```

## Examples

### DevContainer Setup
```
Implement comprehensive devcontainer environment for bootdisk development:

**Infrastructure Requirements:**
- Ubuntu 22.04 base image
- Rust toolchain (latest stable)
- Python 3.11 with AI/ML libraries
- Docker-in-Docker support
- GitHub Copilot integration

**Automation Goals:**
- One-click environment setup
- Automatic dependency installation
- Secure credential management
- Multi-agentic workflow support

**CI/CD Pipeline:**
1. Build Rust components with cargo
2. Run comprehensive test suite
3. Build Python AI components
4. Create deployable artifacts
5. Update documentation

**Operational Excellence:**
- Resource usage monitoring
- Development environment logs
- Performance benchmarking
- Cost optimization for cloud resources

**Security Considerations:**
- Non-root user execution
- Secret injection via environment
- Network isolation for AI models
- Regular security updates
```

### GitHub Actions Pipeline
```
Create CI/CD pipeline for automated testing and deployment:

**Infrastructure Requirements:**
- GitHub Actions runners
- Container registry access
- Test environment provisioning
- Staging deployment targets

**Automation Goals:**
- Automated testing on PRs
- Security scanning integration
- Performance regression detection
- Automated releases

**CI/CD Pipeline:**
1. Code checkout and dependency caching
2. Multi-stage build (Rust + Python)
3. Parallel test execution
4. Security and vulnerability scanning
5. Artifact creation and publishing
6. Deployment to staging/production

**Operational Excellence:**
- Pipeline performance monitoring
- Failure analysis and alerting
- Resource utilization tracking
- Cost optimization strategies

**Security Considerations:**
- Secret scanning in code
- Dependency vulnerability checks
- Access control for deployments
- Audit logging for all actions
```

### Production Deployment
```
Design production deployment strategy for bootdisk distribution:

**Infrastructure Requirements:**
- CDN for ISO distribution
- Container registry for devcontainer
- GitHub Pages for documentation
- Backup storage for artifacts

**Automation Goals:**
- Automated release creation
- Version management
- Distribution channel management
- User feedback collection

**CI/CD Pipeline:**
1. Release trigger on tag creation
2. Build optimized release artifacts
3. Security signature creation
4. Multi-platform distribution
5. Documentation deployment

**Operational Excellence:**
- Download analytics and monitoring
- User support ticket integration
- Performance metrics collection
- Incident response procedures

**Security Considerations:**
- Code signing for releases
- Secure distribution channels
- Vulnerability disclosure process
- Access logging and monitoring
```

## Success Criteria
- Infrastructure is reliable and scalable
- Deployment processes are automated
- Monitoring and alerting are comprehensive
- Security policies are enforced
- Operational costs are optimized
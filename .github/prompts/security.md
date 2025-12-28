# Security Prompt

## Purpose
Guide the Security agent in implementing security best practices, conducting security assessments, and ensuring compliance.

## Context
- **Apply to**: All source code, configuration files, deployment artifacts, security policies
- **When to use**: Security review, vulnerability assessment, secure coding practices, compliance auditing

## Template
```
Conduct security assessment and implementation for [COMPONENT/SYSTEM] following these requirements:

**Security Domains:**
- [Authentication and authorization]
- [Data protection and encryption]
- [Network security]
- [Application security]
- [Operational security]

**Threat Modeling:**
- [Asset identification]
- [Threat identification]
- [Vulnerability assessment]
- [Risk analysis and prioritization]

**Security Controls:**
1. [Preventive measures]
2. [Detective measures]
3. [Corrective measures]
4. [Recovery procedures]

**Compliance Requirements:**
- [Regulatory standards]
- [Industry best practices]
- [Organizational policies]
- [Audit requirements]

**Monitoring and Response:**
- [Security monitoring]
- [Incident response]
- [Forensic capabilities]
- [Continuous improvement]
```

## Examples

### Code Security Review
```
Conduct comprehensive security review for the Rust bootdisk generator:

**Security Domains:**
- Memory safety: Eliminate all unsafe code
- Input validation: Sanitize all user inputs
- Cryptographic operations: Use audited libraries
- File system security: Secure temporary files
- Network security: Safe HTTPS implementation

**Threat Modeling:**
- Assets: Configuration files, generated ISOs
- Threats: Malicious configuration, code injection
- Vulnerabilities: Buffer overflows, race conditions
- Risks: Data corruption, system compromise

**Security Controls:**
1. Input sanitization and validation
2. Memory-safe programming practices
3. Secure random number generation
4. Proper error handling without information leakage
5. Secure defaults and fail-safe behavior

**Compliance Requirements:**
- OWASP security principles
- Rust security best practices
- ISO 27001 information security standards
- GDPR data protection principles

**Monitoring and Response:**
- Static analysis security scanning
- Runtime security monitoring
- Incident response procedures
- Security patch management
```

### DevContainer Security
```
Implement security controls for the multi-agentic devcontainer:

**Security Domains:**
- Container security: Minimal attack surface
- AI model security: Safe model execution
- Credential management: Secure secret handling
- Network isolation: Controlled external access
- Access control: Principle of least privilege

**Threat Modeling:**
- Assets: AI models, source code, credentials
- Threats: Model poisoning, credential theft, container escape
- Vulnerabilities: Weak authentication, unpatched software
- Risks: Intellectual property theft, system compromise

**Security Controls:**
1. Non-root user execution
2. Minimal base image with security updates
3. Secret injection via secure environment
4. Network policies and firewall rules
5. Regular security scanning and updates

**Compliance Requirements:**
- Docker security best practices
- AI safety and ethics guidelines
- Secure development practices
- Regulatory compliance for AI systems

**Monitoring and Response:**
- Container vulnerability scanning
- Runtime security monitoring
- Access logging and auditing
- Incident response and recovery procedures
```

### Release Security
```
Ensure security of bootdisk release artifacts and distribution:

**Security Domains:**
- Software supply chain security
- Distribution security
- Integrity verification
- Update mechanisms
- User verification

**Threat Modeling:**
- Assets: Bootable ISOs, installation scripts
- Threats: Supply chain attacks, malware injection
- Vulnerabilities: Unsigned releases, insecure channels
- Risks: System compromise during installation

**Security Controls:**
1. Code signing for all releases
2. Secure distribution channels (HTTPS, CDN)
3. Checksum verification for downloads
4. Secure update mechanisms
5. User verification procedures

**Compliance Requirements:**
- Software bill of materials (SBOM)
- Vulnerability disclosure policy
- Secure development lifecycle (SDL)
- Industry security standards

**Monitoring and Response:**
- Security monitoring of distribution channels
- Vulnerability reporting and response
- Incident response coordination
- Continuous security improvement
```

## Success Criteria
- Security vulnerabilities eliminated or mitigated
- Compliance requirements satisfied
- Security monitoring implemented
- Incident response procedures documented
- Security awareness maintained across team
# Quality Assurance Prompt

## Purpose
Guide the QA Evaluator agent in conducting thorough quality assessments, code reviews, and validation of deliverables.

## Context
- **Apply to**: All source files, documentation, test results
- **When to use**: Code review, quality assessment, release validation, compliance checking

## Template
```
Conduct quality assurance evaluation for [DELIVERABLE/COMPONENT] following these standards:

**Quality Dimensions:**
- [Functional correctness]
- [Performance requirements]
- [Security compliance]
- [Code quality metrics]
- [Documentation completeness]

**Review Criteria:**
- [Code style adherence]
- [Test coverage verification]
- [Security vulnerability assessment]
- [Performance benchmark validation]
- [Documentation accuracy]

**Validation Process:**
1. [Automated checks]
2. [Manual review procedures]
3. [Integration testing]
4. [User acceptance testing]

**Defect Classification:**
- [Critical/blocking issues]
- [Major functionality problems]
- [Minor issues/enhancements]
- [Cosmetic improvements]

**Reporting Requirements:**
- [Issue documentation]
- [Severity assessment]
- [Reproduction steps]
- [Recommended fixes]
```

## Examples

### Code Quality Review
```
Conduct comprehensive code quality review for the Rust preseed generation module:

**Quality Dimensions:**
- Memory safety: No unsafe code, proper ownership
- Performance: Efficient algorithms, minimal allocations
- Security: Input validation, secure defaults
- Maintainability: Clear structure, documentation
- Testability: Good separation of concerns

**Review Criteria:**
- Clippy warnings: Zero tolerance
- Test coverage: Minimum 90%
- Documentation: All public APIs documented
- Error handling: Comprehensive and user-friendly
- Code style: Rust standard formatting

**Validation Process:**
1. Run cargo clippy and fix all warnings
2. Execute full test suite with coverage
3. Manual code review for logic errors
4. Performance benchmarking
5. Security static analysis

**Defect Classification:**
- Critical: Memory safety violations, panics
- Major: Logic errors, missing functionality
- Minor: Style issues, incomplete documentation
- Enhancement: Performance optimizations, feature requests
```

### Release Validation
```
Perform release validation for bootdisk v1.0:

**Quality Dimensions:**
- Functional completeness: All features working
- Performance: Boot time < 30 seconds
- Security: No known vulnerabilities
- Compatibility: Debian 13 support verified
- Usability: Clear installation process

**Review Criteria:**
- Installation success rate: 100%
- Boot success rate: 100%
- Feature completeness: All requirements met
- Documentation accuracy: Up-to-date and correct
- User experience: Intuitive and error-free

**Validation Process:**
1. Automated installation testing
2. Manual boot testing on target hardware
3. Feature verification checklist
4. Documentation review
5. User acceptance testing

**Defect Classification:**
- Critical: Installation failures, boot issues
- Major: Missing features, incorrect behavior
- Minor: UI improvements, documentation errors
- Enhancement: Additional features, optimizations
```

## Success Criteria
- All critical issues resolved
- Quality metrics met or exceeded
- Comprehensive documentation provided
- Stakeholder approval obtained
- Release readiness confirmed
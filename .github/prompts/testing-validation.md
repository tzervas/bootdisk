# Testing and Validation Prompt

## Purpose
Guide the Test Engineer agent in creating comprehensive test suites and validation procedures for both Rust and Python components.

## Context
- **Apply to**: `tests/**/*.rs`, `tests/**/*.py`, `src/**/*.rs`, `src/**/*.py`
- **When to use**: Test development, validation procedures, quality assurance

## Template
```
Create comprehensive tests and validation for [COMPONENT/FUNCTION] following these requirements:

**Test Coverage Requirements:**
- [Unit test coverage percentage]
- [Integration test scenarios]
- [Edge case coverage]
- [Error condition testing]

**Test Types Needed:**
- [Unit tests]
- [Integration tests]
- [Property-based tests (Rust)]
- [Performance tests]
- [Security tests]

**Validation Criteria:**
- [Success conditions]
- [Failure modes to test]
- [Performance benchmarks]
- [Security requirements]

**Test Implementation:**
1. [Test framework setup]
2. [Test case development]
3. [Mock/stub creation]
4. [CI/CD integration]

**Deliverables:**
- [Test files]
- [Test configuration]
- [Coverage reports]
- [Validation documentation]
```

## Examples

### Rust Unit Testing
```
Create comprehensive unit tests for the preseed generation module:

**Test Coverage Requirements:**
- 95% line coverage
- All public functions tested
- Error paths covered
- Edge cases included

**Test Types Needed:**
- Unit tests with rstest
- Property-based tests with proptest
- Integration tests for file I/O
- Performance regression tests

**Validation Criteria:**
- Valid preseed files generated
- Invalid inputs properly rejected
- Memory safety maintained
- No panics under any conditions

**Test Implementation:**
1. Set up test fixtures with sample data
2. Test valid preseed generation
3. Test error handling for malformed input
4. Test edge cases (empty files, large files)
5. Add property-based tests for data integrity
```

### Python AI Testing
```
Create validation tests for LangChain agent workflows:

**Test Coverage Requirements:**
- All agent interactions tested
- Error recovery scenarios
- Performance under load
- Security of API interactions

**Test Types Needed:**
- Unit tests for individual components
- Integration tests for agent chains
- Mock tests for external APIs
- Load testing for concurrent operations

**Validation Criteria:**
- Agents respond correctly to prompts
- Secure credential handling
- Proper error propagation
- Performance within acceptable limits

**Test Implementation:**
1. Mock Ollama/OpenAI responses
2. Test agent handoffs
3. Validate secure secret injection
4. Performance benchmarking
```

## Success Criteria
- All tests pass consistently
- Coverage requirements met
- CI/CD pipeline integrated
- Documentation of test procedures
- Automated validation in place
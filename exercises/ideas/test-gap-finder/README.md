# Test Gap Finder: Find Missed Test Cases

## 🎯 Overview

An agent skill that analyzes code coverage data and source code to
identify critical test gaps - areas of code that are untested or
under-tested, helping developers write more comprehensive test suites.

## 💡 Problem Statement

Even with good test coverage metrics, critical code paths often remain
untested. Developers need intelligent tools to identify:
- Untested edge cases
- Missing error handling scenarios
- Uncovered conditional branches
- Integration gaps between components

## ✨ Solution

The Test Gap Finder skill combines coverage analysis with static code analysis to identify meaningful test gaps and suggest specific test cases.

## 🔧 Key Features

### 1. **Coverage Analysis**
- Parse coverage reports (lcov, cobertura, Jacoco, etc.)
- Identify untested lines and branches
- Calculate coverage metrics by function/class
- Detect coverage trends over time

### 2. **Static Code Analysis**
- Parse Abstract Syntax Trees (AST)
- Identify conditional branches
- Detect error handling paths
- Analyze function complexity

### 3. **Gap Detection**
- Correlate coverage with code structure
- Identify untested error conditions
- Find missing edge case scenarios
- Detect integration gaps

### 4. **Test Suggestions**
- Generate specific test case ideas
- Provide code examples for tests
- Prioritize gaps by risk
- Suggest testing strategies

## 🎯 Use Cases

- **CI/CD Pipelines**: Automated test gap detection
- **Legacy Code**: Identifying untested areas in old codebases
- **Code Reviews**: Ensuring new code has proper test coverage
- **Test-Driven Development**: Guiding test writing process
- **Quality Assurance**: Comprehensive testing strategies

## 🔄 Workflow

```
1. Collect coverage reports from test runs
2. Parse source code to build AST
3. Analyze coverage data against code structure
4. Identify untested code paths and conditions
5. Generate prioritized list of test gaps
6. Suggest specific test cases for each gap
7. Provide code examples and testing strategies
```

## 📊 Output Format

```markdown
# Test Gap Analysis Report

## 🚨 Critical Gaps (High Risk)

### 1. **PaymentProcessor.handlePayment() - Error Handling**
- **Location**: src/payment/PaymentProcessor.js:42-55
- **Coverage**: 0% (0/12 lines)
- **Risk**: High - Payment failures not tested
- **Suggested Tests**:
  ```javascript
  test('throws error on invalid payment method', () => {
    expect(() => processor.handlePayment('invalid_method')).toThrow();
  });
  
  test('handles network errors gracefully', async () => {
    mockNetworkError();
    await expect(processor.handlePayment('credit_card')).rejects.toThrow('Network error');
  });
  ```

### 2. **AuthService.validateToken() - Edge Cases**
- **Location**: src/auth/AuthService.js:89-102
- **Coverage**: 25% (3/12 lines)
- **Risk**: High - Token validation gaps
- **Missing Scenarios**:
  - Expired tokens with valid format
  - Malformed JWT tokens
  - Tokens from different issuers

## ⚠️ Important Gaps (Medium Risk)

### 3. **UserRepository.findByEmail() - Null Handling**
- **Location**: src/repositories/UserRepository.js:22-35
- **Coverage**: 60% (9/15 lines)
- **Risk**: Medium - Null email scenarios
- **Suggested**: Test with null, undefined, and empty string inputs

## ℹ️ Minor Gaps (Low Risk)

### 4. **StringUtils.capitalize() - Unicode Support**
- **Location**: src/utils/StringUtils.js:10-18
- **Coverage**: 85% (11/13 lines)
- **Risk**: Low - Edge case coverage
- **Suggested**: Test with emoji and special characters

## 📈 Coverage Summary
- **Overall Coverage**: 78.5%
- **Lines Covered**: 4,231/5,390
- **Functions Covered**: 85%
- **Branches Covered**: 72%
- **Critical Gaps Found**: 2
- **Important Gaps Found**: 4
- **Minor Gaps Found**: 8
```

## 🎯 Benefits

- **Improved Code Quality**: Catch bugs before production
- **Better Test Coverage**: Systematic gap identification
- **Faster Development**: Focus testing efforts where needed
- **Reduced Risk**: Prioritize testing of critical paths
- **Documentation**: Clear record of testing decisions
- **Continuous Improvement**: Track coverage trends over time

## 🔗 Integration

- **Coverage Tools**: lcov, cobertura, Jacoco, Istanbul
- **Test Frameworks**: Jest, Mocha, Pytest, JUnit
- **CI/CD Systems**: GitHub Actions, GitLab CI, Jenkins
- **Code Analysis**: ESLint, Pylint, SonarQube
- **IDE Plugins**: VSCode, IntelliJ, WebStorm

## 🚀 Getting Started

### Basic Usage

```bash
# Install the test gap finder
npm install -g test-gap-finder

# Run analysis on your project
test-gap-finder analyze --coverage lcov.info --src src/

# Generate detailed report
test-gap-finder report --output report.md --format markdown
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Test Gap Analysis
  uses: actions/setup-node@v3
  with:
    node-version: 18

- run: npm install -g test-gap-finder

- run: npm test -- --coverage

- run: test-gap-finder analyze --coverage coverage/lcov.info --src src/ > gaps.md

- name: Comment on PR
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const gaps = fs.readFileSync('gaps.md', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: `## Test Gap Analysis\n\n${gaps}`
      });
```

## 📚 Supported Languages

### JavaScript/TypeScript
- **Coverage**: Istanbul, nyc
- **AST Parsing**: @babel/parser, TypeScript compiler
- **Frameworks**: Jest, Mocha, Jasmine

### Python
- **Coverage**: coverage.py, pytest-cov
- **AST Parsing**: ast module
- **Frameworks**: pytest, unittest

### Java
- **Coverage**: Jacoco, Cobertura
- **AST Parsing**: JavaParser, Eclipse JDT
- **Frameworks**: JUnit, TestNG

### Other Languages
- **Go**: go test -cover
- **Ruby**: SimpleCov
- **PHP**: PHPUnit with coverage
- **C#**: dotCover, Coverlet

## 🔧 Advanced Features

### Risk-Based Prioritization
- **Critical Path Analysis**: Identify code paths with highest business impact
- **Error Path Detection**: Find untested error handling scenarios
- **Security Testing**: Detect missing security-related test cases
- **Performance Testing**: Identify untested performance-critical code

### Machine Learning Enhancements
- **Anomaly Detection**: Find unusual patterns in untested code
- **Similarity Analysis**: Compare with similar well-tested code
- **Predictive Modeling**: Estimate risk based on code characteristics
- **Natural Language**: Generate test descriptions from code

### Integration Capabilities
- **IDE Plugins**: Real-time gap detection in editors
- **Git Hooks**: Pre-commit test gap checks
- **Pull Request Integration**: Automated PR comments
- **Dashboard**: Visual coverage and gap tracking

## 📊 Success Metrics

- **Gap Detection Accuracy**: % of real gaps identified
- **False Positive Rate**: % of non-issues flagged
- **Test Suggestion Quality**: Usefulness of generated test ideas
- **Performance**: Analysis time per 1000 lines of code
- **Adoption Rate**: % of developers using the tool regularly

## 🎯 Implementation Roadmap

### Phase 1: Core Functionality
- [ ] Coverage report parsing
- [ ] Basic AST analysis
- [ ] Simple gap detection
- [ ] Basic test suggestions

### Phase 2: Advanced Analysis
- [ ] Branch coverage analysis
- [ ] Error path detection
- [ ] Integration gap finding
- [ ] Risk prioritization

### Phase 3: Integration & UX
- [ ] CI/CD integration
- [ ] IDE plugin development
- [ ] Interactive report generation
- [ ] Team collaboration features

### Phase 4: Machine Learning
- [ ] Anomaly detection models
- [ ] Natural language test generation
- [ ] Predictive risk modeling
- [ ] Continuous learning from feedback

## 🚀 Example Use Cases

### Use Case 1: Legacy Codebase

**Problem**: 10-year-old codebase with 40% test coverage

**Solution**: Test Gap Finder identifies:
- Critical untested error handling in payment processing
- Missing tests for edge cases in authentication
- Untested integration points between microservices

**Result**: Focused testing effort improves coverage to 75% in 3 months

### Use Case 2: Startup MVP

**Problem**: Rapid development with minimal testing

**Solution**: Automated gap detection in CI pipeline
- Flags untested API endpoints
- Identifies missing error scenarios
- Suggests critical test cases

**Result**: 20% fewer production bugs, faster iteration

### Use Case 3: Enterprise Application

**Problem**: Large team, inconsistent testing standards

**Solution**: Team-wide test gap reporting
- Weekly gap analysis reports
- PR integration with gap warnings
- Gamification of test coverage

**Result**: 35% improvement in test coverage quality

## 📚 Related Skills

- **Code Reviewer**: For detailed code review assistance
- **Documentation Drift Detector**: For finding outdated docs
- **PR Review**: For prioritizing code reviews
- **Commit Ghostwriter**: For writing good commit messages

This Test Gap Finder skill provides a comprehensive solution for identifying and addressing test coverage gaps, helping development teams build more robust and reliable software.

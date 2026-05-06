# Documentation Drift Detector: Spot Outdated Documentation

## 🎯 Overview

An agent skill that identifies documentation that has become outdated
or inconsistent with the current codebase, helping maintain accurate
and up-to-date documentation.

## 💡 Problem Statement

Documentation often becomes outdated as code evolves, leading to:
- Developer confusion and wasted time
- Incorrect API usage examples
- Misleading architecture diagrams
- Outdated installation instructions
- Broken code examples

## ✨ Solution

The Documentation Drift Detector skill analyzes documentation
alongside the current codebase to identify inconsistencies, outdated
references, and potential inaccuracies.

## 🔧 Key Features

### 1. **Documentation Analysis**
- Parse various documentation formats (Markdown, RST, HTML)
- Extract code examples and API references
- Identify version-specific content
- Detect deprecated function references
- Analyze cross-references and links

### 2. **Code Analysis**
- Parse source code (AST analysis)
- Extract public APIs and signatures
- Identify deprecated functions and classes
- Track version changes
- Analyze function parameters and return types

### 3. **Drift Detection**
- Compare documentation with current code
- Identify outdated API references
- Find broken code examples
- Detect missing documentation for new features
- Check parameter and return type consistency

### 4. **Reporting**
- Generate detailed drift reports
- Prioritize by severity
- Provide specific correction suggestions
- Track drift over time
- Integrate with CI/CD pipelines

## 🎯 Use Cases

- **API Documentation**: Ensure API docs match current implementations
- **Tutorials**: Verify code examples still work
- **Architecture Docs**: Check consistency with current structure
- **README Files**: Validate installation and usage instructions
- **Release Notes**: Confirm documented changes match actual changes

## 🔄 Workflow

```
1. Collect documentation files to analyze
2. Parse documentation content and extract references
3. Analyze current codebase and extract APIs
4. Compare documentation references with current code
5. Identify inconsistencies and outdated content
6. Generate prioritized drift report
7. Provide correction suggestions
8. Optionally create issues for documented problems
```

## 📊 Output Format

```markdown
# Documentation Drift Analysis Report

## 🚨 Critical Drift (High Severity)

### 1. **Outdated API Reference in payment.md**
- **File**: docs/api/payment.md:42
- **Issue**: Reference to deprecated `processPayment()` function
- **Current API**: `PaymentProcessor.handleTransaction()`
- **Severity**: High - Function was removed in v2.1.0
- **Suggested Fix**:
  ```markdown
  # Payment Processing
  
  Use the new `PaymentProcessor.handleTransaction()` method:
  
  ```javascript
  const result = await PaymentProcessor.handleTransaction({
    amount: 100,
    currency: 'USD',
    method: 'credit_card'
  });
  ```
  ```

### 2. **Broken Code Example in quickstart.md**
- **File**: docs/quickstart.md:89-95
- **Issue**: Code example uses removed parameter
- **Problem**: `initialize()` no longer accepts `debug` parameter
- **Severity**: High - Example will cause runtime errors
- **Current Signature**: `initialize(config: Config, options?: InitOptions)`
- **Suggested Fix**:
  ```javascript
  // Correct initialization
  await system.initialize({
    apiKey: 'your-key',
    environment: 'production'
  }, {
    timeout: 5000
  });
  ```

## ⚠️ Significant Drift (Medium Severity)

### 3. **Missing Documentation for New Feature**
- **File**: src/services/NotificationService.js
- **Issue**: No documentation for new `sendBulkNotifications()` method
- **Added**: v2.3.0 (3 months ago)
- **Severity**: Medium - Important new feature undocumented
- **Suggested Location**: docs/api/notifications.md
- **Suggested Content**:
  ```markdown
  ### Bulk Notifications
  
  Send notifications to multiple users efficiently:
  
  ```javascript
  await notificationService.sendBulkNotifications({
    userIds: ['user1', 'user2'],
    message: 'Hello!',
    channel: 'email'
  });
  ```
  ```

### 4. **Parameter Type Mismatch in auth.md**
- **File**: docs/api/authentication.md:123
- **Issue**: Documentation shows `userId` as string, but code expects number
- **Current Type**: `userId: number`
- **Severity**: Medium - Type mismatch will cause issues
- **Suggested Fix**: Update type in documentation

## ℹ️ Minor Drift (Low Severity)

### 5. **Outdated Version Reference**
- **File**: README.md:15
- **Issue**: References version 1.2.0 as current
- **Current Version**: 2.4.1
- **Severity**: Low - Informational inconsistency
- **Suggested Fix**: Update version references throughout

### 6. **Deprecated Class Reference**
- **File**: docs/architecture/overview.md:35
- **Issue**: Mentions `LegacyAuthService` class
- **Status**: Deprecated in v2.0.0, removed in v2.2.0
- **Severity**: Low - Class no longer exists
- **Suggested Fix**: Remove reference or update to `AuthService`

## 📊 Summary Statistics

- **Files Analyzed**: 42 documentation files
- **Code Files Analyzed**: 234 source files
- **Critical Issues**: 2
- **Significant Issues**: 4
- **Minor Issues**: 8
- **Total Drift Issues**: 14
- **Drift Rate**: 33.3% (14/42 files)
- **Severity Distribution**:
  - High: 2 (14.3%)
  - Medium: 4 (28.6%)
  - Low: 8 (57.1%)

## 📈 Trends

**Drift Over Time:**
- Last Month: 8 issues
- This Month: 14 issues (+75%)
- Most Common Types:
  - Outdated API references (4)
  - Missing documentation (3)
  - Type mismatches (2)

## 🎯 Recommendations

1. **Immediate Actions**:
   - Fix critical API reference issues in payment.md
   - Correct broken code examples in quickstart.md
   - Add documentation for sendBulkNotifications()

2. **Process Improvements**:
   - Run drift detection before each release
   - Add drift check to CI/CD pipeline
   - Assign documentation owners for each feature

3. **Prevention Strategies**:
   - Add documentation requirements to definition of done
   - Implement documentation review process
   - Use code annotations to flag documentation needs

## 🔍 Analysis Notes

- **Most Problematic Files**:
  - docs/api/payment.md (2 critical issues)
  - docs/quickstart.md (1 critical, 1 medium)
  - README.md (2 minor issues)

- **Best Maintained Files**:
  - docs/api/users.md (no issues)
  - docs/installation.md (no issues)

- **Pattern Observations**:
  - API documentation tends to drift fastest
  - Code examples often become outdated
  - Version references frequently missed in updates

## 📅 Follow-up Plan

**Next Steps:**
1. [ ] Fix critical issues within 1 week
2. [ ] Address significant issues within 2 weeks
3. [ ] Schedule documentation review session
4. [ ] Implement continuous drift detection
5. [ ] Add drift metrics to team dashboard
```

## 🎯 Benefits

- **Improved Developer Experience**: Accurate, up-to-date documentation
- **Reduced Support Burden**: Fewer questions about outdated content
- **Better Onboarding**: New team members get correct information
- **Higher Code Quality**: Documentation matches implementation
- **Faster Development**: Less time wasted on incorrect examples
- **Professional Image**: Polished, accurate external documentation

## 🔗 Integration

- **Documentation Formats**: Markdown, RST, HTML, AsciiDoc
- **Code Analysis**: JavaScript, TypeScript, Python, Java, Go
- **CI/CD Systems**: GitHub Actions, GitLab CI, Jenkins
- **Issue Trackers**: Jira, GitHub Issues, GitLab
- **Static Site Generators**: Docusaurus, Sphinx, MkDocs

## 🚀 Getting Started

### Basic Usage

```bash
# Install the drift detector
npm install -g documentation-drift-detector

# Run analysis on your project
doc-drift-detector analyze --docs docs/ --src src/

# Generate detailed report
doc-drift-detector report --output drift-report.md

# Create GitHub issues for critical drift
doc-drift-detector create-issues --severity high --github-repo myorg/myrepo
```

### Example Configuration

```yaml
# drift-detector.config.yaml
documentation:
  paths: ['docs/', 'README.md', 'CONTRIBUTING.md']
  formats: ['markdown', 'md', 'rst']
  
source:
  paths: ['src/', 'lib/']
  languages: ['javascript', 'typescript']
  
exclusions:
  patterns: ['**/node_modules/**', '**/build/**', '**/archive/**']
  files: ['docs/legacy/', 'docs/v1/']
  
severity:
  critical:
    - 'deprecated_function'
    - 'broken_example'
    - 'removed_api'
  
  significant:
    - 'missing_documentation'
    - 'parameter_mismatch'
    - 'return_type_mismatch'
  
  minor:
    - 'version_mismatch'
    - 'deprecated_class'
    - 'outdated_reference'

output:
  format: 'markdown'
  detail: 'detailed'
  include_suggestions: true
  
integration:
  github:
    repo: 'myorg/myrepo'
    token: '${GITHUB_TOKEN}'
    create_issues: true
    issue_labels: ['documentation', 'drift']
```

## 📚 Supported Documentation Types

### 1. API Documentation
- Function signatures and parameters
- Class definitions and methods
- Type definitions and interfaces
- Usage examples and code snippets

### 2. Tutorials and Guides
- Step-by-step instructions
- Code examples and samples
- Expected outputs and results
- Prerequisites and requirements

### 3. Architecture Documents
- System diagrams and flows
- Component descriptions
- Integration points
- Data models and schemas

### 4. Reference Materials
- Configuration options
- Environment variables
- Command-line interfaces
- File formats and structures

## 🔧 Advanced Features

### Cross-Reference Validation
- **Internal Links**: Verify documentation links work
- **API References**: Check referenced functions exist
- **Version References**: Validate version numbers
- **File References**: Confirm referenced files exist

### Code Example Testing
- **Syntax Checking**: Verify code examples are valid
- **Static Analysis**: Check for potential errors
- **Type Checking**: Validate TypeScript/Python types
- **Import Verification**: Confirm imports exist

### Change Impact Analysis
- **Git Integration**: Analyze changes since last update
- **Blame Analysis**: Identify when documentation was last updated
- **Change Correlation**: Link code changes to doc updates
- **Stale Detection**: Find documentation not updated recently

### Machine Learning Enhancements
- **Anomaly Detection**: Find unusual patterns
- **Similarity Analysis**: Compare with well-maintained docs
- **Natural Language**: Improve text understanding
- **Predictive Modeling**: Estimate drift risk

## 📊 Success Metrics

- **Detection Accuracy**: % of real drift issues identified
- **False Positive Rate**: % of non-issues flagged as drift
- **Coverage**: % of documentation analyzed
- **Impact**: Reduction in documentation-related issues
- **Adoption**: % of teams using the tool regularly

## 🎯 Implementation Roadmap

### Phase 1: Core Functionality
- [ ] Basic documentation parsing
- [ ] Simple code analysis
- [ ] Basic drift detection
- [ ] Markdown report generation

### Phase 2: Advanced Analysis
- [ ] Multi-language support
- [ ] Code example validation
- [ ] Cross-reference checking
- [ ] Severity prioritization

### Phase 3: Integration
- [ ] CI/CD pipeline integration
- [ ] GitHub/GitLab issue creation
- [ ] IDE plugin development
- [ ] Web dashboard

### Phase 4: Enhancements
- [ ] Machine learning improvements
- [ ] Historical trend analysis
- [ ] Automated fix suggestions
- [ ] Real-time monitoring

## 🚀 Example Use Cases

### Use Case 1: API Documentation Maintenance

**Problem**: Large API with 150+ endpoints, documentation manually updated

**Solution**: Monthly drift detection runs
- Identifies 23 outdated endpoints
- Finds 8 broken code examples
- Detects 15 missing new features

**Result**: 40% improvement in API documentation accuracy

### Use Case 2: Open Source Project

**Problem**: Community-maintained project with inconsistent documentation

**Solution**: CI/CD integration
- Drift check on every PR merge
- Automatic issue creation for critical drift
- Documentation owners assigned

**Result**: 60% reduction in documentation-related GitHub issues

### Use Case 3: Enterprise Knowledge Base

**Problem**: Large internal wiki with outdated technical documentation

**Solution**: Quarterly comprehensive scans
- Identifies 42 outdated articles
- Prioritizes by business impact
- Assigns to documentation team

**Result**: 30% improvement in internal support ticket resolution time

## 📚 Related Skills

- **Commit Ghostwriter**: For writing good commit messages
- **Code Reviewer**: For detailed code review assistance
- **Meeting Effectuator**: For creating tickets from meetings
- **Test Gap Finder**: For identifying missing test cases

This Documentation Drift Detector skill helps maintain the critical
connection between code and documentation, ensuring that developers
always have access to accurate, up-to-date information about the
systems they work with.


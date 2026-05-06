# Evaluation Approach for PR Review Skill

## 🎯 Evaluation Strategy

To properly evaluate the PR Review skill, we need to test its ability
to accurately prioritize pull requests based on various factors. The
evaluation should focus on the skill's decision-making quality and
integration capabilities.

## 🧪 Test Setup

### Test Repository Structure

```
pr-review-eval/
├── test-repos/            # Mock Git repositories
│   ├── simple-bugfix/     # Small, low-complexity PR
│   ├── complex-feature/   # Large, high-complexity PR  
│   ├── security-patch/     # Critical security fix
│   └── documentation/     # Low-priority docs update
├── mock-api/             # Simulated GitHub/GitLab API
└── expected-results/     # Expected prioritization outputs
```

### Test Data Requirements

1. **Mock PRs with varying characteristics**:
   - Simple bug fixes (low complexity, medium urgency)
   - Complex features (high complexity, high urgency)
   - Security patches (medium complexity, critical urgency)
   - Documentation updates (low complexity, low urgency)
   - Refactoring PRs (high complexity, low urgency)

2. **Team capacity scenarios**:
   - Normal workload
   - Overloaded team
   - Reduced capacity (vacations, etc.)

3. **Integration test cases**:
   - GitHub API responses
   - GitLab API responses
   - Error handling scenarios

## 📊 Evaluation Metrics

### Primary Metrics

1. **Prioritization Accuracy** (60% weight)
   - Does the skill correctly identify high-priority PRs?
   - Are security/critical PRs always prioritized?
   - Are low-priority PRs correctly deprioritized?

2. **Complexity Assessment** (20% weight)
   - Accuracy of code churn analysis
   - File distribution analysis
   - Cyclomatic complexity scoring

3. **Integration Quality** (15% weight)
   - API call handling
   - Error recovery
   - Data parsing accuracy

4. **Output Quality** (5% weight)
   - Readability of reports
   - Usefulness of recommendations
   - Clarity of reasoning

## 🧪 Test Cases

### Test Case 1: Security vs Feature Priority

**Scenario**: Two PRs - one security fix, one new feature

**Input**:
- PR #1: Security vulnerability fix (medium complexity)
- PR #2: New feature request (high complexity)

**Expected**: Security PR ranked higher regardless of complexity

**Evaluation**: Check if security factors override complexity

### Test Case 2: Complexity Analysis

**Scenario**: Multiple PRs with varying complexity

**Input**:
- PR #1: 5 files, 200 lines changed
- PR #2: 25 files, 1500 lines changed
- PR #3: 1 file, 50 lines changed

**Expected**: PR #2 > PR #1 > PR #3 by complexity

**Evaluation**: Verify complexity scoring accuracy

### Test Case 3: Team Capacity Impact

**Scenario**: Same PRs with different team loads

**Input**:
- Normal capacity: 5 available reviewers
- Reduced capacity: 1 available reviewer

**Expected**: More conservative prioritization with reduced capacity

**Evaluation**: Check if team capacity affects recommendations

### Test Case 4: Integration Test

**Scenario**: Real API integration test

**Input**: Mock GitHub API with sample PR data

**Expected**: Successful API calls and data parsing

**Evaluation**: Verify integration works without errors

## 📈 Scoring System

```
Total Score = (Prioritization * 0.6) + (Complexity * 0.2) + (Integration * 0.15) + (Output * 0.05)

Grading Scale:
- 90-100: Excellent - Production ready
- 80-89: Good - Minor improvements needed
- 70-79: Fair - Significant improvements needed
- Below 70: Poor - Major redesign required
```

## 🔧 Evaluation Tools

### Recommended Tools

1. **Mock API Server**: 
   - Use `json-server` or similar for GitHub/GitLab API simulation
   - Configure with sample PR data

2. **Test Framework**:
   - Jest/Mocha for JavaScript
   - Pytest for Python
   - RSpec for Ruby

3. **Assertion Library**:
   - Chai (JavaScript)
   - Pytest assertions (Python)
   - Custom comparators for prioritization results

### Sample Test Code

```javascript
// Example test using Jest
const { prioritizePRs } = require('./pr-review-skill');

describe('PR Review Skill', () => {
  test('prioritizes security over features', async () => {
    const prs = [
      { id: 1, title: 'Security Fix', files: 8, lines: 300, security: true },
      { id: 2, title: 'New Feature', files: 15, lines: 800, security: false }
    ];
    
    const result = await prioritizePRs(prs);
    expect(result[0].id).toBe(1); // Security PR should be first
  });

  test('handles team capacity constraints', async () => {
    const prs = [
      { id: 1, title: 'PR 1', complexity: 50 },
      { id: 2, title: 'PR 2', complexity: 60 }
    ];
    
    // Normal capacity
    let result = await prioritizePRs(prs, { teamCapacity: 5 });
    expect(result.length).toBe(2);
    
    // Reduced capacity
    result = await prioritizePRs(prs, { teamCapacity: 1 });
    expect(result.length).toBe(1); // Should prioritize only most critical
  });
});
```

## 📋 Evaluation Checklist

- [ ] Create mock repositories with sample PRs
- [ ] Set up mock API server for Git platform integration
- [ ] Define expected prioritization outcomes
- [ ] Implement automated test suite
- [ ] Run prioritization accuracy tests
- [ ] Test complexity analysis
- [ ] Test team capacity handling
- [ ] Test integration scenarios
- [ ] Evaluate output quality
- [ ] Document results and findings

## 🎯 Success Criteria

The PR Review skill is considered successful if:

1. **Accuracy**: Correctly prioritizes 90%+ of test cases
2. **Reliability**: Handles edge cases without crashes
3. **Integration**: Works with GitHub/GitLab APIs
4. **Performance**: Processes typical workload in <5 seconds
5. **Usability**: Output is clear and actionable

## 📚 Additional Resources

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [Code Complexity Analysis Guide](https://www.sonarsource.com/resources/clean-code/cognitive-complexity/)
- [PR Prioritization Best Practices](https://github.com/blog/2019-how-to-prioritize-pull-requests)

This evaluation approach provides a comprehensive framework for
testing the PR Review skill's effectiveness and reliability.

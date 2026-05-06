# PR Review: Prioritize Code Reviews

## 🎯 Overview

An agent skill that automatically prioritizes pull requests based on
multiple factors including complexity, urgency, team capacity, and
business impact.

Or automatically prioritizes pull requests based on your expertise and
preference. This adds a learning aspect to the skill.

## 💡 Problem Statement

In busy development teams, pull requests can pile up, making it
difficult to determine which ones should be reviewed first. Manual
prioritization is time-consuming and often subjective.

## ✨ Solution

The PR Review skill analyzes pull requests using a multi-factor
scoring system and provides data-driven prioritization
recommendations.

## 🔧 Key Features

### 1. **Complexity Analysis**
- Code churn metrics (lines added/removed)
- File count and distribution
- Cyclomatic complexity analysis
- Dependency impact assessment

### 2. **Urgency Factors**
- Time since creation
- Linked tickets/issues priority
- Security-related changes
- Production hotfixes

### 3. **Team Capacity**
- Current reviewer workload
- Author's other pending PRs
- Team availability patterns
- Historical review times

### 4. **Business Impact**
- Feature importance
- Customer-facing vs internal
- Release timeline alignment
- Revenue impact estimation

## 🎯 Use Cases

- **Large Teams**: With 10+ developers and many concurrent PRs
- **Open Source Projects**: Managing community contributions
- **Release Management**: Prioritizing critical path changes
- **Onboarding**: Helping new team members understand priorities

## 🔄 Workflow

```
1. Fetch open PRs from GitHub/GitLab
2. Analyze each PR's complexity and content
3. Check linked tickets and urgency factors
4. Assess team capacity and availability
5. Calculate prioritization score
6. Generate prioritized PR list with recommendations
7. Provide detailed reasoning for each priority
```

## 📊 Output Format

```markdown
# PR Prioritization Report

## 🔥 High Priority (Review Immediately)
1. **#42 - Security Fix for SQL Injection**
   - Score: 95/100
   - Complexity: Medium (12 files, 456 lines)
   - Urgency: Critical (Security vulnerability)
   - Impact: Customer data protection
   - Recommended Reviewers: @security-team

## 🚀 High Priority (Review Today)
2. **#37 - Payment Processing Refactor**
   - Score: 88/100
   - Complexity: High (28 files, 1245 lines)
   - Urgency: High (Blocking release)
   - Impact: Revenue-critical feature

## 📅 Medium Priority (Review This Week)
3. **#22 - UI Improvements for Dashboard**
   - Score: 65/100
   - Complexity: Low (5 files, 189 lines)
   - Urgency: Medium (UX enhancement)
```

## 🎯 Benefits

- **Faster Reviews**: Critical PRs get attention sooner
- **Better Resource Allocation**: Team focuses on high-impact work
- **Data-Driven Decisions**: Objective prioritization criteria
- **Improved Metrics**: Track review times and bottlenecks
- **Reduced Context Switching**: Reviewers can plan their work better

## 🔗 Integration

- **GitHub API**: Full PR data access
- **GitLab API**: Alternative platform support
- **Jira Integration**: Ticket priority synchronization
- **Slack/MS Teams**: Notification and alerts
- **CI/CD Pipelines**: Automated trigger on PR creation

## 🚀 Getting Started

To implement this skill:

1. **Set up API access** to your Git platform
2. **Configure scoring weights** based on your team's priorities
3. **Define team capacity** rules and availability patterns
4. **Integrate with notification** systems for alerts
5. **Run regularly** (e.g., daily or on PR creation)

## 📚 Related Skills

- **Commit Ghostwriter**: For writing good commit messages
- **Code Reviewer**: For detailed code review assistance
- **Ticket Prep**: For creating well-structured tickets


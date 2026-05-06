# Implementation Guide for PR Review Skill

## 🚀 Getting Started

This guide provides step-by-step instructions for implementing the PR
Review skill with practical code examples and integration patterns.

## 📋 Prerequisites

### Required Tools

```bash
# Node.js example dependencies
npm install @octokit/rest axios moment lodash

# Python example dependencies  
pip install pygithub requests datetime
```

### API Access

1. **GitHub**: Create a personal access token with `repo` scope
2. **GitLab**: Create an access token with `api` scope
3. Store securely using environment variables

## 🔧 Core Implementation

### 1. API Client Setup

```javascript
// GitHub API Client
const { Octokit } = require("@octokit/rest");

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN
});

async function getOpenPRs(owner, repo) {
  const { data: prs } = await octokit.pulls.list({
    owner,
    repo,
    state: 'open',
    per_page: 100
  });
  return prs;
}
```

### 2. Complexity Analysis

```javascript
function analyzeComplexity(pr) {
  // Code churn metrics
  const linesAdded = pr.additions || 0;
  const linesRemoved = pr.deletions || 0;
  const filesChanged = pr.changed_files || 0;
  
  // Complexity score (0-100)
  const churnScore = Math.min(100, (linesAdded + linesRemoved) / 10);
  const fileScore = Math.min(100, filesChanged * 5);
  
  return {
    score: Math.min(100, churnScore + fileScore),
    details: {
      linesAdded,
      linesRemoved,
      filesChanged,
      churnScore,
      fileScore
    }
  };
}
```

### 3. Urgency Scoring

```javascript
function calculateUrgency(pr) {
  const createdAt = new Date(pr.created_at);
  const ageDays = (Date.now() - createdAt) / (1000 * 60 * 60 * 24);
  
  // Base urgency factors
  let urgency = 0;
  
  // Age factor (older PRs get higher urgency)
  urgency += Math.min(50, ageDays * 2);
  
  // Label-based urgency
  if (pr.labels.some(l => l.name.includes('security'))) urgency += 30;
  if (pr.labels.some(l => l.name.includes('critical'))) urgency += 25;
  if (pr.labels.some(l => l.name.includes('bug'))) urgency += 20;
  
  // Milestone urgency
  if (pr.milestone && pr.milestone.due_on) {
    const daysUntilDue = (new Date(pr.milestone.due_on) - Date.now()) / (1000 * 60 * 60 * 24);
    if (daysUntilDue < 7) urgency += 20; // Less than 1 week
    if (daysUntilDue < 1) urgency += 15; // Less than 1 day
  }
  
  return Math.min(100, urgency);
}
```

### 4. Team Capacity Analysis

```javascript
function assessTeamCapacity(prs, teamConfig) {
  // Analyze current reviewer workload
  const reviewerWorkload = {};
  
  prs.forEach(pr => {
    pr.requested_reviewers.forEach(reviewer => {
      reviewerWorkload[reviewer.login] = (reviewerWorkload[reviewer.login] || 0) + 1;
    });
  });
  
  // Calculate capacity score for each PR
  return prs.map(pr => {
    const reviewerCount = pr.requested_reviewers.length;
    const avgWorkload = reviewerCount > 0 
      ? pr.requested_reviewers.reduce((sum, r) => sum + (reviewerWorkload[r.login] || 0), 0) / reviewerCount
      : 0;
    
    // Capacity score (higher is better - more capacity available)
    const capacityScore = Math.max(0, 100 - (avgWorkload * 10));
    
    return {
      prNumber: pr.number,
      capacityScore,
      reviewerWorkload: avgWorkload
    };
  });
}
```

### 5. Prioritization Algorithm

```javascript
function prioritizePRs(prs, teamConfig = {}) {
  return prs.map(pr => {
    // Calculate individual scores
    const complexity = analyzeComplexity(pr);
    const urgency = calculateUrgency(pr);
    const capacity = assessTeamCapacity([pr], teamConfig)[0];
    
    // Business impact (simplified - would integrate with Jira/etc in production)
    const businessImpact = pr.labels.some(l => 
      l.name.includes('customer') || l.name.includes('revenue')
    ) ? 20 : 10;
    
    // Weighted overall score
    const overallScore = (
      complexity.score * 0.4 + 
      urgency * 0.3 + 
      capacity.capacityScore * 0.2 + 
      businessImpact * 0.1
    );
    
    return {
      number: pr.number,
      title: pr.title,
      score: overallScore,
      complexity: complexity.score,
      urgency,
      capacity: capacity.capacityScore,
      businessImpact,
      url: pr.html_url
    };
  }).sort((a, b) => b.score - a.score); // Sort by score descending
}
```

## 🔄 Complete Workflow

```javascript
async function generatePRReport(owner, repo) {
  // 1. Fetch open PRs
  const prs = await getOpenPRs(owner, repo);
  
  // 2. Analyze and prioritize
  const prioritized = prioritizePRs(prs);
  
  // 3. Generate report
  const report = generateMarkdownReport(prioritized);
  
  // 4. Output results
  console.log(report);
  return report;
}

function generateMarkdownReport(prioritizedPRs) {
  const highPriority = prioritizedPRs.filter(pr => pr.score >= 80);
  const mediumPriority = prioritizedPRs.filter(pr => pr.score >= 60 && pr.score < 80);
  const lowPriority = prioritizedPRs.filter(pr => pr.score < 60);
  
  return `# PR Prioritization Report - ${new Date().toISOString().split('T')[0]}

## 🔥 High Priority (Score ≥ 80)
${highPriority.map(pr => `
- **[#${pr.number}](${pr.url})**: ${pr.title}
  - **Score**: ${pr.score.toFixed(1)}/100
  - **Complexity**: ${pr.complexity.toFixed(1)}
  - **Urgency**: ${pr.urgency.toFixed(1)}
  - **Capacity**: ${pr.capacity.toFixed(1)}`).join('')}

## 📅 Medium Priority (Score 60-79)
${mediumPriority.map(pr => `
- **[#${pr.number}](${pr.url})**: ${pr.title} (${pr.score.toFixed(1)})`).join('')}

## ⏳ Low Priority (Score < 60)
${lowPriority.map(pr => `
- **[#${pr.number}](${pr.url})**: ${pr.title} (${pr.score.toFixed(1)})`).join('')}
`;
}
```

## 🎛️ Configuration

### Configuration Options

```javascript
// config.js
module.exports = {
  // Scoring weights
  weights: {
    complexity: 0.4,
    urgency: 0.3, 
    capacity: 0.2,
    businessImpact: 0.1
  },
  
  // Complexity thresholds
  complexity: {
    low: 30,
    medium: 60,
    high: 80
  },
  
  // Urgency thresholds
  urgency: {
    low: 20,
    medium: 50,
    high: 80
  },
  
  // Team capacity settings
  team: {
    maxWorkload: 5, // Max PRs per reviewer
    availableReviewers: ['user1', 'user2', 'user3']
  },
  
  // Integration settings
  github: {
    owner: 'your-org',
    repo: 'your-repo',
    token: process.env.GITHUB_TOKEN
  }
};
```

## 🔌 Integration Patterns

### 1. GitHub Action

```yaml
# .github/workflows/pr-prioritization.yml
name: PR Prioritization
on:
  schedule:
    - cron: '0 9 * * 1-5' # Weekdays at 9am
  workflow_dispatch:

jobs:
  prioritize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Install dependencies
        run: npm install
      
      - name: Run PR prioritization
        run: node pr-review.js
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Post results to Slack
        if: success()
        uses: slackapi/slack-github-action@v1.23.0
        with:
          payload: |
            {
              "text": "PR Prioritization Report",
              "attachments": [
                {
                  "color": "#36a64f",
                  "text": "$(cat report.md)"
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 2. CLI Tool

```javascript
#!/usr/bin/env node
// pr-review-cli.js

const { program } = require('commander');
const { generatePRReport } = require('./pr-review');

program
  .name('pr-review')
  .description('CLI tool for PR prioritization')
  .version('1.0.0')
  .option('-o, --owner <owner>', 'Repository owner')
  .option('-r, --repo <repo>', 'Repository name')
  .option('-t, --token <token>', 'GitHub token')
  .option('-f, --format <format>', 'Output format (markdown|json|text)', 'markdown')
  .action(async (options) => {
    try {
      const report = await generatePRReport(options.owner, options.repo, options.token);
      
      if (options.format === 'json') {
        console.log(JSON.stringify(report, null, 2));
      } else if (options.format === 'text') {
        console.log(textReport(report));
      } else {
        console.log(report);
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

program.parse();
```

## 🧪 Testing Strategy

### Unit Tests

```javascript
// test/pr-review.test.js
const { analyzeComplexity, calculateUrgency, prioritizePRs } = require('../pr-review');

describe('PR Review Skill', () => {
  describe('Complexity Analysis', () => {
    test('calculates complexity score correctly', () => {
      const pr = {
        additions: 500,
        deletions: 200,
        changed_files: 15
      };
      
      const result = analyzeComplexity(pr);
      expect(result.score).toBeGreaterThan(50);
      expect(result.score).toBeLessThanOrEqual(100);
    });
  });

  describe('Urgency Calculation', () => {
    test('prioritizes security labels', () => {
      const pr = {
        created_at: new Date(Date.now() - 86400000).toISOString(), // 1 day old
        labels: [{ name: 'security' }, { name: 'critical' }]
      };
      
      const urgency = calculateUrgency(pr);
      expect(urgency).toBeGreaterThan(50); // Security + critical should give high urgency
    });
  });

  describe('Prioritization', () => {
    test('sorts PRs by overall score', () => {
      const prs = [
        { number: 1, additions: 100, deletions: 50, changed_files: 5, 
          created_at: new Date().toISOString(), labels: [] },
        { number: 2, additions: 500, deletions: 200, changed_files: 15,
          created_at: new Date(Date.now() - 172800000).toISOString(), 
          labels: [{ name: 'security' }] }
      ];
      
      const result = prioritizePRs(prs);
      expect(result[0].number).toBe(2); // Security PR should be first
    });
  });
});
```

## 📦 Deployment Options

### 1. Serverless Function

```javascript
// AWS Lambda example
exports.handler = async (event) => {
  try {
    const { owner, repo } = event.queryStringParameters;
    const report = await generatePRReport(owner, repo);
    
    return {
      statusCode: 200,
      body: JSON.stringify(report),
      headers: { 'Content-Type': 'application/json' }
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
```

### 2. Docker Container

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "server.js"]
```

## 🔧 Optimization Tips

### Performance Optimization

1. **Caching**: Cache PR data to avoid repeated API calls
2. **Batching**: Process PRs in batches for large repositories
3. **Parallel Processing**: Use Promise.all for independent analyses
4. **Incremental Updates**: Only re-analyze changed PRs

### Accuracy Improvement

1. **Machine Learning**: Train model on historical prioritization data
2. **Feedback Loop**: Incorporate user feedback on recommendations
3. **Context Awareness**: Consider team's current sprint goals
4. **Historical Data**: Use past review times for better estimates

## 📚 Resources

### GitHub API
- [REST API Documentation](https://docs.github.com/en/rest)
- [GraphQL API](https://docs.github.com/en/graphql)
- [Rate Limits](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)

### GitLab API
- [REST API](https://docs.gitlab.com/ee/api/)
- [GraphQL API](https://docs.gitlab.com/ee/api/graphql/)
- [Pagination](https://docs.gitlab.com/ee/api/#pagination)

### Code Analysis
- [ESLint](https://eslint.org/) - JavaScript analysis
- [Pylint](https://www.pylint.org/) - Python analysis
- [SonarQube](https://www.sonarqube.org/) - Multi-language analysis

### Prioritization Algorithms
- [Analytic Hierarchy Process](https://en.wikipedia.org/wiki/Analytic_hierarchy_process)
- [Weighted Sum Model](https://en.wikipedia.org/wiki/Multiple-criteria_decision_analysis)
- [TOPSIS Method](https://en.wikipedia.org/wiki/TOPSIS)

This implementation guide provides everything needed to build a robust
PR Review skill with proper integration, testing, and deployment
strategies.


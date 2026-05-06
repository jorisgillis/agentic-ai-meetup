# Implementation Guide for Meeting Effectuator

## 🚀 Getting Started

This guide provides step-by-step instructions for implementing the Meeting Effectuator skill with practical code examples and integration patterns.

## 📋 Prerequisites

### Required Tools

```bash
# Natural Language Processing
npm install natural compromise nlp.js

# API Integration
npm install axios octokit node-jira-client

# Text Processing
npm install markdown-it lodash moment
```

### API Access

1. **Jira**: Create API token with issue creation permissions
2. **GitHub**: Create personal access token with repo scope
3. **GitLab**: Create access token with api scope
4. Store securely using environment variables

## 🔧 Core Implementation

### 1. Text Parser

```javascript
// text-parser.js
const markdownIt = require('markdown-it');
const { NlpManager } = require('node-nlp');

class MeetingParser {
  constructor() {
    this.md = markdownIt();
    this.manager = new NlpManager({ languages: ['en'] });
    this.setupNLP();
  }

  setupNLP() {
    // Train NLP model for action item detection
    this.manager.addDocument('en', 'implement the payment gateway by march', 'action');
    this.manager.addDocument('en', 'alice will handle the login issues', 'action');
    this.manager.addDocument('en', 'we decided to use stripe and paypal', 'decision');
    this.manager.addDocument('en', 'the meeting was productive', 'none');
    
    this.manager.addNamedEntityText(
      'owner',
      'alice will implement this',
      ['alice'],
      ['owner']
    );
    
    this.manager.addNamedEntityText(
      'deadline',
      'complete by march 31',
      ['march 31'],
      ['deadline']
    );
    
    this.manager.train();
  }

  async parseMeetingNotes(notes) {
    // Parse markdown if applicable
    if (notes.trim().startsWith('#')) {
      return this.parseMarkdown(notes);
    }
    
    // Use NLP for free-form text
    return this.parseWithNLP(notes);
  }

  parseMarkdown(markdown) {
    const tokens = this.md.parse(markdown, {});
    const result = { actionItems: [], decisions: [], notes: [] };
    
    let currentSection = null;
    
    tokens.forEach(token => {
      if (token.type === 'heading_open') {
        const headingText = tokens[tokens.indexOf(token) + 1].content;
        if (headingText.includes('Action Items')) {
          currentSection = 'actionItems';
        } else if (headingText.includes('Decisions')) {
          currentSection = 'decisions';
        } else {
          currentSection = null;
        }
      }
      
      if (token.type === 'inline' && currentSection) {
        const text = token.children.map(c => c.content).join('');
        if (text.trim()) {
          result[currentSection].push(this.parseActionItem(text));
        }
      }
    });
    
    return result;
  }

  async parseWithNLP(text) {
    const response = await this.manager.process('en', text);
    const result = { actionItems: [], decisions: [], notes: [] };
    
    // Split into sentences
    const sentences = text.split(/\.|!|\?/).filter(s => s.trim().length > 10);
    
    sentences.forEach(sentence => {
      const classification = response.classifications.find(c => c.label !== 'none');
      
      if (classification?.label === 'action') {
        result.actionItems.push(this.parseActionItem(sentence));
      } else if (classification?.label === 'decision') {
        result.decisions.push(this.parseDecision(sentence));
      } else {
        result.notes.push(sentence.trim());
      }
    });
    
    return result;
  }

  parseActionItem(text) {
    // Extract owner using @mention or name pattern
    const ownerMatch = text.match(/@(\w+)|\b([A-Z][a-z]+)\b.*(will|handle|implement)/i);
    const owner = ownerMatch ? (ownerMatch[1] || ownerMatch[2]).toLowerCase() : null;
    
    // Extract deadline
    const deadlineMatch = text.match(/by (\w+ \d{1,2}(?:,? \d{4})?)/i);
    const deadline = deadlineMatch ? deadlineMatch[1] : null;
    
    // Extract priority
    const priority = text.match(/high|medium|low/i)?.[0] || 'medium';
    
    // Clean up description
    const description = text
      .replace(/@\w+|\b\w+ will|by \w+ \d{1,2}(?:,? \d{4})?|high|medium|low/gi, '')
      .trim();
    
    return { owner, deadline, priority, description, confidence: 0.8 };
  }

  parseDecision(text) {
    return {
      decision: text.replace(/we decided|team agreed|decision:/i, '').trim(),
      confidence: 0.7
    };
  }
}

module.exports = MeetingParser;
```

### 2. Ticket Generator

```javascript
// ticket-generator.js
const moment = require('moment');

class TicketGenerator {
  constructor(config) {
    this.config = config;
  }

  generateTickets(parsedNotes) {
    return parsedNotes.actionItems.map(item => {
      return {
        title: this.generateTitle(item),
        description: this.generateDescription(item),
        assignee: this.mapOwner(item.owner),
        priority: this.normalizePriority(item.priority),
        dueDate: this.parseDeadline(item.deadline),
        labels: this.generateLabels(item),
        type: this.determineType(item),
        metadata: {
          source: 'meeting-effectuator',
          confidence: item.confidence,
          originalText: item.description
        }
      };
    });
  }

  generateTitle(item) {
    const actionVerbs = ['implement', 'fix', 'update', 'create', 'develop', 'build'];
    const verb = actionVerbs.find(v => item.description.toLowerCase().includes(v)) || 'handle';
    
    return `${verb.charAt(0).toUpperCase() + verb.slice(1)}: ${item.description}`;
  }

  generateDescription(item) {
    return `**Source**: Meeting action item\n\n**Original**: ${item.description}\n\n**Acceptance Criteria**:\n- [ ] Task completed as described\n- [ ] Reviewed by team\n- [ ] Documented appropriately\n\n**Notes**: Generated from meeting notes - verify details with meeting participants if needed.`;
  }

  mapOwner(owner) {
    if (!owner) return this.config.defaultAssignee;
    
    // Map common names to system usernames
    const ownerMap = {
      'alice': 'alice.dev',
      'bob': 'bob.frontend',
      'charlie': 'charlie.qa',
      'diana': 'diana.pm'
    };
    
    return ownerMap[owner] || owner;
  }

  normalizePriority(priority) {
    const priorityMap = {
      'high': 'High',
      'medium': 'Medium',
      'low': 'Low',
      'critical': 'Highest',
      'urgent': 'High'
    };
    
    return priorityMap[priority.toLowerCase()] || 'Medium';
  }

  parseDeadline(deadline) {
    if (!deadline) return null;
    
    // Handle various date formats
    const formats = [
      'MMMM D, YYYY',
      'MMMM D',
      'D MMMM YYYY',
      'D MMMM',
      'YYYY-MM-DD'
    ];
    
    for (const format of formats) {
      const date = moment(deadline, format);
      if (date.isValid()) {
        return date.format('YYYY-MM-DD');
      }
    }
    
    // Relative dates
    if (deadline.includes('next week')) {
      return moment().add(7, 'days').format('YYYY-MM-DD');
    }
    
    if (deadline.includes('end of month')) {
      return moment().endOf('month').format('YYYY-MM-DD');
    }
    
    return null;
  }

  generateLabels(item) {
    const labels = ['meeting-outcome'];
    
    // Add priority label
    labels.push(`priority-${item.priority.toLowerCase()}`);
    
    // Add content-based labels
    if (item.description.toLowerCase().includes('bug')) {
      labels.push('bug');
    }
    
    if (item.description.toLowerCase().includes('feature')) {
      labels.push('feature');
    }
    
    if (item.description.toLowerCase().includes('documentation')) {
      labels.push('documentation');
    }
    
    return labels;
  }

  determineType(item) {
    if (item.description.toLowerCase().includes('bug')) {
      return 'bug';
    }
    
    if (item.description.toLowerCase().includes('documentation')) {
      return 'task';
    }
    
    return 'story'; // Default to user story
  }
}

module.exports = TicketGenerator;
```

### 3. API Integrator

```javascript
// api-integrator.js
const axios = require('axios');

class APIIntegrator {
  constructor(platform, config) {
    this.platform = platform;
    this.config = config;
    this.client = this.createClient();
  }

  createClient() {
    switch (this.platform) {
      case 'jira':
        return this.createJiraClient();
      case 'github':
        return this.createGitHubClient();
      case 'gitlab':
        return this.createGitLabClient();
      default:
        throw new Error(`Unsupported platform: ${this.platform}`);
    }
  }

  createJiraClient() {
    const { JiraClient } = require('jira-connector');
    return new JiraClient({
      host: this.config.host,
      basic_auth: {
        email: this.config.email,
        api_token: this.config.apiToken
      }
    });
  }

  createGitHubClient() {
    const { Octokit } = require("@octokit/rest");
    return new Octokit({
      auth: this.config.token
    });
  }

  createGitLabClient() {
    return axios.create({
      baseURL: `${this.config.host}/api/v4`,
      headers: {
        'PRIVATE-TOKEN': this.config.token
      }
    });
  }

  async createTicket(ticket) {
    try {
      switch (this.platform) {
        case 'jira':
          return await this.createJiraTicket(ticket);
        case 'github':
          return await this.createGitHubIssue(ticket);
        case 'gitlab':
          return await this.createGitLabIssue(ticket);
        default:
          throw new Error(`Unsupported platform: ${this.platform}`);
      }
    } catch (error) {
      console.error(`Failed to create ticket: ${error.message}`);
      throw new Error(`Ticket creation failed: ${error.message}`);
    }
  }

  async createJiraTicket(ticket) {
    const response = await this.client.issue.createIssue({
      fields: {
        project: {
          key: this.config.project
        },
        summary: ticket.title,
        description: ticket.description,
        issuetype: {
          name: ticket.type
        },
        assignee: {
          name: ticket.assignee
        },
        priority: {
          name: ticket.priority
        },
        duedate: ticket.dueDate,
        labels: ticket.labels
      }
    });
    
    return {
      success: true,
      id: response.key,
      url: `${this.config.host}/browse/${response.key}`,
      platform: 'jira'
    };
  }

  async createGitHubIssue(ticket) {
    const [owner, repo] = this.config.repo.split('/');
    
    const response = await this.client.issues.create({
      owner,
      repo,
      title: ticket.title,
      body: ticket.description,
      assignees: [ticket.assignee],
      labels: ticket.labels
    });
    
    return {
      success: true,
      id: response.data.number,
      url: response.data.html_url,
      platform: 'github'
    };
  }

  async createGitLabIssue(ticket) {
    const response = await this.client.post(`/projects/${encodeURIComponent(this.config.project)}/issues`, {
      title: ticket.title,
      description: ticket.description,
      assignee_ids: [this.getGitLabUserId(ticket.assignee)],
      labels: ticket.labels.join(','),
      due_date: ticket.dueDate
    });
    
    return {
      success: true,
      id: response.data.iid,
      url: response.data.web_url,
      platform: 'gitlab'
    };
  }

  async getGitLabUserId(username) {
    // In production, cache this or use a mapping
    const response = await this.client.get(`/projects/${encodeURIComponent(this.config.project)}/users`);
    const user = response.data.find(u => u.username === username);
    return user?.id;
  }

  async validateConnection() {
    try {
      switch (this.platform) {
        case 'jira':
          await this.client.project.getProject({ projectIdOrKey: this.config.project });
          break;
        case 'github':
          const [owner, repo] = this.config.repo.split('/');
          await this.client.repos.get({ owner, repo });
          break;
        case 'gitlab':
          await this.client.get(`/projects/${encodeURIComponent(this.config.project)}`);
          break;
      }
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

module.exports = APIIntegrator;
```

### 4. Main Workflow

```javascript
// main.js
const MeetingParser = require('./text-parser');
const TicketGenerator = require('./ticket-generator');
const APIIntegrator = require('./api-integrator');

class MeetingEffectuator {
  constructor(config) {
    this.parser = new MeetingParser();
    this.generator = new TicketGenerator(config);
    this.integrator = config.platform 
      ? new APIIntegrator(config.platform, config[config.platform])
      : null;
  }

  async processMeetingNotes(notes, options = {}) {
    // 1. Parse meeting notes
    const parsed = await this.parser.parseMeetingNotes(notes);
    
    // 2. Generate tickets
    const tickets = this.generator.generateTickets(parsed);
    
    // 3. Create report
    const report = this.generateReport(parsed, tickets);
    
    // 4. Optionally create tickets in system
    let createdTickets = [];
    if (this.integrator && !options.dryRun) {
      createdTickets = await this.createTickets(tickets);
    }
    
    return {
      parsedNotes: parsed,
      generatedTickets: tickets,
      createdTickets,
      report
    };
  }

  async createTickets(tickets) {
    const results = [];
    
    for (const ticket of tickets) {
      try {
        const result = await this.integrator.createTicket(ticket);
        results.push({
          ...ticket,
          created: true,
          ticketId: result.id,
          ticketUrl: result.url,
          platform: result.platform
        });
      } catch (error) {
        results.push({
          ...ticket,
          created: false,
          error: error.message
        });
      }
    }
    
    return results;
  }

  generateReport(parsed, tickets) {
    const now = new Date().toISOString().split('T')[0];
    const highPriority = tickets.filter(t => t.priority === 'High' || t.priority === 'Highest');
    const mediumPriority = tickets.filter(t => t.priority === 'Medium');
    const lowPriority = tickets.filter(t => t.priority === 'Low' || t.priority === 'Lowest');
    
    return `# Meeting Effectuation Report - ${now}

## 📊 Summary
- **Action Items Found**: ${parsed.actionItems.length}
- **Tickets Generated**: ${tickets.length}
- **Decisions Recorded**: ${parsed.decisions.length}
- **High Priority**: ${highPriority.length}
- **Medium Priority**: ${mediumPriority.length}
- **Low Priority**: ${lowPriority.length}

## ✅ Tickets Generated

${tickets.map((ticket, index) => `
### ${index + 1}. ${ticket.title}
- **Assignee**: ${ticket.assignee}
- **Priority**: ${ticket.priority}
- **Due**: ${ticket.dueDate || 'Not specified'}
- **Type**: ${ticket.type}
- **Labels**: ${ticket.labels.join(', ')}
- **Confidence**: ${(ticket.metadata.confidence * 100).toFixed(0)}%

**Description**: ${ticket.description.split('\n')[0]}

**Original**: "${ticket.metadata.originalText}"`).join('')}

## 📋 Decisions Recorded

${parsed.decisions.map((decision, index) => `
${index + 1}. ${decision.decision} (Confidence: ${(decision.confidence * 100).toFixed(0)}%)`).join('')}

## 💡 Recommendations
1. Review generated tickets for accuracy
2. Clarify any low-confidence items with meeting participants
3. Set deadlines for items without clear timelines
4. Consider breaking large tasks into subtasks
5. Schedule follow-up to monitor progress
`;
  }

  async validateConfiguration() {
    if (!this.integrator) {
      return { valid: true, message: 'No API integration configured (dry run mode)' };
    }
    
    return this.integrator.validateConnection();
  }
}

module.exports = MeetingEffectuator;
```

## 🔄 Complete Workflow Example

```javascript
// example-usage.js
const MeetingEffectuator = require('./main');

async function exampleUsage() {
  // Configuration
  const config = {
    defaultAssignee: 'unassigned',
    platform: 'github',
    github: {
      token: process.env.GITHUB_TOKEN,
      repo: 'my-org/my-repo'
    }
  };

  // Meeting notes
  const meetingNotes = `
    # Sprint Planning Meeting
    
    ## Action Items
    - [ ] @alice Implement payment gateway by March 31 [High]
    - [ ] @bob Fix mobile login issues [Medium]
    - [ ] Update API documentation
    
    ## Decisions
    - Use both Stripe and PayPal for payments
    - Adopt mobile-first approach for new features
  `;

  // Create effectuator
  const effectuator = new MeetingEffectuator(config);

  // Process meeting notes
  const result = await effectuator.processMeetingNotes(meetingNotes);

  console.log(result.report);
  
  // In dry run mode (no actual ticket creation)
  // const dryRunResult = await effectuator.processMeetingNotes(meetingNotes, { dryRun: true });
}

exampleUsage().catch(console.error);
```

## 🎛️ Configuration

```javascript
// config.js
module.exports = {
  // Default settings
  defaultAssignee: 'team-lead',
  defaultPriority: 'Medium',
  defaultType: 'task',
  
  // Owner mapping
  ownerMapping: {
    'alice': 'alice.dev@company.com',
    'bob': 'bob.frontend@company.com',
    'charlie': 'charlie.qa@company.com',
    'diana': 'diana.pm@company.com'
  },
  
  // Priority mapping
  priorityMapping: {
    'high': 'High',
    'medium': 'Medium',
    'low': 'Low',
    'critical': 'Highest',
    'urgent': 'High',
    'important': 'High'
  },
  
  // Platform-specific configurations
  jira: {
    host: 'https://company.atlassian.net',
    email: 'bot@company.com',
    apiToken: process.env.JIRA_API_TOKEN,
    project: 'PROJ'
  },
  
  github: {
    token: process.env.GITHUB_TOKEN,
    repo: 'company/project-repo'
  },
  
  gitlab: {
    host: 'https://gitlab.company.com',
    token: process.env.GITLAB_TOKEN,
    project: 'company/project'
  }
};
```

## 🔌 Integration Patterns

### 1. CLI Tool

```javascript
#!/usr/bin/env node
// meeting-effectuator-cli.js

const { program } = require('commander');
const fs = require('fs');
const MeetingEffectuator = require('./main');

program
  .name('meeting-effectuator')
  .description('Convert meeting notes to tickets')
  .version('1.0.0')

program.command('process')
  .description('Process meeting notes')
  .option('-i, --input <path>', 'Input file path')
  .option('-o, --output <path>', 'Output report path')
  .option('-c, --config <path>', 'Config file path', 'config.js')
  .option('--dry-run', 'Dry run (no ticket creation)')
  .action(async (options) => {
    try {
      const config = require(options.config);
      const notes = options.input ? fs.readFileSync(options.input, 'utf8') : await getStdin();
      
      const effectuator = new MeetingEffectuator(config);
      const result = await effectuator.processMeetingNotes(notes, {
        dryRun: options.dryRun
      });
      
      if (options.output) {
        fs.writeFileSync(options.output, result.report);
        console.log(`Report written to ${options.output}`);
      } else {
        console.log(result.report);
      }
      
      if (result.createdTickets.length > 0) {
        console.log(`\nCreated ${result.createdTickets.length} tickets:`);
        result.createdTickets.forEach(ticket => {
          console.log(`- ${ticket.title}: ${ticket.ticketUrl}`);
        });
      }
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

function getStdin() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => resolve(data));
  });
}

program.parse();
```

### 2. GitHub Action

```yaml
# .github/workflows/meeting-effectuator.yml
name: Meeting Effectuator
on:
  issues:
    types: [labeled]

jobs:
  process-meeting:
    if: github.event.label.name == 'meeting-notes'
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
    
    - name: Install Meeting Effectuator
      run: npm install -g meeting-effectuator
    
    - name: Process meeting notes
      run: |
        NOTES="$(cat << 'EOF'
        ${issue.body}
        EOF
        )"
        meeting-effectuator process --input <(echo "$NOTES") --output report.md --dry-run
    
    - name: Comment with results
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('report.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: `## Meeting Effectuation Results\n\n${report}`
          });
```

### 3. Slack Integration

```javascript
// slack-integration.js
const { App } = require('@slack/bolt');
const MeetingEffectuator = require('./main');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET
});

const effectuator = new MeetingEffectuator(require('./config'));

app.command('/meeting-effectuate', async ({ command, ack, say }) => {
  await ack();
  
  try {
    const result = await effectuator.processMeetingNotes(command.text, { dryRun: true });
    
    await say({
      text: `Meeting Effectuation Results`,
      blocks: [
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Action Items Found*: ${result.parsedNotes.actionItems.length}`
          }
        },
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Tickets Generated*: ${result.generatedTickets.length}`
          }
        },
        {
          type: 'actions',
          elements: [
            {
              type: 'button',
              text: {
                type: 'plain_text',
                text: 'Create Tickets'
              },
              value: JSON.stringify(result.generatedTickets),
              action_id: 'create_tickets'
            }
          ]
        }
      ]
    });
  } catch (error) {
    await say(`Error: ${error.message}`);
  }
});

app.action('create_tickets', async ({ body, ack, say }) => {
  await ack();
  
  try {
    const tickets = JSON.parse(body.actions[0].value);
    const result = await effectuator.createTickets(tickets);
    
    const created = result.filter(t => t.created);
    await say(`✅ Created ${created.length} tickets successfully!`);
    
    created.forEach(ticket => {
      say(`<${ticket.ticketUrl}|${ticket.title}> assigned to ${ticket.assignee}`);
    });
  } catch (error) {
    await say(`❌ Failed to create tickets: ${error.message}`);
  }
});

(async () => {
  await app.start(process.env.PORT || 3000);
  console.log('⚡️ Meeting Effectuator Slack app is running!');
})();
```

## 🧪 Testing Strategy

### Unit Tests

```javascript
// meeting-effectuator.test.js
const MeetingEffectuator = require('./main');

describe('Meeting Effectuator', () => {
  describe('Text Parsing', () => {
    test('parses structured markdown', async () => {
      const effectuator = new MeetingEffectuator({});
      const notes = `
        # Meeting
        ## Action Items
        - [ ] @alice Task 1
      `;
      
      const result = await effectuator.processMeetingNotes(notes, { dryRun: true });
      expect(result.parsedNotes.actionItems.length).toBe(1);
      expect(result.parsedNotes.actionItems[0].owner).toBe('alice');
    });

    test('handles free-form text', async () => {
      const effectuator = new MeetingEffectuator({});
      const notes = 'Alice will implement the feature by Friday.';
      
      const result = await effectuator.processMeetingNotes(notes, { dryRun: true });
      expect(result.parsedNotes.actionItems.length).toBe(1);
    });
  });

  describe('Ticket Generation', () => {
    test('creates proper ticket structure', async () => {
      const effectuator = new MeetingEffectuator({});
      const notes = '- [ ] @alice Implement payment gateway by March 31 [High]';
      
      const result = await effectuator.processMeetingNotes(notes, { dryRun: true });
      const ticket = result.generatedTickets[0];
      
      expect(ticket.assignee).toBe('alice');
      expect(ticket.priority).toBe('High');
      expect(ticket.dueDate).toBe('2024-03-31'); // Assuming current year
    });
  });

  describe('Report Generation', () => {
    test('generates comprehensive report', async () => {
      const effectuator = new MeetingEffectuator({});
      const notes = `
        # Meeting
        ## Action Items
        - [ ] @alice Task 1 [High]
        ## Decisions
        - Decision 1
      `;
      
      const result = await effectuator.processMeetingNotes(notes, { dryRun: true });
      expect(result.report).toContain('Meeting Effectuation Report');
      expect(result.report).toContain('Action Items Found');
      expect(result.report).toContain('Decisions Recorded');
    });
  });
});
```

### Integration Tests

```javascript
// integration.test.js
const MeetingEffectuator = require('./main');
const nock = require('nock');

describe('Integration Tests', () => {
  test('creates GitHub issues successfully', async () => {
    const config = {
      platform: 'github',
      github: {
        token: 'test-token',
        repo: 'test-owner/test-repo'
      }
    };
    
    // Mock GitHub API
    nock('https://api.github.com')
      .post('/repos/test-owner/test-repo/issues')
      .reply(201, {
        number: 123,
        html_url: 'https://github.com/test-owner/test-repo/issues/123'
      });
    
    const effectuator = new MeetingEffectuator(config);
    const notes = '- [ ] @alice Implement feature [High]';
    
    const result = await effectuator.processMeetingNotes(notes);
    expect(result.createdTickets.length).toBe(1);
    expect(result.createdTickets[0].created).toBe(true);
    expect(result.createdTickets[0].ticketUrl).toContain('github.com');
  });

  test('handles API errors gracefully', async () => {
    const config = {
      platform: 'github',
      github: {
        token: 'bad-token',
        repo: 'test-owner/test-repo'
      }
    };
    
    // Mock failed API call
    nock('https://api.github.com')
      .post('/repos/test-owner/test-repo/issues')
      .reply(401, { message: 'Bad credentials' });
    
    const effectuator = new MeetingEffectuator(config);
    const notes = '- [ ] @alice Implement feature [High]';
    
    const result = await effectuator.processMeetingNotes(notes);
    expect(result.createdTickets.length).toBe(1);
    expect(result.createdTickets[0].created).toBe(false);
    expect(result.createdTickets[0].error).toContain('Bad credentials');
  });
});
```

## 📦 Deployment Options

### 1. NPM Package

```json
// package.json
{
  "name": "meeting-effectuator",
  "version": "1.0.0",
  "description": "Convert meeting notes to actionable tickets",
  "main": "dist/index.js",
  "bin": {
    "meeting-effectuator": "./dist/cli.js"
  },
  "scripts": {
    "build": "babel src --out-dir dist",
    "test": "jest",
    "pack": "npm run build && npm pack"
  },
  "keywords": ["meetings", "productivity", "tickets", "automation"],
  "dependencies": {
    "natural": "^6.0.0",
    "compromise": "^14.0.0",
    "markdown-it": "^13.0.0",
    "axios": "^1.0.0",
    "octokit": "^2.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "babel-cli": "^7.0.0",
    "nock": "^13.0.0"
  }
}
```

### 2. Docker Container

```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### 3. Serverless Function

```javascript
// AWS Lambda example
exports.handler = async (event) => {
  try {
    const { notes, config } = JSON.parse(event.body);
    const effectuator = new MeetingEffectuator(config);
    
    const result = await effectuator.processMeetingNotes(notes);
    
    return {
      statusCode: 200,
      body: JSON.stringify(result),
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

## 🔧 Optimization Techniques

### Performance Optimization

1. **Caching**: Cache NLP model and configurations
2. **Batching**: Process multiple meetings in batch
3. **Parallel Processing**: Use worker threads for large notes
4. **Incremental Updates**: Only re-process changed sections

```javascript
// Caching example
class CachedMeetingEffectuator extends MeetingEffectuator {
  constructor(config) {
    super(config);
    this.cache = new Map();
  }

  async processMeetingNotes(notes, options) {
    const cacheKey = hash(notes);
    
    if (this.cache.has(cacheKey) && !options.forceRefresh) {
      return this.cache.get(cacheKey);
    }
    
    const result = await super.processMeetingNotes(notes, options);
    this.cache.set(cacheKey, result);
    
    return result;
  }
}
```

### Accuracy Improvement

1. **Machine Learning**: Train on historical meeting data
2. **User Feedback**: Incorporate corrections over time
3. **Context Awareness**: Consider project context
4. **Continuous Learning**: Improve models with usage

```javascript
// Feedback incorporation
class LearningMeetingEffectuator extends MeetingEffectuator {
  constructor(config) {
    super(config);
    this.feedback = [];
  }

  recordFeedback(original, corrected) {
    this.feedback.push({ original, corrected });
    
    if (this.feedback.length >= 100) {
      this.retrainModel();
    }
  }

  retrainModel() {
    // Retrain NLP model with accumulated feedback
    // This would use the feedback to improve future parsing
  }
}
```

## 📚 Resources

### Natural Language Processing
- [Natural Node.js](https://github.com/NaturalNode/natural)
- [Compromise](https://github.com/spencermountain/compromise)
- [NLP.js](https://github.com/axa-group/nlp.js)
- [Stanford NLP](https://stanfordnlp.github.io/stanfordnlp/)

### API Integrations
- [Jira API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [GitHub API](https://docs.github.com/en/rest)
- [GitLab API](https://docs.gitlab.com/ee/api/)
- [Trello API](https://developer.atlassian.com/cloud/trello/rest/api-group-actions/)

### Meeting Note Formats
- [Markdown Guide](https://www.markdownguide.org/)
- [CommonMark Spec](https://commonmark.org/)
- [Meeting Note Templates](https://www.atlassian.com/team-playbook/plays/meeting-notes)

### Project Management
- [Agile Meeting Practices](https://www.scrumalliance.org/learn/about-scrum)
- [Effective Action Items](https://www.mindtools.com/pages/article/newTMM_07.htm)
- [SMART Criteria](https://en.wikipedia.org/wiki/SMART_criteria)

This implementation guide provides a comprehensive foundation for building the Meeting Effectuator skill with practical examples, integration patterns, and optimization strategies.
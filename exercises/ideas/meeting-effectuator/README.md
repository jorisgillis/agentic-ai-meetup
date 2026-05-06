# Meeting Effectuator: Turn Meeting Notes into Tickets

## 🎯 Overview

An agent skill that transforms meeting notes, action items, and
decisions into structured tickets, tasks, and documentation, ensuring
that meeting outcomes lead to concrete actions.

## 💡 Problem Statement

Meetings often produce valuable decisions and action items, but these
frequently get lost in notes or emails without proper
follow-through. Teams need a systematic way to convert meeting
outcomes into actionable tickets.

## ✨ Solution

The Meeting Effectuator skill analyzes meeting transcripts and notes
to extract action items, decisions, and follow-up tasks, then creates
properly structured tickets in project management systems.

## 🔧 Key Features

### 1. **Meeting Analysis**
- Parse meeting transcripts and notes
- Extract action items and owners
- Identify decisions and commitments
- Detect follow-up requirements
- Recognize deadlines and priorities

### 2. **Structured Output**
- Create well-formatted tickets
- Assign proper owners and labels
- Set appropriate priorities and deadlines
- Link related tickets and dependencies
- Generate clear descriptions and acceptance criteria

### 3. **Integration**
- Connect with Jira, GitHub Issues, GitLab
- Support multiple input formats (text, Markdown, documents)
- Handle different meeting styles and templates
- Provide confirmation and review workflows

### 4. **Intelligent Processing**
- Natural language understanding
- Context-aware ticket creation
- Duplicate detection
- Conflict resolution
- Priority inference

## 🎯 Use Cases

- **Agile Teams**: Convert sprint planning outcomes to tickets
- **Project Management**: Turn meeting decisions into actionable tasks
- **Executive Meetings**: Create follow-up tasks from strategic discussions
- **Client Meetings**: Generate tickets from requirement gatherings
- **Retrospectives**: Create improvement tickets from feedback

## 🔄 Workflow

```
1. Input meeting notes (text, document, or transcript)
2. Parse and analyze content for actionable items
3. Extract action items, owners, and deadlines
4. Identify related decisions and context
5. Generate structured ticket proposals
6. Review and confirm with user
7. Create tickets in target system
8. Provide summary and links
```

## 📊 Output Format

```markdown
# Meeting Effectuation Report

## Meeting Details
- **Date**: 2024-03-15
- **Participants**: Alice, Bob, Charlie, Diana
- **Duration**: 60 minutes
- **Topic**: Sprint Planning for Q2 2024

## 🎯 Action Items Converted to Tickets

### ✅ Ticket Created: IMP-42 - Implement New Payment Gateway
- **Assignee**: Alice (Backend Team)
- **Priority**: High
- **Due Date**: 2024-03-31
- **Description**: Integrate Stripe and PayPal payment gateways with existing checkout system
- **Acceptance Criteria**:
  - Stripe integration complete and tested
  - PayPal integration complete and tested
  - Payment processing works for both methods
  - Error handling implemented
- **Link**: [JIRA-42](https://jira.company.com/browse/IMP-42)
- **Source**: "Alice to implement new payment gateway by end of month"

### ✅ Ticket Created: BUG-17 - Fix Login Page Mobile Issues
- **Assignee**: Bob (Frontend Team)
- **Priority**: Medium
- **Due Date**: 2024-03-22
- **Description**: Resolve mobile responsiveness issues on login page reported in QA testing
- **Acceptance Criteria**:
  - Login page displays correctly on all mobile devices
  - All form elements are properly sized
  - Touch targets meet accessibility standards
  - Visual regression tests pass
- **Link**: [JIRA-17](https://jira.company.com/browse/BUG-17)
- **Source**: "Bob to fix mobile login issues - target next week"

### ⏳ Ticket Proposed: DOC-5 - Update API Documentation
- **Assignee**: Charlie (Documentation Team)
- **Priority**: Low
- **Due Date**: 2024-04-15
- **Description**: Update API documentation for v2.1 endpoints and add new examples
- **Acceptance Criteria**:
  - All new endpoints documented
  - Code examples added for each endpoint
  - Documentation reviewed by dev team
  - Published to developer portal
- **Status**: Awaiting confirmation
- **Source**: "Someone should update the API docs after the release"

## 📋 Decisions Recorded

1. **Payment Gateway Selection**: Decided to implement both Stripe and PayPal
   - Rationale: Customer demand and market coverage
   - Impact: Additional development time but better user experience

2. **Mobile First Approach**: All new features must be mobile-responsive by default
   - Rationale: 75% of traffic comes from mobile devices
   - Impact: Updated development guidelines

## 💬 Follow-up Items

1. **Architecture Review**: Schedule session to discuss payment gateway integration
   - **Owner**: Diana
   - **Action**: Send calendar invite to backend team

2. **Customer Feedback**: Gather requirements for payment gateway features
   - **Owner**: Alice
   - **Action**: Survey top 10 customers about payment preferences

## 📊 Statistics
- **Total Action Items**: 8 identified
- **Tickets Created**: 2
- **Tickets Proposed**: 1
- **Decisions Recorded**: 2
- **Follow-ups**: 2
- **Unclear Items**: 1 (needs clarification)

## 🔍 Analysis Notes
- **Ambiguous Item**: "Improve performance" - needs specific metrics and owner
- **Missing Deadline**: Documentation update has no clear timeline
- **Priority Conflict**: Mobile issues marked medium but mentioned as urgent

## 🎯 Recommendations
1. Review proposed tickets and confirm creation
2. Clarify ambiguous action items with meeting participants
3. Set deadlines for items without clear timelines
4. Resolve priority conflicts through discussion
5. Schedule follow-up meeting to review progress
```

## 🎯 Benefits

- **Increased Accountability**: Clear ownership of action items
- **Better Follow-through**: Meeting decisions lead to concrete actions
- **Improved Documentation**: Automatic recording of decisions
- **Time Savings**: Reduce manual ticket creation effort
- **Consistency**: Standardized ticket formats and structures
- **Traceability**: Link from tickets back to meeting sources

## 🔗 Integration

- **Input Sources**: Meeting transcripts, notes, recordings
- **Ticket Systems**: Jira, GitHub Issues, GitLab, Trello
- **Document Formats**: Markdown, Word, Google Docs, text
- **Communication**: Slack, Microsoft Teams, Email
- **Calendaring**: Google Calendar, Outlook, iCal

## 🚀 Getting Started

### Basic Usage

```bash
# Install the meeting effectuator
npm install -g meeting-effectuator

# Process meeting notes
meeting-effectuator process --input meeting-notes.md --output tickets.json

# Create tickets in Jira
meeting-effectuator create --jira --config jira-config.json --input tickets.json
```

### Example Input

```markdown
# Sprint Planning Meeting - 2024-03-15

## Attendees
- Alice (Backend Lead)
- Bob (Frontend Lead) 
- Charlie (QA)
- Diana (Product Manager)

## Action Items
- [ ] Alice: Implement new payment gateway by end of month (High Priority)
- [ ] Bob: Fix mobile login issues - target next week
- [ ] Charlie: Update API documentation after release
- [ ] Diana: Schedule architecture review for payment integration

## Decisions
- Proceed with both Stripe and PayPal integration
- Adopt mobile-first approach for all new features
- Target Q2 release for payment features

## Discussion Points
- Performance issues reported by customers
- Need to improve error handling in checkout flow
- Consider adding more payment options in future
```

## 📚 Supported Input Formats

### 1. Structured Markdown

```markdown
# Meeting Notes

## Action Items
- [ ] @alice Implement payment gateway by 2024-03-31 [High]
- [ ] @bob Fix mobile issues [Medium]

## Decisions
- Decision: Use Stripe and PayPal
  - Rationale: Customer demand
  - Impact: 2 weeks additional dev time
```

### 2. Free-form Text

```
During the meeting, Alice agreed to implement the payment gateway by the end of March. This is a high priority item. Bob will look into the mobile login issues that QA found last week - he thinks he can have this done by next Friday. We decided to go with both Stripe and PayPal to cover more customers, even though it will take a bit more time to implement both.
```

### 3. Meeting Transcripts

```
[00:12:35] Diana: Alice, can you take on the payment gateway implementation?
[00:12:42] Alice: Yes, I can have that done by end of month. It's high priority.
[00:15:20] Bob: I'll fix those mobile login issues QA reported. Should be done by next week.
[00:22:10] Charlie: We should update the API docs after this release.
[00:25:30] Diana: Team, we've decided to implement both Stripe and PayPal for better coverage.
```

## 🔧 Advanced Features

### Natural Language Processing
- **Entity Recognition**: Identify people, dates, priorities
- **Intent Analysis**: Distinguish actions from discussions
- **Context Understanding**: Relate items to projects and goals
- **Sentiment Analysis**: Detect urgency and importance

### Smart Ticket Creation
- **Template Matching**: Use appropriate ticket templates
- **Field Mapping**: Map meeting items to ticket fields
- **Dependency Detection**: Identify related tickets
- **Duplicate Prevention**: Check for existing similar tickets

### Workflow Automation
- **Automatic Assignment**: Assign tickets to mentioned owners
- **Deadline Calculation**: Set due dates based on context
- **Priority Inference**: Determine priority from language
- **Notification System**: Alert assignees of new tickets

### Quality Assurance
- **Ambiguity Detection**: Flag unclear action items
- **Completion Checking**: Verify all items processed
- **Conflict Resolution**: Handle conflicting information
- **Review Workflow**: Human-in-the-loop confirmation

## 📊 Success Metrics

- **Accuracy**: % of action items correctly identified
- **Completion Rate**: % of created tickets actually completed
- **Time Savings**: Hours saved vs manual ticket creation
- **Coverage**: % of meeting action items captured
- **User Satisfaction**: Team feedback on usefulness

## 🎯 Implementation Roadmap

### Phase 1: Core Functionality
- [ ] Basic text parsing and action item extraction
- [ ] Simple ticket creation workflow
- [ ] Markdown input/output support
- [ ] Basic error handling

### Phase 2: Advanced Processing
- [ ] Natural language understanding
- [ ] Context-aware ticket creation
- [ ] Priority and deadline inference
- [ ] Duplicate detection

### Phase 3: Integration
- [ ] Jira API integration
- [ ] GitHub Issues integration
- [ ] GitLab integration
- [ ] Slack/Teams notifications

### Phase 4: Enhancements
- [ ] Meeting transcript analysis
- [ ] Audio/video meeting processing
- [ ] Machine learning improvements
- [ ] Team-specific customization

## 🚀 Example Use Cases

### Use Case 1: Agile Sprint Planning

**Input**: Sprint planning meeting notes with user stories and tasks

**Output**:
- 12 well-structured Jira tickets
- Properly assigned to team members
- Linked to sprint and epic
- With clear acceptance criteria

**Result**: 40% faster sprint planning, better task clarity

### Use Case 2: Client Requirements Meeting

**Input**: Meeting notes from client requirement gathering

**Output**:
- 8 feature request tickets
- 3 bug report tickets  
- 1 documentation task
- All linked to client project

**Result**: No requirements lost, clear client communication

### Use Case 3: Incident Retrospective

**Input**: Post-mortem meeting notes from outage

**Output**:
- 5 improvement tickets for infrastructure
- 2 documentation update tasks
- 1 monitoring enhancement ticket
- All with clear owners and deadlines

**Result**: Systematic improvement from incidents

## 📚 Related Skills

- **Ticket Prep**: For creating well-structured tickets
- **PR Review**: For managing code review priorities
- **Documentation Drift Detector**: For keeping docs updated
- **Commit Ghostwriter**: For writing good commit messages

This Meeting Effectuator skill bridges the gap between discussions and
actions, ensuring that valuable meeting time translates into concrete
results and continuous progress.

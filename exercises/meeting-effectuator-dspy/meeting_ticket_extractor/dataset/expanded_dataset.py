# Expanded Dataset for Meeting Ticket Extractor
# Additional examples to create a more comprehensive dataset

additional_examples = [
    # Additional Well-Structured Meetings
    {
        "input": """Product Team Sync
Date: 2026-05-10

Decisions Made:
- Proceed with A/B test for new checkout flow
- Target launch date: June 15, 2026

Action Items:
- [Product Manager] Create A/B test plan - Due: 2026-05-12
- [Engineering] Implement checkout variations - Due: 2026-05-20
- [Marketing] Prepare launch materials - Due: 2026-06-01
- [Analytics] Set up tracking for A/B test - Due: 2026-05-18

Open Questions:
- Need to confirm pricing changes with finance team
- Should we include the new feature in the beta?""",
        "expected_tickets": [
            {
                "title": "Create A/B test plan",
                "description": "Develop comprehensive plan for checkout flow A/B test",
                "assignee": "Product Manager",
                "due_date": "2026-05-12",
                "priority": "High"
            },
            {
                "title": "Implement checkout variations",
                "description": "Develop different checkout flow variations for testing",
                "assignee": "Engineering",
                "due_date": "2026-05-20",
                "priority": "High"
            },
            {
                "title": "Prepare launch materials",
                "description": "Create marketing materials for June 15 launch",
                "assignee": "Marketing",
                "due_date": "2026-06-01",
                "priority": "Medium"
            },
            {
                "title": "Set up tracking for A/B test",
                "description": "Configure analytics tracking for checkout A/B test",
                "assignee": "Analytics",
                "due_date": "2026-05-18",
                "priority": "High"
            }
        ],
        "metadata": {
            "complexity": "structured",
            "domain": "product",
            "quality": "high"
        }
    },

    # Additional Semi-Structured Meetings
    {
        "input": """Design Team Standup - May 11, 2026

Quick updates from everyone:
- Sarah finished the mobile app wireframes and shared them in Slack
- Mike is working on the new icon set but needs feedback by EOD
- The client presented some concerns about the color palette during yesterday's call
- We should probably schedule a workshop to address the client's concerns
- Don't forget about the design system documentation that's due next week

Action Items from Last Meeting:
- [Done] Finalize logo variations
- [In Progress] Create style guide for new components
- [Blocked] Need content for about page""",
        "expected_tickets": [
            {
                "title": "Review mobile app wireframes",
                "description": "Team review of completed mobile app wireframes",
                "assignee": "Team",
                "due_date": "2026-05-12",
                "priority": "Medium"
            },
            {
                "title": "Provide feedback on icon set",
                "description": "Review and provide feedback on new icon designs",
                "assignee": "Team",
                "due_date": "2026-05-11",
                "priority": "High"
            },
            {
                "title": "Schedule client workshop on color palette",
                "description": "Organize workshop to address client concerns about colors",
                "assignee": "Unassigned",
                "due_date": "2026-05-15",
                "priority": "High"
            },
            {
                "title": "Complete design system documentation",
                "description": "Finalize and deliver design system documentation",
                "assignee": "Unassigned",
                "due_date": "2026-05-18",
                "priority": "Medium"
            }
        ],
        "metadata": {
            "complexity": "semi-structured",
            "domain": "design",
            "quality": "medium"
        }
    },

    # Additional Unstructured Conversational
    {
        "input": """Slack conversation in #engineering channel:

[10:15 AM] Alice: The CI pipeline is failing on the new feature branch. Can someone take a look?
[10:16 AM] Bob: I'm in a meeting right now but can check after lunch
[10:17 AM] Charlie: I think it might be the test database connection. The credentials might have changed
[10:18 AM] Alice: That makes sense. Charlie, can you verify the credentials?
[10:19 AM] Charlie: Sure, I'll check right now
[10:20 AM] Dave: Also, we should probably update the README with the new setup instructions
[10:21 AM] Alice: Good point Dave. And someone should notify the QA team about the pipeline issues
[10:22 AM] Bob: I can update the README after I fix the pipeline
[10:23 AM] Alice: Thanks everyone!""",
        "expected_tickets": [
            {
                "title": "Fix CI pipeline failure",
                "description": "Investigate and resolve CI pipeline issues on feature branch",
                "assignee": "Bob",
                "due_date": "2026-05-11",
                "priority": "High"
            },
            {
                "title": "Verify test database credentials",
                "description": "Check and update test database connection credentials",
                "assignee": "Charlie",
                "due_date": "2026-05-11",
                "priority": "High"
            },
            {
                "title": "Update README with new setup instructions",
                "description": "Add updated setup instructions to project README",
                "assignee": "Bob",
                "due_date": "2026-05-12",
                "priority": "Medium"
            },
            {
                "title": "Notify QA team about pipeline issues",
                "description": "Inform QA team about current CI pipeline problems",
                "assignee": "Alice",
                "due_date": "2026-05-11",
                "priority": "Medium"
            }
        ],
        "metadata": {
            "complexity": "unstructured",
            "domain": "software",
            "quality": "medium"
        }
    },

    # Additional Technical/Jargon-Heavy
    {
        "input": """DevOps Sync - Infrastructure Updates

Current Issues:
- The EKS cluster in us-west-2 is experiencing intermittent networking issues
- CloudFront cache invalidation is not working as expected after deployments
- Need to implement WAF rules for the new API endpoints
- The Terraform state file has drift that needs to be resolved

Action Items:
- Investigate EKS networking issues and check VPC flow logs (Network Team)
- Debug CloudFront cache invalidation process (Backend Team)
- Implement WAF rules for /api/v2/* endpoints with rate limiting (Security Team)
- Run terraform plan and apply to fix state drift (DevOps Team)
- Update the runbook with new incident response procedures (Documentation Team)

Upcoming:
- AWS re:Invent conference next month - who's interested in attending?""",
        "expected_tickets": [
            {
                "title": "Investigate EKS networking issues",
                "description": "Analyze and resolve intermittent networking problems in us-west-2 EKS cluster",
                "assignee": "Network Team",
                "due_date": "2026-05-15",
                "priority": "High"
            },
            {
                "title": "Debug CloudFront cache invalidation",
                "description": "Fix CloudFront cache invalidation issues after deployments",
                "assignee": "Backend Team",
                "due_date": "2026-05-14",
                "priority": "High"
            },
            {
                "title": "Implement WAF rules for API v2 endpoints",
                "description": "Add WAF rules with rate limiting for new API endpoints",
                "assignee": "Security Team",
                "due_date": "2026-05-18",
                "priority": "High"
            },
            {
                "title": "Fix Terraform state drift",
                "description": "Run terraform plan and apply to resolve state file drift",
                "assignee": "DevOps Team",
                "due_date": "2026-05-13",
                "priority": "High"
            },
            {
                "title": "Update incident response runbook",
                "description": "Add new incident response procedures to documentation",
                "assignee": "Documentation Team",
                "due_date": "2026-05-20",
                "priority": "Medium"
            }
        ],
        "metadata": {
            "complexity": "technical",
            "domain": "devops",
            "quality": "high"
        }
    },

    # Additional No Clear Action Items
    {
        "input": """Quarterly Business Review
Q2 2026 Results

Financial Highlights:
- Revenue grew 15% YoY
- Customer acquisition cost decreased by 8%
- Net promoter score improved to 68

Market Trends:
- Increased adoption of AI-powered tools in our sector
- Competitors launching similar features
- Economic uncertainty may impact enterprise spending

Customer Feedback:
- Generally positive about recent updates
- Some concerns about onboarding complexity
- Requests for more integration options

No specific action items identified - strategic planning session scheduled for next week""",
        "expected_tickets": [],
        "metadata": {
            "complexity": "no-actions",
            "domain": "business",
            "quality": "low"
        }
    }
]


def get_expanded_dataset():
    """Combine initial and additional examples for expanded dataset"""
    from meeting_ticket_extractor.dataset.initial_dataset import initial_dataset
    return initial_dataset + additional_examples


def get_complete_dataset():
    """Get the complete dataset with all examples"""
    expanded = get_expanded_dataset()
    print(f"Complete dataset contains {len(expanded)} examples")
    
    # Show distribution
    complexities = {}
    for example in expanded:
        complexity = example['metadata']['complexity']
        complexities[complexity] = complexities.get(complexity, 0) + 1
    
    print("Complexity distribution:")
    for complexity, count in complexities.items():
        print(f"  {complexity}: {count}")
    
    return expanded


if __name__ == "__main__":
    dataset = get_complete_dataset()
    
    # Test splitting
    from meeting_ticket_extractor.dataset.initial_dataset import split_dataset
    split_data = split_dataset(dataset)
    
    print(f"\nSplit dataset:")
    print(f"Train: {len(split_data['train'])} examples")
    print(f"Validation: {len(split_data['validation'])} examples")
    print(f"Test: {len(split_data['test'])} examples")
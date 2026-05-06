# Initial Dataset for Meeting Ticket Extractor
# Contains examples covering all complexity levels

initial_dataset = [
    # Category 1: Well-Structured Meetings (3 examples)
    {
        "input": """Project Kickoff Meeting
Date: 2026-05-06
Attendees: Product Team

Action Items:
- [Alice] Complete API design document - Due: 2026-05-13
- [Bob] Set up CI/CD pipeline - Due: 2026-05-10
- [Charlie] Schedule client demo - Due: 2026-05-15

Decisions:
- Use React for frontend development
- Target Q3 2026 for beta release""",
        "expected_tickets": [
            {
                "title": "Complete API design document",
                "description": "Create comprehensive API design documentation",
                "assignee": "Alice",
                "due_date": "2026-05-13",
                "priority": "High"
            },
            {
                "title": "Set up CI/CD pipeline",
                "description": "Configure continuous integration and deployment pipeline",
                "assignee": "Bob", 
                "due_date": "2026-05-10",
                "priority": "High"
            },
            {
                "title": "Schedule client demo",
                "description": "Coordinate and schedule demonstration for client",
                "assignee": "Charlie",
                "due_date": "2026-05-15", 
                "priority": "Medium"
            }
        ],
        "metadata": {
            "complexity": "structured",
            "domain": "software",
            "quality": "high"
        }
    },
    
    {
        "input": """Sprint Planning Session
Team: Development
Date: 2026-05-08

Tasks Assigned:
1. Fix login authentication bug (Alice) - ETA: 2 days
2. Update user profile page UI (Bob) - ETA: 3 days  
3. Write API documentation for new endpoints (Charlie) - ETA: 5 days
4. Set up monitoring for production errors (Team) - ETA: 1 week

Blockers:
- Waiting on design assets for profile page
- API documentation template needs approval""",
        "expected_tickets": [
            {
                "title": "Fix login authentication bug",
                "description": "Investigate and resolve login authentication issues",
                "assignee": "Alice",
                "due_date": "2026-05-10",
                "priority": "High"
            },
            {
                "title": "Update user profile page UI", 
                "description": "Implement new design for user profile interface",
                "assignee": "Bob",
                "due_date": "2026-05-11",
                "priority": "Medium"
            },
            {
                "title": "Write API documentation for new endpoints",
                "description": "Create comprehensive documentation for new API endpoints",
                "assignee": "Charlie",
                "due_date": "2026-05-13",
                "priority": "Medium"
            },
            {
                "title": "Set up monitoring for production errors",
                "description": "Implement error monitoring system for production environment",
                "assignee": "Team",
                "due_date": "2026-05-15",
                "priority": "High"
            }
        ],
        "metadata": {
            "complexity": "structured", 
            "domain": "software",
            "quality": "high"
        }
    },

    # Category 2: Semi-Structured Meetings (4 examples)
    {
        "input": """Team Sync Notes - May 6, 2026

- Alice mentioned the database migration needs to happen before the sprint review
- Bob will look into the performance issues reported by QA this week
- We should probably update the onboarding docs - maybe Charlie can handle this?
- Next sprint planning is on Wednesday at 2pm
- The API rate limiting issue should be fixed ASAP""",
        "expected_tickets": [
            {
                "title": "Complete database migration",
                "description": "Execute database migration before sprint review",
                "assignee": "Alice",
                "due_date": "2026-05-13",
                "priority": "High"
            },
            {
                "title": "Investigate performance issues",
                "description": "Analyze and resolve QA-reported performance problems",
                "assignee": "Bob",
                "due_date": "2026-05-13",
                "priority": "High"
            },
            {
                "title": "Update onboarding documentation",
                "description": "Review and revise onboarding materials",
                "assignee": "Charlie",
                "due_date": "2026-05-13",
                "priority": "Medium"
            },
            {
                "title": "Fix API rate limiting issue",
                "description": "Resolve API rate limiting problems",
                "assignee": "Unassigned",
                "due_date": "2026-05-07",
                "priority": "High"
            }
        ],
        "metadata": {
            "complexity": "semi-structured",
            "domain": "software",
            "quality": "medium"
        }
    },

    {
        "input": """Marketing Team Meeting
May 7, 2026

Discussion points:
* The new campaign launch is scheduled for June 1st
* Sarah needs to finalize the social media content calendar by Friday
* We should analyze the Q1 metrics - John can you take a look?
* Budget review shows we have some room for additional influencer partnerships
* Someone should coordinate with the design team about the new branding guidelines

Action items from last meeting:
- [Complete] Finalize target audience personas
- [In Progress] Create campaign landing page""",
        "expected_tickets": [
            {
                "title": "Finalize social media content calendar",
                "description": "Complete and approve content calendar for new campaign",
                "assignee": "Sarah",
                "due_date": "2026-05-12",
                "priority": "High"
            },
            {
                "title": "Analyze Q1 marketing metrics",
                "description": "Review and report on Q1 marketing performance",
                "assignee": "John",
                "due_date": "2026-05-14",
                "priority": "Medium"
            },
            {
                "title": "Coordinate with design team on branding guidelines",
                "description": "Align marketing materials with new branding standards",
                "assignee": "Unassigned",
                "due_date": "2026-05-14",
                "priority": "Medium"
            }
        ],
        "metadata": {
            "complexity": "semi-structured",
            "domain": "marketing",
            "quality": "medium"
        }
    },

    # Category 3: Unstructured Conversational (3 examples)  
    {
        "input": """Alice: Hey team, we really need to fix that memory leak in the data processor
Bob: Yeah, I noticed that too. Also, did anyone check the new user feedback?
Charlie: The feedback looks good overall, but there are some UI complaints about the dashboard
Alice: I can look at the memory leak tomorrow if that works for everyone?
Bob: Sounds good. Maybe we should also schedule a UI review session
Charlie: I'll ping the design team about that
Alice: Great, and someone should update the release notes before Friday
Bob: I can handle the release notes""",
        "expected_tickets": [
            {
                "title": "Fix memory leak in data processor",
                "description": "Investigate and resolve memory leak issue",
                "assignee": "Alice",
                "due_date": "2026-05-07",
                "priority": "High"
            },
            {
                "title": "Schedule UI review session",
                "description": "Coordinate with design team for dashboard review",
                "assignee": "Charlie",
                "due_date": "2026-05-10",
                "priority": "Medium"
            },
            {
                "title": "Update release notes",
                "description": "Review and update release documentation",
                "assignee": "Bob",
                "due_date": "2026-05-12",
                "priority": "Medium"
            }
        ],
        "metadata": {
            "complexity": "unstructured",
            "domain": "software",
            "quality": "medium"
        }
    },

    # Category 4: Technical/Jargon-Heavy (2 examples)
    {
        "input": """Architecture Review - Microservices Migration

Key Points:
- Need to implement circuit breakers for inter-service communication (Hystrix pattern)
- K8s cluster autoscale configuration requires adjustment - current HPA settings are suboptimal
- The new gRPC endpoints for the payment service need load testing before go-live
- Someone should verify the OpenTelemetry instrumentation covers all critical paths
- Database connection pooling parameters need optimization for the new read replicas

Action Items:
- [URGENT] Fix the circuit breaker implementation in the orders service
- Review the Prometheus alerts configuration""",
        "expected_tickets": [
            {
                "title": "Implement circuit breakers for inter-service communication",
                "description": "Add Hystrix pattern circuit breakers to microservices",
                "assignee": "Unassigned",
                "due_date": "2026-05-14",
                "priority": "High"
            },
            {
                "title": "Optimize K8s cluster autoscale configuration",
                "description": "Adjust HPA settings for better performance",
                "assignee": "Unassigned",
                "due_date": "2026-05-14",
                "priority": "High"
            },
            {
                "title": "Load test gRPC endpoints for payment service",
                "description": "Perform load testing on new payment service endpoints",
                "assignee": "Unassigned",
                "due_date": "2026-05-13",
                "priority": "High"
            },
            {
                "title": "Fix circuit breaker implementation in orders service",
                "description": "Resolve urgent circuit breaker issues",
                "assignee": "Unassigned",
                "due_date": "2026-05-07",
                "priority": "Critical"
            }
        ],
        "metadata": {
            "complexity": "technical",
            "domain": "software",
            "quality": "high"
        }
    },

    # Category 5: No Clear Action Items (2 examples)
    {
        "input": """Weekly Status Update - May 6, 2026

- Project timeline is on track for Q3 delivery
- Budget review shows we're under spending by 15%
- Client feedback on last demo was positive
- Team morale is good according to the latest survey
- No major blockers reported this week
- Next check-in scheduled for May 13""",
        "expected_tickets": [],
        "metadata": {
            "complexity": "no-actions",
            "domain": "general",
            "quality": "low"
        }
    },

    {
        "input": """Brainstorming Session: New Product Features
May 7, 2026

Ideas discussed:
- AI-powered recommendations for users
- Dark mode for the mobile app
- Integration with popular productivity tools
- Gamification elements for user engagement
- Advanced analytics dashboard

No decisions made - will follow up next week with prioritization""",
        "expected_tickets": [],
        "metadata": {
            "complexity": "no-actions",
            "domain": "product",
            "quality": "low"
        }
    }
]


def get_initial_dataset():
    """Return the initial dataset for development and testing"""
    return initial_dataset


def split_dataset(dataset, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """Split dataset into train, validation, and test sets"""
    import random
    
    # Shuffle the dataset
    random.shuffle(dataset)
    
    total = len(dataset)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    return {
        'train': dataset[:train_end],
        'validation': dataset[train_end:val_end],
        'test': dataset[val_end:]
    }


if __name__ == "__main__":
    # Test the dataset
    dataset = get_initial_dataset()
    print(f"Initial dataset size: {len(dataset)}")
    
    # Split and show distribution
    split_data = split_dataset(dataset)
    print(f"Train: {len(split_data['train'])} examples")
    print(f"Validation: {len(split_data['validation'])} examples")
    print(f"Test: {len(split_data['test'])} examples")
    
    # Show complexity distribution
    complexities = {}
    for example in dataset:
        complexity = example['metadata']['complexity']
        complexities[complexity] = complexities.get(complexity, 0) + 1
    
    print("\nComplexity distribution:")
    for complexity, count in complexities.items():
        print(f"  {complexity}: {count}")
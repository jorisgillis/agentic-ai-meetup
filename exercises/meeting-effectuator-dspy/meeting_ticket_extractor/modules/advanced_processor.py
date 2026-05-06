# Advanced Meeting Notes Processor
# Two-module architecture: Extraction + Formatting

import dspy
from typing import List, Dict

class ExtractActionsSignature(dspy.Signature):
    """Extract raw action items from meeting notes"""
    meeting_notes = dspy.InputField()
    raw_actions = dspy.OutputField(desc="""
        List of raw action items extracted from the meeting notes.
        Each item should be a dictionary with:
        - text: the raw action item text
        - context: surrounding context that helps understand the action
        - confidence: confidence score (0-1) that this is a real action item
        
        Include all potential action items, even if uncertain.
        The formatting module will refine them.
    """)

class FormatTicketsSignature(dspy.Signature):
    """Convert raw action items into structured tickets"""
    raw_actions = dspy.InputField()
    tickets = dspy.OutputField(desc="""
        List of structured tickets in JSON format. Each ticket should contain:
        - title: concise summary of the action item
        - description: detailed description of what needs to be done
        - assignee: person responsible (use 'Unassigned' if unclear)
        - due_date: deadline in YYYY-MM-DD format (use best estimate if not specified)
        - priority: High, Medium, or Low
        - confidence: confidence score (0-1) for this ticket
        
        Only include items that represent clear actionable tasks.
        Filter out low-confidence items from the extraction phase.
    """)

class AdvancedMeetingProcessor(dspy.Module):
    """Advanced two-module processor for extracting tickets from meeting notes"""
    
    def __init__(self):
        super().__init__()
        # Module 1: Extract raw action items
        self.extract_actions = dspy.ChainOfThought(ExtractActionsSignature)
        
        # Module 2: Format into structured tickets
        self.format_tickets = dspy.ChainOfThought(FormatTicketsSignature)
    
    def forward(self, meeting_notes):
        """Process meeting notes through the two-stage pipeline"""
        # Stage 1: Extract raw actions
        extraction_result = self.extract_actions(meeting_notes=meeting_notes)
        raw_actions = extraction_result.raw_actions
        
        # Stage 2: Format into tickets
        formatting_result = self.format_tickets(raw_actions=raw_actions)
        
        return formatting_result

class PriorityAnalyzer(dspy.Module):
    """Module for analyzing and assigning priorities to tickets"""
    
    def __init__(self):
        super().__init__()
        self.analyze_priority = dspy.Predict("ticket -> priority_analysis")
    
    def forward(self, tickets):
        """Analyze priorities for a list of tickets"""
        prioritized_tickets = []
        
        for ticket in tickets:
            # Analyze priority for each ticket
            analysis = self.analyze_priority(ticket=ticket)
            
            # Add priority to the ticket
            prioritized_ticket = {**ticket, 'priority': analysis.priority_analysis}
            prioritized_tickets.append(prioritized_ticket)
        
        return prioritized_tickets

class CompleteMeetingProcessor(dspy.Module):
    """Complete processing pipeline with extraction, formatting, and prioritization"""
    
    def __init__(self):
        super().__init__()
        self.extractor = AdvancedMeetingProcessor()
        self.prioritizer = PriorityAnalyzer()
    
    def forward(self, meeting_notes):
        """Complete processing pipeline"""
        # Extract and format tickets
        result = self.extractor(meeting_notes)
        tickets = result.tickets
        
        # Analyze priorities
        prioritized_tickets = self.prioritizer(tickets)
        
        # Return the result with prioritized tickets
        return dspy.Prediction(tickets=prioritized_tickets)

def create_advanced_training_examples(dataset):
    """Create training examples for the advanced processor"""
    examples = []
    
    for example in dataset:
        # Create example for the complete pipeline
        dspy_example = dspy.Example(
            meeting_notes=example["input"],
            tickets=example["expected_tickets"]
        ).with_inputs("meeting_notes")
        examples.append(dspy_example)
    
    return examples

def test_advanced_processor():
    """Test the advanced processor structure"""
    print("Testing Advanced Processor...")
    
    # Create processor
    processor = AdvancedMeetingProcessor()
    print("✓ Extraction module initialized")
    
    complete_processor = CompleteMeetingProcessor()
    print("✓ Complete processor (with prioritization) initialized")
    
    # Test with sample input
    test_notes = """
    Engineering Team Meeting
    - Fix critical security vulnerability in auth system (Alice) - ASAP
    - Update API documentation for new endpoints (Bob) - This week
    - Schedule code review for the new feature (Charlie) - Next Monday
    - Research performance optimization options - Low priority
    """
    
    print(f"✓ Test input prepared ({len(test_notes)} characters)")
    print("\nProcessor structure:")
    print("1. ExtractActionsSignature -> raw action items")
    print("2. FormatTicketsSignature -> structured tickets")
    print("3. PriorityAnalyzer -> prioritized tickets")
    
    return processor, complete_processor

if __name__ == "__main__":
    # Test the advanced processor
    extractor, complete = test_advanced_processor()
    
    print("\nAdvanced processor ready!")
    print("Features:")
    print("- Two-stage processing (extraction + formatting)")
    print("- Priority analysis module")
    print("- Confidence scoring at each stage")
    print("- Better handling of ambiguous action items")
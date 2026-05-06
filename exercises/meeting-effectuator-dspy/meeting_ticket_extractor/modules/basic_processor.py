# Basic Meeting Notes Processor
# Single-module implementation using DSPy ChainOfThought

import dspy
import re
from typing import List, Dict

class Ticket(dspy.Signature):
    """Extract actionable tickets from meeting notes"""
    meeting_notes = dspy.InputField()
    tickets = dspy.OutputField(desc="""
        List of extracted tickets in JSON format. Each ticket should contain:
        - title: concise summary of the action item
        - description: detailed description of what needs to be done  
        - assignee: person responsible (use 'Unassigned' if unclear)
        - due_date: deadline in YYYY-MM-DD format (use best estimate if not specified)
        - priority: High, Medium, or Low
        
        Only include items that represent clear actionable tasks.
        Return empty list if no action items are found.
        """)

class BasicMeetingProcessor(dspy.Module):
    """Basic single-module processor for extracting tickets from meeting notes"""
    
    def __init__(self):
        super().__init__()
        # Use ChainOfThought for better reasoning
        self.extract_tickets = dspy.ChainOfThought(Ticket)
    
    def forward(self, meeting_notes):
        """Process meeting notes and extract tickets"""
        result = self.extract_tickets(meeting_notes=meeting_notes)
        
        # Parse tickets - handle different response formats
        tickets = result.tickets
        
        # Handle JSON string responses (including markdown formatted)
        if isinstance(tickets, str):
            # Remove markdown code blocks if present
            tickets_str = tickets.strip()
            if tickets_str.startswith('```json'):
                tickets_str = '\n'.join(tickets_str.split('\n')[1:-1])  # Remove first and last lines
            elif tickets_str.startswith('```'):
                tickets_str = '\n'.join(tickets_str.split('\n')[1:-1])
            
            # Clean up the string for JSON parsing
            # Remove inline comments (// ...)
            tickets_str = re.sub(r'\s*//.*$', '', tickets_str, flags=re.MULTILINE)
            # Remove standalone comment lines
            tickets_str = '\n'.join(
                line for line in tickets_str.split('\n') 
                if line.strip() and not line.strip().startswith('//')
            )
            
            # Convert Python-style single quotes to JSON double quotes
            if "'" in tickets_str and "{" in tickets_str:
                tickets_str = tickets_str.replace("'", '"')
            
            # Try to extract valid JSON - sometimes Mistral returns multiple objects
            try:
                import json
                # Try to find the first valid JSON array in the string
                start_idx = tickets_str.find('[')
                if start_idx != -1:
                    # Try to find matching closing bracket
                    brace_count = 0
                    end_idx = start_idx
                    for i, char in enumerate(tickets_str[start_idx:]):
                        if char == '[':
                            brace_count += 1
                        elif char == ']':
                            brace_count -= 1
                            if brace_count == 0:
                                end_idx = start_idx + i + 1
                                break
                    
                    if end_idx > start_idx:
                        json_part = tickets_str[start_idx:end_idx]
                        tickets = json.loads(json_part)
                    else:
                        tickets = json.loads(tickets_str)
                else:
                    tickets = json.loads(tickets_str)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                print(f"Failed to parse: {tickets_str[:200]}...")  # Show first 200 chars
                tickets = []
        
        # Ensure tickets is always a list
        if not isinstance(tickets, list):
            tickets = [tickets] if tickets else []
        
        return dspy.Prediction(tickets=tickets)

class MeetingProcessorWithFewShot:
    """Meeting processor with few-shot learning capabilities"""
    
    def __init__(self, train_examples=None):
        self.processor = BasicMeetingProcessor()
        self.train_examples = train_examples or []
    
    def process(self, meeting_notes):
        """Process meeting notes through the pipeline"""
        return self.processor(meeting_notes)
    
    def optimize(self, metric=None, num_threads=4):
        """Optimize the processor using few-shot learning"""
        if not self.train_examples:
            print("Warning: No training examples provided for optimization")
            return self.processor
        
        # Set up the optimizer - using BootstrapFewShot from dspy
        optimizer = dspy.BootstrapFewShot(
            metric=metric or self.default_metric,
            max_bootstrapped_demos=3,
            max_labeled_demos=3
        )
        
        # Compile the optimized processor
        optimized_processor = optimizer.compile(
            self.processor,
            trainset=self.train_examples,
            num_threads=num_threads
        )
        
        return optimized_processor
    
    @staticmethod
    def default_metric(example, pred, trace=None):
        """Default evaluation metric for ticket extraction"""
        # Simple metric: check if we extracted the right number of tickets
        expected_count = len(example.expected_tickets)
        predicted_count = len(pred.tickets) if pred.tickets else 0
        
        # Basic accuracy - this will be enhanced later
        return predicted_count == expected_count

def create_training_examples(dataset):
    """Convert dataset to DSPy training examples"""
    examples = []
    for example in dataset:
        dspy_example = dspy.Example(
            meeting_notes=example["input"],
            tickets=example["expected_tickets"]
        ).with_inputs("meeting_notes")
        examples.append(dspy_example)
    return examples

def test_basic_processor():
    """Test the basic processor with sample input"""
    # Initialize processor
    processor = BasicMeetingProcessor()
    
    # Test with a simple example
    test_notes = """
    Team Meeting Notes
    - Alice to fix login bug by Friday
    - Bob will update documentation this week
    - Schedule team building event for next month
    """
    
    print("Basic Processor Test:")
    print(f"Input: {test_notes}")
    print("Processor initialized successfully")
    print("Note: Actual processing requires LM configuration")
    
    # Return the processor instead of result since we can't run without LM
    return processor

if __name__ == "__main__":
    # Test the basic processor
    result = test_basic_processor()
    print("\nTest completed successfully!")
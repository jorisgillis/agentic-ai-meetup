# Main Application for Meeting Ticket Extractor

import os
import sys
from dataset.initial_dataset import get_initial_dataset, split_dataset
from modules.basic_processor import BasicMeetingProcessor, MeetingProcessorWithFewShot, create_training_examples
from evaluation.metrics import evaluate_processor, print_evaluation_summary, create_dspy_metric_function
from utils.config import configure_lm

def main():
    """Main application entry point"""
    print("=== Meeting Ticket Extractor ===")
    print("DSPy-based agent for extracting actionable tickets from meeting notes")
    print()
    
    # Load configuration
    try:
        configure_lm("mock")  # Using mock for now
        print("Configuration loaded successfully")
    except Exception as e:
        print(f"Configuration error: {e}")
        return 1
    
    # Load dataset
    dataset = get_initial_dataset()
    print(f"Loaded dataset with {len(dataset)} examples")
    
    # Split dataset
    split_data = split_dataset(dataset)
    print(f"Dataset split: Train={len(split_data['train'])}, Val={len(split_data['validation'])}, Test={len(split_data['test'])}")
    
    # Create processor
    processor = BasicMeetingProcessor()
    print("Processor initialized")
    
    # Test with a sample
    sample_input = split_data['test'][0]['input']
    print("\n=== Sample Processing ===")
    print("Input:")
    print(sample_input[:200] + "..." if len(sample_input) > 200 else sample_input)
    
    # Note: Can't actually run without real LM, but structure is ready
    print("Processor ready for execution (requires real LM)")
    
    # Show evaluation framework
    print("\n=== Evaluation Framework ===")
    print("Metrics available:")
    print("- Precision/Recall/F1 for ticket extraction")
    print("- Field-level accuracy (assignee, due_date, priority, description)")
    print("- Overall accuracy and detailed per-example analysis")
    
    # Show optimization capabilities
    print("\n=== Optimization Capabilities ===")
    print("Available optimization methods:")
    print("- BootstrapFewShot for prompt improvement")
    print("- Custom metric functions for DSPy optimization")
    print("- Field-level accuracy tracking")
    
    return 0

def demo_evaluation():
    """Demonstrate the evaluation framework"""
    print("\n=== Evaluation Demo ===")
    
    # Create sample data for demo
    demo_expected = [
        {"title": "Fix login bug", "assignee": "Alice", "priority": "High", "due_date": "2026-05-10"},
        {"title": "Update documentation", "assignee": "Bob", "priority": "Medium", "due_date": "2026-05-12"}
    ]
    
    demo_predicted = [
        {"title": "Fix login bug", "assignee": "Alice", "priority": "High", "due_date": "2026-05-10"},
        {"title": "Write documentation", "assignee": "Bob", "priority": "Medium", "due_date": "2026-05-12"}
    ]
    
    # Calculate metrics
    from evaluation.metrics import calculate_precision_recall, calculate_field_accuracy
    
    pr_metrics = calculate_precision_recall(demo_expected, demo_predicted)
    field_metrics = calculate_field_accuracy(demo_expected, demo_predicted)
    
    print(f"Precision: {pr_metrics['precision']:.2f}")
    print(f"Recall: {pr_metrics['recall']:.2f}")
    print(f"F1 Score: {pr_metrics['f1_score']:.2f}")
    print(f"Field Accuracy: {field_metrics}")

def show_usage_examples():
    """Show usage examples"""
    print("\n=== Usage Examples ===")
    
    examples = [
        {
            "name": "Basic Processing",
            "code": """
from modules.basic_processor import BasicMeetingProcessor
from utils.config import configure_lm

# Configure LM
configure_lm("openai", model="gpt-3.5-turbo")

# Create processor
processor = BasicMeetingProcessor()

# Process meeting notes
meeting_notes = "Alice to fix bug by Friday..."
result = processor(meeting_notes)
print(result.tickets)
"""
        },
        {
            "name": "Evaluation",
            "code": """
from evaluation.metrics import evaluate_processor
from dataset.initial_dataset import get_initial_dataset

# Load test data
test_data = get_initial_dataset()[:3]  # Use first 3 examples

# Evaluate processor
evaluation = evaluate_processor(processor, test_data, detailed=True)
print_evaluation_summary(evaluation)
"""
        },
        {
            "name": "Optimization",
            "code": """
from modules.basic_processor import MeetingProcessorWithFewShot
from dataset.initial_dataset import get_initial_dataset

# Create training examples
train_examples = create_training_examples(get_initial_dataset()[:5])

# Create and optimize processor
processor = MeetingProcessorWithFewShot(train_examples)
optimized = processor.optimize()

# Use optimized processor
result = optimized("Meeting notes here...")
"""
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}: {example['name']}")
        print(example['code'])

if __name__ == "__main__":
    # Run main application
    result = main()
    
    # Show additional demos
    demo_evaluation()
    show_usage_examples()
    
    sys.exit(result)
# Comprehensive Evaluation with Mistral AI

from utils.config import configure_lm, load_environment
from modules.basic_processor import BasicMeetingProcessor, create_training_examples
from evaluation.metrics import evaluate_processor, print_evaluation_summary, create_dspy_metric_function
from dataset.expanded_dataset import get_complete_dataset
from dataset.initial_dataset import split_dataset
import os

def evaluate_with_mistral():
    """Run comprehensive evaluation using Mistral AI"""
    print("=== Comprehensive Evaluation with Mistral AI ===")
    
    # Check API key
    load_environment()
    mistral_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_key or mistral_key == "your-mistral-api-key-here":
        print("⚠️  Mistral API key not configured")
        print("Please add your MISTRAL_API_KEY to the .env file")
        return False
    
    # Configure Mistral LM
    print("Configuring Mistral LM...")
    try:
        configure_lm("mistral", model="mistral-tiny")
        print("✓ Mistral LM configured")
    except Exception as e:
        print(f"❌ Failed to configure Mistral: {e}")
        return False
    
    # Load complete dataset
    print("\nLoading dataset...")
    dataset = get_complete_dataset()
    split_data = split_dataset(dataset)
    
    print(f"Dataset: {len(dataset)} total examples")
    print(f"Train: {len(split_data['train'])} | Val: {len(split_data['validation'])} | Test: {len(split_data['test'])}")
    
    # Create processor
    processor = BasicMeetingProcessor()
    print("✓ Processor initialized")
    
    # Run evaluation on test set
    print(f"\nEvaluating on {len(split_data['test'])} test examples...")
    
    evaluation_results = evaluate_processor(
        processor, 
        split_data['test'], 
        detailed=True
    )
    
    # Print summary
    print_evaluation_summary(evaluation_results)
    
    # Show detailed results for each example
    print(f"\n=== Detailed Results ({len(evaluation_results['detailed_results'])} examples) ===")
    
    for i, result in enumerate(evaluation_results['detailed_results'], 1):
        print(f"\nExample {i} ({result['metadata']['complexity']}):")
        print(f"Expected: {len(result['expected'])} tickets")
        print(f"Extracted: {len(result['predicted'])} tickets")
        
        metrics = result['metrics']
        print(f"Precision: {metrics['precision']:.2f}")
        print(f"Recall: {metrics['recall']:.2f}")
        print(f"F1: {metrics['f1_score']:.2f}")
        
        # Show field accuracy if available
        if 'field_accuracy' in metrics:
            field_acc = metrics['field_accuracy']
            print(f"Field Accuracy - Assignee: {field_acc.get('assignee_accuracy', 0):.2f}")
    
    return evaluation_results

def test_optimization_readiness():
    """Test if the processor is ready for optimization"""
    print("\n=== Optimization Readiness Test ===")
    
    # Load dataset
    dataset = get_complete_dataset()
    
    # Create training examples
    train_examples = create_training_examples(dataset[:5])  # Use first 5 for quick test
    
    print(f"Created {len(train_examples)} training examples")
    
    # Test DSPy metric function
    metric_func = create_dspy_metric_function()
    
    if train_examples:
        sample = train_examples[0]
        # Create a mock prediction for testing
        class MockPrediction:
            def __init__(self, tickets):
                self.tickets = tickets
        
        mock_pred = MockPrediction(sample.tickets)  # Use expected as predicted for test
        score = metric_func(sample, mock_pred)
        
        print(f"Metric function test score: {score:.2f}")
        print("✓ Optimization components ready")
    
    return True

def compare_models():
    """Compare different Mistral models (if multiple keys available)"""
    print("\n=== Model Comparison ===")
    
    models = [
        ("mistral-tiny", "Fast, cost-effective"),
        ("mistral-small", "Balanced performance"),
        ("mistral-medium", "Higher quality"),
    ]
    
    print("Available Mistral models for comparison:")
    for model, description in models:
        print(f"- {model}: {description}")
    
    print("\nNote: Model availability depends on your Mistral API plan")
    print("To compare models, run this script with different model names")

if __name__ == "__main__":
    print("Mistral AI Evaluation")
    print("=" * 50)
    
    # Run main evaluation
    results = evaluate_with_mistral()
    
    if results:
        # Test optimization readiness
        test_optimization_readiness()
        
        # Show model comparison info
        compare_models()
        
        print("\n" + "=" * 50)
        print("✅ Evaluation completed successfully!")
        
        overall = results['overall']
        print(f"\nSummary:")
        print(f"- Accuracy: {overall['accuracy']:.2f}")
        print(f"- Avg Precision: {overall['average_precision']:.2f}")
        print(f"- Avg Recall: {overall['average_recall']:.2f}")
        print(f"- Avg F1 Score: {overall['average_f1']:.2f}")
        
        print(f"\nNext steps:")
        print(f"1. Run optimization with BootstrapFewShot")
        print(f"2. Test with different Mistral models")
        print(f"3. Expand dataset for better coverage")
        print(f"4. Fine-tune prompts based on evaluation results")
    else:
        print("\n" + "=" * 50)
        print("❌ Evaluation failed")
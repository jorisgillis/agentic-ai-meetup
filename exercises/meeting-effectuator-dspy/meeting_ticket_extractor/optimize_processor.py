# DSPy Optimization with BootstrapFewShot

from utils.config import configure_lm, load_environment
from modules.basic_processor import BasicMeetingProcessor, create_training_examples
from evaluation.metrics import create_dspy_metric_function, evaluate_processor
from dataset.expanded_dataset import get_complete_dataset
from dataset.initial_dataset import split_dataset
import dspy
import os
import argparse

def optimize_with_bootstrap_fewshot(model_name="mistral-tiny", max_bootstrapped_demos=4, max_labeled_demos=8):
    """Optimize processor using BootstrapFewShot"""
    print(f"=== BootstrapFewShot Optimization ({model_name}) ===")
    
    # Load environment and configure LM
    load_environment()
    configure_lm("mistral", model=model_name)
    
    # Load dataset
    print("Loading dataset...")
    dataset = get_complete_dataset()
    split_data = split_dataset(dataset)
    
    print(f"Dataset: {len(dataset)} examples")
    print(f"Train: {len(split_data['train'])} | Val: {len(split_data['validation'])} | Test: {len(split_data['test'])}")
    
    # Create training examples
    train_examples = create_training_examples(split_data['train'])
    val_examples = create_training_examples(split_data['validation'])
    
    print(f"Created {len(train_examples)} training examples")
    print(f"Created {len(val_examples)} validation examples")
    
    # Create metric function
    metric_func = create_dspy_metric_function()
    
    # Set up optimizer
    print(f"\nConfiguring BootstrapFewShot optimizer...")
    print(f"Max bootstrapped demos: {max_bootstrapped_demos}")
    print(f"Max labeled demos: {max_labeled_demos}")
    
    optimizer = dspy.BootstrapFewShot(
        metric=metric_func,
        max_bootstrapped_demos=max_bootstrapped_demos,
        max_labeled_demos=max_labeled_demos
    )
    
    # Create processor to optimize
    processor = BasicMeetingProcessor()
    
    # Compile with optimizer
    print("Starting optimization...")
    try:
        compiled_processor = optimizer.compile(
            student=processor,
            trainset=train_examples
        )
        
        print("✅ Optimization completed successfully!")
        
        # Save the optimized processor
        compiled_processor.save("optimized_processor.json")
        print("✅ Saved optimized processor to optimized_processor.json")
        
        return compiled_processor
        
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def optimize_with_mirov2(model_name="mistral-tiny", max_rounds=3):
    """Optimize processor using MIPROv2"""
    print(f"=== MIPROv2 Optimization ({model_name}) ===")
    
    # Load environment and configure LM
    load_environment()
    configure_lm("mistral", model=model_name)
    
    # Load dataset
    print("Loading dataset...")
    dataset = get_complete_dataset()
    split_data = split_dataset(dataset)
    
    # Create training examples
    train_examples = create_training_examples(split_data['train'])
    
    # Create metric function
    metric_func = create_dspy_metric_function()
    
    # Set up MIPROv2 optimizer
    print(f"Configuring MIPROv2 optimizer...")
    print(f"Max rounds: {max_rounds}")
    
    optimizer = dspy.MIPROv2(
        metric=metric_func,
        max_rounds=max_rounds
    )
    
    # Create processor to optimize
    processor = BasicMeetingProcessor()
    
    # Compile with optimizer
    print("Starting optimization...")
    try:
        compiled_processor = optimizer.compile(
            student=processor,
            trainset=train_examples
        )
        
        print("✅ MIPROv2 optimization completed successfully!")
        
        # Save the optimized processor
        compiled_processor.save("optimized_processor_mirov2.json")
        print("✅ Saved optimized processor to optimized_processor_mirov2.json")
        
        return compiled_processor
        
    except Exception as e:
        print(f"❌ MIPROv2 optimization failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_models_on_test_set():
    """Compare different Mistral models on test dataset"""
    print("=== Model Comparison on Test Set ===")
    
    # Load environment
    load_environment()
    
    # Models to test
    models = [
        ("mistral-tiny", "Fast, cost-effective"),
        ("mistral-small", "Balanced performance"),
        # "mistral-medium" requires higher tier API access
    ]
    
    # Load dataset
    dataset = get_complete_dataset()
    split_data = split_dataset(dataset)
    test_examples = create_training_examples(split_data['test'])
    
    print(f"Testing on {len(test_examples)} examples")
    
    results = {}
    
    for model_name, description in models:
        print(f"\n--- Testing {model_name} ({description}) ---")
        
        try:
            # Configure model
            configure_lm("mistral", model=model_name)
            
            # Create processor
            processor = BasicMeetingProcessor()
            
            # Evaluate
            evaluation = evaluate_processor(processor, split_data['test'], detailed=False)
            
            overall = evaluation['overall']
            results[model_name] = {
                'accuracy': overall['accuracy'],
                'precision': overall['average_precision'],
                'recall': overall['average_recall'],
                'f1': overall['average_f1'],
                'processing_time': evaluation.get('processing_time', 'N/A')
            }
            
            print(f"Accuracy: {overall['accuracy']:.3f}")
            print(f"Precision: {overall['average_precision']:.3f}")
            print(f"Recall: {overall['average_recall']:.3f}")
            print(f"F1 Score: {overall['average_f1']:.3f}")
            print(f"✅ {model_name} test completed")
            
        except Exception as e:
            print(f"❌ Failed to test {model_name}: {e}")
            results[model_name] = {'error': str(e)}
    
    # Summary
    print(f"\n=== Model Comparison Summary ===")
    print(f"{'Model':<15} {'Accuracy':<10} {'F1':<8} {'Time':<10}")
    print("-" * 50)
    
    for model_name, result in results.items():
        if 'error' in result:
            print(f"{model_name:<15} {'ERROR':<10} {'-':<8} {'-':<10}")
        else:
            print(f"{model_name:<15} {result['accuracy']:.3f}    {result['f1']:.3f}    {result['processing_time']}")
    
    # Recommend best model
    valid_results = {k: v for k, v in results.items() if 'error' not in v}
    if valid_results:
        best_model = max(valid_results.items(), key=lambda x: x[1]['f1'])
        print(f"\n🎯 Recommended model: {best_model[0]} (F1: {best_model[1]['f1']:.3f})")
    
    return results

def evaluate_optimized_processor(processor_path="optimized_processor.json"):
    """Evaluate a saved optimized processor"""
    print(f"=== Evaluating Optimized Processor ({processor_path}) ===")
    
    try:
        # Load optimized processor
        processor = BasicMeetingProcessor()
        processor.load(processor_path)
        
        # Load test data
        dataset = get_complete_dataset()
        split_data = split_dataset(dataset)
        
        # Evaluate
        evaluation = evaluate_processor(processor, split_data['test'], detailed=True)
        
        # Print results
        from evaluation.metrics import print_evaluation_summary
        print_evaluation_summary(evaluation)
        
        return evaluation
        
    except Exception as e:
        print(f"❌ Failed to evaluate optimized processor: {e}")
        return None

def main():
    """Main optimization workflow"""
    parser = argparse.ArgumentParser(description="DSPy Processor Optimization")
    parser.add_argument("--method", choices=["bootstrap", "mirov2", "compare", "evaluate"], 
                       default="bootstrap", help="Optimization method")
    parser.add_argument("--model", default="mistral-tiny", help="Mistral model to use")
    parser.add_argument("--demos", "--max_bootstrapped_demos", type=int, default=4, 
                       help="Max bootstrapped demos for BootstrapFewShot")
    parser.add_argument("--labelled", "--max_labeled_demos", type=int, default=8, 
                       help="Max labeled demos for BootstrapFewShot")
    parser.add_argument("--rounds", type=int, default=3, help="Max rounds for MIPROv2")
    
    args = parser.parse_args()
    
    print("DSPy Processor Optimization")
    print("=" * 50)
    
    if args.method == "bootstrap":
        optimize_with_bootstrap_fewshot(
            model_name=args.model,
            max_bootstrapped_demos=args.demos,
            max_labeled_demos=args.labelled
        )
    
    elif args.method == "mirov2":
        optimize_with_mirov2(
            model_name=args.model,
            max_rounds=args.rounds
        )
    
    elif args.method == "compare":
        compare_models_on_test_set()
    
    elif args.method == "evaluate":
        evaluate_optimized_processor()

if __name__ == "__main__":
    main()
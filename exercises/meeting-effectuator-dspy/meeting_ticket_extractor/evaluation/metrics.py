# Evaluation Metrics for Meeting Ticket Extractor

import json
from typing import List, Dict, Any
from datetime import datetime

def calculate_precision_recall(expected_tickets, predicted_tickets):
    """
    Calculate precision and recall for ticket extraction
    
    Args:
        expected_tickets: List of expected ticket dictionaries
        predicted_tickets: List of predicted ticket dictionaries
        
    Returns:
        dict: precision, recall, f1_score
    """
    if not predicted_tickets:
        return {
            'precision': 0.0,
            'recall': 0.0,
            'f1_score': 0.0,
            'true_positives': 0,
            'false_positives': len(expected_tickets),
            'false_negatives': 0
        }
    
    # Convert to sets for comparison
    expected_set = set(ticket['title'].lower() for ticket in expected_tickets)
    predicted_set = set(ticket['title'].lower() for ticket in predicted_tickets)
    
    # Calculate metrics
    true_positives = len(expected_set & predicted_set)
    false_positives = len(predicted_set - expected_set)
    false_negatives = len(expected_set - predicted_set)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives
    }

def calculate_field_accuracy(expected_tickets, predicted_tickets):
    """
    Calculate accuracy for individual ticket fields
    
    Args:
        expected_tickets: List of expected ticket dictionaries
        predicted_tickets: List of predicted ticket dictionaries
        
    Returns:
        dict: field-level accuracy metrics
    """
    if not expected_tickets or not predicted_tickets:
        return {}
    
    # Match tickets by title (simple matching for now)
    field_metrics = {
        'assignee_accuracy': 0.0,
        'due_date_accuracy': 0.0, 
        'priority_accuracy': 0.0,
        'description_accuracy': 0.0
    }
    
    matched_pairs = 0
    
    for expected in expected_tickets:
        for predicted in predicted_tickets:
            if expected['title'].lower() == predicted['title'].lower():
                matched_pairs += 1
                
                # Calculate field accuracy
                if expected.get('assignee') and predicted.get('assignee'):
                    field_metrics['assignee_accuracy'] += 1 if expected['assignee'].lower() == predicted['assignee'].lower() else 0
                
                if expected.get('priority') and predicted.get('priority'):
                    field_metrics['priority_accuracy'] += 1 if expected['priority'].lower() == predicted['priority'].lower() else 0
                
                # Simple date matching (could be enhanced)
                if expected.get('due_date') and predicted.get('due_date'):
                    try:
                        expected_date = datetime.strptime(expected['due_date'], '%Y-%m-%d')
                        predicted_date = datetime.strptime(predicted['due_date'], '%Y-%m-%d')
                        field_metrics['due_date_accuracy'] += 1 if expected_date == predicted_date else 0
                    except ValueError:
                        pass
                
                # Description similarity (simple for now)
                if expected.get('description') and predicted.get('description'):
                    field_metrics['description_accuracy'] += 1 if expected['description'].lower() in predicted['description'].lower() else 0
                
                break
    
    # Normalize by number of matched pairs
    if matched_pairs > 0:
        for key in field_metrics:
            field_metrics[key] = field_metrics[key] / matched_pairs
    
    return field_metrics

def evaluate_processor(processor, test_dataset, detailed=False):
    """
    Evaluate processor performance on test dataset
    
    Args:
        processor: Meeting processor instance
        test_dataset: List of test examples
        detailed: Whether to return detailed results
        
    Returns:
        dict: Evaluation results
    """
    results = []
    overall_metrics = {
        'total_examples': 0,
        'correct_extraction': 0,
        'precision_sum': 0.0,
        'recall_sum': 0.0,
        'f1_sum': 0.0
    }
    
    field_accuracy_sums = {
        'assignee_accuracy': 0.0,
        'due_date_accuracy': 0.0,
        'priority_accuracy': 0.0,
        'description_accuracy': 0.0
    }
    
    for example in test_dataset:
        try:
            # Process the example
            prediction = processor(example['input'])
            predicted_tickets = prediction.tickets if hasattr(prediction, 'tickets') else []
            
            # Calculate metrics
            pr_metrics = calculate_precision_recall(example['expected_tickets'], predicted_tickets)
            field_metrics = calculate_field_accuracy(example['expected_tickets'], predicted_tickets)
            
            # Update overall metrics
            overall_metrics['total_examples'] += 1
            overall_metrics['precision_sum'] += pr_metrics['precision']
            overall_metrics['recall_sum'] += pr_metrics['recall']
            overall_metrics['f1_sum'] += pr_metrics['f1_score']
            
            # Count as correct if all expected tickets were found
            if pr_metrics['false_negatives'] == 0 and pr_metrics['false_positives'] == 0:
                overall_metrics['correct_extraction'] += 1
            
            # Update field accuracy sums
            for key in field_accuracy_sums:
                field_accuracy_sums[key] += field_metrics.get(key, 0.0)
            
            # Store detailed results if requested
            if detailed:
                results.append({
                    'input': example['input'],
                    'expected': example['expected_tickets'],
                    'predicted': predicted_tickets,
                    'metrics': {
                        **pr_metrics,
                        'field_accuracy': field_metrics
                    },
                    'metadata': example['metadata']
                })
                
        except Exception as e:
            print(f"Error processing example: {e}")
            overall_metrics['total_examples'] += 1
    
    # Calculate averages
    if overall_metrics['total_examples'] > 0:
        overall_metrics['average_precision'] = overall_metrics['precision_sum'] / overall_metrics['total_examples']
        overall_metrics['average_recall'] = overall_metrics['recall_sum'] / overall_metrics['total_examples']
        overall_metrics['average_f1'] = overall_metrics['f1_sum'] / overall_metrics['total_examples']
        overall_metrics['accuracy'] = overall_metrics['correct_extraction'] / overall_metrics['total_examples']
        
        # Calculate average field accuracies
        for key in field_accuracy_sums:
            field_accuracy_sums[key] = field_accuracy_sums[key] / overall_metrics['total_examples']
    
    overall_metrics['field_accuracy'] = field_accuracy_sums
    
    return {
        'overall': overall_metrics,
        'detailed_results': results if detailed else []
    }

def print_evaluation_summary(evaluation_results):
    """Print a summary of evaluation results"""
    overall = evaluation_results['overall']
    
    print("=== Evaluation Summary ===")
    print(f"Total Examples: {overall['total_examples']}")
    print(f"Accuracy: {overall['accuracy']:.2f}")
    print(f"Average Precision: {overall['average_precision']:.2f}")
    print(f"Average Recall: {overall['average_recall']:.2f}")
    print(f"Average F1 Score: {overall['average_f1']:.2f}")
    
    print("\nField Accuracy:")
    for field, accuracy in overall['field_accuracy'].items():
        print(f"  {field.replace('_', ' ').title()}: {accuracy:.2f}")
    
    print(f"\nCorrect Extractions: {overall['correct_extraction']}/{overall['total_examples']}")

def create_dspy_metric_function():
    """Create a DSPy-compatible metric function for optimization"""
    def dspy_metric(example, pred, trace=None):
        """DSPy metric function that returns a score between 0 and 1"""
        expected_tickets = example.tickets
        predicted_tickets = pred.tickets if hasattr(pred, 'tickets') else []
        
        # Calculate precision and recall
        metrics = calculate_precision_recall(expected_tickets, predicted_tickets)
        
        # Use F1 score as the primary metric
        f1_score = metrics['f1_score']
        
        # Add small penalty for false positives and false negatives
        penalty = 0.1 * (metrics['false_positives'] + metrics['false_negatives'])
        
        return max(0, f1_score - penalty)
    
    return dspy_metric

if __name__ == "__main__":
    # Test the metrics with sample data
    expected = [
        {"title": "Fix login bug", "assignee": "Alice", "priority": "High"},
        {"title": "Update documentation", "assignee": "Bob", "priority": "Medium"}
    ]
    
    predicted = [
        {"title": "Fix login bug", "assignee": "Alice", "priority": "High"},
        {"title": "Write documentation", "assignee": "Charlie", "priority": "Medium"}
    ]
    
    print("Testing Evaluation Metrics:")
    print("Expected:", len(expected), "tickets")
    print("Predicted:", len(predicted), "tickets")
    
    pr_metrics = calculate_precision_recall(expected, predicted)
    print(f"Precision: {pr_metrics['precision']:.2f}")
    print(f"Recall: {pr_metrics['recall']:.2f}")
    print(f"F1 Score: {pr_metrics['f1_score']:.2f}")
    
    field_metrics = calculate_field_accuracy(expected, predicted)
    print(f"Field Accuracy: {field_metrics}")
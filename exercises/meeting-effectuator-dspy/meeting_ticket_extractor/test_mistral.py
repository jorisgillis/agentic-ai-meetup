# Test Mistral AI Integration

import os
from utils.config import configure_lm, load_environment
from modules.basic_processor import BasicMeetingProcessor
from dataset.initial_dataset import get_initial_dataset

def test_mistral_connection():
    """Test connection to Mistral AI"""
    print("=== Testing Mistral AI Integration ===")
    
    try:
        # Load environment
        load_environment()
        
        # Check if API key is available
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_key or mistral_key == "your-mistral-api-key-here":
            print("⚠️  Mistral API key not found in .env file")
            print("Please add your MISTRAL_API_KEY to the .env file")
            return False
        
        print("✓ Mistral API key found")
        
        # Configure LM
        print("Configuring Mistral LM...")
        lm = configure_lm("mistral", model="mistral-tiny")
        
        if lm is None:
            print("❌ Failed to configure Mistral LM")
            return False
        
        print("✓ Mistral LM configured successfully")
        
        # Test basic processor
        print("\nTesting basic processor with Mistral...")
        processor = BasicMeetingProcessor()
        
        # Simple test
        test_notes = """
        Quick team sync:
        - Alice needs to fix the login page bug by tomorrow
        - Bob will update the API documentation this week
        """
        
        print(f"Processing test notes: {test_notes[:50]}...")
        
        # Process the notes
        result = processor(test_notes)
        
        print("✓ Processing completed successfully")
        # Handle different result formats
        if hasattr(result, 'tickets'):
            tickets = result.tickets
            if isinstance(tickets, str):
                # Parse JSON string
                try:
                    import json
                    tickets = json.loads(tickets)
                except:
                    tickets = []
            elif not isinstance(tickets, list):
                tickets = [tickets] if tickets else []
        else:
            tickets = []
            
        print(f"Extracted {len(tickets)} tickets:")
        
        for i, ticket in enumerate(tickets, 1):
            print(f"\nTicket {i}:")
            print(f"  Title: {ticket.get('title', 'N/A')}")
            print(f"  Assignee: {ticket.get('assignee', 'N/A')}")
            print(f"  Priority: {ticket.get('priority', 'N/A')}")
            print(f"  Due: {ticket.get('due_date', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_with_dataset():
    """Test processor with actual dataset examples"""
    print("\n=== Testing with Dataset ===")
    
    try:
        # Load a simple example from dataset
        dataset = get_initial_dataset()
        if not dataset:
            print("No dataset available")
            return False
        
        # Use the first example that has expected tickets
        test_example = None
        for example in dataset:
            if example['expected_tickets']:
                test_example = example
                break
        
        if not test_example:
            print("No suitable test example found")
            return False
        
        print(f"Testing with example: {test_example['metadata']['complexity']} complexity")
        
        # Configure Mistral
        configure_lm("mistral", model="mistral-tiny")
        
        # Process with basic processor
        processor = BasicMeetingProcessor()
        result = processor(test_example['input'])
        
        print(f"✓ Processed example successfully")
        print(f"Expected {len(test_example['expected_tickets'])} tickets")
        print(f"Extracted {len(result.tickets)} tickets")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing with dataset: {e}")
        return False

def test_mistral_models():
    """Test different Mistral models"""
    print("\n=== Available Mistral Models ===")
    
    models = [
        "mistral-tiny",
        "mistral-small", 
        "mistral-medium",
        "mistral-large-latest"
    ]
    
    for model in models:
        print(f"- {model}")
    
    print("\nNote: Model availability depends on your Mistral API plan")

if __name__ == "__main__":
    print("Mistral AI Integration Test")
    print("=" * 40)
    
    # Show available models
    test_mistral_models()
    
    # Test connection
    success = test_mistral_connection()
    
    if success:
        # Test with dataset
        test_with_dataset()
        
        print("\n" + "=" * 40)
        print("✅ Mistral integration test completed!")
        print("\nNext steps:")
        print("1. Run full evaluation with test dataset")
        print("2. Optimize processor using Mistral")
        print("3. Compare performance with different models")
    else:
        print("\n" + "=" * 40)
        print("❌ Mistral integration test failed")
        print("Please check your API key and network connection")
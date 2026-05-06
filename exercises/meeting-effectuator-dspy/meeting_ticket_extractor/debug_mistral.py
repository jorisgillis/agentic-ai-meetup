# Debug Mistral AI Response

from utils.config import configure_lm, load_environment
import dspy

def debug_mistral_response():
    """Debug what Mistral is returning"""
    print("=== Debugging Mistral Response ===")
    
    try:
        # Configure Mistral
        load_environment()
        lm = configure_lm("mistral", model="mistral-tiny")
        
        # Test direct LM call
        print("Testing direct LM call...")
        
        # Create a simple signature
        class TestSignature(dspy.Signature):
            """Test signature"""
            input_text = dspy.InputField()
            output = dspy.OutputField()
        
        # Test with ChainOfThought
        test_module = dspy.ChainOfThought(TestSignature)
        
        # Simple test
        result = test_module(input_text="Hello, how are you?")
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        if hasattr(result, 'output'):
            print(f"Output: {result.output}")
        else:
            print("No output attribute found")
            print(f"Available attributes: {dir(result)}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_ticket_extraction():
    """Debug the ticket extraction specifically"""
    print("\n=== Debugging Ticket Extraction ===")
    
    try:
        from modules.basic_processor import Ticket
        
        # Configure Mistral
        load_environment()
        configure_lm("mistral", model="mistral-tiny")
        
        # Create the ticket extraction module
        ticket_module = dspy.ChainOfThought(Ticket)
        
        # Test with simple input
        test_input = "Alice to fix bug by Friday"
        
        print(f"Testing with input: '{test_input}'")
        result = ticket_module(meeting_notes=test_input)
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        if hasattr(result, 'tickets'):
            print(f"Tickets raw: {repr(result.tickets)}")
            print(f"Tickets type: {type(result.tickets)}")
            
            # Try to parse as JSON if it's a string
            if isinstance(result.tickets, str):
                try:
                    import json
                    parsed = json.loads(result.tickets)
                    print(f"Parsed tickets: {parsed}")
                    print(f"Parsed type: {type(parsed)}")
                except Exception as e:
                    print(f"JSON parse error: {e}")
            
            # Check if it's a Prediction object with tickets inside
            if hasattr(result.tickets, 'tickets'):
                print(f"Nested tickets: {result.tickets.tickets}")
        else:
            print("No tickets attribute found")
            print(f"Available attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_mistral_response()
    debug_ticket_extraction()
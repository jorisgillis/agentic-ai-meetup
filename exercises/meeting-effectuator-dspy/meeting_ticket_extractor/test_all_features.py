# Comprehensive Test Script for All Features

import os
import sys
import time
from utils.config import configure_lm, load_environment
from optimize_processor import optimize_with_bootstrap_fewshot, compare_models_on_test_set, evaluate_optimized_processor
from api_wrapper import get_processor, MeetingTicketClient
from test_mistral import test_mistral_connection
from evaluate_mistral import evaluate_with_mistral

def test_feature_1_bootstrap_fewshot():
    """Test BootstrapFewShot optimization"""
    print("=" * 60)
    print("🧪 FEATURE 1: BootstrapFewShot Optimization")
    print("=" * 60)
    
    try:
        # Check if API key is available
        load_environment()
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_key or mistral_key == "your-mistral-api-key-here":
            print("⚠️  Skipping BootstrapFewShot test - no Mistral API key")
            return False
        
        print("Starting BootstrapFewShot optimization...")
        start_time = time.time()
        
        # Run optimization with small dataset for quick test
        processor = optimize_with_bootstrap_fewshot(
            model_name="mistral-tiny",
            max_bootstrapped_demos=2,
            max_labelled_demos=4
        )
        
        optimization_time = time.time() - start_time
        
        if processor:
            print(f"✅ BootstrapFewShot completed in {optimization_time:.1f}s")
            print("✅ Optimized processor saved to optimized_processor.json")
            return True
        else:
            print("❌ BootstrapFewShot failed")
            return False
            
    except Exception as e:
        print(f"❌ BootstrapFewShot test failed: {e}")
        return False

def test_feature_2_model_comparison():
    """Test Model Comparison feature"""
    print("\n" + "=" * 60)
    print("📊 FEATURE 2: Model Comparison")
    print("=" * 60)
    
    try:
        # Check if API key is available
        load_environment()
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_key or mistral_key == "your-mistral-api-key-here":
            print("⚠️  Skipping model comparison test - no Mistral API key")
            return False
        
        print("Running model comparison...")
        start_time = time.time()
        
        results = compare_models_on_test_set()
        
        comparison_time = time.time() - start_time
        
        if results:
            print(f"✅ Model comparison completed in {comparison_time:.1f}s")
            
            # Show summary
            valid_results = {k: v for k, v in results.items() if 'error' not in v}
            if valid_results:
                best_model = max(valid_results.items(), key=lambda x: x[1]['f1'])
                print(f"🎯 Best model: {best_model[0]} (F1: {best_model[1]['f1']:.3f})")
            
            return True
        else:
            print("❌ Model comparison failed")
            return False
            
    except Exception as e:
        print(f"❌ Model comparison test failed: {e}")
        return False

def test_feature_3_api_wrapper():
    """Test API Wrapper feature"""
    print("\n" + "=" * 60)
    print("🌐 FEATURE 3: API Wrapper")
    print("=" * 60)
    
    try:
        # Test processor initialization
        print("Testing processor initialization...")
        processor = get_processor("mistral-tiny")
        print("✅ Processor initialized successfully")
        
        # Test with sample data
        sample_notes = """
        Team Sync Meeting:
        - Alice to fix login bug by Friday
        - Bob will update API documentation this week
        - Charlie needs to review security audit findings
        """
        
        print("Testing processing with sample notes...")
        start_time = time.time()
        
        result = processor(sample_notes)
        processing_time = time.time() - start_time
        
        # Parse tickets
        tickets = result.tickets if hasattr(result, 'tickets') else []
        if isinstance(tickets, str):
            import json
            tickets = json.loads(tickets)
        elif not isinstance(tickets, list):
            tickets = [tickets] if tickets else []
        
        print(f"✅ Processed {len(tickets)} tickets in {processing_time:.2f}s")
        
        # Show tickets
        for i, ticket in enumerate(tickets, 1):
            print(f"\nTicket {i}:")
            print(f"  Title: {ticket.get('title', 'N/A')}")
            print(f"  Assignee: {ticket.get('assignee', 'N/A')}")
            print(f"  Priority: {ticket.get('priority', 'N/A')}")
            print(f"  Due: {ticket.get('due_date', 'N/A')}")
        
        # Test API client
        print("\nTesting API client...")
        client = MeetingTicketClient()
        
        # Test health check (this will fail if API isn't running, but that's expected)
        try:
            health = client.health_check()
            print(f"API Health: {health.get('status', 'unknown')}")
        except:
            print("ℹ️  API server not running (expected for this test)")
        
        print("✅ API wrapper functionality verified")
        return True
        
    except Exception as e:
        print(f"❌ API wrapper test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration_all_features():
    """Test integration of all features"""
    print("\n" + "=" * 60)
    print("🔧 INTEGRATION TEST: All Features Together")
    print("=" * 60)
    
    try:
        # Check API key
        load_environment()
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_key or mistral_key == "your-mistral-api-key-here":
            print("⚠️  Skipping integration test - no Mistral API key")
            return False
        
        print("Running comprehensive integration test...")
        
        # Step 1: Run optimization
        print("\n1️⃣ Running BootstrapFewShot optimization...")
        processor = optimize_with_bootstrap_fewshot(
            model_name="mistral-tiny",
            max_bootstrapped_demos=2,
            max_labelled_demos=3
        )
        
        if not processor:
            print("❌ Optimization failed")
            return False
        
        # Step 2: Evaluate optimized processor
        print("\n2️⃣ Evaluating optimized processor...")
        evaluation = evaluate_optimized_processor("optimized_processor.json")
        
        if evaluation:
            overall = evaluation['overall']
            print(f"Optimized Processor Performance:")
            print(f"  Accuracy: {overall['accuracy']:.3f}")
            print(f"  F1 Score: {overall['average_f1']:.3f}")
        
        # Step 3: Compare with original
        print("\n3️⃣ Comparing with original processor...")
        original_evaluation = evaluate_with_mistral()
        
        if original_evaluation:
            original_f1 = original_evaluation['overall']['average_f1']
            optimized_f1 = evaluation['overall']['average_f1']
            improvement = ((optimized_f1 - original_f1) / original_f1 * 100) if original_f1 > 0 else 0
            
            print(f"Original F1: {original_f1:.3f}")
            print(f"Optimized F1: {optimized_f1:.3f}")
            print(f"Improvement: {improvement:.1f}%")
        
        # Step 4: Test API with optimized processor
        print("\n4️⃣ Testing API with optimized processor...")
        api_processor = get_processor("mistral-tiny", use_optimized=True)
        
        test_notes = "Quick follow-up: Alice to deploy hotfix today"
        api_result = api_processor(test_notes)
        
        api_tickets = api_result.tickets if hasattr(api_result, 'tickets') else []
        if isinstance(api_tickets, str):
            import json
            api_tickets = json.loads(api_tickets)
        
        print(f"✅ API processed {len(api_tickets)} tickets with optimized processor")
        
        print("\n🎉 Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all feature tests"""
    print("🚀 COMPREHENSIVE FEATURE TESTING")
    print("=" * 60)
    
    # Check environment
    load_environment()
    has_api_key = bool(os.getenv("MISTRAL_API_KEY") and os.getenv("MISTRAL_API_KEY") != "your-mistral-api-key-here")
    
    if not has_api_key:
        print("⚠️  Mistral API key not configured")
        print("    Some tests will be skipped")
        print("    Set MISTRAL_API_KEY in .env file for full testing")
    
    # Run tests
    test_results = {}
    
    # Feature 1: BootstrapFewShot
    test_results['bootstrap_fewshot'] = test_feature_1_bootstrap_fewshot()
    
    # Feature 2: Model Comparison
    test_results['model_comparison'] = test_feature_2_model_comparison()
    
    # Feature 3: API Wrapper
    test_results['api_wrapper'] = test_feature_3_api_wrapper()
    
    # Integration Test
    test_results['integration'] = test_integration_all_features()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is fully functional.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

def show_usage_examples():
    """Show usage examples for all features"""
    print("\n" + "=" * 60)
    print("📖 USAGE EXAMPLES")
    print("=" * 60)
    
    print("\n1️⃣ BootstrapFewShot Optimization:")
    print("   python optimize_processor.py --method bootstrap --model mistral-tiny")
    
    print("\n2️⃣ Model Comparison:")
    print("   python optimize_processor.py --method compare")
    
    print("\n3️⃣ API Wrapper:")
    print("   python api_wrapper.py")
    print("   Then send POST requests to http://localhost:8000/process")
    
    print("\n4️⃣ Full Evaluation:")
    print("   python evaluate_mistral.py")
    
    print("\n5️⃣ Testing:")
    print("   python test_mistral.py")
    print("   python test_all_features.py")

if __name__ == "__main__":
    # Run all tests
    success = run_all_tests()
    
    # Show usage examples
    show_usage_examples()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
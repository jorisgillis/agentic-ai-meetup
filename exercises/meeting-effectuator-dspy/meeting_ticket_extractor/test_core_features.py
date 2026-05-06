# Core Features Test (without FastAPI dependencies)

import os
import sys
import time
from utils.config import configure_lm, load_environment
from optimize_processor import optimize_with_bootstrap_fewshot, compare_models_on_test_set, evaluate_optimized_processor
from modules.basic_processor import BasicMeetingProcessor

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
            max_labeled_demos=4
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
        import traceback
        traceback.print_exc()
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
        import traceback
        traceback.print_exc()
        return False

def test_feature_3_api_processor():
    """Test API Processor functionality (core processing without FastAPI)"""
    print("\n" + "=" * 60)
    print("🌐 FEATURE 3: API Processor Core")
    print("=" * 60)
    
    try:
        # Check if API key is available
        load_environment()
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_key or mistral_key == "your-mistral-api-key-here":
            print("⚠️  Skipping API processor test - no Mistral API key")
            return False
        
        print("Testing processor initialization...")
        configure_lm("mistral", model="mistral-tiny")
        processor = BasicMeetingProcessor()
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
        
        # Test with optimized processor if available
        if os.path.exists("optimized_processor.json"):
            print("\nTesting with optimized processor...")
            optimized_processor = BasicMeetingProcessor()
            optimized_processor.load("optimized_processor.json")
            
            opt_result = optimized_processor(sample_notes)
            opt_tickets = opt_result.tickets if hasattr(opt_result, 'tickets') else []
            if isinstance(opt_tickets, str):
                opt_tickets = json.loads(opt_tickets)
            
            print(f"✅ Optimized processor processed {len(opt_tickets)} tickets")
        
        print("✅ API processor core functionality verified")
        return True
        
    except Exception as e:
        print(f"❌ API processor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration of all features"""
    print("\n" + "=" * 60)
    print("🔧 INTEGRATION TEST")
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
            max_labeled_demos=3
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
        
        # Step 3: Test with sample data
        print("\n3️⃣ Testing with sample meeting notes...")
        test_notes = "Quick follow-up: Alice to deploy hotfix today"
        result = processor(test_notes)
        
        test_tickets = result.tickets if hasattr(result, 'tickets') else []
        if isinstance(test_tickets, str):
            import json
            test_tickets = json.loads(test_tickets)
        
        print(f"✅ Integration test processed {len(test_tickets)} tickets")
        
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
    
    # Feature 3: API Processor Core
    test_results['api_processor'] = test_feature_3_api_processor()
    
    # Integration Test
    test_results['integration'] = test_integration()
    
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
    
    print("\n3️⃣ API Processor:")
    print("   from modules.basic_processor import BasicMeetingProcessor")
    print("   processor = BasicMeetingProcessor()")
    print("   result = processor(meeting_notes)")
    
    print("\n4️⃣ Full Evaluation:")
    print("   python evaluate_mistral.py")
    
    print("\n5️⃣ Testing:")
    print("   python test_mistral.py")
    print("   python test_core_features.py")

if __name__ == "__main__":
    # Run all tests
    success = run_all_tests()
    
    # Show usage examples
    show_usage_examples()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
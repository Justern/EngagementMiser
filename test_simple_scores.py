#!/usr/bin/env python3
"""
Test Script for Simple Score Scripts
===================================

Tests each model's simple_score.py script individually to verify they're working.
"""

import subprocess
import sys
import os

def test_model_script(model_name, model_path, tweet_id):
    """Test a single model's simple_score.py script."""
    print(f"🔧 Testing {model_name}...")
    
    try:
        # Get the path to the model's simple_score.py script
        script_path = os.path.join(model_path, 'simple_score.py')
        
        if not os.path.exists(script_path):
            print(f"   ❌ simple_score.py not found")
            return False
        
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, script_path, str(tweet_id)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            try:
                score = float(result.stdout.strip())
                print(f"   ✅ Score: {score:.3f}")
                return True
            except ValueError:
                print(f"   ⚠️  Invalid score format: {result.stdout.strip()}")
                return False
        else:
            print(f"   ❌ Script error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⚠️  Timeout")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}...")
        return False

def main():
    """Main test function."""
    print("🧪 TESTING SIMPLE SCORE SCRIPTS")
    print("=" * 50)
    
    # Test tweet ID
    test_tweet_id = "1238852891915386886"
    print(f"🎯 Testing with Tweet ID: {test_tweet_id}")
    print()
    
    # Model paths
    models = {
        'hyperbole_falsehood': '../Hyperbole_Falsehood_detector',
        'clickbait': '../Clickbait_Headline_Classifier',
        'engagement_mismatch': '../Engagement_Mismatch_Detector',
        'content_recycling': '../Content_Recycling_Detector',
        'coordinated_network': '../Coordinated_Account_Network_Model',
        'emotive_manipulation': '../Emotive_Manipulation_Detector',
        'rapid_engagement_spike': '../Rapid_Engagement_Spike_Detector',
        'generic_comment': '../Generic_Comment_Detector',
        'reply_bait': '../Reply_Bait_Detector'
    }
    
    # Test each model
    successful_tests = 0
    total_tests = len(models)
    
    for model_name, model_path in models.items():
        full_path = os.path.join(os.path.dirname(__file__), model_path)
        success = test_model_script(model_name, full_path, test_tweet_id)
        if success:
            successful_tests += 1
        print()
    
    # Summary
    print("=" * 50)
    print(f"📊 TEST SUMMARY")
    print(f"   Successful: {successful_tests}/{total_tests}")
    print(f"   Failed: {total_tests - successful_tests}/{total_tests}")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")

if __name__ == "__main__":
    main()

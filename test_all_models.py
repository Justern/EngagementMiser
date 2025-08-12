#!/usr/bin/env python3
"""
Comprehensive Model Testing and Fixing Script
============================================

This script tests all individual models and fixes any issues to ensure they can run:
1. Individually (direct execution)
2. As part of the ECS system (subprocess calls)
3. With proper output formatting (only score, no extra text)
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Model paths and expected outputs
MODELS = {
    "hyperbole_falsehood": "../Hyperbole_Falsehood_detector",
    "clickbait": "../Clickbait_Headline_Classifier", 
    "engagement_mismatch": "../Engagement_Mismatch_Detector",
    "content_recycling": "../Content_Recycling_Detector",
    "coordinated_network": "../Coordinated_Account_Network_Model",
    "emotive_manipulation": "../Emotive_Manipulation_Detector",
    "rapid_engagement_spike": "../Rapid_Engagement_Spike_Detector",
    "generic_comment": "../Generic_Comment_Detector",
    "authority_signal": "../Authority_Signal_Manipulation",
    "reply_bait": "../Reply_Bait_Detector"
}

TEST_TWEET_ID = "1233064764357726209"

def test_model_individual(model_name, model_path):
    """Test a model individually by running its simple_score.py script."""
    print(f"🔍 Testing {model_name} individually...")
    
    simple_score_path = os.path.join(model_path, "simple_score.py")
    
    if not os.path.exists(simple_score_path):
        print(f"   ❌ simple_score.py not found in {model_path}")
        return False, "File not found"
    
    try:
        # Run the model script
        result = subprocess.run(
            [sys.executable, simple_score_path, TEST_TWEET_ID],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"   ❌ Script failed with return code {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False, f"Script failed: {result.stderr}"
        
        # Check output
        output = result.stdout.strip()
        print(f"   Raw output: '{output}'")
        
        # Validate output format
        if not output:
            print(f"   ❌ No output produced")
            return False, "No output"
        
        # Check if output contains only a valid score
        try:
            score = float(output)
            if 0.0 <= score <= 1.0:
                print(f"   ✅ Valid score: {score}")
                return True, score
            else:
                print(f"   ❌ Score out of range: {score}")
                return False, f"Score out of range: {score}"
        except ValueError:
            print(f"   ❌ Invalid score format: '{output}'")
            return False, f"Invalid score format: '{output}'"
            
    except subprocess.TimeoutExpired:
        print(f"   ❌ Script timed out")
        return False, "Timeout"
    except Exception as e:
        print(f"   ❌ Error running script: {e}")
        return False, str(e)

def test_model_ecs_integration(model_name, model_path):
    """Test a model as it would be called by the ECS system."""
    print(f"🔧 Testing {model_name} ECS integration...")
    
    simple_score_path = os.path.join(model_path, "simple_score.py")
    
    if not os.path.exists(simple_score_path):
        return False, "File not found"
    
    try:
        # Simulate ECS subprocess call
        result = subprocess.run(
            [sys.executable, simple_score_path, TEST_TWEET_ID],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            return False, f"Script failed: {result.stderr}"
        
        output = result.stdout.strip()
        
        # ECS expects only a numeric score
        try:
            score = float(output)
            if 0.0 <= score <= 1.0:
                return True, score
            else:
                return False, f"Score out of range: {score}"
        except ValueError:
            return False, f"Invalid score format: '{output}'"
            
    except Exception as e:
        return False, str(e)

def fix_model_output(model_name, model_path):
    """Fix common output issues in model scripts."""
    print(f"🔧 Fixing {model_name} output issues...")
    
    simple_score_path = os.path.join(model_path, "simple_score.py")
    
    if not os.path.exists(simple_score_path):
        print(f"   ❌ Cannot fix: simple_score.py not found")
        return False
    
    try:
        # Read the current script
        with open(simple_score_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for common issues
        issues_found = []
        
        # Check for extra print statements
        if content.count('print(') > 2:  # Should only have main print and error prints
            issues_found.append("Extra print statements")
        
        # Check for debug output
        if 'debug' in content.lower() or 'print(' in content.lower():
            # Look for print statements that aren't the main score output
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'print(' in line and 'score' not in line.lower() and 'error' not in line.lower():
                    if not line.strip().startswith('#'):
                        issues_found.append(f"Extra print on line {i+1}: {line.strip()}")
        
        if issues_found:
            print(f"   ⚠️  Issues found: {', '.join(issues_found)}")
            
            # Create a backup
            backup_path = simple_score_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"   💾 Backup created: {backup_path}")
            
            # Try to fix common issues
            fixed_content = content
            
            # Remove any print statements that aren't the main score output
            lines = fixed_content.split('\n')
            fixed_lines = []
            for line in lines:
                # Keep the main score print and error prints
                if ('print(' in line and 
                    ('score' in line.lower() or 'error' in line.lower() or '0.0' in line)):
                    fixed_lines.append(line)
                elif 'print(' not in line:
                    fixed_lines.append(line)
                else:
                    # Comment out extra prints
                    if line.strip().startswith('print('):
                        fixed_lines.append(f"# {line}")
                    else:
                        fixed_lines.append(line)
            
            fixed_content = '\n'.join(fixed_lines)
            
            # Write the fixed version
            with open(simple_score_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            print(f"   ✅ Fixed output issues")
            return True
        else:
            print(f"   ✅ No output issues found")
            return True
            
    except Exception as e:
        print(f"   ❌ Error fixing script: {e}")
        return False

def main():
    """Main testing and fixing function."""
    print("🔍 COMPREHENSIVE MODEL TESTING AND FIXING")
    print("=" * 60)
    print(f"Test tweet ID: {TEST_TWEET_ID}")
    print()
    
    results = {}
    
    # Test each model
    for model_name, model_path in MODELS.items():
        print(f"\n📊 Testing {model_name.upper()}")
        print("-" * 40)
        
        # Check if model directory exists
        if not os.path.exists(model_path):
            print(f"   ❌ Model directory not found: {model_path}")
            results[model_name] = {"status": "missing", "individual": False, "ecs": False}
            continue
        
        # Test individual execution
        individual_ok, individual_result = test_model_individual(model_name, model_path)
        
        # Test ECS integration
        ecs_ok, ecs_result = test_model_ecs_integration(model_name, model_path)
        
        # Store results
        results[model_name] = {
            "status": "working" if (individual_ok and ecs_ok) else "needs_fix",
            "individual": individual_ok,
            "ecs": ecs_ok,
            "individual_result": individual_result,
            "ecs_result": ecs_result
        }
        
        # If there are issues, try to fix them
        if not individual_ok or not ecs_ok:
            print(f"   🔧 Attempting to fix {model_name}...")
            fix_success = fix_model_output(model_name, model_path)
            
            if fix_success:
                # Retest after fixing
                print(f"   🔍 Retesting {model_name} after fixes...")
                individual_ok2, individual_result2 = test_model_individual(model_name, model_path)
                ecs_ok2, ecs_result2 = test_model_ecs_integration(model_name, model_path)
                
                # Update results
                results[model_name].update({
                    "status": "working" if (individual_ok2 and ecs_ok2) else "still_broken",
                    "individual": individual_ok2,
                    "ecs": ecs_ok2,
                    "individual_result": individual_result2,
                    "ecs_result": ecs_result2
                })
        
        print()
    
    # Summary report
    print("\n📊 TESTING SUMMARY")
    print("=" * 60)
    
    working_models = []
    broken_models = []
    
    for model_name, result in results.items():
        if result["status"] == "working":
            working_models.append(model_name)
            print(f"✅ {model_name}: Working")
        else:
            broken_models.append(model_name)
            print(f"❌ {model_name}: {result['status']}")
            if not result["individual"]:
                print(f"   Individual test failed: {result['individual_result']}")
            if not result["ecs"]:
                print(f"   ECS integration failed: {result['ecs_result']}")
    
    print(f"\n🎯 RESULTS:")
    print(f"   Working models: {len(working_models)}/{len(MODELS)}")
    print(f"   Broken models: {len(broken_models)}")
    
    if working_models:
        print(f"\n✅ Working models: {', '.join(working_models)}")
    
    if broken_models:
        print(f"\n❌ Models needing attention: {', '.join(broken_models)}")
        print("\n💡 RECOMMENDATIONS:")
        print("   1. Check the error messages above for each broken model")
        print("   2. Verify the simple_score.py script exists in each model directory")
        print("   3. Ensure each script outputs only a numeric score (0.0-1.0)")
        print("   4. Check for extra print statements or debug output")
    
    return results

if __name__ == "__main__":
    main()

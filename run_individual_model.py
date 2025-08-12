#!/usr/bin/env python3
"""
Individual Model Runner
======================

Run any individual model with any tweet ID for testing.
Usage: python run_individual_model.py <model_name> <tweet_id>
"""

import sys
import os
import subprocess

# Model paths
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

def list_models():
    """List all available models."""
    print("🔍 Available Models:")
    print("=" * 40)
    for i, (model_name, model_path) in enumerate(MODELS.items(), 1):
        status = "✅" if os.path.exists(os.path.join(model_path, "simple_score.py")) else "❌"
        print(f"{i:2d}. {status} {model_name}")
        print(f"    Path: {model_path}")
    print()

def run_model(model_name, tweet_id):
    """Run a specific model with a tweet ID."""
    if model_name not in MODELS:
        print(f"❌ Error: Model '{model_name}' not found!")
        print(f"Available models: {', '.join(MODELS.keys())}")
        return False
    
    model_path = MODELS[model_name]
    simple_score_path = os.path.join(model_path, "simple_score.py")
    
    if not os.path.exists(simple_score_path):
        print(f"❌ Error: simple_score.py not found in {model_path}")
        return False
    
    print(f"🚀 Running {model_name} with tweet ID: {tweet_id}")
    print(f"📁 Model path: {model_path}")
    print("-" * 50)
    
    try:
        # Run the model
        result = subprocess.run(
            [sys.executable, simple_score_path, tweet_id],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"❌ Script failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        
        # Display results
        output = result.stdout.strip()
        print(f"📊 Raw output: '{output}'")
        
        # Validate and display score
        try:
            score = float(output)
            if 0.0 <= score <= 1.0:
                print(f"✅ Valid score: {score}")
                
                # Risk assessment
                if score >= 0.7:
                    risk = "HIGH RISK 🔴"
                elif score >= 0.4:
                    risk = "MEDIUM RISK 🟡"
                else:
                    risk = "LOW RISK 🟢"
                
                print(f"🎯 Risk Level: {risk}")
                print(f"📈 Score interpretation: {score:.1%} manipulation detected")
                
            else:
                print(f"⚠️  Score out of range: {score}")
                
        except ValueError:
            print(f"⚠️  Invalid score format: '{output}'")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Script timed out")
        return False
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False

def main():
    """Main function."""
    print("🔍 INDIVIDUAL MODEL RUNNER")
    print("=" * 40)
    
    if len(sys.argv) == 1:
        # No arguments - show help
        print("Usage: python run_individual_model.py <model_name> <tweet_id>")
        print()
        print("Examples:")
        print("  python run_individual_model.py hyperbole_falsehood 1233064764357726209")
        print("  python run_individual_model.py clickbait 1233064764357726209")
        print("  python run_individual_model.py emotive_manipulation 1233064764357726209")
        print()
        list_models()
        return
    
    if len(sys.argv) != 3:
        print("❌ Error: Please provide exactly 2 arguments: model_name and tweet_id")
        print("Usage: python run_individual_model.py <model_name> <tweet_id>")
        return
    
    model_name = sys.argv[1].lower()
    tweet_id = sys.argv[2]
    
    # Validate tweet ID
    if not tweet_id.isdigit() or len(tweet_id) < 15:
        print("❌ Error: Please provide a valid tweet ID (numeric, at least 15 digits)")
        return
    
    # Run the model
    success = run_model(model_name, tweet_id)
    
    if success:
        print("\n✅ Model execution completed successfully!")
    else:
        print("\n❌ Model execution failed!")

if __name__ == "__main__":
    main()

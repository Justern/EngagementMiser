"""
Simple Usage Script for Engagement Concordance Score
==================================================

A simple interface to run comprehensive engagement analysis on a tweet ID.
"""

from engagement_concordance_score import EngagementConcordanceScore
import sys

def main():
    """Simple interface for running engagement concordance analysis."""
    print("🌐 ENGAGEMENT CONCORDANCE SCORE - SIMPLE USAGE")
    print("=" * 60)
    
    # Initialize the system
    try:
        ecs = EngagementConcordanceScore()
        print(f"✅ System initialized with {len(ecs.models)} models")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return
    
    # Check if models are loaded
    loaded_models = [name for name, info in ecs.models.items() if info.get('loaded', False)]
    if not loaded_models:
        print("❌ No models loaded. Please check model directories and dependencies.")
        return
    
    print(f"📊 Available models: {', '.join(loaded_models)}")
    
    # Get tweet ID
    if len(sys.argv) > 1:
        tweet_id = sys.argv[1]
        print(f"🎯 Analyzing Tweet ID: {tweet_id}")
    else:
        tweet_id = input("\n📝 Enter Tweet ID to analyze: ").strip()
        if not tweet_id:
            print("❌ No tweet ID provided.")
            return
    
    print(f"\n🔍 Starting comprehensive analysis...")
    print("=" * 60)
    
    try:
        # Run comprehensive analysis
        results = ecs.analyze_tweet_comprehensive(tweet_id)
        
        # Print summary
        print(f"\n🎯 COMPOSITE SCORE: {results['composite_score']:.3f}")
        
        # Print risk assessment
        risk = results['risk_assessment']
        print(f"🚨 Risk Level: {risk['risk_level']}")
        print(f"📝 Description: {risk['risk_description']}")
        
        # Print model summary
        successful_models = len([m for m in results['model_results'].values() 
                               if m.get('status') == 'success'])
        total_models = len(ecs.models)
        print(f"📊 Models Analyzed: {successful_models}/{total_models}")
        
        # Ask for detailed report
        detailed = input("\n📋 Show detailed report? (y/n): ").strip().lower()
        if detailed in ['y', 'yes']:
            ecs.print_detailed_report(results)
        
        # Ask to save results
        save = input("\n💾 Save results to file? (y/n): ").strip().lower()
        if save in ['y', 'yes']:
            filename = ecs.save_results(results)
            if filename:
                print(f"✅ Results saved to: {filename}")
        
        print(f"\n✅ Analysis complete for Tweet ID: {tweet_id}")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

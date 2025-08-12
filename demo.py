"""
Demo Script for Engagement Concordance Score System
==================================================

Demonstrates the system's capabilities with sample tweet IDs and analysis.
"""

from engagement_concordance_score import EngagementConcordanceScore
import time

def demo_system_initialization():
    """Demonstrate system initialization and model loading."""
    print("🚀 DEMO: System Initialization")
    print("=" * 50)
    
    try:
        ecs = EngagementConcordanceScore()
        
        print(f"✅ System initialized successfully!")
        print(f"📊 Total models configured: {len(ecs.models)}")
        
        # Show loaded models
        loaded_models = [name for name, info in ecs.models.items() if info.get('loaded', False)]
        failed_models = [name for name, info in ecs.models.items() if not info.get('loaded', False)]
        
        print(f"✅ Successfully loaded: {len(loaded_models)} models")
        if loaded_models:
            print("   • " + "\n   • ".join(loaded_models))
        
        if failed_models:
            print(f"❌ Failed to load: {len(failed_models)} models")
            for model in failed_models:
                error = ecs.models[model].get('error', 'Unknown error')
                print(f"   • {model}: {error[:50]}...")
        
        return ecs, len(loaded_models) > 0
        
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        return None, False

def demo_single_tweet_analysis(ecs, tweet_id):
    """Demonstrate analysis of a single tweet."""
    print(f"\n🔍 DEMO: Single Tweet Analysis")
    print("=" * 50)
    print(f"🎯 Tweet ID: {tweet_id}")
    
    try:
        start_time = time.time()
        results = ecs.analyze_tweet_comprehensive(tweet_id)
        analysis_time = time.time() - start_time
        
        print(f"\n⏱️  Analysis completed in {analysis_time:.2f} seconds")
        print(f"🎯 Composite Score: {results['composite_score']:.3f}")
        
        # Show risk assessment
        risk = results['risk_assessment']
        print(f"🚨 Risk Level: {risk['risk_level']}")
        print(f"📝 Description: {risk['risk_description']}")
        
        # Show model breakdown
        successful_models = len([m for m in results['model_results'].values() 
                               if m.get('status') == 'success'])
        total_models = len(ecs.models)
        print(f"📊 Models Analyzed: {successful_models}/{total_models}")
        
        # Show top risk factors
        if risk['top_risk_factors']:
            print(f"🔴 Top Risk Factors:")
            for i, factor in enumerate(risk['top_risk_factors'], 1):
                print(f"   {i}. {factor['model']}: {factor['score']:.3f} (Weight: {factor['weight']})")
        
        return results
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None

def demo_batch_analysis(ecs, tweet_ids):
    """Demonstrate batch analysis of multiple tweets."""
    print(f"\n📊 DEMO: Batch Analysis")
    print("=" * 50)
    print(f"🎯 Analyzing {len(tweet_ids)} tweets...")
    
    batch_results = []
    
    for i, tweet_id in enumerate(tweet_ids, 1):
        print(f"\n📝 Tweet {i}/{len(tweet_ids)}: {tweet_id}")
        
        try:
            results = ecs.analyze_tweet_comprehensive(tweet_id)
            batch_results.append(results)
            
            print(f"   ✅ Score: {results['composite_score']:.3f} | Risk: {results['risk_assessment']['risk_level']}")
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)[:30]}...")
            batch_results.append({'tweet_id': tweet_id, 'error': str(e)})
    
    # Summary
    successful_analyses = [r for r in batch_results if 'composite_score' in r]
    if successful_analyses:
        scores = [r['composite_score'] for r in successful_analyses]
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        print(f"\n📈 BATCH SUMMARY:")
        print(f"   • Successful analyses: {len(successful_analyses)}/{len(tweet_ids)}")
        print(f"   • Average score: {avg_score:.3f}")
        print(f"   • Score range: {min_score:.3f} - {max_score:.3f}")
        
        # Risk distribution
        risk_levels = {}
        for r in successful_analyses:
            risk = r['risk_assessment']['risk_level']
            risk_levels[risk] = risk_levels.get(risk, 0) + 1
        
        print(f"   • Risk distribution:")
        for risk, count in risk_levels.items():
            print(f"     {risk}: {count}")
    
    return batch_results

def demo_risk_assessment_breakdown(ecs, results):
    """Demonstrate detailed risk assessment breakdown."""
    print(f"\n🚨 DEMO: Risk Assessment Breakdown")
    print("=" * 50)
    
    if not results or 'risk_assessment' not in results:
        print("❌ No results to analyze")
        return
    
    risk = results['risk_assessment']
    print(f"🎯 Tweet ID: {results['tweet_id']}")
    print(f"🏆 Composite Score: {results['composite_score']:.3f}")
    print(f"🚨 Overall Risk Level: {risk['risk_level']}")
    print(f"📝 Risk Description: {risk['risk_description']}")
    
    # Model-by-model breakdown
    print(f"\n📊 MODEL BREAKDOWN:")
    for model_name, model_result in results['model_results'].items():
        if model_result['status'] == 'success':
            score = model_result['score']
            weight = ecs.weights[model_name]
            contribution = score * weight
            risk_icon = "🔴" if score > 0.6 else "🟡" if score > 0.4 else "🟢"
            
            print(f"   {risk_icon} {model_name}:")
            print(f"      Score: {score:.3f} | Weight: {weight} | Contribution: {contribution:.3f}")
            
            # Risk interpretation
            if score > 0.8:
                risk_desc = "CRITICAL"
            elif score > 0.6:
                risk_desc = "HIGH"
            elif score > 0.4:
                risk_desc = "MODERATE"
            elif score > 0.2:
                risk_desc = "LOW"
            else:
                risk_desc = "MINIMAL"
            
            print(f"      Risk Level: {risk_desc}")
    
    # Weighted impact analysis
    print(f"\n⚖️  WEIGHTED IMPACT ANALYSIS:")
    weighted_contributions = []
    for model_name, model_result in results['model_results'].items():
        if model_result['status'] == 'success':
            score = model_result['score']
            weight = ecs.weights[model_name]
            contribution = score * weight
            weighted_contributions.append((model_name, contribution, weight))
    
    # Sort by weighted contribution
    weighted_contributions.sort(key=lambda x: x[1], reverse=True)
    
    for i, (model_name, contribution, weight) in enumerate(weighted_contributions, 1):
        percentage = (contribution / sum([x[1] for x in weighted_contributions])) * 100
        print(f"   {i}. {model_name}: {contribution:.3f} ({percentage:.1f}% of total impact)")

def main():
    """Main demo function."""
    print("🌐 ENGAGEMENT CONCORDANCE SCORE SYSTEM - DEMO")
    print("=" * 70)
    
    # Initialize system
    ecs, success = demo_system_initialization()
    if not success:
        print("❌ Cannot proceed without loaded models")
        return
    
    # Sample tweet IDs for demonstration
    sample_tweets = [
        "1234567890",  # Replace with actual tweet IDs from your database
        "1234567891",
        "1234567892"
    ]
    
    # Demo 1: Single tweet analysis
    if sample_tweets:
        results = demo_single_tweet_analysis(ecs, sample_tweets[0])
        
        if results:
            # Demo 2: Risk assessment breakdown
            demo_risk_assessment_breakdown(ecs, results)
            
            # Demo 3: Batch analysis (if multiple tweets)
            if len(sample_tweets) > 1:
                demo_batch_analysis(ecs, sample_tweets[1:])
    
    print(f"\n🎉 DEMO COMPLETED!")
    print("=" * 70)
    print("💡 To run your own analysis:")
    print("   python simple_usage.py")
    print("   python simple_usage.py <tweet_id>")

if __name__ == "__main__":
    main()

"""
Engagement Concordance Score System
==================================

A composite scoring system that combines multiple engagement analysis models
to provide a comprehensive assessment of tweet engagement quality and manipulation risk.

Models Integrated:
1. Hyperbole & Falsehood Detector (Weight: 0.6)
2. Clickbait Headline Classifier (Weight: 0.8)
3. Engagement Mismatch Detector (Weight: 1.0)
4. Content Recycling Detector (Weight: 0.9)
5. Coordinated Account Network Model (Weight: 1.0)
6. Emotive Manipulation Detector (Weight: 0.6)
7. Rapid Engagement Spike Detector (Weight: 0.5)
8. Generic Comment Detector (Weight: 0.6)
9. Authority-Signal Manipulation (Weight: 0.7)
10. Reply-Bait Detector (Weight: 0.8)
"""

import sys
import os
import importlib.util
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import warnings
warnings.filterwarnings('ignore')

class EngagementConcordanceScore:
    """
    Main class for computing composite engagement concordance scores
    by integrating multiple specialized detection models.
    """
    
    def __init__(self):
        """Initialize the Engagement Concordance Score system."""
        self.models = {}
        self.weights = {
            'hyperbole_falsehood': 0.6,
            'clickbait': 0.8,
            'engagement_mismatch': 1.0,
            'content_recycling': 0.9,
            'coordinated_network': 1.0,
            'emotive_manipulation': 0.6,
            'rapid_engagement_spike': 0.5,
            'generic_comment': 0.6,
            'authority_signal': 0.7,
            'reply_bait': 0.8
        }
        
        self.model_paths = {
            'hyperbole_falsehood': '../Hyperbole_Falsehood_detector',
            'clickbait': '../Clickbait_Headline_Classifier',
            'engagement_mismatch': '../Engagement_Mismatch_Detector',
            'content_recycling': '../Content_Recycling_Detector',
            'coordinated_network': '../Coordinated_Account_Network_Model',
            'emotive_manipulation': '../Emotive_Manipulation_Detector',
            'rapid_engagement_spike': '../Rapid_Engagement_Spike_Detector',
            'generic_comment': '../Generic_Comment_Detector',
            'authority_signal': '../Authority_Signal_Manipulation',
            'reply_bait': '../Reply_Bait_Detector'
        }
        
        self.model_files = {
            'hyperbole_falsehood': 'hyperbole_falsehood_detector.py',
            'clickbait': 'clickbait_classifier.py',
            'engagement_mismatch': 'engagement_mismatch_detector.py',
            'content_recycling': 'content_recycling_detector.py',
            'coordinated_network': 'coordinated_account_network_model.py',
            'emotive_manipulation': 'emotive_manipulation_detector.py',
            'rapid_engagement_spike': 'rapid_engagement_spike_detector.py',
            'generic_comment': 'generic_comment_detector.py',
            'authority_signal': 'authority_signal_detector.py',
            'reply_bait': 'reply_bait_detector.py'
        }
        
        self.analysis_methods = {
            'hyperbole_falsehood': 'simple_score',         # ✅ Uses simple_score.py script
            'clickbait': 'simple_score',                   # ✅ Uses simple_score.py script
            'engagement_mismatch': 'simple_score',          # ✅ Uses simple_score.py script
            'content_recycling': 'simple_score',            # ✅ Uses simple_score.py script
            'coordinated_network': 'simple_score',          # ✅ Uses simple_score.py script
            'emotive_manipulation': 'simple_score',         # ✅ Uses simple_score.py script
            'rapid_engagement_spike': 'simple_score',       # ✅ Uses simple_score.py script
            'generic_comment': 'simple_score',              # ✅ Uses simple_score.py script
            'authority_signal': 'simple_score',             # ✅ Uses simple_score.py script
            'reply_bait': 'simple_score'                    # ✅ Uses simple_score.py script
        }
        
        self.score_keys = {
            'hyperbole_falsehood': 'manipulation_score',
            'clickbait': 'clickbait_score',
            'engagement_mismatch': 'mismatch_score',
            'content_recycling': 'recycling_score',
            'coordinated_network': 'coordination_score',
            'emotive_manipulation': 'manipulation_score',
            'rapid_engagement_spike': 'spike_score',
            'generic_comment': 'generic_content_score',
            'authority_signal': 'authority_score',
            'reply_bait': 'reply_bait_score'
        }
        
        self.load_models()
    
    def load_models(self):
        """Load all available models by checking simple_score.py scripts."""
        print("🔧 Loading Engagement Analysis Models...")
        
        for model_name, model_path in self.model_paths.items():
            try:
                # Check if model directory exists
                full_path = os.path.join(os.path.dirname(__file__), model_path)
                if not os.path.exists(full_path):
                    print(f"⚠️  Model directory not found: {model_name}")
                    self.models[model_name] = {'loaded': False, 'error': 'Directory not found'}
                    continue
                
                # Check if simple_score.py exists
                script_path = os.path.join(full_path, 'simple_score.py')
                if not os.path.exists(script_path):
                    print(f"⚠️  simple_score.py not found: {model_name}")
                    self.models[model_name] = {'loaded': False, 'error': 'simple_score.py not found'}
                    continue
                
                # Mark as loaded if script exists
                self.models[model_name] = {'loaded': True}
                print(f"✅ Loaded: {model_name}")
                        
            except Exception as e:
                print(f"⚠️  Error loading {model_name}: {str(e)[:50]}...")
                self.models[model_name] = {'loaded': False, 'error': str(e)}
        
        print(f"📊 Loaded {len([m for m in self.models.values() if m.get('loaded', False)])} models successfully")
    
    def analyze_tweet_comprehensive(self, tweet_id: str) -> Dict[str, Any]:
        """
        Run comprehensive analysis on a tweet using all available models.
        
        Args:
            tweet_id (str): The tweet ID to analyze
            
        Returns:
            Dict containing comprehensive analysis results and composite score
        """
        print(f"🔍 Analyzing Tweet ID: {tweet_id}")
        print("=" * 60)
        
        results = {
            'tweet_id': tweet_id,
            'timestamp': datetime.now().isoformat(),
            'model_results': {},
            'composite_score': 0.0,
            'weighted_breakdown': {},
            'risk_assessment': {},
            'summary': {}
        }
        
        total_weight = 0
        weighted_sum = 0
        
        # Run each model
        for model_name, model_info in self.models.items():
            if not model_info.get('loaded', False):
                print(f"⏭️  Skipping {model_name} (not loaded)")
                continue
            
            print(f"🔧 Running {model_name}...")
            
            try:
                method_name = self.analysis_methods[model_name]
                
                if method_name == 'simple_score':
                    # Call the simple_score.py script for this model
                    try:
                        # Get the path to the model's simple_score.py script
                        model_dir = os.path.join(os.path.dirname(__file__), self.model_paths[model_name])
                        script_path = os.path.join(model_dir, 'simple_score.py')
                        
                        if os.path.exists(script_path):
                            # Run the script as a subprocess
                            result = subprocess.run(
                                [sys.executable, script_path, tweet_id],
                                capture_output=True,
                                text=True,
                                timeout=30  # 30 second timeout
                            )
                            
                            if result.returncode == 0:
                                # Parse the score from stdout
                                try:
                                    score = float(result.stdout.strip())
                                    if 0 <= score <= 1:
                                        model_result = {self.score_keys[model_name]: score}
                                    else:
                                        print(f"   ⚠️  Invalid score range: {score}")
                                        model_result = {self.score_keys[model_name]: 0.0}
                                except ValueError:
                                    print(f"   ⚠️  Invalid score format: {result.stdout.strip()}")
                                    model_result = {self.score_keys[model_name]: 0.0}
                            else:
                                print(f"   ⚠️  Script error: {result.stderr.strip()}")
                                model_result = {self.score_keys[model_name]: 0.0}
                        else:
                            print(f"   ⚠️  simple_score.py not found for {model_name}")
                            model_result = {self.score_keys[model_name]: 0.0}
                            
                    except subprocess.TimeoutExpired:
                        print(f"   ⚠️  Timeout running {model_name} script")
                        model_result = {self.score_keys[model_name]: 0.0}
                    except Exception as e:
                        print(f"   ❌ Error running {model_name} script: {str(e)[:50]}...")
                        model_result = {self.score_keys[model_name]: 0.0}
                else:
                    # Fallback for other method types (shouldn't happen now)
                    print(f"   ⚠️  Unexpected method type: {method_name}")
                    model_result = {self.score_keys[model_name]: 0.0}
                
                # Extract the score
                score_key = self.score_keys[model_name]
                if isinstance(model_result, dict) and score_key in model_result:
                    score = model_result[score_key]
                    if isinstance(score, (int, float)) and 0 <= score <= 1:
                        results['model_results'][model_name] = {
                            'score': score,
                            'full_result': model_result,
                            'status': 'success'
                        }
                        
                        # Calculate weighted contribution
                        weight = self.weights[model_name]
                        weighted_contribution = score * weight
                        weighted_sum += weighted_contribution
                        total_weight += weight
                        
                        results['weighted_breakdown'][model_name] = {
                            'raw_score': score,
                            'weight': weight,
                            'weighted_contribution': weighted_contribution
                        }
                        
                        print(f"   ✅ Score: {score:.3f} (Weight: {weight}, Contribution: {weighted_contribution:.3f})")
                    else:
                        print(f"   ⚠️  Invalid score format: {score}")
                        results['model_results'][model_name] = {
                            'score': None,
                            'full_result': model_result,
                            'status': 'invalid_score'
                        }
                else:
                    print(f"   ⚠️  Score key '{score_key}' not found in result")
                    results['model_results'][model_name] = {
                        'score': None,
                        'full_result': model_result,
                        'status': 'score_not_found'
                    }
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:50]}...")
                results['model_results'][model_name] = {
                    'score': None,
                    'full_result': None,
                    'status': 'error',
                    'error': str(e)
                }
        
        # Calculate composite score
        if total_weight > 0:
            results['composite_score'] = weighted_sum / total_weight
            print(f"\n🎯 COMPOSITE SCORE: {results['composite_score']:.3f}")
        else:
            results['composite_score'] = 0.0
            print(f"\n❌ No valid scores to calculate composite")
        
        # Generate risk assessment
        results['risk_assessment'] = self._assess_overall_risk(results)
        
        # Generate summary
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _assess_overall_risk(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall risk based on composite score and individual model results."""
        composite_score = results['composite_score']
        
        # Risk level based on composite score
        if composite_score >= 0.8:
            risk_level = "CRITICAL"
            risk_description = "Very high manipulation risk detected across multiple dimensions"
        elif composite_score >= 0.6:
            risk_level = "HIGH"
            risk_description = "High manipulation risk with concerning patterns"
        elif composite_score >= 0.4:
            risk_level = "MODERATE"
            risk_description = "Moderate risk with some concerning indicators"
        elif composite_score >= 0.2:
            risk_level = "LOW"
            risk_description = "Low risk with minimal concerning indicators"
        else:
            risk_level = "MINIMAL"
            risk_description = "Minimal risk, appears to be genuine engagement"
        
        # Identify top risk factors
        risk_factors = []
        for model_name, model_result in results['model_results'].items():
            if (model_result.get('status') == 'success' and 
                model_result.get('score', 0) > 0.5):
                risk_factors.append({
                    'model': model_name,
                    'score': model_result['score'],
                    'weight': self.weights[model_name]
                })
        
        # Sort by weighted impact
        risk_factors.sort(key=lambda x: x['score'] * x['weight'], reverse=True)
        
        return {
            'risk_level': risk_level,
            'risk_description': risk_description,
            'top_risk_factors': risk_factors[:3],
            'composite_score': composite_score
        }
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a human-readable summary of the analysis."""
        composite_score = results['composite_score']
        risk_assessment = results['risk_assessment']
        
        # Count successful analyses
        successful_models = len([m for m in results['model_results'].values() 
                               if m.get('status') == 'success'])
        total_models = len(self.models)
        
        # Generate recommendations
        recommendations = []
        if composite_score >= 0.6:
            recommendations.append("Consider flagging for manual review")
            recommendations.append("Monitor for similar patterns")
        if composite_score >= 0.4:
            recommendations.append("Review engagement patterns")
        if composite_score < 0.2:
            recommendations.append("Engagement appears genuine")
        
        return {
            'models_analyzed': f"{successful_models}/{total_models}",
            'composite_score': f"{composite_score:.3f}",
            'risk_level': risk_assessment['risk_level'],
            'recommendations': recommendations,
            'analysis_confidence': 'high' if successful_models >= 7 else 'medium' if successful_models >= 4 else 'low'
        }
    
    def print_detailed_report(self, results: Dict[str, Any]):
        """Print a detailed analysis report."""
        print("\n" + "=" * 80)
        print("📊 ENGAGEMENT CONCORDANCE SCORE - DETAILED REPORT")
        print("=" * 80)
        
        print(f"🎯 Tweet ID: {results['tweet_id']}")
        print(f"⏰ Analysis Time: {results['timestamp']}")
        print(f"🏆 Composite Score: {results['composite_score']:.3f}")
        
        print(f"\n🚨 RISK ASSESSMENT:")
        risk = results['risk_assessment']
        print(f"   Level: {risk['risk_level']}")
        print(f"   Description: {risk['risk_description']}")
        
        if risk['top_risk_factors']:
            print(f"   Top Risk Factors:")
            for i, factor in enumerate(risk['top_risk_factors'], 1):
                print(f"     {i}. {factor['model']}: {factor['score']:.3f} (Weight: {factor['weight']})")
        
        print(f"\n📈 MODEL BREAKDOWN:")
        for model_name, model_result in results['model_results'].items():
            status_icon = "✅" if model_result['status'] == 'success' else "⚠️" if model_result['status'] == 'invalid_score' else "❌"
            print(f"   {status_icon} {model_name}: {model_result['status']}")
            
            if model_result['status'] == 'success':
                score = model_result['score']
                weight = self.weights[model_name]
                contribution = score * weight
                print(f"      Score: {score:.3f} | Weight: {weight} | Contribution: {contribution:.3f}")
        
        print(f"\n📋 SUMMARY:")
        summary = results['summary']
        print(f"   Models Analyzed: {summary['models_analyzed']}")
        print(f"   Analysis Confidence: {summary['analysis_confidence'].upper()}")
        print(f"   Recommendations:")
        for rec in summary['recommendations']:
            print(f"     • {rec}")
        
        print("=" * 80)
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save analysis results to a JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"engagement_analysis_{results['tweet_id']}_{timestamp}.json"
        
        try:
            import json
            # Convert numpy types to native Python types for JSON serialization
            def convert_numpy(obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                elif isinstance(obj, np.floating):
                    return float(obj)
                elif isinstance(obj, np.ndarray):
                    return obj.tolist()
                return obj
            
            # Clean results for JSON serialization
            clean_results = json.loads(json.dumps(results, default=convert_numpy))
            
            with open(filename, 'w') as f:
                json.dump(clean_results, f, indent=2, default=str)
            
            print(f"💾 Results saved to: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return None


def main():
    """Main function for command-line usage."""
    print("🌐 ENGAGEMENT CONCORDANCE SCORE SYSTEM")
    print("=" * 50)
    
    # Initialize the system
    ecs = EngagementConcordanceScore()
    
    if not ecs.models:
        print("❌ No models loaded. Please check model directories.")
        return
    
    # Get tweet ID from user
    tweet_id = input("\n📝 Enter Tweet ID to analyze: ").strip()
    
    if not tweet_id:
        print("❌ No tweet ID provided.")
        return
    
    # Run comprehensive analysis
    results = ecs.analyze_tweet_comprehensive(tweet_id)
    
    # Print detailed report
    ecs.print_detailed_report(results)
    
    # Ask if user wants to save results
    save_choice = input("\n💾 Save results to file? (y/n): ").strip().lower()
    if save_choice in ['y', 'yes']:
        ecs.save_results(results)


if __name__ == "__main__":
    main()

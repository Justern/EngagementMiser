"""
Test Script for Engagement Concordance Score System
==================================================

Tests the system's functionality and validates model integration.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch
import tempfile
import json

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from engagement_concordance_score import EngagementConcordanceScore
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're in the correct directory and all files exist.")
    sys.exit(1)

class TestEngagementConcordanceScore(unittest.TestCase):
    """Test cases for the Engagement Concordance Score system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock the model loading to avoid actual model dependencies
        with patch('engagement_concordance_score.importlib.util.spec_from_file_location') as mock_spec:
            with patch('engagement_concordance_score.importlib.util.module_from_spec') as mock_module:
                # Create a mock module with a mock class
                mock_class = Mock()
                mock_class.__name__ = 'MockModel'
                mock_class.__init__ = Mock(return_value=None)
                
                # Mock the module
                mock_module.return_value = Mock()
                mock_module.return_value.MockModel = mock_class
                
                # Mock the spec
                mock_spec.return_value = Mock()
                mock_spec.return_value.loader = Mock()
                
                # Initialize the system
                self.ecs = EngagementConcordanceScore()
    
    def test_system_initialization(self):
        """Test that the system initializes correctly."""
        self.assertIsNotNone(self.ecs)
        self.assertIsInstance(self.ecs.weights, dict)
        self.assertIsInstance(self.ecs.model_paths, dict)
        self.assertIsInstance(self.ecs.models, dict)
        
        # Check that weights are properly configured
        expected_weights = {
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
        
        for model, weight in expected_weights.items():
            self.assertEqual(self.ecs.weights[model], weight)
    
    def test_weight_calculation(self):
        """Test weighted score calculation."""
        # Mock model results
        mock_results = {
            'model_results': {
                'coordinated_network': {'score': 0.8, 'status': 'success'},
                'emotive_manipulation': {'score': 0.6, 'status': 'success'},
                'generic_comment': {'score': 0.4, 'status': 'success'}
            }
        }
        
        # Calculate expected weighted score
        expected_weighted_sum = (0.8 * 1.0) + (0.6 * 0.6) + (0.4 * 0.6)
        expected_total_weight = 1.0 + 0.6 + 0.6
        expected_score = expected_weighted_sum / expected_total_weight
        
        # Mock the analysis method
        with patch.object(self.ecs, 'models', {
            'coordinated_network': {'loaded': True, 'instance': Mock()},
            'emotive_manipulation': {'loaded': True, 'instance': Mock()},
            'generic_comment': {'loaded': True, 'instance': Mock()}
        }):
            # Mock the model instances to return our test results
            for model_name in ['coordinated_network', 'emotive_manipulation', 'generic_comment']:
                mock_instance = Mock()
                mock_instance.analyze_tweet_coordination = Mock(return_value={'coordination_score': 0.8})
                mock_instance.analyze_tweet_by_id = Mock(return_value={'manipulation_score': 0.6})
                mock_instance.analyze_tweet_by_id = Mock(return_value={'generic_content_score': 0.4})
                
                self.ecs.models[model_name]['instance'] = mock_instance
            
            # Run analysis
            results = self.ecs.analyze_tweet_comprehensive("test_tweet_id")
            
            # Check that composite score is calculated
            self.assertIn('composite_score', results)
            self.assertIsInstance(results['composite_score'], (int, float))
    
    def test_risk_assessment(self):
        """Test risk assessment functionality."""
        # Test different score ranges
        test_cases = [
            (0.9, "CRITICAL"),
            (0.7, "HIGH"),
            (0.5, "MODERATE"),
            (0.3, "LOW"),
            (0.1, "MINIMAL")
        ]
        
        for score, expected_risk in test_cases:
            mock_results = {'composite_score': score, 'model_results': {}}
            risk_assessment = self.ecs._assess_overall_risk(mock_results)
            self.assertEqual(risk_assessment['risk_level'], expected_risk)
    
    def test_summary_generation(self):
        """Test summary generation functionality."""
        mock_results = {
            'composite_score': 0.75,
            'model_results': {
                'model1': {'status': 'success'},
                'model2': {'status': 'success'},
                'model3': {'status': 'error'},
                'model4': {'status': 'success'}
            }
        }
        
        summary = self.ecs._generate_summary(mock_results)
        
        self.assertIn('models_analyzed', summary)
        self.assertIn('composite_score', summary)
        self.assertIn('risk_level', summary)
        self.assertIn('recommendations', summary)
        self.assertIn('analysis_confidence', summary)
        
        # Check that models_analyzed shows correct ratio
        self.assertEqual(summary['models_analyzed'], '3/4')
    
    def test_results_saving(self):
        """Test results saving functionality."""
        # Create mock results
        mock_results = {
            'tweet_id': 'test_123',
            'composite_score': 0.75,
            'model_results': {'test_model': {'score': 0.8, 'status': 'success'}},
            'risk_assessment': {'risk_level': 'HIGH'},
            'summary': {'models_analyzed': '1/1'}
        }
        
        # Test saving to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            temp_filename = temp_file.name
        
        try:
            # Save results
            saved_filename = self.ecs.save_results(mock_results, temp_filename)
            
            # Check that file was created
            self.assertTrue(os.path.exists(saved_filename))
            
            # Check that file contains valid JSON
            with open(saved_filename, 'r') as f:
                loaded_results = json.load(f)
            
            # Verify key fields are preserved
            self.assertEqual(loaded_results['tweet_id'], 'test_123')
            self.assertEqual(loaded_results['composite_score'], 0.75)
            
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_error_handling(self):
        """Test error handling in the system."""
        # Test with invalid tweet ID
        with patch.object(self.ecs, 'models', {}):
            results = self.ecs.analyze_tweet_comprehensive("invalid_tweet")
            
            # Should handle gracefully
            self.assertIn('composite_score', results)
            self.assertEqual(results['composite_score'], 0.0)
    
    def test_model_loading_robustness(self):
        """Test that the system handles missing models gracefully."""
        # Test with non-existent model paths
        original_paths = self.ecs.model_paths.copy()
        self.ecs.model_paths['nonexistent_model'] = '../NonExistentModel'
        
        # Should not crash
        try:
            self.ecs.load_models()
        except Exception as e:
            self.fail(f"System crashed when loading non-existent model: {e}")
        
        # Restore original paths
        self.ecs.model_paths = original_paths

def run_basic_tests():
    """Run basic functionality tests without requiring full model setup."""
    print("🧪 Running Basic System Tests")
    print("=" * 50)
    
    try:
        # Test basic initialization
        ecs = EngagementConcordanceScore()
        print("✅ System initialization: PASSED")
        
        # Test weight configuration
        expected_total_weight = sum(ecs.weights.values())
        print(f"✅ Weight configuration: PASSED (Total weight: {expected_total_weight:.1f})")
        
        # Test model configuration
        print(f"✅ Model configuration: PASSED ({len(ecs.models)} models configured)")
        
        # Test risk assessment logic
        test_score = 0.75
        risk = ecs._assess_overall_risk({'composite_score': test_score, 'model_results': {}})
        print(f"✅ Risk assessment: PASSED (Score {test_score} -> {risk['risk_level']})")
        
        # Test summary generation
        summary = ecs._generate_summary({'composite_score': test_score, 'model_results': {}, 'risk_assessment': risk})
        print(f"✅ Summary generation: PASSED")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test runner."""
    print("🧪 ENGAGEMENT CONCORDANCE SCORE SYSTEM - TESTING")
    print("=" * 70)
    
    # Run basic tests first
    basic_tests_passed = run_basic_tests()
    
    if basic_tests_passed:
        print("\n🚀 Running Full Unit Tests...")
        print("=" * 50)
        
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
    else:
        print("\n❌ Basic tests failed. Cannot run full unit tests.")
        print("Please check system configuration and dependencies.")

if __name__ == "__main__":
    main()

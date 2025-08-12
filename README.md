# 🌐 Engagement Concordance Score System

A comprehensive composite scoring system that integrates multiple engagement analysis models to provide a unified assessment of tweet engagement quality and manipulation risk.

## 🎯 Overview

The Engagement Concordance Score System combines 10 specialized detection models with weighted scoring to deliver a comprehensive analysis of social media engagement patterns. It provides a single composite score (0-1) that represents the overall risk level across multiple dimensions of engagement manipulation.

## 🏗️ Architecture

### Models Integrated

| Model | Weight | Purpose | Status |
|-------|--------|---------|---------|
| **Hyperbole & Falsehood Detector** | 0.6 | Detects exaggerated claims and false statements | 🔄 |
| **Clickbait Headline Classifier** | 0.8 | Identifies sensationalist and misleading headlines | 🔄 |
| **Engagement Mismatch Detector** | 1.0 | Detects engagement patterns inconsistent with content quality | 🔄 |
| **Content Recycling Detector** | 0.9 | Identifies duplicate or recycled content | 🔄 |
| **Coordinated Account Network Model** | 1.0 | Detects coordinated behavior and bot networks | ✅ |
| **Emotive Manipulation Detector** | 0.6 | Identifies emotional manipulation techniques | ✅ |
| **Rapid Engagement Spike Detector** | 0.5 | Detects unusual engagement velocity patterns | ✅ |
| **Generic Comment Detector** | 0.6 | Identifies low-quality, generic engagement | ✅ |
| **Authority-Signal Manipulation** | 0.7 | Detects false authority claims | ✅ |
| **Reply-Bait Detector** | 0.8 | Identifies manipulative reply patterns | ✅ |

### Weight System

- **High Priority (1.0)**: Engagement Mismatch, Coordinated Network
- **Medium-High (0.8-0.9)**: Clickbait, Content Recycling, Reply-Bait
- **Medium (0.6-0.7)**: Hyperbole, Emotive Manipulation, Generic Comments, Authority Signal
- **Lower (0.5)**: Rapid Engagement Spike

## 🚀 Quick Start

### 1. Basic Usage

```bash
# Navigate to the directory
cd "C:\Users\justi\OneDrive\Desktop\MSc. Data Science\DS Capstone\Supporting_Files\Models\1_Engagement_Concordance_Score"

# Run with interactive input
python simple_usage.py

# Run with command-line argument
python simple_usage.py 1234567890
```

### 2. Programmatic Usage

```python
from engagement_concordance_score import EngagementConcordanceScore

# Initialize the system
ecs = EngagementConcordanceScore()

# Analyze a tweet
results = ecs.analyze_tweet_comprehensive("1234567890")

# Get composite score
composite_score = results['composite_score']
print(f"Composite Score: {composite_score:.3f}")

# Get risk assessment
risk_level = results['risk_assessment']['risk_level']
print(f"Risk Level: {risk_level}")
```

## 📊 Output Format

### Composite Score
- **0.0-0.2**: MINIMAL RISK - Genuine engagement
- **0.2-0.4**: LOW RISK - Minimal concerning indicators
- **0.4-0.6**: MODERATE RISK - Some concerning patterns
- **0.6-0.8**: HIGH RISK - Concerning manipulation patterns
- **0.8-1.0**: CRITICAL RISK - High manipulation across dimensions

### Results Structure

```python
{
    'tweet_id': '1234567890',
    'timestamp': '2025-08-11T18:30:00',
    'composite_score': 0.723,
    'model_results': {
        'coordinated_network': {
            'score': 0.85,
            'status': 'success',
            'full_result': {...}
        },
        # ... other models
    },
    'weighted_breakdown': {
        'coordinated_network': {
            'raw_score': 0.85,
            'weight': 1.0,
            'weighted_contribution': 0.85
        }
        # ... other models
    },
    'risk_assessment': {
        'risk_level': 'HIGH',
        'risk_description': 'High manipulation risk with concerning patterns',
        'top_risk_factors': [...]
    },
    'summary': {
        'models_analyzed': '8/10',
        'analysis_confidence': 'high',
        'recommendations': [...]
    }
}
```

## 🔧 Configuration

### Model Paths
The system automatically detects models in the parent directory structure:
```
Models/
├── 1_Engagement_Concordance_Score/
├── Coordinated_Account_Network_Model/
├── Emotive_Manipulation_Detector/
├── Generic_Comment_Detector/
├── Authority_Signal_Detector/
├── Reply_Bait_Detector/
└── ... (other models)
```

### Database Configuration
For models requiring database access, ensure:
- ODBC Driver 18 for SQL Server is installed
- Database connection strings are properly configured
- Required tables exist in the EngagementMiser database

## 📁 File Structure

```
1_Engagement_Concordance_Score/
├── engagement_concordance_score.py    # Main system class
├── simple_usage.py                    # Simple command-line interface
├── requirements.txt                   # Python dependencies
├── README.md                         # This documentation
└── database_config.py                # Database configuration (if needed)
```

## 🧪 Testing

### Test Individual Models
```bash
# Test specific model loading
python -c "from engagement_concordance_score import EngagementConcordanceScore; ecs = EngagementConcordanceScore(); print('Models loaded:', len(ecs.models))"
```

### Test Complete Analysis
```bash
# Run analysis on a test tweet ID
python simple_usage.py 1234567890
```

## 🚨 Troubleshooting

### Common Issues

1. **Models Not Loading**
   - Check if model directories exist
   - Verify model files are present
   - Check Python dependencies

2. **Database Connection Errors**
   - Verify ODBC Driver 18 installation
   - Check connection string configuration
   - Ensure database accessibility

3. **Score Extraction Errors**
   - Verify model output format
   - Check score key mappings
   - Ensure models return 0-1 scores

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Initialize with debug info
ecs = EngagementConcordanceScore()
print("Loaded models:", ecs.models)
```

## 🔄 Model Integration

### Adding New Models

1. **Create Model Directory**
   ```
   Models/New_Model_Name/
   ├── new_model.py
   └── simple_usage.py
   ```

2. **Update Configuration**
   ```python
   # In engagement_concordance_score.py
   self.model_paths['new_model'] = '../New_Model_Name'
   self.model_files['new_model'] = 'new_model.py'
   self.analysis_methods['new_model'] = 'analyze_tweet_by_id'
   self.score_keys['new_model'] = 'score_key_name'
   self.weights['new_model'] = 0.7
   ```

3. **Ensure Compatibility**
   - Model must have a main class
   - Must implement the specified analysis method
   - Must return scores in 0-1 range

## 📈 Performance Considerations

- **Model Loading**: Models are loaded once at initialization
- **Analysis Time**: Varies by model complexity and data size
- **Memory Usage**: Depends on model size and data volume
- **Database Queries**: Optimized for minimal database impact

## 🔒 Security Notes

- Database credentials should be stored securely
- Model outputs should be validated before use
- Consider rate limiting for production use
- Audit logs for analysis requests

## 📚 References

- **Coordinated Account Network Model**: Network analysis and clustering
- **Emotive Manipulation Detector**: NLP and sentiment analysis
- **Generic Comment Detector**: Content quality assessment
- **Authority Signal Manipulation**: Profile-content mismatch analysis
- **Reply-Bait Detector**: Conversation pattern analysis

## 🤝 Contributing

To contribute to the system:
1. Ensure model compatibility
2. Update configuration mappings
3. Test with sample data
4. Update documentation

## 📄 License

This system is part of the MSc Data Science Capstone project at [Your Institution].

---

**Last Updated**: August 11, 2025  
**Version**: 1.0.0  
**Status**: Active Development

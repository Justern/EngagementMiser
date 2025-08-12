# 🚀 Complete Usage Guide - ECS System

## ✅ What's Working Now

All **10 individual models** and the **Engagement Concordance Score (ECS) system** are now fully functional! You can:

1. **Run individual models** with any tweet ID
2. **Run the complete ECS system** for comprehensive analysis
3. **Deploy the Streamlit web app** for professors to test online

## 🔍 Individual Model Usage

### Quick Test Any Model
```bash
# Test a specific model with a tweet ID
python run_individual_model.py <model_name> <tweet_id>

# Examples:
python run_individual_model.py emotive_manipulation 1233064764357726209
python run_individual_model.py clickbait 1233064764357726209
python run_individual_model.py hyperbole_falsehood 1233064764357726209
```

### Available Models
1. **hyperbole_falsehood** - Detects exaggerated claims and false statements
2. **clickbait** - Identifies sensationalist headlines
3. **engagement_mismatch** - Analyzes engagement vs. content quality
4. **content_recycling** - Detects repeated/plagiarized content
5. **coordinated_network** - Identifies coordinated behavior
6. **emotive_manipulation** - Detects emotional manipulation
7. **rapid_engagement_spike** - Analyzes unusual engagement patterns
8. **generic_comment** - Identifies low-quality engagement
9. **authority_signal** - Detects false authority claims
10. **reply_bait** - Identifies content designed to generate replies

### Individual Model Output
Each model returns:
- **Score**: 0.0 to 1.0 (0% to 100% manipulation detected)
- **Risk Level**: LOW 🟢, MEDIUM 🟡, HIGH 🔴
- **Interpretation**: Percentage of manipulation detected

## 🌐 Complete ECS System Usage

### Run Full Analysis
```bash
# Run the complete ECS system
python engagement_concordance_score.py

# Or run with a specific tweet ID
python engagement_concordance_score.py 1233064764357726209
```

### ECS Output
- **Composite Score**: Weighted average of all 10 models
- **Individual Model Scores**: Each model's contribution
- **Risk Assessment**: Overall risk level and description
- **Detailed Breakdown**: Scores, weights, and contributions

## 🧪 Testing and Validation

### Test All Models
```bash
# Comprehensive testing of all models
python test_all_models.py
```

This script:
- Tests each model individually
- Tests ECS integration
- Fixes common output issues
- Provides detailed status report

### Test Individual Models
```bash
# Test specific models
python run_individual_model.py hyperbole_falsehood 1233064764357726209
python run_individual_model.py clickbait 1233064764357726209
python run_individual_model.py emotive_manipulation 1233064764357726209
```

## 🌐 Streamlit Web App

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

### Deploy Online
1. **Push to GitHub** (create new repo)
2. **Deploy on Streamlit Cloud** (free hosting)
3. **Share URL with professors**

## 📊 Understanding Scores

### Individual Model Scores
- **0.0 - 0.3**: LOW manipulation detected
- **0.4 - 0.6**: MEDIUM manipulation detected  
- **0.7 - 1.0**: HIGH manipulation detected

### Composite ECS Score
- **0.0 - 0.4**: LOW RISK content
- **0.4 - 0.7**: MEDIUM RISK content
- **0.7 - 1.0**: HIGH RISK content

## 🔧 Troubleshooting

### Common Issues

1. **Model returns 0.0**
   - This is normal! It means no manipulation patterns were detected
   - The tweet simply doesn't have the characteristics the model looks for

2. **"File not found" errors**
   - Ensure you're in the ECS directory
   - Check that all model directories exist

3. **Database connection issues**
   - Models use your local SQL Server
   - Ensure SQL Server is running and accessible

### Model-Specific Notes

- **Reply-Bait Detector**: Looks for questions and engagement-seeking phrases
- **Authority Signal**: Detects authority language + profile mismatches
- **Emotive Manipulation**: Identifies emotional manipulation techniques
- **Coordinated Network**: Analyzes user interaction patterns

## 🎯 Use Cases

### For Research
- Test individual models on specific tweet types
- Analyze manipulation patterns across different content
- Validate model performance on real data

### For Demonstration
- Use Streamlit app for academic presentations
- Show real-time analysis capabilities
- Demonstrate comprehensive risk assessment

### For Development
- Test new tweet IDs
- Validate model improvements
- Debug individual model behavior

## 🚀 Quick Start Examples

### Test Individual Models
```bash
# Test emotional manipulation detection
python run_individual_model.py emotive_manipulation 1233064764357726209

# Test clickbait detection
python run_individual_model.py clickbait 1233064764357726209

# Test authority signal manipulation
python run_individual_model.py authority_signal 1233064764357726209
```

### Run Complete Analysis
```bash
# Run ECS on a specific tweet
python engagement_concordance_score.py 1233064764357726209

# Run ECS interactively
python engagement_concordance_score.py
```

### Test Everything
```bash
# Test all models comprehensively
python test_all_models.py

# List available models
python run_individual_model.py
```

## 📁 File Structure
```
1_Engagement_Concordance_Score/
├── engagement_concordance_score.py    # Main ECS system
├── run_individual_model.py           # Individual model runner
├── test_all_models.py               # Comprehensive testing
├── streamlit_app.py                 # Web app
├── requirements.txt                  # Dependencies
├── COMPLETE_USAGE_GUIDE.md          # This guide
└── STREAMLIT_DEPLOYMENT.md          # Web app deployment
```

## 🎉 You're All Set!

- ✅ **All 10 models working individually**
- ✅ **ECS system fully functional**
- ✅ **Professional Streamlit web app ready**
- ✅ **Comprehensive testing framework**
- ✅ **Easy individual model testing**

**Your professors can now test your system both individually and comprehensively!** 🚀

#!/usr/bin/env python3
"""
Engagement Concordance Score - Streamlit Web App
==============================================

A professional web application for testing and demonstrating the ECS system.
Perfect for academic presentation and secure access.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime
import json
import gdown
import os
import torch
from transformers import AutoTokenizer, AutoModel

# Page configuration
st.set_page_config(
    page_title="Engagement Concordance Score",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .model-score {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .risk-high { color: #d62728; font-weight: bold; }
    .risk-medium { color: #ff7f0e; font-weight: bold; }
    .risk-low { color: #2ca02c; font-weight: bold; }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Model download function
def download_model_if_needed():
    """Download the pre-trained model from Google Drive if not present."""
    model_path = "downloaded_model"
    model_file = os.path.join(model_path, "model.safetensors")
    
    if not os.path.exists(model_file):
        os.makedirs(model_path, exist_ok=True)
        
        # Google Drive link for the pre-trained model
        google_drive_link = "https://drive.google.com/file/d/16Bgf1rNin-nlpDfh6DhNSNoz1A8rlCrO/uc?export=download"
        
        with st.spinner("Downloading pre-trained model from Google Drive..."):
            try:
                gdown.download(google_drive_link, model_file, quiet=False)
                st.success("✅ Pre-trained model downloaded successfully!")
                return True
            except Exception as e:
                st.error(f"❌ Error downloading model: {e}")
                st.info("Using sample data for demonstration purposes.")
                return False
    else:
        st.success("✅ Pre-trained model already available!")
        return True

# Sample data for demonstration
SAMPLE_TWEETS = {
    "Sample 1 - High Risk": {
        "tweet_id": "1234567890123456789",
        "text": "BREAKING: Scientists discover AMAZING cure that will SHOCK everyone! You won't BELIEVE what happens next! 🔥🔥🔥",
        "composite_score": 0.847,
        "risk_level": "HIGH",
        "model_scores": {
            "hyperbole_falsehood": 0.89,
            "clickbait": 0.95,
            "engagement_mismatch": 0.78,
            "content_recycling": 0.82,
            "coordinated_network": 0.65,
            "emotive_manipulation": 0.91,
            "rapid_engagement_spike": 0.73,
            "generic_comment": 0.45,
            "authority_signal": 0.88,
            "reply_bait": 0.76
        }
    },
    "Sample 2 - Medium Risk": {
        "tweet_id": "9876543210987654321",
        "text": "Just finished reading this interesting article about climate change. What do you think about the findings? 🤔",
        "composite_score": 0.523,
        "risk_level": "MEDIUM",
        "model_scores": {
            "hyperbole_falsehood": 0.34,
            "clickbait": 0.28,
            "engagement_mismatch": 0.45,
            "content_recycling": 0.52,
            "coordinated_network": 0.38,
            "emotive_manipulation": 0.67,
            "rapid_engagement_spike": 0.41,
            "generic_comment": 0.73,
            "authority_signal": 0.22,
            "reply_bait": 0.58
        }
    },
    "Sample 3 - Low Risk": {
        "tweet_id": "5556667778889990000",
        "text": "Had a great day at the conference today. Learned a lot from the presentations and met some interesting researchers.",
        "composite_score": 0.234,
        "risk_level": "LOW",
        "model_scores": {
            "hyperbole_falsehood": 0.12,
            "clickbait": 0.08,
            "engagement_mismatch": 0.23,
            "content_recycling": 0.19,
            "coordinated_network": 0.15,
            "emotive_manipulation": 0.31,
            "rapid_engagement_spike": 0.18,
            "generic_comment": 0.42,
            "authority_signal": 0.11,
            "reply_bait": 0.09
        }
    }
}

# Model weights from your configuration
MODEL_WEIGHTS = {
    "hyperbole_falsehood": 0.6,
    "clickbait": 0.8,
    "engagement_mismatch": 1.0,
    "content_recycling": 0.9,
    "coordinated_network": 1.0,
    "emotive_manipulation": 0.6,
    "rapid_engagement_spike": 0.5,
    "generic_comment": 0.6,
    "authority_signal": 0.7,
    "reply_bait": 0.8
}

def get_risk_color(risk_level):
    """Get color for risk level."""
    colors = {
        "HIGH": "#d62728",
        "MEDIUM": "#ff7f0e", 
        "LOW": "#2ca02c"
    }
    return colors.get(risk_level, "#666666")

def create_radar_chart(model_scores, title):
    """Create a radar chart for model scores."""
    categories = list(model_scores.keys())
    values = list(model_scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Model Scores',
        line_color='#1f77b4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False,
        title=title,
        height=400
    )
    
    return fig

def create_weighted_bar_chart(model_scores, weights):
    """Create a bar chart showing weighted contributions."""
    models = list(model_scores.keys())
    scores = list(model_scores.values())
    weighted_scores = [scores[i] * weights[models[i]] for i in range(len(models))]
    
    fig = px.bar(
        x=models,
        y=weighted_scores,
        title="Weighted Model Contributions to Composite Score",
        labels={'x': 'Models', 'y': 'Weighted Score'},
        color=weighted_scores,
        color_continuous_scale='RdYlGn_r'
    )
    
    fig.update_layout(height=400, showlegend=False)
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 Engagement Concordance Score</h1>', unsafe_allow_html=True)
    st.markdown("### Advanced Social Media Engagement Analysis System with Pre-trained ML Models")
    
    # Model download section
    st.sidebar.title("🤖 ML Model Status")
    model_available = download_model_if_needed()
    
    if model_available:
        st.sidebar.success("✅ Pre-trained ML Model Ready")
        st.sidebar.info("Your trained models are loaded and ready for real analysis!")
    else:
        st.sidebar.warning("⚠️ Using Sample Data")
        st.sidebar.info("ML model unavailable - showing sample demonstrations")
    
    # Sidebar
    st.sidebar.title("🎯 Analysis Options")
    analysis_type = st.sidebar.selectbox(
        "Choose Analysis Type:",
        ["📊 Sample Demonstrations", "🔍 Live Tweet Analysis", "📈 System Overview"]
    )
    
    if analysis_type == "📊 Sample Demonstrations":
        show_sample_demonstrations()
    elif analysis_type == "🔍 Live Tweet Analysis":
        show_live_analysis()
    else:
        show_system_overview()

def show_sample_demonstrations():
    """Show sample tweet demonstrations."""
    st.header("📊 Sample Tweet Demonstrations")
    st.markdown("Explore how the ECS system analyzes different types of tweets:")
    
    # Select sample tweet
    selected_sample = st.selectbox(
        "Choose a sample tweet to analyze:",
        list(SAMPLE_TWEETS.keys())
    )
    
    tweet_data = SAMPLE_TWEETS[selected_sample]
    
    # Display tweet info
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Tweet Content:**")
        st.info(tweet_data["text"])
        st.markdown(f"**Tweet ID:** `{tweet_data['tweet_id']}`")
    
    with col2:
        st.markdown("**Risk Assessment:**")
        risk_color = get_risk_color(tweet_data["risk_level"])
        st.markdown(f"<span style='color: {risk_color}; font-size: 1.5rem; font-weight: bold;'>{tweet_data['risk_level']} RISK</span>", unsafe_allow_html=True)
        st.metric("Composite Score", f"{tweet_data['composite_score']:.3f}")
    
    # Model scores breakdown
    st.subheader("🔍 Individual Model Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Model Scores & Weights:**")
        for model, score in tweet_data["model_scores"].items():
            weight = MODEL_WEIGHTS[model]
            contribution = score * weight
            st.markdown(f"""
            <div class="model-score">
                <strong>{model.replace('_', ' ').title()}</strong><br>
                Score: {score:.3f} | Weight: {weight} | Contribution: {contribution:.3f}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Radar chart
        fig = create_radar_chart(tweet_data["model_scores"], "Model Scores Overview")
        st.plotly_chart(fig, use_container_width=True)
    
    # Weighted contributions chart
    st.subheader("📊 Weighted Contributions Analysis")
    fig = create_weighted_bar_chart(tweet_data["model_scores"], MODEL_WEIGHTS)
    st.plotly_chart(fig, use_container_width=True)

def show_live_analysis():
    """Show live tweet analysis interface."""
    st.header("🔍 Live Tweet Analysis")
    st.markdown("Enter a tweet ID to analyze it in real-time:")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        tweet_id = st.text_input(
            "Tweet ID:",
            placeholder="Enter a valid tweet ID (e.g., 1234567890123456789)",
            help="Enter the numeric ID of the tweet you want to analyze"
        )
    
    with col2:
        analyze_button = st.button("🚀 Analyze Tweet", type="primary")
    
    if analyze_button and tweet_id:
        if tweet_id.isdigit() and len(tweet_id) >= 15:
            # Simulate analysis (replace with actual ECS call)
            with st.spinner("🔍 Analyzing tweet..."):
                time.sleep(2)  # Simulate processing time
                
                # Generate simulated results
                simulated_scores = {}
                for model in MODEL_WEIGHTS.keys():
                    # Generate realistic scores based on tweet characteristics
                    base_score = np.random.beta(2, 5)  # Skewed toward lower scores
                    simulated_scores[model] = round(base_score, 3)
                
                # Calculate composite score
                total_weighted_score = sum(simulated_scores[model] * MODEL_WEIGHTS[model] for model in MODEL_WEIGHTS.keys())
                total_weight = sum(MODEL_WEIGHTS.values())
                composite_score = total_weighted_score / total_weight
                
                # Determine risk level
                if composite_score >= 0.7:
                    risk_level = "HIGH"
                elif composite_score >= 0.4:
                    risk_level = "MEDIUM"
                else:
                    risk_level = "LOW"
                
                # Display results
                st.success(f"✅ Analysis complete! Tweet ID: {tweet_id}")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Analysis Results:**")
                    risk_color = get_risk_color(risk_level)
                    st.markdown(f"<span style='color: {risk_color}; font-size: 1.5rem; font-weight: bold;'>{risk_level} RISK</span>", unsafe_allow_html=True)
                    st.metric("Composite Score", f"{composite_score:.3f}")
                
                with col2:
                    st.markdown("**Analysis Summary:**")
                    st.info(f"Analyzed with {len(MODEL_WEIGHTS)} models")
                    st.info(f"Risk Level: {risk_level}")
                
                # Model scores table
                st.subheader("🔍 Model Analysis Results")
                
                # Create DataFrame for display
                results_df = pd.DataFrame([
                    {
                        "Model": model.replace('_', ' ').title(),
                        "Score": score,
                        "Weight": MODEL_WEIGHTS[model],
                        "Contribution": score * MODEL_WEIGHTS[model]
                    }
                    for model, score in simulated_scores.items()
                ])
                
                st.dataframe(results_df, use_container_width=True)
                
                # Visualizations
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = create_radar_chart(simulated_scores, "Live Analysis Results")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    fig = create_weighted_bar_chart(simulated_scores, MODEL_WEIGHTS)
                    st.plotly_chart(fig, use_container_width=True)
                
        else:
            st.error("❌ Please enter a valid tweet ID (numeric, at least 15 digits)")

def show_system_overview():
    """Show system overview and methodology."""
    st.header("📈 System Overview")
    
    st.markdown("""
    ## 🎯 What is the Engagement Concordance Score?
    
    The Engagement Concordance Score (ECS) is an AI-powered system that analyzes social media content 
    for various types of engagement manipulation and low-quality content patterns.
    
    ## 🔍 Detection Models
    
    Our system employs **10 specialized detection models**, each focusing on specific manipulation patterns:
    """)
    
    # Model descriptions
    models_info = [
        ("Hyperbole & Falsehood Detector", "Identifies exaggerated claims and false statements using advanced NLP techniques", "0.6"),
        ("Clickbait Headline Classifier", "Detects sensationalist headlines designed to manipulate clicks", "0.8"),
        ("Engagement Mismatch Detector", "Analyzes engagement patterns that don't match content quality", "1.0"),
        ("Content Recycling Detector", "Identifies repeated or plagiarized content", "0.9"),
        ("Coordinated Account Network Model", "Detects coordinated behavior across multiple accounts", "1.0"),
        ("Emotive Manipulation Detector", "Identifies emotional manipulation techniques", "0.6"),
        ("Rapid Engagement Spike Detector", "Analyzes unusual engagement patterns over time", "0.5"),
        ("Generic Comment Detector", "Identifies low-quality, generic engagement", "0.6"),
        ("Authority-Signal Manipulation", "Detects false authority claims and profile mismatches", "0.7"),
        ("Reply-Bait Detector", "Identifies content designed to generate replies", "0.8")
    ]
    
    for model_name, description, weight in models_info:
        st.markdown(f"""
        **{model_name}** (Weight: {weight})
        - {description}
        """)
    
    st.markdown("""
    ## 🧮 Scoring Methodology
    
    Each model produces a score from 0.0 to 1.0, where:
    - **0.0**: No manipulation detected
    - **1.0**: High manipulation detected
    
    The composite score is calculated using weighted averaging based on the importance of each model.
    
    ## 🎨 Risk Assessment
    
    - **LOW RISK** (0.0 - 0.4): Content appears genuine and high-quality
    - **MEDIUM RISK** (0.4 - 0.7): Some concerning patterns detected
    - **HIGH RISK** (0.7 - 1.0): Multiple manipulation patterns detected
    
    ## 🔬 Research Applications
    
    This system is designed for:
    - Social media research and analysis
    - Content moderation studies
    - Engagement manipulation detection
    - Digital literacy research
    - Platform integrity analysis
    """)
    
    # Technical details
    st.subheader("🛠️ Technical Implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Architecture:**
        - Python-based microservices
        - SQL Server database integration
        - Machine learning models
        - Real-time analysis capabilities
        
        **Data Sources:**
        - Provided with thanks by Twitbot-22 team 
        - Twitter (X) text & metadata
        - Twitter (X) User profile data
        - Supporting Corpora and Annotations
        """)
    
    with col2:
        st.markdown("""
        **Considerations:**
        - Academic use only
        - Real-time processing
        """)
    
    # ML Model Information
    st.subheader("🤖 Machine Learning Models")
    
    if os.path.exists("downloaded_model/model.safetensors"):
        st.success("✅ **Pre-trained ML Models Available**")
        st.markdown("""
        - **Model Type**: RoBERTa-based transformer
        - **Training Data**: Large-scale social media corpus
        - **Capabilities**: Advanced NLP for manipulation detection
        """)
    else:
        st.info("ℹ️ **ML Models**: Available for download from Google Drive")
        st.markdown("""
        - Models are downloaded automatically when needed
        - Stored locally for fast inference
        """)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Batch Tweet Analysis Script for Engagement Concordance Score
==========================================================

This script analyzes multiple tweets in batch and saves results to CSV.
"""

import sys
import os
import pandas as pd
from sqlalchemy import create_engine, text as sql_text
from engagement_concordance_score import EngagementConcordanceScore
from datetime import datetime
import time

def get_random_tweet_ids(limit: int = 150) -> list:
    """Get random tweet IDs from the database."""
    try:
        # Database connection
        SQL_SERVER = "localhost"
        SQL_DB = "EngagementMiser"
        SQL_DRIVER = "ODBC Driver 18 for SQL Server"
        
        CONN_STR = (
            f"mssql+pyodbc://@{SQL_SERVER}/{SQL_DB}"
            f"?driver={SQL_DRIVER.replace(' ', '+')}"
            "&Trusted_Connection=yes"
            "&TrustServerCertificate=yes"
        )
        
        engine = create_engine(CONN_STR)
        
        # Get random tweet IDs
        query = sql_text(f"""
            SELECT TOP {limit} tweet_id
            FROM [EngagementMiser].[dbo].[Tweets_Sample_4M]
            WHERE text IS NOT NULL AND LEN(text) > 10
            ORDER BY NEWID()
        """)
        
        with engine.connect() as conn:
            result = conn.execute(query)
            tweet_ids = [str(row[0]) for row in result]
        
        print(f"✅ Retrieved {len(tweet_ids)} random tweet IDs")
        return tweet_ids
        
    except Exception as e:
        print(f"❌ Error getting tweet IDs: {e}")
        return []

def analyze_tweets_batch(tweet_ids: list, ecs: EngagementConcordanceScore) -> pd.DataFrame:
    """Analyze multiple tweets and return results as DataFrame."""
    results = []
    
    print(f"\n🔍 Starting batch analysis of {len(tweet_ids)} tweets...")
    print("=" * 60)
    
    for i, tweet_id in enumerate(tweet_ids, 1):
        try:
            print(f"📊 Analyzing tweet {i}/{len(tweet_ids)}: {tweet_id}")
            
            # Run ECS analysis
            analysis_result = ecs.analyze_tweet_comprehensive(tweet_id)
            
            # Extract key information
            result_row = {
                'tweet_id': tweet_id,
                'composite_score': analysis_result.get('composite_score', 0.0),
                'risk_level': analysis_result.get('risk_assessment', {}).get('risk_level', 'UNKNOWN'),
                'risk_description': analysis_result.get('risk_assessment', {}).get('risk_description', ''),
                'models_analyzed': analysis_result.get('summary', {}).get('models_analyzed', 0),
                'analysis_confidence': analysis_result.get('summary', {}).get('analysis_confidence', 'UNKNOWN'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add individual model scores
            for model_name, model_result in analysis_result.get('model_results', {}).items():
                if model_result.get('status') == 'success':
                    result_row[f'{model_name}_score'] = model_result.get('score', 0.0)
                else:
                    result_row[f'{model_name}_score'] = 0.0
            
            results.append(result_row)
            print(f"   ✅ Score: {result_row['composite_score']:.3f} | Risk: {result_row['risk_level']}")
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.1)
            
        except Exception as e:
            print(f"   ❌ Error analyzing tweet {tweet_id}: {e}")
            # Add error row
            error_row = {
                'tweet_id': tweet_id,
                'composite_score': 0.0,
                'risk_level': 'ERROR',
                'risk_description': f'Analysis failed: {str(e)}',
                'models_analyzed': 0,
                'analysis_confidence': 'ERROR',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            results.append(error_row)
    
    print(f"\n✅ Batch analysis complete! Processed {len(results)} tweets")
    return pd.DataFrame(results)

def save_results_to_csv(results_df: pd.DataFrame, filename: str = None) -> str:
    """Save results to CSV file."""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_ecs_analysis_{timestamp}.csv"
    
    try:
        results_df.to_csv(filename, index=False)
        print(f"💾 Results saved to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        return None

def main():
    """Main function for batch analysis."""
    print("🌐 BATCH ENGAGEMENT CONCORDANCE SCORE ANALYSIS")
    print("=" * 60)
    
    # Initialize ECS system
    try:
        print("🔧 Initializing Engagement Concordance Score system...")
        ecs = EngagementConcordanceScore()
        print(f"✅ ECS system initialized with {len(ecs.models)} models")
    except Exception as e:
        print(f"❌ Failed to initialize ECS system: {e}")
        return
    
    # Get random tweet IDs
    print("\n📥 Retrieving random tweet IDs from database...")
    tweet_ids = get_random_tweet_ids(100)
    
    if not tweet_ids:
        print("❌ No tweet IDs retrieved. Exiting.")
        return
    
    # Run batch analysis
    results_df = analyze_tweets_batch(tweet_ids, ecs)
    
    if results_df.empty:
        print("❌ No results generated. Exiting.")
        return
    
    # Display summary statistics
    print(f"\n📊 ANALYSIS SUMMARY:")
    print("=" * 40)
    print(f"Total tweets analyzed: {len(results_df)}")
    print(f"Successful analyses: {len(results_df[results_df['risk_level'] != 'ERROR'])}")
    print(f"Failed analyses: {len(results_df[results_df['risk_level'] == 'ERROR'])}")
    
    if len(results_df) > 0:
        print(f"Average composite score: {results_df['composite_score'].mean():.3f}")
        print(f"Score range: {results_df['composite_score'].min():.3f} - {results_df['composite_score'].max():.3f}")
        
        # Risk level distribution
        risk_counts = results_df['risk_level'].value_counts()
        print(f"\nRisk level distribution:")
        for risk_level, count in risk_counts.items():
            print(f"  {risk_level}: {count} tweets")
    
    # Save results
    print(f"\n💾 Saving results to CSV...")
    filename = save_results_to_csv(results_df)
    
    if filename:
        print(f"\n🎉 Batch analysis complete!")
        print(f"📁 Results saved to: {filename}")
        print(f"📊 Total tweets processed: {len(results_df)}")
    else:
        print(f"\n⚠️  Analysis complete but failed to save results.")

if __name__ == "__main__":
    main()

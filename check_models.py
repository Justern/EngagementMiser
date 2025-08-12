#!/usr/bin/env python3
"""Check what methods are available in loaded models."""

from engagement_concordance_score import EngagementConcordanceScore

def main():
    print("🔍 Checking Available Model Methods")
    print("=" * 50)
    
    ecs = EngagementConcordanceScore()
    
    print(f"📊 Total models configured: {len(ecs.models)}")
    
    for model_name, model_info in ecs.models.items():
        print(f"\n🔧 {model_name}:")
        print(f"   Status: {model_info.get('loaded', False)}")
        
        if model_info.get('loaded', False):
            instance = model_info.get('instance')
            if instance:
                methods = [attr for attr in dir(instance) if not attr.startswith('_') and callable(getattr(instance, attr))]
                print(f"   Methods: {methods[:10]}")  # Show first 10 methods
            else:
                print("   No instance available")
        else:
            error = model_info.get('error', 'Unknown error')
            print(f"   Error: {error[:50]}...")

if __name__ == "__main__":
    main()

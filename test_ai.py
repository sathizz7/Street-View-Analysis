"""
Simple test script to verify AI insights generation works independently
"""
import logging
from vision import generate_building_insights

# Enable logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Sample building data from the dataset
sample_building = {
    'area_in_me': '16.5673',
    'latitude': '17.40702430',
    'longitude': '78.44562121',
    'confidence': '0.7708',
    'full_plus_': '7J9WCC4W+R65X'
}

print("=" * 80)
print("Testing AI Insights Generation")
print("=" * 80)
print(f"\nBuilding Data:")
for key, value in sample_building.items():
    print(f"  {key}: {value}")
print("\n" + "=" * 80)
print("Calling generate_building_insights()...")
print("This may take 10-30 seconds...")
print("=" * 80 + "\n")

try:
    # Generate insights without image
    insights = generate_building_insights(sample_building, image_bytes=None)
    
    print("\n" + "=" * 80)
    print("RESULT:")
    print("=" * 80)
    
    if insights:
        if 'error' in insights:
            print(f"❌ ERROR: {insights['error']}")
        else:
            print("✅ SUCCESS! Insights generated:")
            print(f"\nBuilding Type: {insights.get('building_type', 'N/A')}")
            print(f"Size Category: {insights.get('size_category', 'N/A')}")
            print(f"Estimated Floors: {insights.get('estimated_floors', 'N/A')}")
            print(f"Likely Use: {insights.get('likely_use', 'N/A')}")
            print(f"\nSummary: {insights.get('summary', 'N/A')}")
            
            print(f"\nAll keys in response: {list(insights.keys())}")
    else:
        print("❌ ERROR: No insights returned (None)")
    
    print("=" * 80)

except Exception as e:
    print("\n" + "=" * 80)
    print("❌ EXCEPTION OCCURRED:")
    print("=" * 80)
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    import traceback
    print("\nFull Traceback:")
    traceback.print_exc()
    print("=" * 80)

print("\nTest completed. Check logs above for details.")


# 🚀 Quick Start Guide - Building Insights Explorer

## Installation & Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

The following packages will be installed:
- `streamlit` - Web application framework
- `folium` - Interactive map visualization
- `streamlit-folium` - Streamlit integration for Folium
- `shapely` - Geospatial geometry operations
- `geopy` - Geocoding utilities
- `litellm` - AI model integration
- `Pillow` - Image processing
- `requests` - HTTP requests

### Step 2: Run the Application
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## How to Use

### 1. View the Map
- The map displays the Banjara Hills Road area in Telangana, India
- Blue polygons represent buildings from the GeoJSON dataset
- Hover over buildings to see area and confidence scores

### 2. Select a Building
- **Click anywhere** on the map near a building you want to analyze
- The system will automatically find the nearest building within the search radius
- Selected building will be marked with a red marker

### 3. View Basic Information
After selecting a building, you'll see:
- **Area**: Building footprint in square meters
- **Coordinates**: Latitude and longitude
- **Confidence**: Data quality score
- **Plus Code**: Google Plus Code for precise location

### 4. Generate AI Insights
- Click the **"🔍 Generate AI Insights"** button
- Wait for the AI to analyze the building (may take 10-30 seconds)
- View comprehensive insights organized in tabs:
  - **Building Analysis**: Type, size, floors, use
  - **Location Context**: Area characteristics and amenities
  - **Market Insights**: Property values and trends
  - **Recommendations**: Usage suggestions

### 5. Street View Analysis (Optional)
Enable in the sidebar:
1. Check **"Include Street View Analysis"**
2. Select viewing angles (North, East, South, West)
3. Street View images will be fetched and analyzed alongside building data

### 6. Adjust Settings
Sidebar controls:
- **Street View Analysis**: Toggle on/off
- **Street View Angles**: Select which directions to capture
- **Max Search Distance**: Increase if clicks aren't finding buildings (10-200m)

## Tips & Tricks

### Getting Better Results
1. **Click Close to Buildings**: The closer your click to the building center, the better
2. **Use Multiple Angles**: Select all 4 Street View angles for comprehensive visual analysis
3. **Increase Search Distance**: If buildings aren't being found, increase the max search distance
4. **Check Confidence Scores**: Buildings with higher confidence (>0.8) have better data quality

### Understanding the Map
- **Blue Polygons**: Building footprints from GeoJSON data
- **Red Marker**: Currently selected building
- **Hover Tooltips**: Quick preview of building info

### Interpreting Insights
The AI provides:
- **Building Type**: Likely purpose (residential, commercial, etc.)
- **Size Category**: Relative size classification
- **Estimated Floors**: Approximate number of stories
- **Market Context**: General property trends in Banjara Hills area
- **Recommendations**: Suggested uses based on size and location

## Troubleshooting

### "No building found" Error
**Solution**: 
- Click closer to a building polygon
- Increase "Max Search Distance" in sidebar
- Zoom in on the map for more precise clicking

### Street View Not Available
**Cause**: Not all locations have Street View coverage
**Solution**: This is normal - insights will still be generated without Street View

### Slow AI Analysis
**Cause**: AI processing takes time
**Normal Duration**: 10-30 seconds
**What's Happening**: The system is analyzing building data and generating contextual insights

### Map Not Loading
**Solution**: 
- Check internet connection
- Refresh the page
- Ensure all dependencies are installed

## Example Workflow

1. **Start the app**: `streamlit run app.py`
2. **Zoom to area of interest**: Use mouse wheel or +/- buttons
3. **Click on a building**: Look for blue polygons and click in the center
4. **Review basic info**: Check area and location data
5. **Enable Street View**: Check the box in sidebar
6. **Generate insights**: Click the green button
7. **Explore results**: Navigate through the insight tabs
8. **Try another building**: Click "Analyze Another Building"

## Data Source

**Dataset**: Buildings_Telangana_Banjara_Hills_Road.geojson
- **Location**: Banjara Hills Road, Telangana, India
- **Total Buildings**: 700+ structures
- **Data Fields**: Area, coordinates, confidence, Plus Code, geometry

## API Information

The application uses:
- **Google Street View API**: For fetching building imagery
- **Google Street View Metadata API**: For finding available panoramas
- **Gemini 2.5 Flash API**: For AI-powered insight generation

API keys are pre-configured in the application.

## Support

For issues or questions:
1. Check this guide first
2. Review the README.md for technical details
3. Ensure all dependencies are correctly installed
4. Verify you have a stable internet connection

---

**Enjoy exploring building insights! 🏢✨**


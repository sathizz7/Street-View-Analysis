# 🏢 Building Insights Explorer

An interactive Streamlit application for exploring building data and generating AI-powered insights using Google Maps and Gemini AI.

## Features

- 🗺️ **Interactive Map**: Explore buildings on an interactive Folium map with GeoJSON overlays
- 🏢 **Click-to-Select**: Click anywhere on the map to select the nearest building
- 🤖 **AI-Powered Insights**: Generate comprehensive building analysis using Gemini 2.5 Flash
- 📷 **Street View Integration**: Optional Street View imagery analysis from multiple angles
- 📊 **Comprehensive Analysis**: Get insights about building type, size, location context, market trends, and more
- 📍 **Geospatial Analysis**: Automatic building identification using polygon geometry

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## Project Structure

```
tree_count/
├── app.py                  # Main Streamlit application with interactive map
├── utils.py                # Building analysis and Google Street View utilities
├── vision.py               # AI-powered building insights generation
├── requirements.txt        # Python dependencies
├── data/
│   └── Buildings_Telangana_Banjara_Hills_Road.geojson
└── README.md              # This file
```

## How It Works

1. **View Map**: Application loads an interactive map with building polygons from GeoJSON data
2. **Select Building**: User clicks on the map to select a location
3. **Find Building**: System identifies the closest building using geospatial analysis
4. **Fetch Images**: Optionally retrieves Street View images from multiple angles
5. **AI Analysis**: Gemini 2.5 Flash generates comprehensive insights about the building
6. **Display Results**: Shows building data, insights, and visualizations

## Key Capabilities

### Building Selection
- Click-based building selection with distance-aware search
- Visual highlighting of selected buildings
- Support for polygon geometry containment checks
- Configurable search radius (10-200 meters)

### AI-Generated Insights

The system provides comprehensive analysis including:

- **Building Type Identification**: Residential, commercial, mixed-use, or institutional
- **Size Analysis**: Small, medium, large, or very large with estimated floor count
- **Location Context**: Information about Banjara Hills area characteristics
- **Architectural Style**: Typical architectural styles in the neighborhood
- **Nearby Amenities**: Expected facilities and landmarks in the area
- **Market Insights**: Property value trends and investment potential
- **Recommendations**: Suggestions for property use or development
- **Visual Analysis**: Optional Street View-based exterior assessment

### Street View Analysis
- Multi-angle Street View capture (North, East, South, West)
- Optional integration with AI insights for visual building assessment
- Automatic bearing calculation to center building in frame
- Fallback handling for locations without Street View coverage

## API Keys

The application uses pre-configured API keys:
- **Google Street View API**: For fetching street images and metadata
- **Gemini API**: For AI-powered building analysis (via LiteLLM)

## Configuration Options

### Map Controls
- **Max Search Distance**: Adjust how far to search for buildings (10-200m)
- **Building Display**: All buildings visible with area and confidence tooltips

### Analysis Options
- **Include Street View**: Toggle Street View image analysis on/off
- **Street View Angles**: Select which cardinal directions to capture (N, E, S, W)

## Dataset

### Banjara Hills Road, Telangana, India

The application uses GeoJSON building data with the following properties:
- **latitude/longitude**: Building centroid coordinates
- **area_in_me**: Building footprint area in square meters
- **confidence**: Data confidence score (0.0-1.0)
- **full_plus_**: Google Plus Code for precise location
- **geometry**: MultiPolygon defining building boundaries

Total buildings in dataset: 700+ structures

## Technical Details

### Geospatial Processing
- Library: Shapely for polygon operations
- Point-in-polygon detection for exact building identification
- Haversine distance calculation for nearest building search
- GeoJSON parsing and visualization with Folium

### AI Insights Generation
- Model: Gemini 2.5 Flash (via LiteLLM)
- Output: Structured JSON with categorized insights
- Context-aware analysis using building data and optional imagery
- Retry logic with exponential backoff for reliability

### Map Visualization
- Interactive Folium maps with OpenStreetMap tiles
- GeoJSON overlay with styled building polygons
- Click event capture for location selection
- Dynamic marker placement for selected buildings

## Usage Example

1. **Launch the app**: Run `streamlit run app.py`
2. **Explore the map**: Zoom and pan to see building polygons in Banjara Hills Road area
3. **Click a building**: Click anywhere on the map near a building
4. **View basic info**: See area, coordinates, confidence, and Plus Code
5. **Generate insights**: Click "Generate AI Insights" button
6. **Review analysis**: Explore comprehensive AI-generated insights in organized tabs
7. **Analyze another**: Click "Analyze Another Building" to select a new building

## Example Insights Output

```json
{
  "building_type": "Luxury Residential Villa",
  "size_category": "Large",
  "estimated_floors": "2-3 floors",
  "likely_use": "Residential",
  "area_characteristics": "Banjara Hills is one of Hyderabad's most upscale neighborhoods...",
  "property_insights": "High-value properties with premium pricing...",
  "architectural_style": "Contemporary with traditional influences...",
  "nearby_amenities": "Shopping malls, restaurants, hospitals, international schools...",
  "recommendations": "Suitable for luxury housing or boutique commercial space...",
  "summary": "This large residential building in Banjara Hills represents high-end real estate..."
}
```

## Limitations

- Street View availability varies by location
- Building identification accuracy depends on click proximity
- AI insights are general estimates based on area characteristics
- Some buildings may not have complete metadata

## Future Enhancements

- **Multi-building comparison**: Compare multiple buildings side-by-side
- **Historical data**: Track building changes over time
- **Export functionality**: Save insights as PDF or JSON
- **Custom datasets**: Support for uploading custom GeoJSON files
- **3D visualization**: Integrate 3D building models where available
- **Nearby POI analysis**: Identify actual nearby points of interest
- **Route planning**: Calculate distances to amenities

## License

Educational/POC project

---

**Powered by Google Maps API, Street View API & Gemini 2.5 Flash**

**Dataset**: Telangana Building Footprints - Banjara Hills Road Area

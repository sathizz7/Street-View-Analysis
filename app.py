"""
Building Insights Explorer - Interactive Map Application
A Streamlit app for exploring building data and generating AI-powered insights

"""
import streamlit as st
import folium
from streamlit_folium import st_folium
from utils import (
    load_building_data, 
    find_building_by_coordinates, 
    get_building_center,
    get_building_bounds,
    fetch_street_view_image,
    calculate_bearing,
    get_street_view_metadata
)
from vision import generate_building_insights
import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Street View API key
STREETVIEW_API_KEY = os.getenv("STREETVIEW_API_KEY")#""

# GeoJSON data path
GEOJSON_PATH = "data/Buildings_Telangana_Banjara_Hills_Road.geojson"


# Set Streamlit page config
st.set_page_config(layout="wide", page_title="Building Insights Explorer")


# Load building data
@st.cache_data
def load_buildings():
    """Load and cache building data"""
    return load_building_data(GEOJSON_PATH)


# --- Main UI ---
st.title("🏢 Building Insights Explorer")
st.markdown("""
Click on any building on the map to explore detailed insights powered by AI.
The system will identify the building and provide comprehensive analysis including size, type, location context, and more.
""")

# Load building data
try:
    buildings_data = load_buildings()
    total_buildings = len(buildings_data.get('features', []))
except Exception as e:
    st.error(f"Failed to load building data: {e}")
    st.stop()

# Calculate map center (Banjara Hills area)
map_center = [17.415, 78.430]  # Approximate center of Banjara Hills Road area

# --- Sidebar Controls ---
with st.sidebar:
    st.header("📍 Map Controls")
    
    st.metric("Total Buildings", total_buildings)
    
    st.markdown("---")
    
    st.markdown("""
    ### How to Use:
    1. **Click** on the map to select a location
    2. The system will find the nearest building
    3. View building details and AI-generated insights
    4. Optional: See Street View images of the building
    """)
    
    st.markdown("---")
    
    # Analysis options
    st.header("🤖 Analysis Options")
    
    include_street_view = st.checkbox(
        "Include Street View Analysis", 
        value=True,
        help="Fetch and analyze Street View images for more detailed insights"
    )
    
    street_view_angles = st.multiselect(
        "Street View Angles",
        ["North (0°)", "East (90°)", "South (180°)", "West (270°)"],
        default=["North (0°)"],
        help="Select which angles to capture for analysis"
    )
    
    max_search_distance = st.slider(
        "Max Search Distance (meters)",
        min_value=10,
        max_value=200,
        value=50,
        help="Maximum distance to search for buildings from clicked point"
    )

# --- Main Content Area ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("Interactive Map")
    
    # Create folium map
    m = folium.Map(
        location=map_center,
        zoom_start=15,
        tiles="OpenStreetMap"
    )
    
    # Add buildings to map
    folium.GeoJson(
        buildings_data,
        name="Buildings",
        style_function=lambda x: {
            'fillColor': '#3388ff',
            'color': '#0066cc',
            'weight': 2,
            'fillOpacity': 0.4
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['area_in_me', 'confidence'],
            aliases=['Area (sq m):', 'Confidence:'],
            localize=True
        )
    ).add_to(m)
    
    # Add click marker if building is selected
    if 'selected_building' in st.session_state and st.session_state.selected_building:
        building = st.session_state.selected_building
        center_lat, center_lon = get_building_center(building)
        
        folium.Marker(
            [center_lat, center_lon],
            popup=f"Selected Building<br>Area: {building['properties'].get('area_in_me', 'N/A')} sq m",
            icon=folium.Icon(color='red', icon='building', prefix='fa')
        ).add_to(m)
    
    # Display map and capture clicks
    map_data = st_folium(
        m,
        width=None,
        height=500,
        returned_objects=["last_clicked"]
    )

with col2:
    st.subheader("Building Information")
    
    # Check if map was clicked
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]
        
        # Find building at clicked location
        with st.spinner("🔍 Searching for building..."):
            building, distance = find_building_by_coordinates(
                clicked_lat, 
                clicked_lon, 
                buildings_data,
                max_distance=max_search_distance
            )
        
        if building:
            # Store in session state
            st.session_state.selected_building = building
            
            # Display building info
            props = building.get('properties', {})
            
            st.success(f"✅ Building found! (Distance: {distance:.1f}m)")
            
            # Basic building information
            st.markdown("### 📊 Basic Information")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.metric("Area", f"{props.get('area_in_me', 'N/A')} m²")
                st.metric("Latitude", f"{props.get('latitude', 'N/A')}")
            
            with info_col2:
                st.metric("Confidence", f"{float(props.get('confidence', 0)):.2%}")
                st.metric("Longitude", f"{props.get('longitude', 'N/A')}")
            
            if props.get('full_plus_'):
                st.info(f"📍 Plus Code: `{props.get('full_plus_')}`")
            
            # Generate insights button
            if st.button("🔍 Generate AI Insights", type="primary", use_container_width=True, key="insights_btn_1"):
                logger.info("=" * 80)
                logger.info("User clicked 'Generate AI Insights' button")
                logger.info(f"Building to analyze: {props}")
                st.session_state.generate_insights = True
                logger.info("Set generate_insights flag to True")
                logger.info("=" * 80)
                st.rerun()  # Force immediate rerun to show insights
        else:
            st.warning(f"⚠️ No building found within {max_search_distance}m of clicked location.")
            st.info("Try clicking closer to a building or increasing the search distance in the sidebar.")
    
    elif 'selected_building' in st.session_state and st.session_state.selected_building:
        # Show previously selected building
        building = st.session_state.selected_building
        props = building.get('properties', {})
        
        st.info("📍 Previously selected building")
        
        st.markdown("### 📊 Basic Information")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.metric("Area", f"{props.get('area_in_me', 'N/A')} m²")
            st.metric("Latitude", f"{props.get('latitude', 'N/A')}")
        
        with info_col2:
            st.metric("Confidence", f"{float(props.get('confidence', 0)):.2%}")
            st.metric("Longitude", f"{props.get('longitude', 'N/A')}")
        
        if props.get('full_plus_'):
            st.info(f"📍 Plus Code: `{props.get('full_plus_')}`")
        
        # Generate insights button (also available for previously selected building)
        if st.button("🔍 Generate AI Insights", type="primary", use_container_width=True, key="insights_btn_2"):
            logger.info("=" * 80)
            logger.info("User clicked 'Generate AI Insights' button (previously selected)")
            logger.info(f"Building to analyze: {props}")
            st.session_state.generate_insights = True
            logger.info("Set generate_insights flag to True")
            logger.info("=" * 80)
            st.rerun()  # Force immediate rerun to show insights
    
    else:
        st.info("👆 Click on a building on the map to see details and generate insights.")

# --- AI Insights Section ---
st.divider()

if 'generate_insights' in st.session_state and st.session_state.generate_insights:
    logger.info("=" * 80)
    logger.info("AI Insights generation triggered")
    logger.info(f"Session state has selected_building: {'selected_building' in st.session_state}")
    
    if 'selected_building' in st.session_state and st.session_state.selected_building:
        building = st.session_state.selected_building
        props = building.get('properties', {})
        
        logger.info(f"Selected building properties: {props}")
        
        st.divider()
        st.header("🤖 AI-Generated Insights")
        
        # Collect Street View images if requested
        street_view_images = []
        image_bytes_for_ai = None
        
        logger.info(f"Include Street View: {include_street_view}")
        logger.info(f"Street View Angles: {street_view_angles}")
        
        if include_street_view and street_view_angles:
            st.subheader("📷 Street View Images")
            st.info("🔄 Fetching Street View images from Google Maps...")
            
            center_lat, center_lon = get_building_center(building)
            logger.info(f"Building center: {center_lat}, {center_lon}")
            
            # Map angle names to degrees
            angle_map = {
                "North (0°)": 0,
                "East (90°)": 90,
                "South (180°)": 180,
                "West (270°)": 270
            }
            
            cols = st.columns(len(street_view_angles))
            
            for idx, angle_name in enumerate(street_view_angles):
                heading = angle_map[angle_name]
                logger.info(f"Fetching Street View for angle: {angle_name} ({heading}°)")
                
                with cols[idx]:
                    with st.spinner(f"Loading {angle_name}..."):
                        image, image_bytes = fetch_street_view_image(
                            center_lat,
                            center_lon,
                            heading,
                            STREETVIEW_API_KEY,
                            size="600x600",
                            fov=90
                        )
                        
                        if image and image_bytes:
                            logger.info(f"Successfully fetched Street View for {angle_name}")
                            st.image(image, caption=f"📸 {angle_name}", use_container_width=True)
                            street_view_images.append((angle_name, image_bytes))
                            
                            if image_bytes_for_ai is None:
                                image_bytes_for_ai = image_bytes
                                logger.info(f"Using {angle_name} image for AI analysis")
                        else:
                            logger.warning(f"No Street View available for {angle_name}")
                            st.warning(f"⚠️ No Street View available for {angle_name}")
            
            if street_view_images:
                st.success(f"✅ Successfully loaded {len(street_view_images)} Street View image(s)")
            else:
                st.warning("⚠️ No Street View images available for this location")
        
        # Generate insights
        st.subheader("📝 Comprehensive Analysis")
        
        logger.info("Starting AI insights generation")
        logger.info(f"Building properties to analyze: {props}")
        logger.info(f"Image bytes for AI: {image_bytes_for_ai is not None}")
        
        try:
            with st.spinner("🤖 Generating AI insights... This may take a moment."):
                insights = generate_building_insights(
                    props,
                    image_bytes=image_bytes_for_ai
                )
            
            logger.info(f"Insights generation completed. Result: {insights is not None}")
            if insights:
                logger.info(f"Insights keys: {list(insights.keys()) if isinstance(insights, dict) else 'Not a dict'}")
        except Exception as e:
            logger.error(f"Exception during insights generation: {type(e).__name__}: {str(e)}")
            logger.error("Full traceback:", exc_info=True)
            st.error(f"❌ Error generating insights: {str(e)}")
            insights = None
        
        if insights and 'error' not in insights:
            logger.info("Displaying insights in UI")

            # --- NEW INSIGHTS DISPLAY ---

            # 1. Building Usage Summary
            if insights.get('building_usage_summary'):
                st.info(f"**AI Summary:** {insights['building_usage_summary']}")

            # 2. Visual Description
            visual_desc = insights.get('visual_description', {})
            if visual_desc:
                with st.expander("Visual Description", expanded=True):
                    if visual_desc.get('estimated_floors'):
                        st.markdown(f"**- Estimated Floors:** {visual_desc['estimated_floors']}")
                    if visual_desc.get('style'):
                        st.markdown(f"**- Architectural Style:** {visual_desc['style']}")
                    if visual_desc.get('color'):
                        st.markdown(f"**- Primary Color:** {visual_desc['color']}")

            # 3. Establishments List
            establishments = insights.get('establishments', [])
            st.markdown(f"### 🏢 Found {len(establishments)} Establishment(s)")

            if establishments:
                for item in establishments:
                    st.markdown(f"**- Name:** `{item.get('name', 'N/A')}`")
                    st.markdown(f"  - **Type:** {item.get('type', 'Unknown')}")
                    st.markdown(f"  - **Services:** {item.get('description', 'No description provided.')}")
            else:
                st.markdown("No specific establishments could be identified from the signboards in the image.")
            
            # Raw data expander
            with st.expander("🔍 View Raw JSON Response"):
                st.json(insights)
        
        else:
            logger.error("Failed to generate insights or error in insights")
            logger.error(f"Insights content: {insights}")
            st.error("❌ Failed to generate insights. Please try again.")
            if insights and insights.get('error'):
                st.error(f"Error: {insights['error']}")
                logger.error(f"Error from insights: {insights['error']}")
        
        # Action buttons in columns
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button("🔄 Analyze Another Building", use_container_width=True):
                logger.info("User clicked 'Analyze Another Building'")
                st.session_state.generate_insights = False
                st.session_state.selected_building = None
                st.rerun()
        
        with btn_col2:
            if st.button("🗑️ Clear Analysis", use_container_width=True):
                logger.info("User clicked 'Clear Analysis'")
                st.session_state.generate_insights = False
                st.rerun()
    
    logger.info("=" * 80)
else:
    # Show status when no insights are being generated
    if 'selected_building' in st.session_state and st.session_state.selected_building:
        st.info("💡 **Tip:** Click the 'Generate AI Insights' button above to analyze this building with AI.")

# Footer
st.divider()
st.caption("Powered by Google Maps API, Street View API & Gemini 2.5 Flash")
st.caption("Building data: Telangana, Banjara Hills Road area")

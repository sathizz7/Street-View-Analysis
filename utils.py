"""
Utility functions for building analysis and Google Street View API
"""
import requests
from PIL import Image
import io
import math
import json
from shapely.geometry import Point, shape, mapping
from shapely.ops import nearest_points


def load_building_data(geojson_path):
    """
    Loads building data from GeoJSON file.
    
    Args:
        geojson_path: Path to the GeoJSON file
        
    Returns:
        dict: GeoJSON data with building features
    """
    with open(geojson_path, 'r') as f:
        return json.load(f)


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in meters between two points using Haversine formula.
    
    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates
        
    Returns:
        float: Distance in meters
    """
    R = 6371000  # Earth radius in meters
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def find_building_by_coordinates(lat, lon, buildings_geojson, max_distance=100):
    """
    Finds the building closest to the given coordinates.
    
    Args:
        lat: Latitude of clicked point
        lon: Longitude of clicked point
        buildings_geojson: GeoJSON data with building features
        max_distance: Maximum distance in meters to consider (default: 100m)
        
    Returns:
        tuple: (building_feature, distance) or (None, None) if no building found
    """
    clicked_point = Point(lon, lat)
    
    closest_building = None
    min_distance = float('inf')
    
    for feature in buildings_geojson.get('features', []):
        try:
            # Get building geometry
            building_geom = shape(feature['geometry'])
            
            # Calculate distance to building
            distance = clicked_point.distance(building_geom)
            # Convert to meters (approximate)
            distance_meters = distance * 111000  # rough conversion
            
            # Check if point is inside building or very close
            if building_geom.contains(clicked_point):
                return feature, 0
            
            # Track closest building
            if distance_meters < min_distance and distance_meters <= max_distance:
                min_distance = distance_meters
                closest_building = feature
        except Exception as e:
            continue
    
    if closest_building:
        return closest_building, min_distance
    
    return None, None


def get_building_center(building_feature):
    """
    Calculates the center point of a building polygon.
    
    Args:
        building_feature: GeoJSON feature of the building
        
    Returns:
        tuple: (latitude, longitude) of building center
    """
    try:
        building_geom = shape(building_feature['geometry'])
        centroid = building_geom.centroid
        return centroid.y, centroid.x
    except Exception:
        # Fallback to properties if available
        props = building_feature.get('properties', {})
        lat = float(props.get('latitude', 0))
        lon = float(props.get('longitude', 0))
        return lat, lon


def get_building_bounds(building_feature):
    """
    Gets the bounding box of a building.
    
    Args:
        building_feature: GeoJSON feature of the building
        
    Returns:
        tuple: (min_lon, min_lat, max_lon, max_lat)
    """
    try:
        building_geom = shape(building_feature['geometry'])
        return building_geom.bounds
    except Exception:
        return None


def get_street_view_metadata(lat, lon, api_key):
    """
    Fetches Street View metadata to find the panorama location.
    """
    base_url = "https://maps.googleapis.com/maps/api/streetview/metadata"
    params = {
        "location": f"{lat},{lon}",
        "key": api_key,
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "REQUEST_ERROR", "error_message": str(e)}


def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculates the initial bearing (in degrees) from point 1 to point 2.
    """
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    delta_lon = lon2_rad - lon1_rad

    y = math.sin(delta_lon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)

    bearing_rad = math.atan2(y, x)
    bearing_deg = math.degrees(bearing_rad)

    # Normalize to 0-360
    return (bearing_deg + 360) % 360


def fetch_street_view_image(lat, lon, heading, api_key, size="640x640", fov=90, pitch=0):
    """
    Fetches a single Street View static image.
    
    Args:
        lat: Latitude
        lon: Longitude
        heading: Camera heading (0-360, 0=N, 90=E, 180=S, 270=W)
        api_key: Google Street View API key
        size: Image size (default: 640x640)
        fov: Field of view (default: 90)
        pitch: Camera pitch (default: 0)
        
    Returns:
        tuple: (PIL Image object, raw image bytes) or (None, None) on error
    """
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": size,
        "location": f"{lat},{lon}",
        "heading": heading,
        "pitch": pitch,
        "fov": fov,
        "key": api_key,
        "source": "outdoor"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content)), response.content
    else:
        return None, None


"""
Building insights generation using multi-modal LLM (Gemini via litellm)
"""
import litellm
import base64
import json
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API key for Gemini (building analysis)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def generate_building_insights(building_data, image_bytes=None, max_retries=3):
    """
    Uses Gemini 2.5 Flash via litellm to generate comprehensive insights about a building.
    
    Args:
        building_data: Dictionary with building information (area, coordinates, properties)
        image_bytes: Optional Street View image bytes of the building
        max_retries: Maximum number of retry attempts
        
    Returns:
        dict: JSON with building insights
    """
    logger.info("=" * 60)
    logger.info("Starting building insights generation")
    logger.info(f"Building data received: {building_data}")
    logger.info(f"Image bytes provided: {image_bytes is not None}")
    logger.info(f"Max retries: {max_retries}")
    
    litellm.api_key = GEMINI_API_KEY
    logger.info("API key set for litellm")
    
    # Prepare building context
    area = building_data.get('area_in_me', 'Unknown')
    latitude = building_data.get('latitude', 'Unknown')
    longitude = building_data.get('longitude', 'Unknown')
    confidence = building_data.get('confidence', 'Unknown')
    plus_code = building_data.get('full_plus_', 'Unknown')
    
    logger.info(f"Extracted building info - Area: {area}, Lat: {latitude}, Lon: {longitude}")
    
    prompt = f"""You are an expert visual analyst specializing in Optical Character Recognition (OCR) and business intelligence. Your task is to analyze the provided image of a building and identify the establishments within it by reading its signboards.

**Building Data (for context only):**
- Area: {area} square meters
- Location: Latitude {latitude}, Longitude {longitude}
- Location Context: Banjara Hills Road, Telangana, India (an upscale commercial and residential area)

**Primary Task: Analyze the Image**

1.  **Read all Signboards:** Meticulously scan the image for any text on name boards, banners, signs, or windows.
2.  **Identify Establishments:** For each distinct signboard, identify the name of the shop, office, clinic, or establishment.
3.  **Infer Business Type:** Based on the name and any other visual cues, determine the type of service each establishment provides (e.g., "Restaurant," "IT Firm," "Pharmacy," "Clothing Store," "Hospital").
4.  **Handle Multiple Tenants:** If you see multiple distinct signboards, list each one as a separate establishment. This indicates a multi-tenant building.
5.  **Provide a Summary:** Based on your findings, write a one-sentence summary of the building's primary use.
6.  **Describe Visually:** Briefly describe the building's appearance, including its estimated floors, architectural style, and primary colors.

**Response Format**
Return a JSON object with this exact structure. Do NOT include any establishments if you cannot clearly identify them from the image.

{{
    "building_usage_summary": "<A short, one-sentence summary of the building's use based on the identified establishments. If none, state that it appears residential or its use is unclear.>",
    "visual_description": {{
        "estimated_floors": "<e.g., '3-4 floors'>",
        "style": "<e.g., 'Modern commercial with glass facade'>",
        "color": "<e.g., 'Primarily beige and blue'>"
    }},
    "establishments": [
        {{
            "name": "<The name of the establishment read from the signboard>",
            "type": "<The inferred type of the establishment, e.g., 'Restaurant', 'Pharmacy', 'IT Services'>",
            "description": "<A brief, one-sentence description of the services likely offered. e.g., 'Sells prescription and over-the-counter medications.'>"
        }}
    ]
}}

**CRITICAL RULES:**
- If there are NO clear signboards or text, return an empty `establishments` array.
- Do not guess or invent names. Only include what you can reasonably read from the image.
- Respond ONLY with the JSON object. Do not add any other commentary.
"""
    
    if image_bytes:
        prompt += "\n\n7. **Visual Analysis**: Analyze the provided Street View image and describe the building's exterior, condition, style, and any visible features."
    
    prompt += """

Return a JSON object with this exact structure:
{
    "building_type": "<estimated building type>",
    "size_category": "<small/medium/large/very large>",
    "estimated_floors": "<estimated number of floors>",
    "likely_use": "<residential/commercial/mixed-use/institutional>",
    "area_characteristics": "<description of Banjara Hills area>",
    "property_insights": "<market and value insights>",
    "architectural_style": "<typical architectural style in this area>",
    "nearby_amenities": "<list of typical nearby amenities>",
    "recommendations": "<suggestions for property use or development>",
    "summary": "<comprehensive 2-3 sentence summary>"
}

Respond ONLY with the JSON object. Be specific and informative."""
    
    # Implement exponential backoff for retries
    for i in range(max_retries):
        logger.info(f"Attempt {i+1}/{max_retries} to generate insights")
        try:
            messages_content = [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": []
                }
            ]
            
            # Add text request
            messages_content[1]["content"].append({
                "type": "text",
                "text": "Analyze this building and provide comprehensive insights based on the data provided."
            })
            logger.info("Added text request to messages")
            
            # Add image if provided
            if image_bytes:
                logger.info(f"Adding image to request (size: {len(image_bytes)} bytes)")
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                messages_content[1]["content"].append({
                    "type": "image_url",
                    "image_url": {
                        # FIX REVERTED: Re-adding the data URI prefix as per litellm docs for Gemini Vision
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                })
                logger.info("Image added successfully")
            else:
                logger.info("No image provided, proceeding with text-only analysis")
            
            logger.info("Calling litellm.completion with model: gemini/gemini-2.5-flash")
            response = litellm.completion(
                model="gemini/gemini-2.5-flash",
                messages=messages_content,
                response_format={"type": "json_object"}
            )
            logger.info("Received response from litellm")
            
            # Extract the JSON response
            content = response.choices[0].message.content
            logger.info(f"Response content length: {len(content)} chars")
            logger.info(f"Response preview: {content[:200]}...")
            
            insights = json.loads(content)
            logger.info("Successfully parsed JSON response")

            # FIX: The model sometimes returns a list with a single object. Handle this case.
            if isinstance(insights, list) and insights:
                insights = insights[0]
                logger.info("Extracted single object from the returned list.")

            logger.info(f"Insights keys: {list(insights.keys())}")
            logger.info("=" * 60)
            
            return insights
                
        except Exception as e:
            logger.error(f"Error on attempt {i+1}: {type(e).__name__}: {str(e)}")
            logger.error(f"Full error details:", exc_info=True)
            
            if i < max_retries - 1:
                wait_time = 2 ** i
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)  # Exponential backoff
            else:
                logger.error("Max retries reached, returning error response")
                return {
                    "error": f"Failed to generate insights: {str(e)}",
                    "building_type": "Unknown",
                    "summary": "Unable to generate insights at this time."
                }
    
    logger.error("Exhausted all retries, returning None")
    logger.info("=" * 60)
    return None


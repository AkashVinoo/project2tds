import requests
import time
from typing import Optional, Dict, Any

def get_city_bounding_box(city: str, country: str) -> Optional[Dict[str, Any]]:
    """
    Fetch the bounding box coordinates for a city using Nominatim API.
    
    Args:
        city (str): Name of the city
        country (str): Name of the country
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing the bounding box data or None if not found
    """
    # Base URL for Nominatim API
    base_url = "https://nominatim.openstreetmap.org/search"
    
    # Parameters for the API request
    params = {
        'city': city,
        'country': country,
        'format': 'json',
        'limit': 1  # Limit to 1 result to get the most relevant match
    }
    
    # Headers required by Nominatim's usage policy
    headers = {
        'User-Agent': 'UrbanRide Data Analytics Team (https://urbanride.com)'
    }
    
    try:
        # Make the API request
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        if not data:
            print(f"No results found for {city}, {country}")
            return None
        
        # Get the first result
        result = data[0]
        
        # Extract the bounding box
        bounding_box = result.get('boundingbox')
        if not bounding_box:
            print(f"No bounding box found for {city}, {country}")
            return None
        
        # Convert string values to float
        bounding_box = [float(coord) for coord in bounding_box]
        
        return {
            'min_lat': bounding_box[0],
            'max_lat': bounding_box[1],
            'min_lon': bounding_box[2],
            'max_lon': bounding_box[3],
            'display_name': result.get('display_name', '')
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error processing response: {e}")
        return None

def main():
    # City and country to search for
    city = "Kinshasa"
    country = "DR Congo"
    
    # Get the bounding box
    result = get_city_bounding_box(city, country)
    
    if result:
        print(f"\nResults for {city}, {country}:")
        print(f"Display Name: {result['display_name']}")
        print(f"Minimum Latitude: {result['min_lat']}")
        print(f"Maximum Latitude: {result['max_lat']}")
        print(f"Minimum Longitude: {result['min_lon']}")
        print(f"Maximum Longitude: {result['max_lon']}")
    else:
        print(f"Could not find bounding box for {city}, {country}")

if __name__ == "__main__":
    main() 
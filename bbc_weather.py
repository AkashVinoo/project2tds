import requests
import json
from datetime import datetime

class BBCWeatherAPI:
    def __init__(self):
        self.base_url = "https://weather-broker-cdn.api.bbci.co.uk"
        self.locator_url = f"{self.base_url}/locator/v1/places"
        self.weather_url = f"{self.base_url}/public/weather/forecast"
        self.api_key = "AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.bbc.com',
            'Referer': 'https://www.bbc.com/'
        }
        
    def get_location_id(self, city):
        """Get location ID for a city using the locator service."""
        params = {
            'api_key': self.api_key,
            'locale': 'en',
            'filter': 'international',
            'place': city,
            'format': 'json'
        }
        
        try:
            response = requests.get(
                self.locator_url,
                params=params,
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            
            if data and 'results' in data and len(data['results']) > 0:
                return data['results'][0]['id']
            else:
                print(f"No location found for {city}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error getting location ID: {str(e)}")
            print(f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}")
            return None
            
    def get_weather_forecast(self, location_id):
        """Get weather forecast for a location using the weather broker API."""
        params = {
            'api_key': self.api_key,
            'locale': 'en',
            'location': location_id,
            'format': 'json'
        }
        
        try:
            response = requests.get(
                self.weather_url,
                params=params,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting weather forecast: {str(e)}")
            print(f"Response content: {e.response.content if hasattr(e, 'response') else 'No response content'}")
            return None
            
    def transform_weather_data(self, weather_data):
        """Transform weather data into the required format."""
        if not weather_data or 'forecasts' not in weather_data:
            return {}
            
        transformed_data = {}
        
        for forecast in weather_data['forecasts']:
            if 'localDate' in forecast and 'enhancedWeatherDescription' in forecast:
                date = forecast['localDate']
                description = forecast['enhancedWeatherDescription']
                transformed_data[date] = description
                
        return transformed_data
        
    def get_paris_weather(self):
        """Get weather forecast for Paris."""
        print("Getting location ID for Paris...")
        location_id = self.get_location_id("Paris")
        
        if not location_id:
            print("Failed to get location ID for Paris")
            return None
            
        print(f"Location ID for Paris: {location_id}")
        print("\nFetching weather forecast...")
        
        weather_data = self.get_weather_forecast(location_id)
        if not weather_data:
            print("Failed to get weather forecast")
            return None
            
        print("Transforming weather data...")
        transformed_data = self.transform_weather_data(weather_data)
        
        return transformed_data

def save_to_json(data, filename="paris_weather.json"):
    """Save the transformed data to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nWeather data saved to {filename}")

def main():
    print("Starting BBC Weather API integration...")
    
    # Create API instance
    weather_api = BBCWeatherAPI()
    
    # Get weather data for Paris
    weather_data = weather_api.get_paris_weather()
    
    if weather_data:
        # Save to JSON file
        save_to_json(weather_data)
        
        # Print the data
        print("\nWeather forecast for Paris:")
        for date, description in weather_data.items():
            print(f"{date}: {description}")
    else:
        print("Failed to get weather data for Paris")

if __name__ == "__main__":
    main() 
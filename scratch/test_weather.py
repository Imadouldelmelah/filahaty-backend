import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.weather_service import weather_service

def test_weather():
    # Sidi Bel Abbes coordinates
    lat, lon = 35.19, -0.63
    
    print(f"Testing Weather Service for coordinates: {lat}, {lon}...")
    result = weather_service.get_weather(lat, lon)
    
    print("\nWeather Results:")
    print("-" * 20)
    for key, value in result.items():
        print(f"{key.capitalize()}: {value}")
    print("-" * 20)
    
    # Simple validation
    if result["temperature"] is not None:
        print("\nTest Passed: Successfully retrieved real-time weather data.")
    else:
        print("\nTest Failed: Could not retrieve weather data.")

if __name__ == "__main__":
    test_weather()

import requests
from utils.logger import logger

class WeatherService:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, lat: float, lon: float):
        """
        Fetches real-time weather data for given coordinates.
        Returns:
            dict: {temperature, humidity, rain, wind}
        """
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,rain,wind_speed_10m"
            }
            
            logger.info(f"Fetching weather for: {lat}, {lon}")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            current = data.get("current", {})
            
            return {
                "temperature": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "rain": current.get("rain"),
                "wind": current.get("wind_speed_10m")
            }
        except Exception as e:
            logger.error(f"Weather API Error: {str(e)}")
            return {
                "temperature": None,
                "humidity": None,
                "rain": None,
                "wind": None
            }

weather_service = WeatherService()

from utils.logger import logger

class WeatherIntelligenceService:
    def __init__(self):
        # Thresholds for decision logic
        self.RAIN_THRESHOLD = 2.0  # mm/h
        self.HEAT_THRESHOLD = 35.0  # °C
        self.HUMIDITY_THRESHOLD = 90.0  # %

    def analyze_weather(self, weather_data: dict):
        """
        Analyzes meteorological data to provide farming alerts and recommendations.
        Args:
            weather_data (dict): {temperature, humidity, rain, wind}
        Returns:
            dict: {alerts: List[str], recommendations: List[str]}
        """
        alerts = []
        recommendations = []

        temp = weather_data.get("temperature")
        humidity = weather_data.get("humidity")
        rain = weather_data.get("rain")

        # 1. Irrigation Logic
        if rain is not None and rain >= self.RAIN_THRESHOLD:
            recommendations.append("Rainfall detected: Skip manual irrigation today to conserve water.")
        elif rain is not None and rain > 0:
            recommendations.append("Light rain detected: Consider reducing irrigation volume.")
        else:
            recommendations.append("Standard irrigation schedule recommended.")

        # 2. Heat Stress Logic
        if temp is not None and temp >= self.HEAT_THRESHOLD:
            alerts.append("CRITICAL: High Heat Stress Warning.")
            recommendations.append("Hydrate crops early in the morning. Avoid any transplanting or pruning during midday peak.")
        elif temp is not None and temp >= 30:
            alerts.append("ADVISORY: Moderate Heat.")
            recommendations.append("Monitor soil moisture closely as evaporation rates are high.")

        # 3. Disease Risk Logic (Fungal/Mildew)
        if humidity is not None and humidity >= self.HUMIDITY_THRESHOLD:
            alerts.append("CRITICAL: High Fungal Disease Risk.")
            recommendations.append("Avoid overhead watering. Ensure maximum airflow around plants and inspect for signs of blight.")
        elif humidity is not None and humidity >= 80:
            alerts.append("ADVISORY: Elevated Humidity.")
            recommendations.append("Check for pests that thrive in humid environments (e.g., aphids).")

        return {
            "alerts": alerts,
            "recommendations": recommendations,
            "summary": self._generate_summary(temp, rain)
        }

    def generate_smart_alerts(self, weather_data: dict, crop_name: str = "", current_stage: str = ""):
        """
        Generates crop-aware alerts based on weather and growth stage sensitivity.
        """
        analysis = self.analyze_weather(weather_data)
        smart_alerts = []
        
        temp = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        rain = weather_data.get("rain", 0)
        
        crop_lower = crop_name.lower()
        stage_lower = current_stage.lower()

        # 1. Heat Alerts (Stage Aware)
        if temp >= self.HEAT_THRESHOLD:
            msg = f"High temperature risk for {crop_name}."
            rec = "Hydrate crops early in the morning. Avoid midday transplanting."
            if "flowering" in stage_lower:
                msg = f"Critical: High heat risk during Flowering!"
                rec = f"{crop_name} blossom drop may occur at {temp}°C. Ensure deep irrigation and consider shade cloths."
            smart_alerts.append({"type": "heat", "message": msg, "recommendation": rec})
        
        # 2. Rain Alerts (Stage Aware)
        if rain >= self.RAIN_THRESHOLD:
            msg = f"Significant rainfall for {crop_name}."
            rec = "Check field drainage to prevent waterlogging."
            if "seedling" in stage_lower:
                msg = f"Warning: Heavy rain risk for Seedlings!"
                rec = f"Young {crop_name} plants are vulnerable to physical damage. Consider temporary cover."
            smart_alerts.append({"type": "rain", "message": msg, "recommendation": rec})
            
        # 3. Disease Risk alerts
        if humidity >= self.HUMIDITY_THRESHOLD:
            msg = f"Extreme moisture risk for {crop_name}."
            rec = "Ensure maximum airflow and inspect lower leaves."
            if "growth" in stage_lower or "fruit" in stage_lower:
                msg = f"High Disease Risk (Blight/Mildew)!"
                rec = f"Humid conditions (> {humidity}%) favor pathogens on {crop_name}. Apply preventive organic fungicide if needed."
            smart_alerts.append({"type": "disease_risk", "message": msg, "recommendation": rec})

        return smart_alerts

    def _generate_summary(self, temp, rain):
        if temp is None: return "Weather data incomplete."
        condition = "Clear" if (rain or 0) == 0 else "Rainy"
        return f"Currently {temp}°C and {condition}."

weather_intelligence = WeatherIntelligenceService()

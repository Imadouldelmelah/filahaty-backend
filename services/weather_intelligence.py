from utils.logger import logger

class WeatherIntelligenceService:
    def __init__(self):
        # Thresholds for decision logic
        self.RAIN_THRESHOLD = 2.0  # mm/h
        self.HEAT_THRESHOLD = 35.0  # °C
        self.HUMIDITY_THRESHOLD = 90.0  # %

    def analyze_weather(self, weather_data: dict, monitoring_data: dict = None):
        """
        Analyzes meteorological and sensor data to provide farming alerts and recommendations.
        Args:
            weather_data (dict): {temperature, humidity, rain, wind}
            monitoring_data (dict): {soil_moisture, ph, ...}
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

        # 4. Integrated Soil Health Logic
        if monitoring_data:
            soil_moisture = monitoring_data.get("soil_moisture", 50)
            if soil_moisture > 75 and (rain or 0) > 0.5:
                alerts.append("CRITICAL: Root Suffocation / Waterlogging Risk.")
                recommendations.append("Soil is already saturated. Heavy rain detected. Ensure drainage is clear.")
            elif soil_moisture < 25:
                alerts.append("ADVISORY: Low Soil Moisture.")
                recommendations.append("Soil is dangerously dry. Deep irrigation required immediately.")

        return {
            "alerts": alerts,
            "recommendations": recommendations,
            "summary": self._generate_summary(temp, rain)
        }

    def generate_smart_alerts(self, weather_data: dict, crop_name: str = "", current_stage: str = "", monitoring_data: dict = None):
        """
        Generates crop-aware alerts based on weather, growth stage, and sensor data.
        """
        analysis = self.analyze_weather(weather_data, monitoring_data)
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

        # 4. Soil pH and Moisture Alerts
        if monitoring_data:
            soil_moiture = monitoring_data.get("soil_moisture", 50)
            ph = monitoring_data.get("ph", 7.0)
            
            if soil_moiture > 80:
                smart_alerts.append({
                    "type": "waterlogging_risk", 
                    "message": "Critical: Field saturation detected!", 
                    "recommendation": "Risk of root rot. Delay any overhead irrigation and inspect drainage channels."
                })
            
            if ph < 5.5 or ph > 7.5:
                smart_alerts.append({
                    "type": "ph_mismatch",
                    "message": "Advisory: Soil pH is outside optimal range.",
                    "recommendation": f"Current pH {ph} may lock out nutrients for {crop_name or 'crops'}. Consult soil treatment guide."
                })

        return smart_alerts

    def _generate_summary(self, temp, rain):
        if temp is None: return "Weather data incomplete."
        condition = "Clear" if (rain or 0) == 0 else "Rainy"
        return f"Currently {temp}°C and {condition}."
# Class exported for on-demand initialization

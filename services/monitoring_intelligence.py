class MonitoringIntelligenceService:
    def __init__(self):
        # Thresholds
        self.SOIL_MOISTURE_LOW = 30.0    # %
        self.SOIL_MOISTURE_HIGH = 80.0   # %
        self.TEMP_HIGH = 35.0            # °C
        self.TEMP_LOW = 5.0              # °C
        self.HUMIDITY_HIGH = 90.0        # %
        self.PH_LOW = 5.5
        self.PH_HIGH = 7.5

    def analyze_monitoring_data(self, monitoring_data: dict, crop_name: str = "Crop") -> dict:
        """
        Analyzes real-time field monitoring data to generate structural deterministic alerts and actions.
        """
        alerts = []
        actions = []

        if not monitoring_data:
            return {"alerts": alerts, "actions": actions}

        moisture = monitoring_data.get("soil_moisture")
        temperature = monitoring_data.get("temperature")
        humidity = monitoring_data.get("humidity")
        ph = monitoring_data.get("ph")

        # 1. Soil Moisture Logic
        if moisture is not None:
            if moisture < self.SOIL_MOISTURE_LOW:
                alerts.append({
                    "type": "water_stress",
                    "severity": "CRITICAL",
                    "message": f"Critical Moisture: Soil is very dry ({moisture}%)."
                })
                actions.append("Initiate deep irrigation immediately.")
            elif moisture > self.SOIL_MOISTURE_HIGH:
                alerts.append({
                    "type": "waterlogging",
                    "severity": "CRITICAL",
                    "message": f"Waterlogging Risk: Soil is saturated ({moisture}%)."
                })
                actions.append("Stop all irrigation. Clear drainage trenches immediately to prevent root rot.")

        # 2. Temperature Logic
        if temperature is not None:
            if temperature > self.TEMP_HIGH:
                alerts.append({
                    "type": "heat_stress",
                    "severity": "CRITICAL",
                    "message": f"Heat Warning: Field temperature has reached {temperature}°C."
                })
                actions.append("Avoid midday fertilizing. Ensure maximum hydration.")
            elif temperature < self.TEMP_LOW:
                alerts.append({
                    "type": "frost_risk",
                    "severity": "WARNING",
                    "message": f"Frost Risk: Field temperature has dropped to {temperature}°C."
                })
                actions.append("Deploy crop covers or activate frost protection systems.")

        # 3. Humidity/Disease Logic
        if humidity is not None:
            if humidity > self.HUMIDITY_HIGH and temperature and 20 <= temperature <= 30:
                alerts.append({
                    "type": "disease_risk",
                    "severity": "CRITICAL",
                    "message": f"High Disease Risk: High humidity ({humidity}%) with warm temperatures detected."
                })
                actions.append("Apply preventive organic fungicide. Ensure maximum airflow by pruning lower leaves.")

        # 4. Soil pH Logic
        if ph is not None:
            if ph < self.PH_LOW:
                alerts.append({
                    "type": "acidity",
                    "severity": "WARNING",
                    "message": f"High Acidity: Soil pH is {ph}."
                })
                actions.append(f"Apply agricultural lime to raise the pH for optimal {crop_name} nutrient uptake.")
            elif ph > self.PH_HIGH:
                alerts.append({
                    "type": "alkalinity",
                    "severity": "WARNING",
                    "message": f"High Alkalinity: Soil pH is {ph}."
                })
                actions.append("Apply elemental sulfur or composted manure to lower the pH.")

        return {
            "alerts": alerts,
            "actions": actions
        }

monitoring_intelligence = MonitoringIntelligenceService()

class FieldHealthScoreService:
    def __init__(self):
        pass

    def calculate_health_score(self, monitoring_data: dict, current_stage: str = "") -> dict:
        """
        Calculates a simple 0-100 health score for a field based on real-time parameters.
        Returns a dictionary containing the score and a status label.
        """
        score = 100
        
        if not monitoring_data:
            return {"score": 0, "status": "Unknown (No Data)"}
            
        moisture = monitoring_data.get("soil_moisture")
        temperature = monitoring_data.get("temperature")
        humidity = monitoring_data.get("humidity")
        
        # 1. Soil Moisture Assessment
        if moisture is not None:
            if moisture < 20: 
                score -= 35  # Severe drought
            elif moisture < 30:
                score -= 20  # Moderate drought
            elif moisture < 40:
                score -= 5   # Slight dryness
            elif moisture > 85:
                score -= 25  # Severe waterlogging
            elif moisture > 75:
                score -= 10  # Mild waterlogging

        # 2. Temperature Assessment
        if temperature is not None:
            if temperature > 40:
                score -= 30  # Extreme heat
            elif temperature > 35:
                score -= 15  # Heat stress
            elif temperature < 0:
                score -= 40  # Freezing
            elif temperature < 5:
                score -= 15  # Frost risk

        # 3. Humidity & Disease Component (Stage aware)
        stage_lower = current_stage.lower()
        if humidity is not None:
            # High humidity during fruiting/harvest is very dangerous for fungal growth
            if humidity > 85:
                if "fruit" in stage_lower or "harvest" in stage_lower:
                    score -= 20
                else:
                    score -= 10

        # Bound the score between 0 and 100
        score = max(0, min(100, score))
        
        # Calculate status text
        if score >= 90:
            status = "Excellent"
        elif score >= 70:
            status = "Good"
        elif score >= 50:
            status = "Warning"
        else:
            status = "Critical"
            
        return {
            "score": score,
            "status": status
        }
# Class exported for on-demand initialization

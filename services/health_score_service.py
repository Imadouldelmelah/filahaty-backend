from services.crops_data import CROPS

class FieldHealthScoreService:
    """
    Agricultural Health Scoring System.
    Evaluates field parameters against crop-specific agronomic ranges from CROPS database.
    """
    
    def calculate_health_score(self, monitoring_data: dict, crop_name: str = "tomato") -> dict:
        """
        Calculates a real-time health score based on parameter proximity to ideal crop ranges.
        Assessments: Moisture, Temperature, Humidity, pH, Nitrogen.
        """
        if not monitoring_data:
            return {"health_score": 0, "status": "No Data"}
            
        # 1. Fetch Crop Profile
        crop_key = crop_name.lower().strip()
        crop_data = CROPS.get(crop_key, CROPS["tomato"])
        
        parameter_scores = []
        
        # 2. Score Individual Parameters (100=Ideal, 70=Acceptable, 40=Bad)
        # Soil Moisture
        moisture = monitoring_data.get("soil_moisture", 50)
        parameter_scores.append(self._calculate_param_score(moisture, crop_data["moisture_range"]))
        
        # Temperature
        temp = monitoring_data.get("temperature", 25)
        parameter_scores.append(self._calculate_param_score(temp, crop_data["temp_range"]))

        # Humidity
        humidity = monitoring_data.get("humidity", 65)
        parameter_scores.append(self._calculate_param_score(humidity, crop_data["humidity_range"]))
        
        # Soil pH
        ph = monitoring_data.get("soil_ph") or monitoring_data.get("ph") or 6.5
        parameter_scores.append(self._calculate_param_score(ph, crop_data["ph_range"]))
        
        # Nitrogen
        nitrogen = monitoring_data.get("nitrogen", 100)
        parameter_scores.append(self._calculate_param_score(nitrogen, crop_data["nitrogen_range"]))
            
        # 3. Compute Average Score
        final_score = int(sum(parameter_scores) / len(parameter_scores))
        
        # 4. Status Mapping
        if final_score >= 80:
            status = "Excellent"
        elif final_score >= 60:
            status = "Stable"
        elif final_score >= 40:
            status = "Warning"
        else:
            status = "Critical"
            
        return {
            "health_score": final_score,
            "status": status,
            "crop_assessed": crop_data["name"],
            "details": {
                "moisture_score": parameter_scores[0],
                "temp_score": parameter_scores[1],
                "humidity_score": parameter_scores[2],
                "ph_score": parameter_scores[3],
                "nitrogen_score": parameter_scores[4]
            }
        }

    def _calculate_param_score(self, value: float, ideal_range: list) -> int:
        """
        Calculates score (100, 70, or 40) based on proximity to range.
        - In range: 100
        - Within 20% margin: 70
        - Further: 40
        """
        low, high = ideal_range
        margin = (high - low) * 0.5 # use a 50% buffer for the 'near' zone
        
        if low <= value <= high:
            return 100
        elif (low - margin) <= value <= (high + margin):
            return 70
        else:
            return 40
# Class exported for on-demand initialization

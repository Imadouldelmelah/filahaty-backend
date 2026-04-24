from services.crops_data import CROPS
from services.health_score_service import FieldHealthScoreService

class CropRecommenderService:
    """
    Deterministic Crop Recommendation Engine.
    Matches current field monitoring data against the crop database to find the best biological fit.
    """
    def __init__(self):
        self.health_svc = FieldHealthScoreService()

    def get_recommendations(self, data: dict) -> dict:
        """
        Refined Weighted Scoring Recommendation Engine.
        Weights:
        - soil_ph: 25%
        - temp: 20%
        - soil_moisture: 20%
        - nitrogen: 15%
        - humidity: 10%
        - phosphorus: 5%
        - potassium: 5%
        """
        if not data:
            return {"best_crop": "Wheat", "confidence": 50, "alternatives": []}

        scored_crops = []
        
        # 1. Extraction with defaults
        ph = data.get("soil_ph", data.get("ph", 6.5))
        temp = data.get("temperature", 25)
        moisture = data.get("soil_moisture", 50)
        n = data.get("nitrogen", 40)
        p = data.get("phosphorus", 30)
        k = data.get("potassium", 30)
        hum = data.get("humidity", 60)

        for crop_id, profile in CROPS.items():
            # Param scores (100, 70, 30)
            s_ph = self._calculate_param_score(ph, profile["ph_range"])
            s_temp = self._calculate_param_score(temp, profile["temp_range"])
            s_moist = self._calculate_param_score(moisture, profile["moisture_range"])
            s_n = self._calculate_param_score(n, profile["nitrogen_range"])
            s_p = self._calculate_param_score(p, profile["phosphorus_range"])
            s_k = self._calculate_param_score(k, profile["potassium_range"])
            s_hum = self._calculate_param_score(hum, profile["humidity_range"])

            # Weighted sum calculation
            final_score = (
                s_ph * 0.25 + 
                s_temp * 0.20 + 
                s_moist * 0.20 + 
                s_n * 0.15 + 
                s_hum * 0.10 + 
                s_p * 0.05 + 
                s_k * 0.05
            )
            
            # Application of constraints: no 100% unless perfect + 92% cap
            is_perfect = (s_ph == 100 and s_temp == 100 and s_moist == 100 and 
                          s_n == 100 and s_p == 100 and s_k == 100 and s_hum == 100)
            
            if not is_perfect:
                final_score = min(final_score, 92.0)
            
            scored_crops.append({
                "crop": profile["name"],
                "score": int(final_score)
            })

        # 2. Rank and Selection
        scored_crops.sort(key=lambda x: x["score"], reverse=True)
        best = scored_crops[0]
        
        return {
            "best_crop": best["crop"],
            "confidence": best["score"],
            "alternatives": [
                {"crop": c["crop"], "score": c["score"]} for c in scored_crops[1:4]
            ]
        }

    def _calculate_param_score(self, value: float, target_range: tuple) -> float:
        """
        Bins values into 100 (perfect), 70 (near), or 30 (far).
        """
        min_val, max_val = target_range
        # 50% tolerance for 'near'
        range_width = max_val - min_val
        tolerance = range_width * 0.5 if range_width > 0 else 2.0
        
        if min_val <= value <= max_val:
            return 100.0
        elif (min_val - tolerance) <= value <= (max_val + tolerance):
            return 70.0
        else:
            return 30.0

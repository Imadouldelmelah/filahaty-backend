from services.crops_data import CROPS
from services.health_score_service import FieldHealthScoreService

class CropRecommenderService:
    """
    Deterministic Crop Recommendation Engine.
    Matches current field monitoring data against the crop database to find the best biological fit.
    """
    def __init__(self):
        self.health_svc = FieldHealthScoreService()

    def get_recommendations(self, monitoring_data: dict) -> dict:
        """
        Evaluates all known crops against the monitoring data and returns the best matches.
        """
        if not monitoring_data:
            return {"best_crop": "Unknown", "alternatives": []}

        scored_crops = []

        for crop_id, crop_data in CROPS.items():
            # Calculate health score for this specific crop with current monitoring data
            assessment = self.health_svc.calculate_health_score(monitoring_data, crop_id)
            score = assessment["health_score"]
            
            scored_crops.append({
                "id": crop_id,
                "name": crop_data["name"],
                "score": score
            })

        # Sort by score descending
        scored_crops.sort(key=lambda x: x["score"], reverse=True)

        if not scored_crops:
            return {"best_crop": "Unknown", "alternatives": []}

        best_crop = scored_crops[0]["name"]
        # Exclude best crop from alternatives and take top 3
        alternatives = [c["name"] for c in scored_crops[1:4]]

        return {
            "best_crop": best_crop,
            "alternatives": alternatives
        }

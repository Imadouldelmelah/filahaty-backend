import json
import os
import uuid
from datetime import datetime
from services.agronomy_engine import CROP_PLANS

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "journeys.json")

class TrackingService:
    def __init__(self):
        self._ensure_data_file()

    def _ensure_data_file(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)

    def _load_journeys(self):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def _save_journeys(self, journeys):
        with open(DATA_FILE, "w") as f:
            json.dump(journeys, f, indent=4)

    def start_journey(self, crop_name: str, start_date: str, lat: float = None, lon: float = None):
        """
        Starts a new farming journey.
        Args:
            crop_name (str): Name of the crop.
            start_date (str): Start date in YYYY-MM-DD format.
            lat (float): Latitude of the farm.
            lon (float): Longitude of the farm.
        Returns:
            str: Unique journey_id.
        """
        journey_id = str(uuid.uuid4())
        journeys = self._load_journeys()
        
        # Validate start_date format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")

        journeys[journey_id] = {
            "journey_id": journey_id,
            "crop_name": crop_name.lower(),
            "start_date": start_date,
            "latitude": lat,
            "longitude": lon,
            "history": []
        }
        self._save_journeys(journeys)
        return journey_id

    def get_progress(self, journey_id: str):
        """
        Calculates the current day and growth stage for a journey.
        """
        journeys = self._load_journeys()
        if journey_id not in journeys:
            return {"error": "Journey not found"}

        journey = journeys[journey_id]
        crop_name = journey["crop_name"]
        start_date = datetime.strptime(journey["start_date"], "%Y-%m-%d")
        today = datetime.now()
        
        # Calculate current day (1-indexed)
        delta = today - start_date
        current_day = max(1, delta.days + 1)

        # Get stage from agronomy engine
        stage = self._calculate_stage(crop_name, current_day)
        
        return {
            "journey_id": journey_id,
            "crop": crop_name,
            "day": current_day,
            "stage": stage,
            "start_date": journey["start_date"],
            "latitude": journey.get("latitude"),
            "longitude": journey.get("longitude"),
            "history": journey.get("history", [])
        }

    def record_action(self, journey_id: str, action: str):
        """
        Records a completed action in the journey history.
        """
        journeys = self._load_journeys()
        if journey_id not in journeys:
            return {"error": "Journey not found"}
        
        if "history" not in journeys[journey_id]:
            journeys[journey_id]["history"] = []
            
        journeys[journey_id]["history"].append({
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
        self._save_journeys(journeys)
        return {"status": "success", "message": "Action recorded"}

    def _calculate_stage(self, crop_name: str, day: int):
        if crop_name not in CROP_PLANS:
            return "Unknown"

        stages = CROP_PLANS[crop_name]["stages"]
        for stage in stages:
            days_range = stage["days"]
            if "-" in days_range:
                start, end = map(int, days_range.split("-"))
                if start <= day <= end:
                    return stage["name"]
            else:
                if day == int(days_range):
                    return stage["name"]
        
        # Fallback if beyond defined stages
        return stages[-1]["name"] if day > int(stages[-1]["days"].split("-")[-1]) else "Seed"
# Export the class for on-demand initialization

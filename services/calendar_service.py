"""
Calendar Service Module
Generates dynamic 30-day agricultural projections based on crop logic and sensor data.
"""
from services.agronomy_engine import get_crop_plan, get_smart_journey_logic

class CalendarService:
    def generate_30_day_projection(self, crop_name: str, current_day: int, monitoring_data: dict) -> list:
        """
        Refined 3-layer Calendar Projection Engine.
        1. Stage-based (Biological)
        2. Monitoring-based (Real-time triggers)
        3. Default fallback (Always Available)
        """
        projection = []
        
        # 1. Real-time condition assessment (Layer 2 & 3 Pre-calc)
        moisture = monitoring_data.get("soil_moisture", 50)
        nitrogen = monitoring_data.get("nitrogen", 30)
        temp = monitoring_data.get("temperature", 25)
        humidity = monitoring_data.get("humidity", 65)
        
        for i in range(30):
            target_day = current_day + i
            
            # --- LAYER 1: Stage-based tasks ---
            stage = self._get_stage_name(target_day)
            priority = "low"
            
            if "planting" in stage.lower():
                daily_task = "Soil preparation and Initial Irrigation"
                priority = "high"
            elif "growth" in stage.lower():
                daily_task = "Irrigation and Routine Fertilization"
                priority = "medium"
            elif "flower" in stage.lower():
                daily_task = "Advanced Monitoring and Pest Control"
                priority = "high"
            elif "harvest" in stage.lower():
                daily_task = "Harvesting and Post-harvest Storage"
                priority = "high"
            else:
                daily_task = "Standard Field Monitoring"
                priority = "low"

            # --- LAYER 2: Monitoring-based overrides (Immediate 3-day focus) ---
            if i < 3:
                if moisture < 35:
                    daily_task = "URGENT: Irrigation system activation (Dry soil)"
                    priority = "high"
                elif nitrogen < 20:
                    daily_task = "CRITICAL: Targeted Nitrogen fertilization"
                    priority = "high"
                elif temp > 32:
                    daily_task = "ALERT: Apply heat stress protection"
                    priority = "medium"
                elif humidity > 75:
                    daily_task = "WARNING: Fungal risk check (High humidity)"
                    priority = "medium"

            # --- LAYER 3: Default fallback (If something went wrong or gap exists) ---
            if not daily_task or daily_task.strip() == "":
                daily_task = "General Irrigation and Field Inspection"
                priority = "medium"

            projection.append({
                "day": target_day,
                "task": daily_task,
                "priority": priority,
                "stage": stage
            })

        # Final Stability Check: Ensure at least 14 days
        if len(projection) < 14:
            for i in range(len(projection), 14):
                projection.append({
                    "day": current_day + i,
                    "task": "Standard Field Maintenance",
                    "priority": "low",
                    "stage": "Unknown"
                })

        return projection

    def _get_stage_name(self, day: int) -> str:
        """Determines growth stage based on day count (Indestructible mapping)."""
        if 1 <= day <= 10: return "Planting"
        if 11 <= day <= 30: return "Growth"
        if 31 <= day <= 60: return "Flowering"
        return "Harvest"

    def _is_day_in_stage(self, day: int, day_range: str) -> bool:
        """Helper to check if a day falls within a 'start-end' range string."""
        try:
            if "-" in day_range:
                start, end = map(int, day_range.split("-"))
                return start <= day <= end
            else:
                return day == int(day_range)
        except:
            return False

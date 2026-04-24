"""
Calendar Service Module
Generates dynamic 30-day agricultural projections based on crop logic and sensor data.
"""
from services.agronomy_engine import get_crop_plan, get_smart_journey_logic

class CalendarService:
    def generate_30_day_projection(self, crop_name: str, current_day: int, monitoring_data: dict) -> list:
        """
        Generates a 30-day task projection starting from current_day.
        Adjusts tasks dynamically based on biological stage and monitoring alerts.
        """
        plan = get_crop_plan(crop_name)
        if "error" in plan:
            return [{"day": current_day + i, "task": "General Maintenance", "priority": "medium"} for i in range(30)]
            
        projection = []
        stages = plan.get("stages", [])
        
        # 1. Capture Monitoring Alerts
        is_dry = monitoring_data.get("soil_moisture", 50) < 35
        low_nitrogen = monitoring_data.get("nitrogen", 30) < 20
        heat_warning = monitoring_data.get("temperature", 25) > 32
        acidic_soil = monitoring_data.get("soil_ph", 7.0) < 6.0
        heavy_rain = monitoring_data.get("rainfall", 0) > 8.0
        
        for i in range(30):
            target_day = current_day + i
            
            # 2. Identify Current Biological Stage
            stage_data = next(
                (s for s in stages if self._is_day_in_stage(target_day, s["days"])), 
                stages[-1] if stages else None
            )
            stage_name = stage_data["name"] if stage_data else "Unknown"
            
            # 3. Apply Stage-Specific Task Logic (Base Overlay)
            if "seed" in stage_name.lower() or "planting" in stage_name.lower():
                daily_task = "Irrigation and Soil Preparation"
                priority = "high"
            elif "growth" in stage_name.lower():
                daily_task = "Fertilization and Monitoring"
                priority = "medium"
            elif "flower" in stage_name.lower():
                daily_task = "Advanced Pest Control"
                priority = "high"
            elif "harvest" in stage_name.lower():
                daily_task = "Strategic Harvesting"
                priority = "high"
            else:
                daily_task = "Standard Field Inspection"
                priority = "low"
            
            # 4. Merge Real-time Monitoring Alerts (Urgent Overrides)
            # Sensors have priority over lifecycle in the immediate 48 hours
            if i < 2:
                if heavy_rain:
                    daily_task = "WARNING: Heavy rain forecast: Protect crops and check drainage"
                    priority = "high"
                elif is_dry:
                    daily_task = "URGENT: Irrigation system activation (Dry soil detected)"
                    priority = "high"
                elif low_nitrogen:
                    daily_task = "CRITICAL: Fertilization required (Nutrient depletion)"
                    priority = "high"
                elif acidic_soil:
                    daily_task = "ADVISORY: pH correction needed (Acidic soil detected)"
                    priority = "medium"
                elif heat_warning:
                    daily_task = "ALERT: Heat stress protection (Extreme temp)"
                    priority = "medium"
            
            projection.append({
                "day": target_day,
                "task": daily_task,
                "stage": stage_name,
                "priority": priority
            })
            
        return projection

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

"""
Calendar Service Module
Generates dynamic 30-day agricultural projections based on crop logic and sensor data.
"""
from services.agronomy_engine import get_crop_plan, get_smart_journey_logic

class CalendarService:
    def generate_30_day_projection(self, crop_name: str, current_day: int, monitoring_data: dict) -> list:
        """
        Generates a 30-day task projection starting from current_day.
        Adjusts tasks dynamically based on monitoring_data stress triggers.
        """
        plan = get_crop_plan(crop_name)
        if "error" in plan:
            # Fallback for unknown crops
            return [{"day": current_day + i, "task": "General Crop Maintenance"} for i in range(30)]
            
        projection = []
        stages = plan.get("stages", [])
        
        # Stress factors from monitoring data
        is_dry = monitoring_data.get("soil_moisture", 50) < 35
        low_nitrogen = monitoring_data.get("nitrogen", 30) < 20
        
        for i in range(30):
            target_day = current_day + i
            
            # 1. Find stage for target day
            stage = next(
                (s for s in stages if self._is_day_in_stage(target_day, s["days"])), 
                stages[-1] if stages else None
            )
            
            # 2. Extract base task (rotate through stage tasks)
            base_tasks = stage["tasks"] if stage else ["General Checkup"]
            task_index = i % len(base_tasks)
            daily_task = base_tasks[task_index]
            
            # 3. Dynamic Adjustments (Priority Overrides)
            # If stressed, inject corrective tasks in the immediate future (first 3 days)
            if i < 3:
                if is_dry and i == 0:
                    daily_task = "CRITICAL: Heavy Irrigation (Low Moisture Detected)"
                elif low_nitrogen and i == 1:
                    daily_task = "CRITICAL: Nitrogen Fertilization (Nutrient Depletion)"
            
            projection.append({
                "day": target_day,
                "task": daily_task,
                "stage": stage["name"] if stage else "Unknown"
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

"""
Calendar Service Module
Generates dynamic 30-day agricultural projections based on crop logic and sensor data.
"""
from services.agronomy_engine import get_crop_plan, get_smart_journey_logic

class CalendarService:
    def generate_30_day_projection(self, crop_name: str, current_day: int, monitoring_data: dict, lang: str = "en") -> list:
        """
        Refined 3-layer Calendar Projection Engine.
        1. Stage-based (Biological)
        2. Monitoring-based (Real-time triggers)
        3. Default fallback (Always Available)
        """
        from datetime import datetime, timedelta
        
        projection = []
        today = datetime.now()
        
        # Translation Dictionary
        translations = {
            "en": {
                "planting_task": "Soil preparation and Initial Irrigation",
                "growth_task": "Irrigation and Routine Fertilization",
                "flowering_task": "Advanced Monitoring and Pest Control",
                "harvest_task": "Harvesting and Post-harvest Storage",
                "urgent_irrigation": "URGENT: Irrigation system activation (Dry soil)",
                "critical_nitrogen": "CRITICAL: Targeted Nitrogen fertilization",
                "alert_heat": "ALERT: Apply heat stress protection",
                "warning_fungal": "WARNING: Fungal risk check (High humidity)",
                "irrigation_soil": "Irrigation and Soil monitoring",
                "soil_monit": "Soil monitoring"
            },
            "fr": {
                "planting_task": "Préparation du sol et irrigation initiale",
                "growth_task": "Irrigation et fertilisation de routine",
                "flowering_task": "Surveillance avancée et lutte antiparasitaire",
                "harvest_task": "Récolte et stockage post-récolte",
                "urgent_irrigation": "URGENT : Activation du système d'irrigation (sol sec)",
                "critical_nitrogen": "CRITICAL : Fertilisation azotée ciblée",
                "alert_heat": "ALERTE : Appliquer une protection contre le stress thermique",
                "warning_fungal": "AVERTISSEMENT : Risque fongique (humidité élevée)",
                "irrigation_soil": "Irrigation et surveillance du sol",
                "soil_monit": "Surveillance du sol"
            },
            "ar": {
                "planting_task": "تحضير التربة والري الأولي",
                "growth_task": "الري والتسميد الروتيني",
                "flowering_task": "المراقبة المتقدمة ومكافحة الآفات",
                "harvest_task": "الحصاد والتخزين بعد الحصاد",
                "urgent_irrigation": "عاجل: تفعيل نظام الري (تربة جافة)",
                "critical_nitrogen": "هام: التسميد النيتروجيني المستهدف",
                "alert_heat": "تنبيه: تطبيق الحماية من الإجهاد الحراري",
                "warning_fungal": "تحذير: خطر الفطريات (رطوبة عالية)",
                "irrigation_soil": "الري ومراقبة التربة",
                "soil_monit": "مراقبة التربة"
            }
        }
        
        t = translations.get(lang, translations["en"])
        
        try:
            # 1. Real-time condition assessment (Layer 2 & 3 Pre-calc)
            moisture = monitoring_data.get("soil_moisture", 50)
            nitrogen = monitoring_data.get("nitrogen", 30)
            temp = monitoring_data.get("temperature", 25)
            humidity = monitoring_data.get("humidity", 65)
            
            for i in range(30):
                target_day = current_day + i
                target_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
                
                daily_task = None
                priority = "medium"
                
                # --- LAYER 1: Stage-based tasks ---
                stage = self._get_stage_name(target_day)
                
                if "planting" in stage.lower():
                    daily_task = t["planting_task"]
                    priority = "high"
                elif "growth" in stage.lower():
                    daily_task = t["growth_task"]
                    priority = "medium"
                elif "flower" in stage.lower():
                    daily_task = t["flowering_task"]
                    priority = "high"
                elif "harvest" in stage.lower():
                    daily_task = t["harvest_task"]
                    priority = "high"

                # --- LAYER 2: Monitoring-based overrides (Immediate 3-day focus) ---
                if i < 3:
                    if moisture < 35:
                        daily_task = t["urgent_irrigation"]
                        priority = "high"
                    elif nitrogen < 20:
                        daily_task = t["critical_nitrogen"]
                        priority = "high"
                    elif temp > 32:
                        daily_task = t["alert_heat"]
                        priority = "medium"
                    elif humidity > 75:
                        daily_task = t["warning_fungal"]
                        priority = "medium"

                # --- LAYER 3: Default fallback (If something went wrong or gap exists) ---
                if not daily_task or daily_task.strip() == "":
                    if i % 2 == 0:
                        daily_task = t["irrigation_soil"]
                        priority = "high"
                    else:
                        daily_task = t["soil_monit"]
                        priority = "medium"

                projection.append({
                    "date": target_date,
                    "task": daily_task,
                    "priority": priority
                })

        except Exception as e:
            # If logic fails entirely, return a guaranteed 30-day baseline
            projection = []
            for i in range(30):
                target_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
                if i % 2 == 0:
                    task = t["irrigation_soil"]
                    priority = "high"
                else:
                    task = t["soil_monit"]
                    priority = "medium"
                
                projection.append({
                    "date": target_date,
                    "task": task,
                    "priority": priority
                })

        # Final Safety Check: Ensure never empty and exactly 30 days
        if not projection or len(projection) < 30:
            current_len = len(projection)
            for i in range(current_len, 30):
                target_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
                if i % 2 == 0:
                    task = t["irrigation_soil"]
                    priority = "high"
                else:
                    task = t["soil_monit"]
                    priority = "medium"
                projection.append({
                    "date": target_date,
                    "task": task,
                    "priority": priority
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

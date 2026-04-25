import time
import uuid
from datetime import datetime, timedelta
from collections import deque
from utils.logger import logger

class AlertService:
    """
    Agricultural Alert Generation and Storage System.
    Analyzes monitoring data and maintains a persistent history of notifications.
    """
    
    # Persistent in-memory storage (Class-level to persist across requests)
    _notifications = deque(maxlen=50)

    TRANSLATIONS = {
        "en": {
            "alert_soil_low": "Irrigation needed: Soil moisture is dangerously low.",
            "alert_temp_high": "Heat stress risk: High temperature detected in the field.",
            "alert_nitrogen_low": "Fertilization required: Nitrogen levels are below optimum.",
            "alert_humidity_high": "Fungal disease risk: High humidity detected, monitor for signs of infection."
        },
        "fr": {
            "alert_soil_low": "Irrigation nécessaire : L'humidité du sol est dangereusement basse.",
            "alert_temp_high": "Risque de stress thermique : Température élevée détectée dans le champ.",
            "alert_nitrogen_low": "Fertilisation requise : Les niveaux d'azote sont inférieurs à l'optimum.",
            "alert_humidity_high": "Risque de maladie fongique : Humidité élevée détectée, surveillez les signes d'infection."
        },
        "ar": {
            "alert_soil_low": "مطلوب ري: رطوبة التربة منخفضة بشكل خطير.",
            "alert_temp_high": "خطر إجهاد حراري: تم اكتشاف درجة حرارة عالية في الحقل.",
            "alert_nitrogen_low": "مطلوب تسميد: مستويات النيتروجين أقل من المستوى الأمثل.",
            "alert_humidity_high": "خطر أمراض فطرية: تم اكتشاف رطوبة عالية، راقب علامات العدوى."
        }
    }

    def _t(self, key, lang="en"):
        lang = lang if (lang and lang in self.TRANSLATIONS) else "en"
        return self.TRANSLATIONS[lang].get(key, self.TRANSLATIONS["en"].get(key, key))

    def generate_alerts(self, monitoring_data: dict, lang: str = "en") -> list:
        """
        Analyzes telemetry, generates alerts, and stores unique ones in history.
        """
        raw_triggers = [
            (monitoring_data.get("soil_moisture", 100) < 35, "alert_soil_low", "critical"),
            (monitoring_data.get("temperature", 0) > 32, "alert_temp_high", "warning"),
            (monitoring_data.get("nitrogen", 100) < 20, "alert_nitrogen_low", "warning"),
            (monitoring_data.get("humidity", 0) > 75, "alert_humidity_high", "warning")
        ]
        
        detected_alerts = []
        
        for triggered, key, alert_type in raw_triggers:
            if triggered:
                message = self._t(key, lang)
                # Always show in current monitoring response
                alert = self._create_alert(message, key, alert_type)
                detected_alerts.append(alert)
                
                # Only store in history if not a duplicate
                if not self._is_duplicate(message):
                    self._notifications.appendleft(alert)
                    logger.info(f"NOTIFICATION_STORED: {message}")
        
        return detected_alerts

    def get_all_notifications(self, lang: str = "en") -> list:
        """Returns the history of stored notifications, ensuring they match requested language if possible."""
        # Note: In a real system, we might want to store keys and translate on-the-fly.
        # For this demo, we'll return the history. If history items have keys, we can re-translate.
        results = []
        for alert in self._notifications:
            localized_alert = alert.copy()
            if "message_key" in alert:
                localized_alert["message"] = self._t(alert["message_key"], lang)
            results.append(localized_alert)
        return results

    def _is_duplicate(self, message: str) -> bool:
        """Checks if the same message was generated in the last 10 minutes."""
        ten_mins_ago = datetime.now() - timedelta(minutes=10)
        for alert in self._notifications:
            try:
                alert_time = datetime.fromisoformat(alert["timestamp"])
                if alert["message"] == message and alert_time > ten_mins_ago:
                    return True
            except (ValueError, KeyError):
                continue
        return False

    def _create_alert(self, message: str, key: str, alert_type: str) -> dict:
        """Helper to structure alert objects."""
        return {
            "id": str(uuid.uuid4()),
            "message": message,
            "message_key": key,
            "type": alert_type,
            "timestamp": datetime.now().isoformat()
        }

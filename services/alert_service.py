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

    def generate_alerts(self, monitoring_data: dict) -> list:
        """
        Analyzes telemetry, generates alerts, and stores unique ones in history.
        Returns the FULL list of currently detected alerts for real-time display.
        """
        raw_triggers = [
            (monitoring_data.get("soil_moisture", 100) < 35, "Irrigation needed: Soil moisture is dangerously low.", "critical"),
            (monitoring_data.get("temperature", 0) > 32, "Heat stress risk: High temperature detected in the field.", "warning"),
            (monitoring_data.get("nitrogen", 100) < 20, "Fertilization required: Nitrogen levels are below optimum.", "warning"),
            (monitoring_data.get("humidity", 0) > 75, "Fungal disease risk: High humidity detected, monitor for signs of infection.", "warning")
        ]
        
        detected_alerts = []
        
        for triggered, message, alert_type in raw_triggers:
            if triggered:
                # Always show in current monitoring response
                alert = self._create_alert(message, alert_type)
                detected_alerts.append(alert)
                
                # Only store in history if not a duplicate
                if not self._is_duplicate(message):
                    self._notifications.appendleft(alert) # Newest first
                    logger.info(f"NOTIFICATION_STORED: {message}")
                else:
                    logger.debug(f"NOTIFICATION_SKIPPED_DUPLICATE: {message}")
        
        return detected_alerts

    def get_all_notifications(self) -> list:
        """Returns the history of stored notifications."""
        return list(self._notifications)

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

    def _create_alert(self, message: str, alert_type: str) -> dict:
        """Helper to structure alert objects."""
        return {
            "id": str(uuid.uuid4()),
            "message": message,
            "type": alert_type,
            "timestamp": datetime.now().isoformat()
        }

import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.monitoring_intelligence import monitoring_intelligence

def run_tests():
    print("--- Testing Monitoring Intelligence ---")
    
    # 1. Low moisture
    data_1 = {"soil_moisture": 25.0, "temperature": 25.0, "humidity": 50.0, "ph": 7.0}
    res_1 = monitoring_intelligence.analyze_monitoring_data(data_1)
    
    # 2. Heat and humidity disease risk
    data_2 = {"soil_moisture": 60.0, "temperature": 28.0, "humidity": 95.0, "ph": 7.0}
    res_2 = monitoring_intelligence.analyze_monitoring_data(data_2)

    # 3. High pH
    data_3 = {"soil_moisture": 50.0, "temperature": 20.0, "humidity": 40.0, "ph": 8.0}
    res_3 = monitoring_intelligence.analyze_monitoring_data(data_3)

    print("\nResult 1 (Low Moisture):")
    for a in res_1["alerts"]: print(f" - {a['message']}")
    for a in res_1["actions"]: print(f" -> {a}")

    print("\nResult 2 (Heat + High Humidity):")
    for a in res_2["alerts"]: print(f" - {a['message']}")
    for a in res_2["actions"]: print(f" -> {a}")

    print("\nResult 3 (High pH):")
    for a in res_3["alerts"]: print(f" - {a['message']}")
    for a in res_3["actions"]: print(f" -> {a}")


if __name__ == "__main__":
    run_tests()

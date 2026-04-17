import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.health_score_service import field_health_score_service

def test_health_score():
    print("--- Testing Field Health Score System ---")
    
    # 1. Perfect Conditions
    data_excellent = {"soil_moisture": 55.0, "temperature": 24.0, "humidity": 50.0}
    res_exc = field_health_score_service.calculate_health_score(data_excellent, "Growth")
    
    # 2. Good Conditions
    data_good = {"soil_moisture": 45.0, "temperature": 32.0, "humidity": 60.0} # Slight dryness + warm
    res_good = field_health_score_service.calculate_health_score(data_good, "Growth")

    # 3. Warning Conditions
    data_warn = {"soil_moisture": 25.0, "temperature": 36.0, "humidity": 40.0} # Drought + heat stress
    res_warn = field_health_score_service.calculate_health_score(data_warn, "Flowering")
    
    # 4. Critical Conditions
    data_crit = {"soil_moisture": 18.0, "temperature": 41.0, "humidity": 90.0} # Extreme heat + extreme drought + high humidity (impossible but testing math)
    res_crit = field_health_score_service.calculate_health_score(data_crit, "Fruiting")

    print("\nScenario 1: Ideal Conditions")
    print(json.dumps(res_exc, indent=2))
    
    print("\nScenario 2: Acceptable Conditions")
    print(json.dumps(res_good, indent=2))
    
    print("\nScenario 3: Stress Conditions")
    print(json.dumps(res_warn, indent=2))
    
    print("\nScenario 4: Extreme Danger Conditions")
    print(json.dumps(res_crit, indent=2))

if __name__ == "__main__":
    test_health_score()

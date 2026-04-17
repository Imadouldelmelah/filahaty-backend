import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.weather_intelligence import weather_intelligence

def test_weather_logic():
    print("Testing Weather Decision Logic...\n")

    # Scenario 1: Heavy Rain
    print("Scenario 1: Heavy Rain (10mm/h)")
    rainy_data = {"temperature": 20, "humidity": 60, "rain": 10}
    result1 = weather_intelligence.analyze_weather(rainy_data)
    print(f"Recommendations: {result1['recommendations']}")
    assert any("Skip manual irrigation" in r for r in result1["recommendations"])

    # Scenario 2: Heat Stress
    print("\nScenario 2: Extreme Heat (42°C)")
    heat_data = {"temperature": 42, "humidity": 20, "rain": 0}
    result2 = weather_intelligence.analyze_weather(heat_data)
    print(f"Alerts: {result2['alerts']}")
    assert any("High Heat Stress" in a for a in result2["alerts"])

    # Scenario 3: Disease Risk
    print("\nScenario 3: High Humidity (95%)")
    humid_data = {"temperature": 18, "humidity": 95, "rain": 0}
    result3 = weather_intelligence.analyze_weather(humid_data)
    print(f"Alerts: {result3['alerts']}")
    assert any("Fungal Disease Risk" in a for a in result3["alerts"])

    # Scenario 4: Perfect Weather
    print("\nScenario 4: Ideal Conditions (24°C, 50% humidity)")
    ideal_data = {"temperature": 24, "humidity": 50, "rain": 0}
    result4 = weather_intelligence.analyze_weather(ideal_data)
    print(f"Alerts: {result4['alerts']}")
    print(f"Recommendations: {result4['recommendations']}")
    assert len(result4["alerts"]) == 0

    print("\nTest Passed: Weather intelligence logic correctly identifies all scenarios.")

if __name__ == "__main__":
    test_weather_logic()

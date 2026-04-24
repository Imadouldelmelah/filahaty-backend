"""
Agronomy Engine Module
Provides expert-level structured crop plans for smart farming.
"""

CROP_PLANS = {
    "tomato": {
        "crop": "Tomato",
        "description": "High-value fruit crop requiring consistent moisture and nutrient management.",
        "stages": [
            {
                "name": "Seed",
                "days": "1-14",
                "tasks": [
                    "Prepare soil with organic compost and basal phosphorus",
                    "Maintain soil temperature (20-25°C) for optimal germination",
                    "Light irrigation (misting) to keep soil moist but not waterlogged",
                    "Monitor for damping-off fungi and early seedling vigor"
                ],
                "irrigation": "Light misting, keeping top 2cm of soil moist.",
                "fertilizer": "Basal Phosphorus and high-quality organic compost.",
                "monitoring": "Check Soil Temperature and Germination Rate."
            },
            {
                "name": "Growth",
                "days": "15-45",
                "tasks": [
                    "Apply Nitrogen-rich NPK fertilizer for leaf and stem development",
                    "Install staking or trellising for plant support",
                    "Transition to drip irrigation for deep root watering",
                    "Prune lower yellowing leaves to improve airflow"
                ],
                "irrigation": "Drip irrigation, 2-3 liters per plant depending on evapotranspiration.",
                "fertilizer": "Balanced NPK (e.g., 20-20-20) every 10-14 days.",
                "monitoring": "Scout for Aphids and Early Blight on lower canopy."
            },
            {
                "name": "Flowering",
                "days": "46-75",
                "tasks": [
                    "Switch to high Potassium (K) and Calcium (Ca) fertigation",
                    "Prune side shoots (suckers) to focus energy on fruit production",
                    "Ensure consistent soil moisture to prevent blossom-end rot",
                    "Scout leaf surfaces for thrips or spider mites"
                ],
                "irrigation": "Increased frequency; maintain high soil moisture consistency.",
                "fertilizer": "High Potassium (K) and Calcium (Ca) supplement.",
                "monitoring": "Blossom-end rot check and Moisture Sensor levels."
            },
            {
                "name": "Harvest",
                "days": "76-120",
                "tasks": [
                    "Regular harvesting to encourage further fruit set",
                    "Reduce irrigation slightly to enhance fruit flavor and prevent cracking",
                    "Remove diseased or old foliage to focus energy",
                    "Check for uniform ripening and sort by quality"
                ],
                "irrigation": "Moderate; reduce by 20% to avoid fruit splitting.",
                "fertilizer": "Minimal feeding; maintain Potassium levels for fruit quality.",
                "monitoring": "Fruit Quality, Ripening Uniformity, and Fruit Worms."
            }
        ]
    },
    "pepper": {
        "crop": "Pepper",
        "description": "Heat-loving crop with specific demands for warm soil and steady feeding.",
        "stages": [
            {
                "name": "Seed",
                "days": "1-10",
                "tasks": [
                    "Sow seeds in warm, well-draining starting mix",
                    "Maintain 24-29°C for optimal germination speed",
                    "Keep moisture even; avoid drowning seeds in heavy containers"
                ],
                "irrigation": "Surface misting to maintain high humidity.",
                "fertilizer": "Starter solution high in Phosphorus.",
                "monitoring": "Germination percentage and Soil warmth."
            },
            {
                "name": "Growth",
                "days": "11-50",
                "tasks": [
                    "Transplant to field once soil temperature remains above 15°C",
                    "Apply balanced NPK to establish strong root systems",
                    "Use organic mulch to retain moisture and suppress weeds"
                ],
                "irrigation": "Moderate regular watering to establish roots.",
                "fertilizer": "Balanced NPK (15-15-15) during establishment.",
                "monitoring": "Growth rate and Weed competition."
            },
            {
                "name": "Flowering",
                "days": "51-80",
                "tasks": [
                    "Monitor for blossom drop under high heat stress",
                    "Ensure Magnesium (Mg) availability for healthy green leaves",
                    "Stake heavy-bearing plants to prevent stem breakage"
                ],
                "irrigation": "Maintain upper root zone moisture during bloom.",
                "fertilizer": "Supplementary Magnesium and low-nitrogen feeding.",
                "monitoring": "Blossom drop and Calcium deficiency signs."
            },
            {
                "name": "Harvest",
                "days": "81-120",
                "tasks": [
                    "Harvest early fruit to encourage continued production",
                    "Cut stems cleanly with shears rather than pulling",
                    "Store in cool, dry conditions immediately after picking"
                ],
                "irrigation": "Reduce slightly to enhance shelf life.",
                "fertilizer": "None required.",
                "monitoring": "Fruit firmness and color uniformity."
            }
        ]
    }
}

def get_crop_plan(crop_name: str):
    """
    Returns a structured crop plan based on the crop name.
    """
    crop_name_lower = crop_name.lower()
    if crop_name_lower in CROP_PLANS:
        return CROP_PLANS[crop_name_lower]
    
    return {
        "error": "Crop not found",
        "message": f"Agronomy data for '{crop_name}' is not yet available in the engine.",
        "available_crops": list(CROP_PLANS.keys())
    }

def get_rule_based_crop(data: dict) -> dict:
    """
    Core Agronomic Expert System.
    Identifies the best crop based on sensor thresholds.
    """
    temp = data.get("temperature", 0)
    humidity = data.get("humidity", 0)
    ph = data.get("ph", 7.0)
    
    # Priority 1: Heat (Corn)
    if temp > 30:
        return {
            "crop": "Corn",
            "confidence": "medium",
            "reason": f"High temperature detected ({temp}°C). Recommending heat-tolerant Corn.",
            "alternatives": ["Sorghum", "Millet"],
            "status": "offline_optimized"
        }
    
    # Priority 2: Humidity (Rice)
    if humidity > 80:
        return {
            "crop": "Rice",
            "confidence": "medium",
            "reason": f"High humidity detected ({humidity}%). Recommending Rice for moisture compatibility.",
            "alternatives": ["Sugarcane", "Taro"],
            "status": "offline_optimized"
        }
        
    # Priority 3: Acidity (Potato)
    if ph < 6:
        return {
            "crop": "Potato",
            "confidence": "medium",
            "reason": f"Acidic soil detected (pH {ph}). Recommending Potato choice.",
            "alternatives": ["Blueberry", "Radish"],
            "status": "offline_optimized"
        }
        
    # Priority 4: Optimal Balance (Tomato)
    # Check if N-P-K are in 'moderate' ranges (simulated check)
    if 6.0 <= ph <= 7.5:
        return {
            "crop": "Tomato",
            "confidence": "medium",
            "reason": "Balanced soil and climate detected. Recommending high-value Tomato cultivation.",
            "alternatives": ["Pepper", "Cucumber"],
            "status": "offline_optimized"
        }
        
    # Default: Wheat
    return {
        "crop": "Wheat",
        "confidence": "medium",
        "reason": "Stable Algerian Wheat recommended based on historic soil resilience (offline recommendation).",
        "alternatives": ["Barley", "Oats"],
        "status": "offline_optimized"
    }

def get_rule_based_advice(crop_name: str, stage_name: str) -> dict:
    """
    Extracts stage-specific advice from expert plans as a baseline.
    """
    plan = get_crop_plan(crop_name)
    if "error" in plan:
        return {
            "stage": stage_name,
            "tasks": ["Check field conditions", "Monitor soil moisture"],
            "advice": "Follow standard regional protocols.",
            "alerts": [],
            "status": "offline_optimized"
        }
        
    stage_data = next(
        (s for s in plan.get("stages", []) if s["name"].lower() == stage_name.lower()), 
        None
    )
    
    if not stage_data:
        return {
            "stage": stage_name,
            "tasks": ["General maintenance", "Observe growth"],
            "advice": f"Review standard {crop_name} management practices for the {stage_name} stage.",
            "alerts": [],
            "status": "offline_optimized"
        }
        
    return {
        "stage": stage_data["name"],
        "tasks": stage_data["tasks"],
        "advice": f"Expert Goal: {stage_data['irrigation']} Fertilizer: {stage_data['fertilizer']}",
        "alerts": [],
        "status": "offline_optimized"
    }

def get_static_journey_data(day: int) -> dict:
    """
    Returns static, indestructible farming journey data based on fixed day ranges.
    Guaranteed to work offline without AI dependencies.
    """
    if 1 <= day <= 10:
        return {
            "stage": "Planting",
            "tasks": [
                "Prepare soil with organic compost",
                "Sow seeds at correct depth",
                "Light misting for moisture",
                "Verify soil temperature (20-25°C)"
            ],
            "alerts": [
                "Watch for temperature drops",
                "Protect from heavy rain"
            ],
            "tips": [
                "Use certified high-quality seeds for better yield",
                "Plant in early morning or late afternoon"
            ]
        }
    elif 11 <= day <= 30:
        return {
            "stage": "Growth",
            "tasks": [
                "Apply leaf-friendly Nitrogen fertilizer",
                "Remove competing weeds",
                "Transition to deep root irrigation",
                "Support plants with stakes if needed"
            ],
            "alerts": [
                "Monitor for early pest signs",
                "Check for yellowing leaves"
            ],
            "tips": [
                "Ensure at least 6-8 hours of direct sunlight",
                "Avoid over-watering to prevent root rot"
            ]
        }
    elif 31 <= day <= 60:
        return {
            "stage": "Flowering",
            "tasks": [
                "Switch to Potassium-rich fertilizer",
                "Ensure steady water supply (avoid stress)",
                "Monitor pollination activity",
                "Remove early diseased foliage"
            ],
            "alerts": [
                "Critical stage: Water stress causes blossom drop",
                "Check for insects on blossoms"
            ],
            "tips": [
                "Avoid high-nitrogen fertilizer as it delays flowering",
                "Be gentle with plants during work"
            ]
        }
    else: # day 61+
        return {
            "stage": "Harvest",
            "tasks": [
                "Test ripeness/maturity level",
                "Harvest using clean, sharp tools",
                "Sort produce by size and quality",
                "Prepare storage in cool, dry area"
            ],
            "alerts": [
                "Over-ripening will reduce shelf life",
                "Handle fruit gently to avoid bruising"
            ],
            "tips": [
                "Harvest in the morning for best freshness",
                "Keep harvested crops out of direct sun"
            ]
        }

def get_smart_journey_logic(base_data: dict, monitoring: dict) -> dict:
    """
    Applies expert rules to base journey data using real-time monitoring inputs.
    Injects dynamic tasks and alerts based on environmental conditions.
    """
    if not monitoring:
        return base_data
        
    tasks = list(base_data.get("tasks", []))
    alerts = list(base_data.get("alerts", []))
    recommendations = list(base_data.get("tips", [])) # Use tips as base recommendations
    
    # 1. Irrigation Logic: soil_moisture < 35 -> irrigation task
    moisture = monitoring.get("soil_moisture", 50)
    if moisture < 35:
        tasks.insert(0, "URGENT: Run irrigation system (Moisture at {}%)".format(moisture))
        alerts.insert(0, "Critical soil moisture: Crop stress risk is high.")
        
    # 2. Heat Stress: temperature > 32 -> heat alert
    temp = monitoring.get("temperature", 25)
    if temp > 32:
        alerts.insert(0, "HEAT ALERT: High temperature ({}°C) may cause wilting.".format(temp))
        recommendations.append("Apply organic mulch to protect roots from extreme heat.")
        
    # 3. Fertilization: nitrogen < 20 -> fertilization task
    nitrogen = monitoring.get("nitrogen", 30)
    if nitrogen < 20:
        tasks.append("Apply Nitrogen fertilization (Low levels detected: {} mg/kg)".format(nitrogen))
        recommendations.append("Test soil again in 7 days to verify Nitrogen uptake.")
        
    # 4. Soil Acidity: soil_ph < 6 -> soil correction alert
    ph = monitoring.get("soil_ph", 7.0)
    if ph < 6.0:
        alerts.append("Soil acidity correction needed (pH is dangerously low: {})".format(ph))
        tasks.append("Apply lime/calcium carbonate to raise soil pH values.")

    return {
        "stage": base_data.get("stage", "Unknown"),
        "tasks": tasks,
        "alerts": alerts,
        "recommendations": recommendations
    }

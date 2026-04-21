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

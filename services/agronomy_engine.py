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
    Args:
        crop_name (str): Name of the crop (e.g., 'tomato', 'pepper').
    Returns:
        dict: Structured plan or error message.
    """
    crop_name_lower = crop_name.lower()
    if crop_name_lower in CROP_PLANS:
        return CROP_PLANS[crop_name_lower]
    
    return {
        "error": "Crop not found",
        "message": f"Agronomy data for '{crop_name}' is not yet available in the engine.",
        "available_crops": list(CROP_PLANS.keys())
    }

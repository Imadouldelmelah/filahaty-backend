from fastapi import APIRouter, HTTPException, Query
from models.soil_models import SoilData, MSPRequest
from utils.logger import logger

router = APIRouter(tags=["Crop Prediction"])

# Consolidated MSP Mapping from Legacy Client
MSP_MAPPING = {
    "rice": "Paddy - Common",
    "maize": "Maize",
    "chana": "Gram",
    "rajma": "Masur (Lentil)",
    "toordal": "Arhar (Tur)",
    "matkidal": "Urad",
    "moongdal": "Moong",
    "uraddal": "Urad",
    "masoordal": "Masur (Lentil)",
    "pomegranate": "45300.0",
    "banana": "16349.23",
    "mango": "32104.56",
    "grapes": "24987.60",
    "watermelon": "8675.833",
    "muskmelon": "18800.78",
    "apple": "86017.82",
    "orange": "49897.71",
    "papaya": "22700.08",
    "coconut": "Copra - Milling",
    "cotton": "Cotton",
    "jute": "Jute",
    "coffee": "NA"
}

# 2024 Base Market Support Prices (in local currency/quintal)
BASE_PRICES = {
    "Paddy - Common": 2183,
    "Maize": 2090,
    "Gram": 5440,
    "Masur (Lentil)": 6425,
    "Arhar (Tur)": 7000,
    "Urad": 6950,
    "Moong": 8558,
    "Copra - Milling": 10860,
    "Cotton": 6620,
    "Jute": 5050
}

@router.post("/predict_msp")
def predict_msp(request: MSPRequest):
    print(f"--- MSP PREDICTION START ---")
    print(f"INPUT: {request}")
    
    crop_query = request.crop_name.lower()
    mapping = MSP_MAPPING.get(crop_query, crop_query.capitalize())
    
    # Check if we have a direct numeric value from legacy data
    try:
        float(mapping)
        return {"predicted_msp": mapping}
    except ValueError:
        pass
        
    # Check our base price database
    price = BASE_PRICES.get(mapping, "NA")
    
    # Simulate a "prediction" trend based on year (very basic)
    if isinstance(price, (int, float)):
        year_diff = request.current_year - 2024
        predicted_price = price * (1 + (0.05 * year_diff))
        return {"predicted_msp": f"{predicted_price:.2f}"}
        
    return {"predicted_msp": "Market Price Unavailable"}

# High-quality agricultural image mapping for the professional UI
CROP_IMAGES = {
    "Wheat": "https://unsplash.com/photos/beautiful-nature-background-with-close-up-of-ears-of-ripe-wheat-on-cereal-field-w6ZMTahJGoE",
    "Tomato": "https://unsplash.com/photos/closeup-photo-of-red-tomato-against-black-background-S-de8PboZmI",
    "Potato": "https://unsplash.com/photos/brown-potato-lot-B0s3Xndk6tw",
    "Olive": "https://unsplash.com/photos/a-pile-of-green-and-black-olives-sitting-on-top-of-each-other-bavD_RW9pTQ",
    "Onion": "https://unsplash.com/photos/white-garlic-on-brown-wooden-table-CNZ-9s5p2i8",
    "Barley": "https://unsplash.com/photos/a-close-up-of-a-bunch-of-seeds-P3xfVJ5Gyu0",
    "Maize": "https://unsplash.com/photos/a-pile-of-yellow-corn-on-the-cob-RNHpv06LWMU",
    "Watermelon": "https://www.istockphoto.com/photo/fresh-watermelons-on-a-street-fruit-stall-in-summer-gm2217809693-634379736?utm_source=unsplash&utm_medium=affiliate&utm_campaign=srp_photos_bottom&utm_content=https%3A%2F%2Funsplash.com%2Fs%2Fphotos%2Fwathermelon&utm_term=wathermelon%3A%3A%3A%3A00d800e2-2676-4959-95b3-7c537140f46c",
    "Rice": "https://images.unsplash.com/photo-1586201375761-83865001e31c?q=80&w=800",
    "Chickpea": "https://images.unsplash.com/photo-1515543904379-3d757afe72e2?q=80&w=800",
    "Dates": "https://images.unsplash.com/photo-1593361848529-68800923057e?q=80&w=800",
    "Default": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=800"
}

# Rule-Based Engine: Comprehensive Soil Profiles (Min, Max) Optimal Ranges
CROP_PROFILES = {
    "Wheat": {"N": (40, 60), "P": (40, 60), "K": (40, 60), "temp": (10, 25), "hum": (40, 60), "ph": (6.0, 7.5), "rain": (400, 800)},
    "Tomato": {"N": (70, 100), "P": (30, 50), "K": (40, 60), "temp": (20, 35), "hum": (50, 70), "ph": (6.0, 7.0), "rain": (400, 800)},
    "Potato": {"N": (30, 50), "P": (40, 60), "K": (50, 80), "temp": (15, 25), "hum": (70, 100), "ph": (5.0, 6.5), "rain": (600, 1200)},
    "Olive": {"N": (20, 40), "P": (10, 30), "K": (20, 40), "temp": (15, 30), "hum": (30, 60), "ph": (6.0, 8.0), "rain": (100, 400)},
    "Onion": {"N": (40, 60), "P": (30, 50), "K": (40, 60), "temp": (13, 25), "hum": (50, 70), "ph": (6.0, 7.5), "rain": (300, 700)},
    "Barley": {"N": (30, 50), "P": (20, 40), "K": (30, 50), "temp": (12, 25), "hum": (30, 50), "ph": (6.0, 8.0), "rain": (100, 300)},
    "Maize": {"N": (70, 100), "P": (40, 60), "K": (40, 60), "temp": (20, 35), "hum": (50, 80), "ph": (5.5, 7.5), "rain": (500, 1000)},
    "Watermelon": {"N": (40, 60), "P": (30, 50), "K": (40, 60), "temp": (25, 35), "hum": (50, 70), "ph": (6.0, 7.0), "rain": (400, 800)}
}

# North African geographic adaptation priority (Lower is better)
NORTH_AFRICAN_PRIORITY = {
    "Olive": 1,
    "Wheat": 2,
    "Barley": 3,
    "Onion": 4,
    "Potato": 5,
    "Tomato": 6,
    "Watermelon": 7,
    "Maize": 8
}

def call_ai(prompt):
    import os
    import requests

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "AI temporarily unavailable"

    try:
        print("Calling AI...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=15
        )
        print(f"AI Response Status: {response.status_code}")

        if response.status_code != 200:
            return "AI temporarily unavailable"

        return response.json()["choices"][0]["message"]["content"]

    except Exception:
        return "AI temporarily unavailable"

@router.post("/predict")
async def predict_crop(data: SoilData):
    logger.info(f"--- CROP RECOMMENDATION ENGINE START ---")
    logger.info(f"INPUT DATA RECEIVED: {data.model_dump()}")
    
    try:
        best_crop = "Unknown"
        max_score = -1
        debug_scores = {}
        
        n, p, k = data.nitrogen, data.phosphorus, data.potassium
        temp, hum, ph, rain = data.temperature, data.humidity, data.ph, data.rainfall
        
        for crop, profile in CROP_PROFILES.items():
            score = 0
            if profile["N"][0] <= n <= profile["N"][1]: score += 1
            if profile["P"][0] <= p <= profile["P"][1]: score += 1
            if profile["K"][0] <= k <= profile["K"][1]: score += 1
            if profile["temp"][0] <= temp <= profile["temp"][1]: score += 1
            if profile["hum"][0] <= hum <= profile["hum"][1]: score += 1
            if profile["ph"][0] <= ph <= profile["ph"][1]: score += 1
            if profile["rain"][0] <= rain <= profile["rain"][1]: score += 1
            
            debug_scores[crop] = score
            
            if score > max_score:
                max_score = score
                best_crop = crop
            elif score == max_score and max_score > 0:
                if NORTH_AFRICAN_PRIORITY.get(crop, 99) < NORTH_AFRICAN_PRIORITY.get(best_crop, 99):
                    best_crop = crop
                    
        if max_score == 0:
            best_crop = "Wheat"
            
        confidence_mapping = {7: 95, 6: 85, 5: 75, 4: 65, 3: 50, 2: 35, 1: 20, 0: 10}
        confidence = confidence_mapping.get(max_score, 10)
        img_url = CROP_IMAGES.get(best_crop, CROP_IMAGES["Default"])
        
        reason = "Based on precise soil constraints, " + best_crop + " achieves a " + str(confidence) + "% viability match."
        
        if os.getenv("OPENROUTER_API_KEY"):
            from services.crop_recommendation_service import CropRecommendationService
            crop_svc = CropRecommendationService()
            ai_rec = await crop_svc.generate_recommendation(data.model_dump())
            
            # Use AI recommendation if it provides one, otherwise stick to rule-based fallback
            best_crop = ai_rec.get("crop", best_crop)
            confidence = ai_rec.get("confidence", confidence)
            reason = ai_rec.get("reason", reason)
            
        return {
            "crop": best_crop,
            "confidence": str(confidence),
            "reason": reason,
            "explanation": reason, # Backward compatibility
            "debug_scores": debug_scores,
            "image_url": img_url
        }
    except Exception as e:
        logger.error(f"CRITICAL_PREDICTION_ERROR: {str(e)}")
        # Task 1 & 2: Never return 500, always return valid JSON fallback
        return {
            "crop": "wheat",
            "confidence": "low",
            "reason": "Our recommendation engine is facing a temporary technical issue. Falling back to standard Algerian wheat profile.",
            "explanation": "fallback due to server error",
            "status": "fallback"
        }

@router.get("/predict/auto")
async def predict_crop_automatically(
    field_id: str = Query("default_field"),
    lat: float = Query(None),
    lon: float = Query(None)
):
    """
    Standardized 'Crop Suggestion' powered by real-time field sensors and weather.
    """
    try:
        # 1. Fetch Monitoring Data (Single Source of Truth)
        from services.fake_monitoring_service import FakeMonitoringService
        monitoring_svc = FakeMonitoringService()
        sensors = monitoring_svc.get_fake_monitoring_data(field_id)
        
        # 2. Fetch Weather Data (if location available)
        weather = {"temperature": sensors["temperature"], "humidity": sensors["humidity"], "rain": sensors["rainfall"]}
        if lat is not None and lon is not None:
             from services.weather_service import WeatherService
             weather_svc = WeatherService()
             weather = weather_svc.get_weather(lat, lon)
        
        # 3. Map to SoilData model (Using standardized long-form keys)
        soil_data = SoilData(
            nitrogen=sensors["nitrogen"],
            phosphorus=sensors["phosphorus"],
            potassium=sensors["potassium"],
            temperature=weather["temperature"] or sensors["temperature"],
            humidity=weather["humidity"] or sensors["humidity"],
            ph=sensors["ph"],
            rainfall=weather["rain"] or sensors["rainfall"]
        )
        
        # 4. Use existing prediction logic
        prediction = await predict_crop(soil_data)
        
        # 5. Include sensor data for client-side reuse
        prediction["sensors"] = sensors
        return prediction
        
    except Exception as e:
        logger.error(f"AUTO_PREDICT_ERROR: {str(e)}")
        # Never fail: Return a standard fallback for stability
        fallback_sensors = {
            "nitrogen": 50, "phosphorus": 40, "potassium": 40, 
            "temperature": 25.0, "humidity": 60.0, 
            "ph": 6.5, "rainfall": 500.0
        }
        return {
            "crop": "Wheat",
            "confidence": "50",
            "reason": "Our auto-monitoring system is currently under maintenance. We recommend standard Algerian Wheat as a stable fallback for this season.",
            "explanation": "standard fallback due to technical issue",
            "image_url": CROP_IMAGES.get("Wheat"),
            "sensors": fallback_sensors
        }

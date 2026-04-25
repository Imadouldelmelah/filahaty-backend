"""
Agronomy Engine Module
Provides expert-level structured crop plans for smart farming.
"""

TRANSLATIONS = {
    "en": {
        "crop_not_found": "Crop not found",
        "crop_not_found_msg": "Agronomy data for '{crop_name}' is not yet available in the engine.",
        "corn_reason": "High temperature detected ({temp}°C). Recommending heat-tolerant Corn.",
        "rice_reason": "High humidity detected ({humidity}%). Recommending Rice for moisture compatibility.",
        "potato_reason": "Acidic soil detected (pH {ph}). Recommending Potato choice.",
        "tomato_reason": "Balanced soil and climate detected. Recommending high-value Tomato cultivation.",
        "wheat_reason": "Stable Algerian Wheat recommended based on historic soil resilience (offline recommendation).",
        "baseline_tasks": ["Check field conditions", "Monitor soil moisture"],
        "baseline_advice": "Follow standard regional protocols.",
        "stage_maintenance_tasks": ["General maintenance", "Observe growth"],
        "stage_review_advice": "Review standard {crop_name} management practices for the {stage_name} stage.",
        "expert_goal_advice": "Expert Goal: {irrigation} Fertilizer: {fertilizer}",
        "low_moisture_alert": "LOW MOISTURE ALERT: Soil moisture is at {moisture}%.",
        "low_moisture_task": "Immediate irrigation required to prevent root stress.",
        "low_moisture_rec": "Increase irrigation frequency during dry spells.",
        "heat_stress_alert": "HEAT STRESS ALERT: High temperature ({temp}°C) detected.",
        "heat_stress_task": "Apply heat protection or shading if possible.",
        "heat_stress_rec": "Monitor plant posture for wilting during peak sun.",
        "low_nitrogen_alert": "LOW NITROGEN ALERT: Nutrient levels are below threshold ({nitrogen} mg/kg).",
        "low_nitrogen_task": "Apply balanced Nitrogen-rich fertilizer (e.g., Urea or NPK).",
        "low_nitrogen_rec": "Regularly test NPK levels during growth phase.",
        "routine_monitoring": "Routine field monitoring",
        "system_stable": "System status: Stable",
        "follow_protocols": "Follow standard regional crop protocols",
        "planting_stage": "Planting",
        "growth_stage": "Growth",
        "flowering_stage": "Flowering",
        "harvest_stage": "Harvest",
        "decision_maintain_monitoring": "Maintain Routine Monitoring",
        "decision_stable_environment": "Current sensor baselines indicate a stable agricultural environment.",
        "decision_ensure_sensors_clean": "Ensure all sensors are clean and properly calibrated while monitoring plant vigor visually.",
        "advanced_chat_offline_msg": "Smart offline mode activated: I can still guide you based on agricultural knowledge.",
        "journey_day1_tasks": ["Prepare soil with organic compost", "Sow seeds at correct depth", "Light misting for moisture"],
        "journey_day1_alerts": ["Protect from sudden temperature drops"],
        "journey_day1_recs": ["Use certified high-quality seeds for better yield"],
        "journey_day11_tasks": ["Apply leaf-friendly Nitrogen fertilizer", "Remove competing weeds", "Establish drip irrigation lines"],
        "journey_day11_alerts": ["Monitor for early pest signs"],
        "journey_day11_recs": ["Ensure at least 6-8 hours of direct sunlight"],
        "journey_day31_tasks": ["Switch to Potassium-rich fertilizer", "Ensure steady water supply (avoid stress)", "Monitor pollination activity"],
        "journey_day31_alerts": ["Water stress causes blossom drop"],
        "journey_day31_recs": ["Avoid high-nitrogen fertilizer as it delays flowering"],
        "journey_day61_tasks": ["Test maturity level and fruit firmness", "Harvest using clean, sharp tools", "Sort produce by size and quality"],
        "journey_day61_alerts": ["Over-ripening will reduce shelf life"],
        "journey_day61_recs": ["Harvest in the early morning for best freshness"]
    },
    "fr": {
        "crop_not_found": "Culture non trouvée",
        "crop_not_found_msg": "Les données agronomiques pour '{crop_name}' ne sont pas encore disponibles.",
        "corn_reason": "Température élevée détectée ({temp}°C). Recommandation de maïs résistant à la chaleur.",
        "rice_reason": "Humidité élevée détectée ({humidity}%). Recommandation de riz pour la compatibilité avec l'humidité.",
        "potato_reason": "Sol acide détecté (pH {ph}). Recommandation de pomme de terre.",
        "tomato_reason": "Sol et climat équilibrés détectés. Recommandation de culture de tomates à haute valeur.",
        "wheat_reason": "Blé algérien stable recommandé sur la base de la résilience historique du sol.",
        "baseline_tasks": ["Vérifier les conditions du champ", "Surveiller l'humidité du sol"],
        "baseline_advice": "Suivre les protocoles régionaux standard.",
        "stage_maintenance_tasks": ["Entretien général", "Observer la croissance"],
        "stage_review_advice": "Passer en revue les pratiques de gestion standard de {crop_name} pour le stade {stage_name}.",
        "expert_goal_advice": "Objectif Expert: {irrigation} Engrais: {fertilizer}",
        "low_moisture_alert": "ALERTE FAIBLE HUMIDITÉ: L'humidité du sol est à {moisture}%.",
        "low_moisture_task": "Irrigation immédiate requise pour éviter le stress des racines.",
        "low_moisture_rec": "Augmenter la fréquence d'irrigation pendant les périodes sèches.",
        "heat_stress_alert": "ALERTE STRESS THERMIQUE: Température élevée ({temp}°C) détectée.",
        "heat_stress_task": "Appliquer une protection thermique ou un ombrage si possible.",
        "heat_stress_rec": "Surveiller la posture des plantes pour le flétrissement pendant le pic de soleil.",
        "low_nitrogen_alert": "ALERTE FAIBLE AZOTE: Les niveaux de nutriments sont en dessous du seuil ({nitrogen} mg/kg).",
        "low_nitrogen_task": "Appliquer un engrais équilibré riche en azote (ex: Urée ou NPK).",
        "low_nitrogen_rec": "Tester régulièrement les niveaux de NPK pendant la phase de croissance.",
        "routine_monitoring": "Surveillance de routine du champ",
        "system_stable": "État du système: Stable",
        "follow_protocols": "Suivre les protocoles de culture régionaux standard",
        "planting_stage": "Plantation",
        "growth_stage": "Croissance",
        "flowering_stage": "Floraison",
        "harvest_stage": "Récolte",
        "decision_maintain_monitoring": "Maintenir une surveillance de routine",
        "decision_stable_environment": "Les lignes de base des capteurs actuelles indiquent un environnement agricole stable.",
        "decision_ensure_sensors_clean": "Assurez-vous que tous les capteurs sont propres et correctement étalonnés tout en surveillant visuellement la vigueur des plantes.",
        "advanced_chat_offline_msg": "Mode hors ligne intelligent activé : je peux toujours vous guider en me basant sur mes connaissances agricoles.",
        "journey_day1_tasks": ["Préparer le sol avec du compost organique", "Semer les graines à la bonne profondeur", "Légère brumisation pour l'humidité"],
        "journey_day1_alerts": ["Protéger contre les baisses soudaines de température"],
        "journey_day1_recs": ["Utiliser des semences certifiées de haute qualité pour un meilleur rendement"],
        "journey_day11_tasks": ["Appliquer un engrais azoté favorable aux feuilles", "Enlever les mauvaises herbes concurrentes", "Établir des lignes d'irrigation goutte à goutte"],
        "journey_day11_alerts": ["Surveiller les premiers signes de ravageurs"],
        "journey_day11_recs": ["Garantir au moins 6 à 8 heures de lumière directe du soleil"],
        "journey_day31_tasks": ["Passer à un engrais riche en potassium", "Assurer un approvisionnement en eau régulier (éviter le stress)", "Surveiller l'activité de pollinisation"],
        "journey_day31_alerts": ["Le stress hydrique provoque la chute des fleurs"],
        "journey_day31_recs": ["Éviter les engrais riches en azote car ils retardent la floraison"],
        "journey_day61_tasks": ["Tester le niveau de maturité et la fermeté des fruits", "Récolter en utilisant des outils propres et tranchants", "Trier les produits par taille et qualité"],
        "journey_day61_alerts": ["Le sur-mûrissement réduira la durée de conservation"],
        "journey_day61_recs": ["Récolter tôt le matin pour une meilleure fraîcheur"]
    },
    "ar": {
        "crop_not_found": "المحصول غير موجود",
        "crop_not_found_msg": "البيانات الزراعية لـ '{crop_name}' غير متوفرة بعد في المحرك.",
        "corn_reason": "تم اكتشاف درجة حرارة عالية ({temp} درجة مئوية). نوصي بالذرة المتحملة للحرارة.",
        "rice_reason": "تم اكتشاف رطوبة عالية ({humidity}%). نوصي بالأرز للتوافق مع الرطوبة.",
        "potato_reason": "تم اكتشاف تربة حمضية (درجة الحموضة {ph}). نوصي بالبطاطس.",
        "tomato_reason": "تم اكتشاف توازن في التربة والمناخ. نوصي بزراعة الطماطم عالية القيمة.",
        "wheat_reason": "يوصى بالقمح الجزائري المستقر بناءً على مرونة التربة التاريخية.",
        "baseline_tasks": ["فحص ظروف الحقل", "مراقبة رطوبة التربة"],
        "baseline_advice": "اتبع البروتوكولات الإقليمية القياسية.",
        "stage_maintenance_tasks": ["صيانة عامة", "مراقبة النمو"],
        "stage_review_advice": "راجعي ممارسات الإدارة القياسية لـ {crop_name} لمرحلة {stage_name}.",
        "expert_goal_advice": "هدف الخبير: {irrigation} السماد: {fertilizer}",
        "low_moisture_alert": "تنبيه انخفاض الرطوبة: رطوبة التربة عند {moisture}%.",
        "low_moisture_task": "مطلوب ري فوري لمنع إجهاد الجذور.",
        "low_moisture_rec": "زيادة تكرار الري خلال فترات الجفاف.",
        "heat_stress_alert": "تنبيه إجهاد حراري: تم اكتشاف درجة حرارة عالية ({temp} درجة مئوية).",
        "heat_stress_task": "استخدم حماية من الحرارة أو تظليل إن أمكن.",
        "heat_stress_rec": "راقب وضعية النباتات للكشف عن الذبول أثناء ذروة الشمس.",
        "low_nitrogen_alert": "تنبيه انخفاض النيتروجين: مستويات العناصر الغذائية أقل من الحد المسموح به ({nitrogen} ملجم/كجم).",
        "low_nitrogen_task": "استخدم سماداً متوازناً غنياً بالنيتروجين (مثل اليوريا أو NPK).",
        "low_nitrogen_rec": "اختبر مستويات NPK بانتظام خلال مرحلة النمو.",
        "routine_monitoring": "مراقبة الحقل الروتينية",
        "system_stable": "حالة النظام: مستقرة",
        "follow_protocols": "اتبع بروتوكولات المحاصيل الإقليمية القياسية",
        "planting_stage": "الزراعة",
        "growth_stage": "النمو",
        "flowering_stage": "الإزهار",
        "harvest_stage": "الحصاد",
        "decision_maintain_monitoring": "الحفاظ على المراقبة الروتينية",
        "decision_stable_environment": "تشير مستويات المستشعرات الحالية إلى بيئة زراعية مستقرة.",
        "decision_ensure_sensors_clean": "تأكد من نظافة جميع المستشعرات ومعايرتها بشكل صحيح مع مراقبة قوة النبات بصريًا.",
        "advanced_chat_offline_msg": "تم تنشيط الوضع الذكي دون اتصال: لا يزال بإمكاني إرشادك بناءً على المعرفة الزراعية.",
        "journey_day1_tasks": ["تحضير التربة بالسماد العضوي", "زرع البذور بالعمق الصحيح", "ترطيب خفيف للرطوبة"],
        "journey_day1_alerts": ["الحماية من الانخفاض المفاجئ في درجات الحرارة"],
        "journey_day1_recs": ["استخدام بذور معتمدة عالية الجودة لزيادة المردود"],
        "journey_day11_tasks": ["استخدام سماد نيتروجيني صديق للأوراق", "إزالة الأعشاب الضارة المنافسة", "إنشاء خطوط ري بالتنقيط"],
        "journey_day11_alerts": ["مراقبة العلامات المبكرة للآفات"],
        "journey_day11_recs": ["ضمان ما لا يقل عن 6-8 ساعات من أشعة الشمس المباشرة"],
        "journey_day31_tasks": ["التبديل إلى سماد غني بالبوتاسيوم", "ضمان إمدادات مياه ثابتة (تجنب الإجهاد)", "مراقبة نشاط التلقيح"],
        "journey_day31_alerts": ["الإجهاد المائي يسبب تساقط الأزهار"],
        "journey_day31_recs": ["تجنب السماد عالي النيتروجين لأنه يؤخر الإزهار"],
        "journey_day61_tasks": ["اختبار مستوى النضج وصلابة الفاكهة", "الحصاد باستخدام أدوات نظيفة وحادة", "فرز المنتجات حسب الحجم والجودة"],
        "journey_day61_alerts": ["النضج الزائد سيقلل من مدة الصلاحية"],
        "journey_day61_recs": ["الحصاد في الصباح الباكر للحصول على أفضل نضارة"]
    }
}

def _t(key, lang="en", **kwargs):
    lang = lang if (lang and lang in TRANSLATIONS) else "en"
    text = TRANSLATIONS[lang].get(key, TRANSLATIONS["en"].get(key, key))
    if isinstance(text, list):
        return text
    return text.format(**kwargs)

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

def get_crop_plan(crop_name: str, lang: str = "en"):
    """
    Returns a structured crop plan based on the crop name.
    """
    crop_name_lower = crop_name.lower()
    if crop_name_lower in CROP_PLANS:
        return CROP_PLANS[crop_name_lower]
    
    return {
        "error": _t("crop_not_found", lang),
        "message": _t("crop_not_found_msg", lang, crop_name=crop_name),
        "available_crops": list(CROP_PLANS.keys())
    }

def get_rule_based_crop(data: dict, lang: str = "en") -> dict:
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
            "reason": _t("corn_reason", lang, temp=temp),
            "alternatives": ["Sorghum", "Millet"],
            "status": "offline_optimized"
        }
    
    # Priority 2: Humidity (Rice)
    if humidity > 80:
        return {
            "crop": "Rice",
            "confidence": "medium",
            "reason": _t("rice_reason", lang, humidity=humidity),
            "alternatives": ["Sugarcane", "Taro"],
            "status": "offline_optimized"
        }
        
    # Priority 3: Acidity (Potato)
    if ph < 6:
        return {
            "crop": "Potato",
            "confidence": "medium",
            "reason": _t("potato_reason", lang, ph=ph),
            "alternatives": ["Blueberry", "Radish"],
            "status": "offline_optimized"
        }
        
    # Priority 4: Optimal Balance (Tomato)
    if 6.0 <= ph <= 7.5:
        return {
            "crop": "Tomato",
            "confidence": "medium",
            "reason": _t("tomato_reason", lang),
            "alternatives": ["Pepper", "Cucumber"],
            "status": "offline_optimized"
        }
        
    # Default: Wheat
    return {
        "crop": "Wheat",
        "confidence": "medium",
        "reason": _t("wheat_reason", lang),
        "alternatives": ["Barley", "Oats"],
        "status": "offline_optimized"
    }

def get_rule_based_advice(crop_name: str, stage_name: str, lang: str = "en") -> dict:
    """
    Extracts stage-specific advice from expert plans as a baseline.
    """
    plan = get_crop_plan(crop_name, lang)
    if "error" in plan:
        return {
            "stage": stage_name,
            "tasks": _t("baseline_tasks", lang),
            "advice": _t("baseline_advice", lang),
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
            "tasks": _t("stage_maintenance_tasks", lang),
            "advice": _t("stage_review_advice", lang, crop_name=crop_name, stage_name=stage_name),
            "alerts": [],
            "status": "offline_optimized"
        }
        
    return {
        "stage": stage_data["name"],
        "tasks": stage_data["tasks"],
        "advice": _t("expert_goal_advice", lang, irrigation=stage_data['irrigation'], fertilizer=stage_data['fertilizer']),
        "alerts": [],
        "status": "offline_optimized"
    }

def get_static_journey_data(day: int, lang: str = "en") -> dict:
    """
    Returns static, indestructible farming journey data based on fixed day ranges.
    """
    if 1 <= day <= 10:
        return {
            "stage": _t("planting_stage", lang),
            "tasks": _t("journey_day1_tasks", lang),
            "alerts": _t("journey_day1_alerts", lang),
            "recommendations": _t("journey_day1_recs", lang)
        }
    elif 11 <= day <= 30:
        return {
            "stage": _t("growth_stage", lang),
            "tasks": _t("journey_day11_tasks", lang),
            "alerts": _t("journey_day11_alerts", lang),
            "recommendations": _t("journey_day11_recs", lang)
        }
    elif 31 <= day <= 60:
        return {
            "stage": _t("flowering_stage", lang),
            "tasks": _t("journey_day31_tasks", lang),
            "alerts": _t("journey_day31_alerts", lang),
            "recommendations": _t("journey_day31_recs", lang)
        }
    else: # day 61+
        return {
            "stage": _t("harvest_stage", lang),
            "tasks": _t("journey_day61_tasks", lang),
            "alerts": _t("journey_day61_alerts", lang),
            "recommendations": _t("journey_day61_recs", lang)
        }

def get_smart_journey_logic(progress: dict, monitoring: dict, lang: str = "en") -> dict:
    """
    Enhanced Dynamic Journey Engine.
    Combines stage baseline with real-time sensor triggers.
    """
    day = progress.get("day", 1)
    base_data = get_static_journey_data(day, lang)
    
    tasks = list(base_data.get("tasks", []))
    alerts = list(base_data.get("alerts", []))
    recommendations = list(base_data.get("recommendations", []))
    
    if monitoring:
        # Rule 1: low moisture → irrigation alert
        moisture = monitoring.get("soil_moisture", 50)
        if moisture < 35:
            alerts.insert(0, _t("low_moisture_alert", lang, moisture=moisture))
            tasks.insert(0, _t("low_moisture_task", lang))
            recommendations.append(_t("low_moisture_rec", lang))

        # Rule 2: high temp → heat stress
        temp = monitoring.get("temperature", 25)
        if temp > 32:
            alerts.insert(0, _t("heat_stress_alert", lang, temp=temp))
            tasks.append(_t("heat_stress_task", lang))
            recommendations.append(_t("heat_stress_rec", lang))

        # Rule 3: low nitrogen → fertilization
        nitrogen = monitoring.get("nitrogen", 30)
        if nitrogen < 20:
            alerts.append(_t("low_nitrogen_alert", lang, nitrogen=nitrogen))
            tasks.append(_t("low_nitrogen_task", lang))
            recommendations.append(_t("low_nitrogen_rec", lang))

    # Guarantee non-empty lists
    if not tasks: tasks = [_t("routine_monitoring", lang)]
    if not alerts: alerts = [_t("system_stable", lang)]
    if not recommendations: recommendations = [_t("follow_protocols", lang)]

    return {
        "stage": base_data["stage"],
        "tasks": tasks,
        "alerts": alerts,
        "recommendations": recommendations
    }

from utils.logger import logger

class WeatherIntelligenceService:
    def __init__(self):
        # Thresholds for decision logic
        self.RAIN_THRESHOLD = 2.0  # mm/h
        self.HEAT_THRESHOLD = 35.0  # °C
        self.HUMIDITY_THRESHOLD = 90.0  # %

        # Simple translation dictionary
        self.translations = {
            "en": {
                "rain_detected": "Rainfall detected: Skip manual irrigation today to conserve water.",
                "light_rain": "Light rain detected: Consider reducing irrigation volume.",
                "standard_irrigation": "Standard irrigation schedule recommended.",
                "heat_stress_critical": "CRITICAL: High Heat Stress Warning.",
                "heat_stress_rec": "Hydrate crops early in the morning. Avoid any transplanting or pruning during midday peak.",
                "moderate_heat": "ADVISORY: Moderate Heat.",
                "moderate_heat_rec": "Monitor soil moisture closely as evaporation rates are high.",
                "fungal_risk_critical": "CRITICAL: High Fungal Disease Risk.",
                "fungal_risk_rec": "Avoid overhead watering. Ensure maximum airflow around plants and inspect for signs of blight.",
                "elevated_humidity": "ADVISORY: Elevated Humidity.",
                "elevated_humidity_rec": "Check for pests that thrive in humid environments (e.g., aphids).",
                "waterlogging_critical": "CRITICAL: Root Suffocation / Waterlogging Risk.",
                "waterlogging_rec": "Soil is already saturated. Heavy rain detected. Ensure drainage is clear.",
                "low_moisture_advisory": "ADVISORY: Low Soil Moisture.",
                "low_moisture_rec": "Soil is dangerously dry. Deep irrigation required immediately.",
                "heat_risk_crop": "High temperature risk for {crop_name}.",
                "heat_risk_flowering": "Critical: High heat risk during Flowering!",
                "blossom_drop": "{crop_name} blossom drop may occur at {temp}°C. Ensure deep irrigation and consider shade cloths.",
                "heavy_rain_crop": "Significant rainfall for {crop_name}.",
                "heavy_rain_rec": "Check field drainage to prevent waterlogging.",
                "heavy_rain_seedling": "Warning: Heavy rain risk for Seedlings!",
                "seedling_physical_damage": "Young {crop_name} plants are vulnerable to physical damage. Consider temporary cover.",
                "extreme_moisture": "Extreme moisture risk for {crop_name}.",
                "extreme_moisture_rec": "Ensure maximum airflow and inspect lower leaves.",
                "high_disease_risk": "High Disease Risk (Blight/Mildew)!",
                "disease_moisture_rec": "Humid conditions (> {humidity}%) favor pathogens on {crop_name}. Apply preventive organic fungicide if needed.",
                "field_saturation": "Critical: Field saturation detected!",
                "field_saturation_rec": "Risk of root rot. Delay any overhead irrigation and inspect drainage channels.",
                "ph_mismatch": "Advisory: Soil pH is outside optimal range.",
                "ph_mismatch_rec": "Current pH {ph} may lock out nutrients for {crop_name}. Consult soil treatment guide.",
                "weather_incomplete": "Weather data incomplete.",
                "weather_summary": "Currently {temp}°C and {condition}.",
                "condition_clear": "Clear",
                "condition_rainy": "Rainy",
                "syncing_alerts": "Weather system syncing: No critical alerts currently active."
            },
            "fr": {
                "rain_detected": "Pluie détectée : Ignorez l'irrigation manuelle aujourd'hui pour économiser l'eau.",
                "light_rain": "Pluie légère détectée : Envisagez de réduire le volume d'irrigation.",
                "standard_irrigation": "Programme d'irrigation standard recommandé.",
                "heat_stress_critical": "CRITIQUE : Alerte de stress thermique élevé.",
                "heat_stress_rec": "Hydratez les cultures tôt le matin. Évitez tout repiquage ou taille pendant le pic de midi.",
                "moderate_heat": "AVIS : Chaleur modérée.",
                "moderate_heat_rec": "Surveillez de près l'humidité du sol car les taux d'évaporation sont élevés.",
                "fungal_risk_critical": "CRITIQUE : Risque élevé de maladies fongiques.",
                "fungal_risk_rec": "Évitez l'arrosage par le haut. Assurez une circulation d'air maximale et inspectez les signes de mildiou.",
                "elevated_humidity": "AVIS : Humidité élevée.",
                "elevated_humidity_rec": "Vérifiez les parasites qui prospèrent dans les environnements humides (ex: pucerons).",
                "waterlogging_critical": "CRITIQUE : Risque d'asphyxie des racines / engorgement.",
                "waterlogging_rec": "Le sol est déjà saturé. Forte pluie détectée. Assurez-vous que le drainage est dégagé.",
                "low_moisture_advisory": "AVIS : Faible humidité du sol.",
                "low_moisture_rec": "Le sol est dangereusement sec. Irrigation profonde requise immédiatement.",
                "heat_risk_crop": "Risque de température élevée pour {crop_name}.",
                "heat_risk_flowering": "Critique : Risque de forte chaleur pendant la floraison !",
                "blossom_drop": "La chute des fleurs de {crop_name} peut survenir à {temp}°C. Assurez une irrigation profonde.",
                "heavy_rain_crop": "Précipitations importantes pour {crop_name}.",
                "heavy_rain_rec": "Vérifiez le drainage du champ pour éviter l'engorgement.",
                "heavy_rain_seedling": "Attention : Risque de pluie forte pour les semis !",
                "seedling_physical_damage": "Les jeunes plantes de {crop_name} sont vulnérables aux dommages physiques.",
                "extreme_moisture": "Risque d'humidité extrême pour {crop_name}.",
                "extreme_moisture_rec": "Assurez une circulation d'air maximale.",
                "high_disease_risk": "Risque élevé de maladie (mildiou/oïdium) !",
                "disease_moisture_rec": "Les conditions humides (> {humidity}%) favorisent les agents pathogènes sur {crop_name}.",
                "field_saturation": "Critique : Saturation du champ détectée !",
                "field_saturation_rec": "Risque de pourriture des racines. Retardez toute irrigation.",
                "ph_mismatch": "Avis : Le pH du sol est en dehors de la plage optimale.",
                "ph_mismatch_rec": "Le pH actuel {ph} peut bloquer les nutriments pour {crop_name}.",
                "weather_incomplete": "Données météo incomplètes.",
                "weather_summary": "Actuellement {temp}°C et {condition}.",
                "condition_clear": "Clair",
                "condition_rainy": "Pluvieux",
                "syncing_alerts": "Synchronisation du système météo : aucune alerte critique active pour le moment."
            },
            "ar": {
                "rain_detected": "تم اكتشاف تساقط الأمطار: تخطى الري اليدوي اليوم لتوفير المياه.",
                "light_rain": "تم اكتشاف مطر خفيف: فكر في تقليل حجم الري.",
                "standard_irrigation": "يوصى بجدول ري قياسي.",
                "heat_stress_critical": "حرج: تحذير من إجهاد حراري عالٍ.",
                "heat_stress_rec": "رطب المحاصيل في الصباح الباكر. تجنب أي شتل أو تقليم خلال ذروة منتصف النهار.",
                "moderate_heat": "تنبيه: حرارة معتدلة.",
                "moderate_heat_rec": "راقب رطوبة التربة عن كثب لأن معدلات التبخر عالية.",
                "fungal_risk_critical": "حرج: مخاطر عالية للأمراض الفطرية.",
                "fungal_risk_rec": "تجنب الري العلوي. تأكد من توفير أقصى جزيئات للهواء حول النباتات وافحص علامات اللفحة.",
                "elevated_humidity": "تنبيه: رطوبة مرتفعة.",
                "elevated_humidity_rec": "افحص الآفات التي تزدهر في البيئات الرطبة (مثل المن).",
                "waterlogging_critical": "حرج: خطر اختناق الجذور / الغرق بالمياه.",
                "waterlogging_rec": "التربة مشبعة بالفعل. تم اكتشاف أمطار غزيرة. تأكد من أن قنوات التصريف مفتوحة.",
                "low_moisture_advisory": "تنبيه: رطوبة التربة منخفضة.",
                "low_moisture_rec": "التربة جافة بشكل خطير. مطلوب ري عميق فوراً.",
                "heat_risk_crop": "خطر ارتفاع درجة الحرارة لـ {crop_name}.",
                "heat_risk_flowering": "حرج: خطر حرارة عالية أثناء الإزهار!",
                "blossom_drop": "قد يحدث تساقط أزهار {crop_name} عند {temp} درجة مئوية. تأكد من الري العميق.",
                "heavy_rain_crop": "أمطار غزيرة لـ {crop_name}.",
                "heavy_rain_rec": "افحص تصريف الحقل لمنع غرق المحصول.",
                "heavy_rain_seedling": "تحذير: خطر أمطار غزيرة على الشتلات!",
                "seedling_physical_damage": "نباتات {crop_name} الصغيرة عرضة للتلف المادي. فكر في غطاء مؤقت.",
                "extreme_moisture": "خطر رطوبة قصوى لـ {crop_name}.",
                "extreme_moisture_rec": "تأكد من أقصى تدفق للهواء وافحص الأوراق السفلية.",
                "high_disease_risk": "خطر عالٍ للإصابة بالأمراض (اللفحة/البياض)!",
                "disease_moisture_rec": "الظروف الرطبة (> {humidity}%) تساعد الممرضات على {crop_name}.",
                "field_saturation": "حرج: تم اكتشاف تشبع الحقل!",
                "field_saturation_rec": "خطر تعفن الجذور. أخر أي ري علوي وافحص قنوات التصريف.",
                "ph_mismatch": "تنبيه: درجة حموضة التربة خارج النطاق الأمثل.",
                "ph_mismatch_rec": "درجة الحموضة الحالية {ph} قد تمنع امتصاص العناصر الغذائية لـ {crop_name}.",
                "weather_incomplete": "بيانات الطقس غير مكتملة.",
                "weather_summary": "حالياً {temp} درجة مئوية و {condition}.",
                "condition_clear": "صافٍ",
                "condition_rainy": "ممطر",
                "syncing_alerts": "جاري مزامنة نظام الطقس: لا توجد تنبيهات حرجة نشطة حالياً."
            }
        }

    def _t(self, key, lang="en", **kwargs):
        """Helper to get translated strings"""
        lang = lang if (lang and lang in self.translations) else "en"
        text = self.translations[lang].get(key, self.translations["en"].get(key, key))
        return text.format(**kwargs)

    def analyze_weather(self, weather_data: dict, monitoring_data: dict = None, lang: str = "en"):
        """
        Analyzes meteorological and sensor data to provide farming alerts and recommendations.
        """
        alerts = []
        recommendations = []

        temp = weather_data.get("temperature")
        humidity = weather_data.get("humidity")
        rain = weather_data.get("rain")

        # 1. Irrigation Logic
        if rain is not None and rain >= self.RAIN_THRESHOLD:
            recommendations.append(self._t("rain_detected", lang))
        elif rain is not None and rain > 0:
            recommendations.append(self._t("light_rain", lang))
        else:
            recommendations.append(self._t("standard_irrigation", lang))

        # 2. Heat Stress Logic
        if temp is not None and temp >= self.HEAT_THRESHOLD:
            alerts.append(self._t("heat_stress_critical", lang))
            recommendations.append(self._t("heat_stress_rec", lang))
        elif temp is not None and temp >= 30:
            alerts.append(self._t("moderate_heat", lang))
            recommendations.append(self._t("moderate_heat_rec", lang))

        # 3. Disease Risk Logic (Fungal/Mildew)
        if humidity is not None and humidity >= self.HUMIDITY_THRESHOLD:
            alerts.append(self._t("fungal_risk_critical", lang))
            recommendations.append(self._t("fungal_risk_rec", lang))
        elif humidity is not None and humidity >= 80:
            alerts.append(self._t("elevated_humidity", lang))
            recommendations.append(self._t("elevated_humidity_rec", lang))

        # 4. Integrated Soil Health Logic
        if monitoring_data:
            soil_moisture = monitoring_data.get("soil_moisture", 50)
            if soil_moisture > 75 and (rain or 0) > 0.5:
                alerts.append(self._t("waterlogging_critical", lang))
                recommendations.append(self._t("waterlogging_rec", lang))
            elif soil_moisture < 25:
                alerts.append(self._t("low_moisture_advisory", lang))
                recommendations.append(self._t("low_moisture_rec", lang))

        return {
            "alerts": alerts,
            "recommendations": recommendations,
            "summary": self._generate_summary(temp, rain, lang)
        }

    def generate_smart_alerts(self, weather_data: dict, crop_name: str = "", current_stage: str = "", monitoring_data: dict = None, lang: str = "en"):
        """
        Generates crop-aware alerts based on weather, growth stage, and sensor data.
        """
        analysis = self.analyze_weather(weather_data, monitoring_data, lang)
        smart_alerts = []
        
        temp = weather_data.get("temperature", 0)
        humidity = weather_data.get("humidity", 0)
        rain = weather_data.get("rain", 0)
        
        stage_lower = current_stage.lower()

        # 1. Heat Alerts (Stage Aware)
        if temp >= self.HEAT_THRESHOLD:
            msg = self._t("heat_risk_crop", lang, crop_name=crop_name)
            rec = self._t("heat_stress_rec", lang)
            if "flowering" in stage_lower:
                msg = self._t("heat_risk_flowering", lang)
                rec = self._t("blossom_drop", lang, crop_name=crop_name, temp=temp)
            smart_alerts.append({"type": "heat", "message": msg, "recommendation": rec})
        
        # 2. Rain Alerts (Stage Aware)
        if rain >= self.RAIN_THRESHOLD:
            msg = self._t("heavy_rain_crop", lang, crop_name=crop_name)
            rec = self._t("heavy_rain_rec", lang)
            if "seedling" in stage_lower:
                msg = self._t("heavy_rain_seedling", lang)
                rec = self._t("seedling_physical_damage", lang, crop_name=crop_name)
            smart_alerts.append({"type": "rain", "message": msg, "recommendation": rec})
            
        # 3. Disease Risk alerts
        if humidity >= self.HUMIDITY_THRESHOLD:
            msg = self._t("extreme_moisture", lang, crop_name=crop_name)
            rec = self._t("extreme_moisture_rec", lang)
            if "growth" in stage_lower or "fruit" in stage_lower:
                msg = self._t("high_disease_risk", lang)
                rec = self._t("disease_moisture_rec", lang, humidity=humidity, crop_name=crop_name)
            smart_alerts.append({"type": "disease_risk", "message": msg, "recommendation": rec})

        # 4. Soil pH and Moisture Alerts
        if monitoring_data:
            soil_moiture = monitoring_data.get("soil_moisture", 50)
            ph = monitoring_data.get("ph", 7.0)
            
            if soil_moiture > 80:
                smart_alerts.append({
                    "type": "waterlogging_risk", 
                    "message": self._t("field_saturation", lang), 
                    "recommendation": self._t("field_saturation_rec", lang)
                })
            
            if ph < 5.5 or ph > 7.5:
                smart_alerts.append({
                    "type": "ph_mismatch",
                    "message": self._t("ph_mismatch", lang),
                    "recommendation": self._t("ph_mismatch_rec", lang, ph=ph, crop_name=crop_name or "crops")
                })

        return smart_alerts

    def _generate_summary(self, temp, rain, lang="en"):
        if temp is None: return self._t("weather_incomplete", lang)
        condition = self._t("condition_clear", lang) if (rain or 0) == 0 else self._t("condition_rainy", lang)
        return self._t("weather_summary", lang, temp=temp, condition=condition)
# Class exported for on-demand initialization

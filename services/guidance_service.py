from services.gemini_service import GeminiService
from services.tracking_service import tracking_service
from services.agronomy_engine import CROP_PLANS
from utils.logger import logger

class GuidanceService:
    def __init__(self):
        self.ai = GeminiService()

    async def get_daily_guidance(self, journey_id: str):
        """
        Generates personalized AI guidance based on the current progress and expert data.
        """
        # 1. Get journey status
        progress = tracking_service.get_progress(journey_id)
        if "error" in progress:
            return {"error": progress["error"]}

        crop_name = progress["crop"]
        current_day = progress["day"]
        current_stage_name = progress["stage"]

        # 2. Get Expert Data
        if crop_name not in CROP_PLANS:
            return {"error": f"Expert data for {crop_name} not available"}

        plan = CROP_PLANS[crop_name]
        stage_data = next((s for s in plan["stages"] if s["name"] == current_stage_name), None)
        
        if not stage_data:
            return {"error": "Stage data mapping error"}

        # 3. Construct Prompt
        prompt = f"""
        Provide professional agricultural guidance for a farmer growing {crop_name}.
        
        Current Status:
        - Day: {current_day}
        - Growth Stage: {current_stage_name}
        
        Expert Requirements for this stage:
        - Tasks: {', '.join(stage_data['tasks'])}
        - Irrigation: {stage_data['irrigation']}
        - Fertilization: {stage_data['fertilizer']}
        - Monitoring: {stage_data['monitoring']}
        
        Instructions:
        1. Start the response with "Today you should...".
        2. Combine the tasks, irrigation, fertilization, and monitoring advice into a natural, encouraging, and concise summary.
        3. Maintain an expert agronomist tone.
        4. Focus on what is most important for Day {current_day}.
        5. Keep it under 100 words.
        """

        # 4. Generate AI Message
        guidance_text = await self.ai.generate(prompt)
        
        return {
            "journey_id": journey_id,
            "crop": crop_name,
            "day": current_day,
            "stage": current_stage_name,
            "guidance": guidance_text
        }

guidance_service = GuidanceService()

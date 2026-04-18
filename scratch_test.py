import asyncio
from services.ai_agronomist import ai_agronomist

async def test():
    context = {
        "crop_name": "Tomatoes",
        "current_stage": "Flowering",
        "soil": "Clay",
        "monitoring_data": {"soil_moisture": 25, "ph": 5.5}
    }
    msg = "My tomatoes are looking a bit sad today, what should I do?"
    res = await ai_agronomist.generate_advanced_chat(context, msg)
    print("AI Response:", res)

asyncio.run(test())

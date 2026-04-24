"""
Crops Data Module
Provides a structured agronomic knowledge base for environmental assessment.
"""

CROPS = {
    "tomato": {
        "name": "Tomato",
        "ph_range": [6.0, 7.0],
        "temp_range": [20.0, 30.0],
        "humidity_range": [60.0, 80.0],
        "moisture_range": [50.0, 70.0],
        "nitrogen_range": [100.0, 150.0],
        "phosphorus_range": [30.0, 50.0],
        "potassium_range": [40.0, 60.0]
    },
    "potato": {
        "name": "Potato",
        "ph_range": [5.5, 6.5],
        "temp_range": [15.0, 20.0],
        "humidity_range": [70.0, 90.0],
        "moisture_range": [60.0, 80.0],
        "nitrogen_range": [120.0, 180.0],
        "phosphorus_range": [40.0, 60.0],
        "potassium_range": [50.0, 80.0]
    },
    "wheat": {
        "name": "Wheat",
        "ph_range": [6.0, 7.5],
        "temp_range": [10.0, 25.0],
        "humidity_range": [40.0, 60.0],
        "moisture_range": [30.0, 60.0],
        "nitrogen_range": [80.0, 140.0],
        "phosphorus_range": [30.0, 50.0],
        "potassium_range": [30.0, 50.0]
    },
    "corn": {
        "name": "Corn",
        "ph_range": [6.0, 7.0],
        "temp_range": [20.0, 35.0],
        "humidity_range": [50.0, 80.0],
        "moisture_range": [50.0, 80.0],
        "nitrogen_range": [150.0, 250.0],
        "phosphorus_range": [50.0, 80.0],
        "potassium_range": [60.0, 90.0]
    },
    "carrot": {
        "name": "Carrot",
        "ph_range": [6.0, 6.8],
        "temp_range": [15.0, 22.0],
        "humidity_range": [60.0, 80.0],
        "moisture_range": [60.0, 80.0],
        "nitrogen_range": [60.0, 100.0],
        "phosphorus_range": [30.0, 50.0],
        "potassium_range": [30.0, 50.0]
    },
    "onion": {
        "name": "Onion",
        "ph_range": [6.0, 7.5],
        "temp_range": [13.0, 24.0],
        "humidity_range": [60.0, 70.0],
        "moisture_range": [50.0, 75.0],
        "nitrogen_range": [80.0, 130.0],
        "phosphorus_range": [35.0, 55.0],
        "potassium_range": [35.0, 55.0]
    },
    "pepper": {
        "name": "Pepper",
        "ph_range": [6.0, 7.0],
        "temp_range": [20.0, 30.0],
        "humidity_range": [60.0, 80.0],
        "moisture_range": [55.0, 75.0],
        "nitrogen_range": [100.0, 160.0],
        "phosphorus_range": [30.0, 50.0],
        "potassium_range": [30.0, 50.0]
    },
    "lettuce": {
        "name": "Lettuce",
        "ph_range": [6.0, 7.0],
        "temp_range": [7.0, 20.0],
        "humidity_range": [60.0, 85.0],
        "moisture_range": [65.0, 85.0],
        "nitrogen_range": [50.0, 90.0],
        "phosphorus_range": [25.0, 45.0],
        "potassium_range": [25.0, 45.0]
    }
}

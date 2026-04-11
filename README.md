# Crop Recommendation Backend API

This is a FastAPI-based backend utilizing OpenAI to generate crop recommendations based on soil and weather data tailored for North Africa and Algeria.

## Setup Instructions

1. **Install dependencies:**
   Make sure you have Python 3.8+ installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   You must set your `OPENAI_API_KEY`. You can export it or create a `.env` file in this directory:
   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

3. **Run the Server:**
   Start the FastAPI development server using Uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Usage

**Endpoint:** `POST /predict`
**Content-Type:** `application/json`

**Example Request payload:**
```json
{
  "nitrogen": 90,
  "phosphorus": 42,
  "potassium": 43,
  "temperature": 20.87,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}
```

**Example Response:**
```json
{
  "crop": "rice",
  "explanation": "Rice requires high humidity and significant rainfall, which perfectly matches these parameters. A slightly acidic to neutral pH combined with rich nitrogen is ideal for optimal yield."
}
```
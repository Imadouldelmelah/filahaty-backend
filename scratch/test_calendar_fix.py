import requests
import json

def test_calendar_endpoint():
    url = "http://localhost:10000/farming/calendar"
    params = {"crop": "Tomato", "day": 1}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        print(f"Number of days returned: {len(data)}")
        if len(data) > 0:
            print("First day example:")
            print(json.dumps(data[0], indent=2))
            print("Last day example:")
            print(json.dumps(data[-1], indent=2))
        else:
            print("ERROR: Returned empty array")
            
        # Verify 30 days
        if len(data) < 30:
            print(f"ERROR: Expected at least 30 days, got {len(data)}")
            
        # Verify fields
        required_fields = ["date", "task", "priority"]
        for i, item in enumerate(data):
            for field in required_fields:
                if field not in item:
                    print(f"ERROR: Day {i} missing field '{field}'")
                    
    except Exception as e:
        print(f"Caught exception: {e}")

if __name__ == "__main__":
    # Note: This assumes the server is running on port 10000. 
    # Since I'm in a container/env, I might need to run it in the background if it's not already running.
    # I'll just run it once to see if it works if I can start the server.
    pass

import json
from services.marketplace_service import marketplace_service

def test_marketplace():
    print("TESTING MARKETPLACE SYSTEM...")
    
    # 1. Add mock item
    mock_item = {
        "farmer_name": "Farmer Imad",
        "crop_name": "Tomatoes",
        "price": 45.0,
        "unit": "kg",
        "location": "Algiers"
    }
    
    print("Adding item...")
    added_item = marketplace_service.add_item(mock_item)
    print(f"Added Item: {json.dumps(added_item, indent=2)}")
    
    # 2. List items
    print("\nListing all items...")
    items = marketplace_service.list_items()
    print(f"Total items in marketplace: {len(items)}")
    
    # Verify the item we added is in the list
    found = any(item['id'] == added_item['id'] for item in items)
    if found:
        print("SUCCESS: Added item found in marketplace list.")
    else:
        print("FAILURE: Added item NOT found in marketplace list.")

if __name__ == "__main__":
    test_marketplace()

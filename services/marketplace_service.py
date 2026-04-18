import json
import os
import uuid
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "marketplace.json")

class MarketplaceService:
    def __init__(self):
        self._ensure_data_file()

    def _ensure_data_file(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump([], f)

    def _load_items(self):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def _save_items(self, items):
        with open(DATA_FILE, "w") as f:
            json.dump(items, f, indent=4)

    def add_item(self, item_data: dict):
        """
        Adds a new crop listing to the marketplace.
        """
        item_id = str(uuid.uuid4())
        items = self._load_items()
        
        new_item = {
            "id": item_id,
            "farmer_name": item_data["farmer_name"],
            "crop_name": item_data["crop_name"],
            "price": item_data["price"],
            "unit": item_data["unit"],
            "location": item_data["location"],
            "timestamp": datetime.now().isoformat()
        }
        
        items.append(new_item)
        self._save_items(items)
        return new_item

    def list_items(self):
        """
        Returns all active listings.
        """
        return self._load_items()
# Class exported for on-demand instantiation

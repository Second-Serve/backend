import json
import os
import uuid
from models.Restaurant import Restaurant

def read_from_file(file_path: str, default_data=None):
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return default_data or {}

def save_to_file(data, file_path: str):
    with open(file_path, "w") as f:
        json.dump(data, f)

class Database:
    def __init__(self, restaurant_file="restaurants.json"):
        self.restaurant_file = restaurant_file
        self.restaurants = read_from_file(restaurant_file, {})

    def get_all_restaurants(self):
        return [Restaurant(**data) for data in self.restaurants.values()]

    def get_restaurant_by_id(self, restaurant_id: str):
        if restaurant_id in self.restaurants:
            return Restaurant(**self.restaurants[restaurant_id])
        raise ValueError("No restaurant with that ID")

    def add_restaurant(self, restaurant_data: dict):
        restaurant_id = str(uuid.uuid4())
        self.restaurants[restaurant_id] = {**restaurant_data, "id": restaurant_id}
        save_to_file(self.restaurants, self.restaurant_file)
        return Restaurant(**self.restaurants[restaurant_id])

    def delete_restaurant(self, restaurant_id: str):
        if restaurant_id in self.restaurants:
            del self.restaurants[restaurant_id]
            save_to_file(self.restaurants, self.restaurant_file)
        else:
            raise ValueError("No restaurant with that ID")
from fastapi import APIRouter, HTTPException
from models.Restaurant import Restaurant
from db import Database


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    responses={404: {"description": "Not found"}},
)

db = Database()

@router.get("/")
async def list_restaurants():
    return {"restaurants": [restaurant.dict() for restaurant in db.get_all_restaurants()]}

@router.get("/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    try:
        restaurant = db.get_restaurant_by_id(restaurant_id)
        return restaurant.dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
async def create_restaurant(restaurant: Restaurant):
    new_restaurant = db.add_restaurant(restaurant.dict())
    return new_restaurant.dict()

@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: str):
    try:
        db.delete_restaurant(restaurant_id)
        return {"status": "Restaurant deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
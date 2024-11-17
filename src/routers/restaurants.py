import db

from fastapi import APIRouter, HTTPException

from models.restaurant import Restaurant

from util.api import APIResponseClass


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_class=APIResponseClass)
async def list_restaurants():
    return {"restaurants": [restaurant.dict() for restaurant in db.get_all_restaurants()]}


@router.get("/{restaurant_id}", response_class=APIResponseClass)
async def get_restaurant(restaurant_id: str):
    try:
        restaurant = db.get_restaurant_by_id(restaurant_id)
        return restaurant.dict()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_class=APIResponseClass)
async def create_restaurant(restaurant: Restaurant):
    new_restaurant = db.create_restaurant(restaurant.dict())
    return new_restaurant.dict()


@router.delete("/{restaurant_id}", response_class=APIResponseClass)
async def delete_restaurant(restaurant_id: str):
    try:
        db.delete_restaurant(restaurant_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
import db

from fastapi import APIRouter, Depends, HTTPException

from models.restaurant import Restaurant, RestaurantRegistrationInfo

from util.api import APIResponseClass, bearer_is_admin, oauth2_scheme


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    responses={404: {"description": "Not found"}},
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


@router.put("/{restaurant_id}", response_class=APIResponseClass)
async def update_restaurant(restaurant_id: str, restaurant: RestaurantRegistrationInfo, token: Annotated[str, Depends(oauth2_scheme)]):
    if bearer_is_admin(token):
        try:
            updated_restaurant = db.update_restaurant(restaurant_id, restaurant)
            return updated_restaurant.dict()
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(status_code=403, detail="User is not an admin")


@router.put("/me", response_class=APIResponseClass)
async def update_my_restaurant(restaurant: RestaurantRegistrationInfo, token: Annotated[str, Depends(oauth2_scheme)]):
    user = db.verify_bearer(token)
    updated_restaurant = db.update_restaurant(user.restaurant.id, restaurant)
    return updated_restaurant.dict()
import db
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile

from models.restaurant import Restaurant, RestaurantRegistrationInfo

from util.api import APIResponseClass, bearer_is_admin, oauth2_scheme


router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=APIResponseClass)
async def list_restaurants(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    if db.verify_bearer(token) is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    return {"restaurants": [restaurant.dict() for restaurant in db.get_all_restaurants()]}


@router.get("/{restaurant_id}", response_class=APIResponseClass)
async def get_restaurant(restaurant_id: str, token: Annotated[str, Depends(oauth2_scheme)]) -> Restaurant:
    if db.verify_bearer(token) is None:
        raise HTTPException(status_code=400, detail="Invalid token")

    try:
        restaurant = db.get_restaurant_by_id(restaurant_id)
        return restaurant
    except ValueError as e:
        # ValueError means the restaurant was not found
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{restaurant_id}", response_class=APIResponseClass)
async def delete_restaurant(restaurant_id: str, token: Annotated[str, Depends(oauth2_scheme)]):
    if bearer_is_admin(token):
        try:
            db.delete_restaurant(restaurant_id)
        except ValueError as e:
            # ValueError means the restaurant was not found
            raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(status_code=403, detail="User is not an admin")


@router.put("/{restaurant_id}", response_class=APIResponseClass)
async def update_restaurant(restaurant_id: str, restaurant: RestaurantRegistrationInfo, token: Annotated[str, Depends(oauth2_scheme)]):
    if bearer_is_admin(token):
        try:
            updated_restaurant = db.update_restaurant(restaurant_id, restaurant)
            return updated_restaurant.dict()
        except ValueError as e:
            # ValueError means the restaurant was not found
            raise HTTPException(status_code=404, detail=str(e))
    else:
        raise HTTPException(status_code=403, detail="User is not an admin")


@router.put("/me", response_class=APIResponseClass)
async def update_my_restaurant(restaurant: RestaurantRegistrationInfo, token: Annotated[str, Depends(oauth2_scheme)]):
    user = db.verify_bearer(token)

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    if user.restaurant is None:
        raise HTTPException(status_code=404, detail="User does not have a restaurant")

    try:
        updated_restaurant = db.update_restaurant(user.restaurant.id, restaurant)
        return updated_restaurant.dict()
    except ValueError as e:
        # ValueError means the restaurant was not found
        raise HTTPException(status_code=404, detail=str(e))


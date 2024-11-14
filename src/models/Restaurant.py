from pydantic import BaseModel
from typing import List, Optional

class Restaurant(BaseModel):
    id: str
    name: str
    address: str
    pickup_hours: str
    menu_items: Optional[List[str]] = []
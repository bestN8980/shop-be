from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies.database import get_db
from dependencies.auth import get_current_user

from modules.orders import service, schema
from modules.orders.schema import OrderCreate
from modules.users.model import User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/")
def create_order_route(
    data: OrderCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return service.create_order(db, user.id, data.items)


@router.get("/")
def get_my_orders(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return service.get_orders(db, user.id)  
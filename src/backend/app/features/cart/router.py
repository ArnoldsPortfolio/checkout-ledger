from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.cart.service import CartService
router = APIRouter(prefix="/cart", tags=["cart"])
class LineBody(BaseModel):
    product_id: str
    qty: int = Field(ge=1, le=99)
class QtyBody(BaseModel):
    product_id: str
    qty: int = Field(ge=0, le=99)
@router.get("")
def view_cart(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return CartService(db).view(user_id)
@router.post("/add")
def add_line(body: LineBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return CartService(db).add(user_id, body.product_id, body.qty)
@router.post("/qty")
def set_qty(body: QtyBody, user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return CartService(db).set_qty(user_id, body.product_id, body.qty)

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.checkout.service import CheckoutService
from app.kernel.ids import new_id
router = APIRouter(prefix="/orders", tags=["checkout"])
@router.get("")
def list_orders(user_id: str = Depends(get_user_id), db: Session = Depends(get_db)):
    return CheckoutService(db).list_orders(user_id)
@router.post("")
def place_order(user_id: str = Depends(get_user_id), db: Session = Depends(get_db), idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    return CheckoutService(db).place(user_id, idempotency_key or new_id())

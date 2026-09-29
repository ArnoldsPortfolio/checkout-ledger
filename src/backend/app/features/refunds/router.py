from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.deps import get_db, get_user_id
from app.features.checkout.service import CheckoutService
from app.features.refunds.service import RefundService
from app.kernel.ids import new_id
router = APIRouter(prefix="/orders", tags=["refunds"])
@router.post("/{order_id}/refund")
def refund_order(order_id: str, user_id: str = Depends(get_user_id), db: Session = Depends(get_db), idempotency_key: str | None = Header(default=None, alias="Idempotency-Key")):
    order = CheckoutService(db).get(user_id, order_id)
    return RefundService(db).issue(order, idempotency_key or new_id())

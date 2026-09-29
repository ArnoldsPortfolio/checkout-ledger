from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.inventory.service import InventoryService
from app.kernel.errors import Conflict
from app.kernel.ids import new_id
from app.models import OrderLineRow, OrderRow, RefundRow
class RefundService:
    def __init__(self, db: Session):
        self.db = db
    def issue(self, order: OrderRow, key: str) -> dict:
        existing = self.db.scalar(select(RefundRow).where(RefundRow.idempotency_key == key))
        if existing:
            return {"id": existing.id, "cents": existing.cents, "order_id": existing.order_id}
        if order.status == "refunded":
            raise Conflict("Already refunded")
        stock = InventoryService(self.db)
        for line in self.db.scalars(select(OrderLineRow).where(OrderLineRow.order_id == order.id)):
            stock.restock(line.product_id, line.qty)
        refund = RefundRow(id=new_id(), order_id=order.id, cents=order.total_cents, idempotency_key=key)
        order.status = "refunded"
        self.db.add(refund)
        self.db.commit()
        return {"id": refund.id, "cents": refund.cents, "order_id": order.id}

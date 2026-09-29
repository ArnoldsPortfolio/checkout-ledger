from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.cart.service import CartService
from app.features.inventory.service import InventoryService
from app.kernel.errors import Conflict, NotFound
from app.kernel.ids import new_id
from app.models import HoldRow, OrderLineRow, OrderRow
class CheckoutService:
    def __init__(self, db: Session):
        self.db = db
    def place(self, owner_id: str, key: str) -> dict:
        existing = self.db.scalar(select(OrderRow).where(OrderRow.idempotency_key == key))
        if existing:
            return self._out(existing)
        cart = CartService(self.db).view(owner_id)
        if not cart["items"]:
            raise Conflict("Cart empty")
        order = OrderRow(id=new_id(), owner_id=owner_id, total_cents=cart["total_cents"], idempotency_key=key, status="placed")
        stock = InventoryService(self.db)
        self.db.add(order)
        for item in cart["items"]:
            stock.reserve(order.id, item["id"], item["qty"])
            self.db.add(OrderLineRow(id=new_id(), order_id=order.id, product_id=item["id"], title=item["title"], qty=item["qty"], unit_cents=item["price_cents"]))
        order.status = "paid"
        for hold in self.db.scalars(select(HoldRow).where(HoldRow.order_id == order.id)):
            stock.commit(hold)
        CartService(self.db).clear(owner_id)
        self.db.commit()
        return self._out(order)
    def list_orders(self, owner_id: str) -> list[dict]:
        return [self._out(o) for o in self.db.scalars(select(OrderRow).where(OrderRow.owner_id == owner_id))]
    def get(self, owner_id: str, order_id: str) -> OrderRow:
        order = self.db.get(OrderRow, order_id)
        if not order or order.owner_id != owner_id:
            raise NotFound("Order not found")
        return order
    def _out(self, order: OrderRow) -> dict:
        lines = list(self.db.scalars(select(OrderLineRow).where(OrderLineRow.order_id == order.id)))
        return {"id": order.id, "status": order.status, "total_cents": order.total_cents, "lines": [{"title": l.title, "qty": l.qty, "unit_cents": l.unit_cents} for l in lines]}

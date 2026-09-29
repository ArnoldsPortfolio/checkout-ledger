from sqlalchemy.orm import Session
from app.kernel.errors import Conflict, NotFound
from app.kernel.ids import new_id
from app.models import HoldRow, ProductRow
class InventoryService:
    def __init__(self, db: Session):
        self.db = db
    def reserve(self, order_id: str, product_id: str, qty: int) -> HoldRow:
        product = self._product(product_id)
        if product.on_hand - product.reserved < qty:
            raise Conflict("Not enough stock")
        product.reserved += qty
        hold = HoldRow(id=new_id(), order_id=order_id, product_id=product_id, qty=qty, state="held")
        self.db.add(hold)
        return hold
    def commit(self, hold: HoldRow) -> None:
        product = self._product(hold.product_id)
        product.reserved -= hold.qty
        product.on_hand -= hold.qty
        hold.state = "committed"
    def release(self, hold: HoldRow) -> None:
        product = self._product(hold.product_id)
        product.reserved -= hold.qty
        hold.state = "released"
    def restock(self, product_id: str, qty: int) -> None:
        self._product(product_id).on_hand += qty
    def _product(self, product_id: str) -> ProductRow:
        product = self.db.get(ProductRow, product_id)
        if not product:
            raise NotFound("Product not found")
        return product

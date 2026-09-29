from sqlalchemy import select
from sqlalchemy.orm import Session
from app.features.catalog.service import _out
from app.kernel.errors import Conflict, NotFound
from app.kernel.ids import new_id
from app.models import CartLineRow, ProductRow
class CartService:
    def __init__(self, db: Session):
        self.db = db
    def view(self, owner_id: str) -> dict:
        lines = list(self.db.scalars(select(CartLineRow).where(CartLineRow.owner_id == owner_id)))
        items = [self._line(row) for row in lines]
        return {"items": items, "total_cents": sum(i["line_cents"] for i in items)}
    def add(self, owner_id: str, product_id: str, qty: int) -> dict:
        product = self.db.get(ProductRow, product_id)
        if not product:
            raise NotFound("Product not found")
        row = self.db.scalar(select(CartLineRow).where(CartLineRow.owner_id == owner_id, CartLineRow.product_id == product_id))
        if row:
            row.qty += qty
        else:
            self.db.add(CartLineRow(id=new_id(), owner_id=owner_id, product_id=product_id, qty=qty))
        self.db.commit()
        return self.view(owner_id)
    def set_qty(self, owner_id: str, product_id: str, qty: int) -> dict:
        row = self.db.scalar(select(CartLineRow).where(CartLineRow.owner_id == owner_id, CartLineRow.product_id == product_id))
        if not row:
            raise NotFound("Line not in cart")
        if qty <= 0:
            self.db.delete(row)
        else:
            row.qty = qty
        self.db.commit()
        return self.view(owner_id)
    def clear(self, owner_id: str) -> None:
        for row in self.db.scalars(select(CartLineRow).where(CartLineRow.owner_id == owner_id)):
            self.db.delete(row)
        self.db.commit()
    def _line(self, row: CartLineRow) -> dict:
        product = self.db.get(ProductRow, row.product_id)
        if not product:
            raise Conflict("Missing product")
        return {**_out(product), "qty": row.qty, "line_cents": product.price_cents * row.qty}

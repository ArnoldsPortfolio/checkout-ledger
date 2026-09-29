from sqlalchemy import select
from sqlalchemy.orm import Session
from app.kernel.ids import new_id
from app.models import ProductRow
SEED = [("SKU-MUG", "Stone mug", 1800, 12), ("SKU-TOTE", "Canvas tote", 2400, 8), ("SKU-NOTE", "Ledger notebook", 1200, 20)]
class CatalogService:
    def __init__(self, db: Session):
        self.db = db
    def seed(self) -> None:
        if self.db.scalar(select(ProductRow.id)):
            return
        self.db.add_all([ProductRow(id=new_id(), sku=s, title=t, price_cents=p, on_hand=q) for s, t, p, q in SEED])
        self.db.commit()
    def list(self) -> list[dict]:
        self.seed()
        return [_out(p) for p in self.db.scalars(select(ProductRow))]
def _out(p: ProductRow) -> dict:
    available = max(0, p.on_hand - p.reserved)
    return {"id": p.id, "sku": p.sku, "title": p.title, "price_cents": p.price_cents, "on_hand": p.on_hand, "reserved": p.reserved, "available": available}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.features.catalog.service import CatalogService
router = APIRouter(prefix="/catalog", tags=["catalog"])
@router.get("")
def list_catalog(db: Session = Depends(get_db)):
    return CatalogService(db).list()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.db import Base
from app.deps import engine
from app.features.cart.router import router as cart_router
from app.features.catalog.router import router as catalog_router
from app.features.checkout.router import router as checkout_router
from app.features.identity.router import router as identity_router
from app.features.refunds.router import router as refunds_router
from app.kernel.errors import DomainError
app = FastAPI(title="Checkout Ledger API", version="0.1.0", redirect_slashes=False)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
@app.exception_handler(DomainError)
async def domain_error(_, exc: DomainError):
    return JSONResponse({"code": exc.code, "message": exc.message}, status_code=exc.status)
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
@app.get("/health")
def health():
    return {"status": "ok"}
app.include_router(identity_router)
app.include_router(catalog_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(refunds_router)

from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_secret: str = "checkout-ledger-dev"
    database_url: str = "sqlite:///./checkout_ledger.db"

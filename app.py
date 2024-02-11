from fastapi import FastAPI
from fastapi.openapi.models import Info, OpenAPI
from utils.security import SecurityAPI
from users.api.api import UsersAPI
from products.api.api import ProductsAPI

app = FastAPI(
    title="Shop Online",
    description="API para comprar productos online",
    version="1.0.0",
)

app.include_router(SecurityAPI.router, tags=["Login"])
app.include_router(UsersAPI.router, tags=["Users"])
app.include_router(ProductsAPI.router, tags=["Products"])
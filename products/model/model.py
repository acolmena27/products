# Para Modelos de datos que se usaran en la api de usuaros crear eliminar modificar etc
from pydantic import BaseModel

from typing import Optional, List

# Importamos uuid crea un id unico serializado
import uuid

# LIST USER
# ===============================================
# ===============================================
# Creamos el modelo de datos estos son los campos a mostrar en el json
class AllMyProducts(BaseModel):
    product_name: str 
    price: str
    shop: bool = True
    uuid: str = str(uuid.uuid4())
    
# SEARCH
# ===============================================
# ===============================================
# Creamos el modelo de datos estos son los campos a mostrar en el json
class MyProducts(BaseModel):
    username: str
    uuid: str
    first_name: str
    last_name: str
    email: str
    dni: str
    purchased_products: str

# INSERT
# ===============================================
# ===============================================
# Creamos el modelo de datos para agregar usuarios
class MyProductsAdd(BaseModel):
    product_name: str 
    price: str
    shop: bool = True
    uuid: str = str(uuid.uuid4())
    
# PURCHASED
# ===============================================
# ===============================================
# Creamos el modelo de datos para agregar usuarios
class MyPurchasedAdd(BaseModel):
    purchased_products: str 
    uuid: str = str(uuid.uuid4())
    
# ORDERS
# ===============================================
# ===============================================
# Creamos el modelo de datos para agregar usuarios
class MyOrderAdd(BaseModel):
    product_name: str
    order_uuid: str = str(uuid.uuid4())
    paid: bool
    user_uuid: str = str(uuid.uuid4())
    
# SEARCH ORDERS
# ===============================================
# ===============================================
class Order(BaseModel):
    product_name: str
    order_uuid: str
    paid: bool
    
class User(BaseModel):
    username: str
    uuid: str
    first_name: str
    last_name: str
    email: str
    dni: str
    orders: List[Order]
    
# UPDATE
# ===============================================
# ===============================================
# Modelo Pydantic para la respuesta de actualización de usuario
class MyUpdateItem(BaseModel):   
    product_name: Optional[str]
    price: Optional[str] 
    shop: Optional[bool] 
    uuid: Optional[str]

# Modelo Pydantic para la respuesta de actualización de usuario
class UpdateItemResponse(BaseModel):
    code: str
    status: str
    message: str

# DELETE
# ===============================================
# ===============================================
# Modelo Pydantic para eliminar usuario   
class DeleteItem(BaseModel):
    product_name: str
    

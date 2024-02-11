# Informacio: Esta api de users se divide en api, models, use_case, sql_statement y connection para separar y ordenar el codigo

# Importamos fastAPI
from fastapi import APIRouter, HTTPException, Body, Depends, Path, Query, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, List

from typing import Optional

# Variable para almacenar el token JWT
current_access_token: Optional[str] = None

from utils.security import token_security, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from users.service.service import UserCase
from products.service.service import ProductsCase
from products.model.model import User, MyProducts, MyProductsAdd, MyPurchasedAdd, MyOrderAdd, DeleteItem, UpdateItemResponse, MyUpdateItem
            
class ProductsAPI:
       
    # Declararamos la aplicacion con la variable app
    router = APIRouter()
    
    # ALL PRODUCTS
    # ===============================================
    # ===============================================
    # Router para listar todos los usuarios
    @router.get("/products/")
    async def list_products():
        
        token_security.token_validator()
        
        products = ProductsCase.get_all_products()
        return products
    
    # SEARCH
    # ===============================================
    # ===============================================
    # Ruta para buscar usuarios registrados en la api
    @router.get("/search_products", response_model=List[MyProducts])
    def product_shop(uuid: str):
        
        token_security.token_validator()
        
        products = ProductsCase.get_products_by_shop(uuid)
        return products

    # INSERT
    # ===============================================
    # ===============================================
    # Ruta para crear el usuario en la api o EndPoint
    @router.post("/register-products/", response_model=Dict[str, str])
    def register_products(products_data: MyProductsAdd):
        
        token_security.token_validator()
        
        try:
            # Llama a tu función `create_user` para insertar el usuario en la base de datos
            products = ProductsCase.create_product(products_data)

            return {
                "code": "200",
                "status": "OK",
                "message": "Registro creado exitosamente"
            }
            
        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir al registrar al usuario
            raise HTTPException(status_code=500, detail=str(e))
    
    # PURCHASED
    # ===============================================
    # ===============================================
    # Ruta para crear el usuario en la api o EndPoint
    @router.post("/register-purchased/", response_model=Dict[str, str])
    def register_purchased(products_data: MyPurchasedAdd):
        
        token_security.token_validator()
        
        try:
            # Llama a tu función `create_user` para insertar el usuario en la base de datos
            products = ProductsCase.create_purchased(products_data)

            return {
                "code": "200",
                "status": "OK",
                "message": "Registro creado exitosamente"
            }
            
        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir al registrar al usuario
            raise HTTPException(status_code=500, detail=str(e))
    
    # ORDERS
    # ===============================================
    # ===============================================
    # Ruta para crear el usuario en la api o EndPoint
    @router.post("/register-orders/", response_model=Dict[str, str])
    def register_orders(order_data: MyOrderAdd):
        
        token_security.token_validator()
        
        try:
            # Llama a tu función `create_user` para insertar el usuario en la base de datos
            order = ProductsCase.create_order(order_data)

            return {
                "code": "200",
                "status": "OK",
                "message": "Registro creado exitosamente"
            }
            
        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir al registrar al usuario
            raise HTTPException(status_code=500, detail=str(e))
        
    # SEARCH ORDERS
    # ===============================================
    # ===============================================
    # Ruta para buscar usuarios registrados en la api
    @router.get("/search_orders", response_model=User)
    def search_orders(uuid: str):
        
        token_security.token_validator()
        
        orders = ProductsCase.get_orders_by_user(uuid)
        return orders

    # UPDATE
    # ===============================================
    # ===============================================
    # Ruta para actualizar usuario en la api o EndPoint
    @router.put("/update-item/", response_model=UpdateItemResponse)
    def update_item(uuid: str, item_data: MyUpdateItem):
        
        token_security.token_validator()
        
        try:
            # Valida el dni del usuario
            if not uuid:
                raise HTTPException(status_code=400, detail="DNI is required")
            else: 
                # Llama a la función `my_update_user` para actualizar el usuario en la base de datos
                ProductsCase.my_update_item(uuid, item_data)

                # Crea una instancia de UpdateUserResponse con la información actualizada del usuario
                item_info = item_data.dict()
                item_info['uuid'] = uuid
                
                response_data = UpdateItemResponse(
                    code="200",
                    status="OK",
                    message="Registro actualizado exitosamente",
                    item=item_info
                )

                return response_data
            
        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir al actualizar al usuario
            raise HTTPException(status_code=500, detail=str(e))
    
    # DELETE
    # ===============================================
    # ===============================================
    # Ruta para crear el usuario en la api o EndPoint
    @router.delete("/delete-item/", response_model=Dict[str, str])
    def del_item(del_data: DeleteItem):
        
        token_security.token_validator()
        
        try:
            # Llama a tu función `del_user` para insertar el usuario en la base de datos
            item = ProductsCase.del_item(del_data)

            if item:
                return {
                    "code": "200",
                    "status": "OK",
                    "message": "Registro eliminado exitosamente"
                }
            else:
                return {
                "code": "404",
                "status": "Not Found",
                "message": "Item no encontrado"
                }
                
        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir al registrar al usuario
            raise HTTPException(status_code=500, detail=str(e))
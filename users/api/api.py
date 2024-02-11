# Informacio: Esta api de users se divide en api, models, use_case, sql_statement y connection para separar y ordenar el codigo

# Importamos fastAPI
from fastapi import APIRouter, HTTPException, Body, Depends, Path, Query, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, List
from datetime import datetime, timedelta

from typing import Optional

# Variable para almacenar el token JWT
current_access_token: Optional[str] = None

from utils.security import token_security, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from users.service.service import UserCase
from users.model.model import UserLogin, MyUser, MyUserAdd
            
class UsersAPI:
       
    # Declararamos la aplicacion con la variable app
    router = APIRouter()
    
    # ALL USER
    # ===============================================
    # ===============================================
    # Router para listar todos los usuarios
    @router.get("/users/")
    async def list_users():
        
        token_security.token_validator()
        
        users = UserCase.get_all_users()
        return users
    
    # ALL USER PURCHASED
    # ===============================================
    # ===============================================
    # Router para listar todos los usuarios
    @router.get("/users-purchased/")
    async def list_users_purchased():
        
        token_security.token_validator()
        
        users_purchased = UserCase.get_all_users_purchased()
        return users_purchased
    
    # SEARCH
    # ===============================================
    # ===============================================
    # Ruta para buscar usuarios registrados en la api
    @router.get("/search_user", response_model=List[MyUser])
    def user_dni(shop: bool):
        
        token_security.token_validator()
        
        user = UserCase.get_user_by_shop(shop)
        return user

    # INSERT
    # ===============================================
    # ===============================================
    # Ruta para crear el usuario en la api o EndPoint
    @router.post("/register-user/", response_model=Dict[str, str])
    def register_user(user_data: MyUserAdd):
        
        # token_security.token_validator()
        
        try:
            # Llama a tu función `create_user` para insertar el usuario en la base de datos
            user = UserCase.create_user(user_data)

            return {
                "code": "200",
                "status": "OK",
                "message": "Registro creado exitosamente"
            }
            
        except Exception as e:
            # Maneja cualquier excepción que pueda ocurrir al registrar al usuario
            raise HTTPException(status_code=500, detail=str(e))
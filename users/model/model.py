# Para Modelos de datos que se usaran en la api de usuaros crear eliminar modificar etc
from pydantic import BaseModel

from typing import Optional

# Importamos uuid crea un id unico serializado
import uuid

# Para trabajar conn fechas
from datetime import date, datetime

# TOKEN SECURE
# ===============================================
# ===============================================
# Modelo para ingresar usuario y contraseña
class UserLogin(BaseModel):
    username: str
    password: str

# LIST USER
# ===============================================
# ===============================================
# Creamos el modelo de datos estos son los campos a mostrar en el json
class AllMyUser(BaseModel):
    username: str 
    password: str
    uuid: str = str(uuid.uuid4())
    shop: bool
    first_name: str
    last_name: str
    email: str
    dni: str
    
# SEARCH
# ===============================================
# ===============================================
# Creamos el modelo de datos estos son los campos a mostrar en el json
class MyUser(BaseModel):
    username: str 
    password: str
    uuid: str = str
    shop: bool
    first_name: str
    last_name: str
    email: str
    dni: str

# INSERT
# ===============================================
# ===============================================
# Creamos el modelo de datos para agregar usuarios
class MyUserAdd(BaseModel):
    username: str 
    password: str
    uuid: str = str(uuid.uuid4())
    shop: bool = False
    first_name: str
    last_name: str
    email: str
    dni: str
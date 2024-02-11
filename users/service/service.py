# Casos de uso que se utilizaran segun la operacion a realizar buscar agregar actualizar o eliminar usuarios
import jwt
from fastapi import HTTPException, status, Depends
from sqlalchemy import text

from utils.connection.conn import engine, SessionLocal
from users.model.model import MyUser, MyUserAdd
from datetime import datetime, timedelta

# Encriptar contraseñas
from passlib.hash import argon2
from passlib.context import CryptContext

# Importamos la sentencia sql para usuarios
from users.statement.sql_statement import ALL_USER, ALL_USER_PURCHASED, SEARCH_USER, CREATE_USER

# Configuramos el contexto de hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class UserCase:
    def __init__(self):
        pass
    
    # ALL USER
    # ===============================================
    # ===============================================
    def get_all_users():
        with SessionLocal() as session:
            # Ejecuta la consulta SQL
            query = text(ALL_USER)
            result = session.execute(query)
            
            users = result.fetchall()
            
            # Convierte los resultados en una lista de diccionarios
            user_list = []
            
            for user in users:
                user_dict = {
                    "username": user[0], 
                    "password": user[1],
                    "uuid": user[2],
                    "shop": user[3],
                    "first_name": user[4], 
                    "last_name": user[5], 
                    "email": user[6], 
                    "dni": user[7]
                }
                user_list.append(user_dict)

            return user_list
    
    # ALL USER PURCHASED
    # ===============================================
    # ===============================================
    def get_all_users_purchased():
        with SessionLocal() as session:
            # Ejecuta la consulta SQL
            query = text(ALL_USER_PURCHASED)
            result = session.execute(query)
            
            users_purchased = result.fetchall()
            
            # Convierte los resultados en una lista de diccionarios
            user_purchased_list = []
            
            for user in users_purchased:
                user_purchased_dict = {
                    "username": user[0], 
                    "password": user[1],
                    "uuid": user[2],
                    "shop": user[3],
                    "first_name": user[4], 
                    "last_name": user[5], 
                    "email": user[6], 
                    "dni": user[7]
                }
                user_purchased_list.append(user_purchased_dict)

            return user_purchased_list
    
    # SEARCH
    # ===============================================
    # ===============================================
    # Declaramos la función para consultar usuarios
    def get_user_by_shop(shop: bool):
        # Abre una sesión de base de datos
        with SessionLocal() as session:
            # Ejecuta la consulta SQL
            query = text(SEARCH_USER)
            result = session.execute(query, {"shop": shop})
            
            # Devuelve el usuario
            user = result.fetchall()
            if user is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return user

    # INSERT
    # ===============================================
    # ===============================================
    # Declaramos el caso de uso que sera un insert
    def create_user(data: MyUserAdd):
        # Convierte el objeto MyUserAdd en un diccionario
        user_data = dict(data)
        
        # Configura el contexto de Passlib con Argon2
        pwd_context = CryptContext(schemes=["argon2"])

        hashed_password = pwd_context.hash(data.password)
        
        # Agrega el hash de la contraseña a los datos del usuario
        user_data['password'] = hashed_password

        # Abre una sesión de base de datos
        with SessionLocal() as session:
        
        # Crea una consulta SQL para insertar el usuario
            query = text(CREATE_USER)

            # Pasa los datos del usuario a la consulta
            session.execute(query, user_data)
            session.commit()
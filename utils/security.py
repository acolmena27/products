import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import text
from datetime import datetime, timedelta

# Encriptar contraseñas
from passlib.hash import argon2
from passlib.context import CryptContext

# Importamos la sentencia sql para usuarios
from users.statement.sql_statement import LOGIN_USER

# Configuramos el contexto de hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

from utils.connection.conn import engine, SessionLocal
from users.model.model import UserLogin

# Configura las credenciales
SECRET_KEY = "tu_secreto_super_secreto"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

current_access_token = None

class token_security:
    # TOKEN SECURE
    # ===============================================
    # ===============================================
    # Función para crear un token JWT
    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # Función para verificar un token JWT
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    # Validamos el token
    def token_validator():
        if current_access_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Debes iniciar sesión para acceder a esta operación"
            )

        # Verifica el token JWT almacenado en la variable de estado
        try:
            token_security.decode_token(current_access_token)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
    # LOGIN USER
    # ===============================================
    # ===============================================
    # Función para autenticar al usuario
    def authenticate_user(username: str, password: str):
        # Abre una sesión de base de datos
        with SessionLocal() as session:
            # Ejecuta la consulta SQL
            query = text(LOGIN_USER)
            result = session.execute(query, {"username": username})
                
            # Devuelve el usuario
            user = result.fetchone()
                
            if user is None or not pwd_context.verify(password, user[1]):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
                
            return {"username": username}  # Retorna los datos del usuario autenticado

class SecurityAPI:
       
    # Declararamos la aplicacion con la variable app
    router = APIRouter()
    
    # LOGIN
    # ===============================================
    # ===============================================
    # Ruta para iniciar sesión y obtener un token JWT
    @router.post("/login_user", response_model=dict)
    def login_user(user_login: UserLogin):
        username = user_login.username
        password = user_login.password
        user = token_security.authenticate_user(username, password)
            
        if user:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = token_security.create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
                
            # Almacena el token JWT en la variable de estado
            global current_access_token
            current_access_token = access_token
                
            return {"access_token": access_token, "token_type": "bearer"}
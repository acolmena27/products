# Casos de uso que se utilizaran segun la operacion a realizar buscar agregar actualizar o eliminar usuarios
import jwt
from fastapi import HTTPException, status, Depends
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound

from utils.connection.conn import engine, SessionLocal
from datetime import datetime, timedelta

# Encriptar contraseñas
from passlib.hash import argon2
from passlib.context import CryptContext

# Importamos la sentencia sql para usuarios
from products.statement.sql_statement import ALL_PRODUCTS, SEARCH_PRODUCTS, CREATE_PRODUCTS, CREATE_PURCHASED, CREATED_ORDER, SEARCH_ORDER, DELETE_ITEM, SEARCH_UPDATE
from products.model.model import User, Order, MyProductsAdd, MyPurchasedAdd, MyOrderAdd, DeleteItem, MyUpdateItem

# Configuramos el contexto de hashing
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class ProductsCase:
    def __init__(self):
        pass
    
    # ALL USER
    # ===============================================
    # ===============================================
    def get_all_products():
        with SessionLocal() as session:
            # Ejecuta la consulta SQL
            query = text(ALL_PRODUCTS)
            result = session.execute(query)
            
            products = result.fetchall()
            
            # Convierte los resultados en una lista de diccionarios
            products_list = []
            
            for product in products:
                products_dict = {
                    "product_name":product[0],
                    "price":product[1],
                    "shop":product[2],
                    "uuid":product[3]
                }
                products_list.append(products_dict)

            return products_list
    
    # SEARCH
    # ===============================================
    # ===============================================
    # Declaramos la función para consultar usuarios
    def get_products_by_shop(uuid: str):
        # Abre una sesión de base de datos
        with SessionLocal() as session:
            # Ejecuta la consulta SQL
            query = text(SEARCH_PRODUCTS)
            result = session.execute(query, {"uuid": uuid})
            
            # Devuelve el usuario
            purchased = result.fetchall()
            if purchased is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return purchased

    # INSERT
    # ===============================================
    # ===============================================
    # Declaramos el caso de uso que sera un insert
    def create_product(data: MyProductsAdd):
        # Convierte el objeto MyUserAdd en un diccionario
        product_data = dict(data)

        # Abre una sesión de base de datos
        with SessionLocal() as session:
        
        # Crea una consulta SQL para insertar el usuario
            query = text(CREATE_PRODUCTS)

            # Pasa los datos del usuario a la consulta
            session.execute(query, product_data)
            session.commit()
    
    # PURCHASED
    # ===============================================
    # ===============================================
    # Declaramos el caso de uso que sera un insert
    def create_purchased(data: MyPurchasedAdd):
        # Convierte el objeto MyUserAdd en un diccionario
        product_data = dict(data)

        # Abre una sesión de base de datos
        with SessionLocal() as session:
        
        # Crea una consulta SQL para insertar el usuario
            query = text(CREATE_PURCHASED)

            # Pasa los datos del usuario a la consulta
            session.execute(query, product_data)
            session.commit()
            
    # CREATED ORDERS
    # ===============================================
    # ===============================================
    # Declaramos el caso de uso que sera un insert
    def create_order(order: MyOrderAdd):
        # Convierte el objeto MyUserAdd en un diccionario
        order_data = dict(order)

        # Abre una sesión de base de datos
        with SessionLocal() as session:
        
        # Crea una consulta SQL para insertar el usuario
            query = text(CREATED_ORDER)

            # Pasa los datos del usuario a la consulta
            session.execute(query, order_data)
            session.commit()
            
    # SEARCH ORDERS
    # ===============================================
    # ===============================================
    # Declaramos la función para consultar usuarios
    def get_orders_by_user(uuid: str):
        
        with SessionLocal() as session:
            # Ejecuta la consulta SQL
            query = text(SEARCH_ORDER)
            result = session.execute(query, {"uuid": uuid})

            # Verifica si hay resultados
            if result.rowcount == 0:
                raise NoResultFound("Orden no encontrada")

            # Mapea los resultados a un objeto User
            user_data = None
            orders = []

            for row in result:
                if user_data is None:
                    user_data = {
                        "username": row[0],
                        "uuid": row[1],
                        "first_name": row[2],
                        "last_name": row[3],
                        "email": row[4],
                        "dni": row[5],
                    }

                orders.append(
                    Order(
                        product_name=row[6],
                        order_uuid=row[7],
                        paid=row[8]
                    )
                )

            user = User(**user_data, orders=orders)

            return user
        
    # UPDATE
    # ===============================================
    # ===============================================
    # Declaramos el caso de uso que sera un update
    def my_update_item(uuid: str, item_data: MyUpdateItem):
        # Abre una sesión de base de datos
        with SessionLocal() as session:
            # Busca el usuario en la base
            query = text(SEARCH_UPDATE)
            item = session.execute(query, {"uuid": uuid}).first()
        
            if not item:
                raise HTTPException(status_code=404, detail="Products not found")

            # Construye un diccionario con los campos a actualizar
            update_fields = {key: value for key, value in item_data.dict().items() if value is not None}

            # Actualiza los datos del usuario en la base de datos
            if update_fields:
                update_query = text(f"""UPDATE products SET {', '.join([f"{field} = :{field}" for field in update_fields.keys()])} WHERE uuid = :uuid""")
                session.execute(update_query, {"uuid": uuid, **update_fields})

            # Guarda los cambios en la base
            session.commit()
        
    # DELETE
    # ===============================================
    # ===============================================     
    def del_item(item_id: DeleteItem):
        item_del = dict(item_id)
        
        # Abre una sesión de base de datos
        with SessionLocal() as session:
            query = text(DELETE_ITEM)
            
            # Pasa los datos del usuario a la consulta
            session.execute(query, item_del)
            session.commit()
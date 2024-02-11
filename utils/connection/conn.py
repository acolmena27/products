# Para uso de PostgreSQL y querys y estable cer la conexion de datos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Creamos la conexion a la base de datos
engine = create_engine("postgresql://postgres:alex5354@localhost/productos", pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

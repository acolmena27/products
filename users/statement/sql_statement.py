# Aqui las sentencias SQL para realizar operaciones referente a los casos de uso
LOGIN_USER = """
SELECT username, password FROM users WHERE username = :username
"""

ALL_USER = """
SELECT
username, 
password,
uuid,
shop, 
first_name, 
last_name, 
email,
dni 
FROM users
"""

ALL_USER_PURCHASED = """
SELECT
username, 
password,
uuid,
shop, 
first_name, 
last_name, 
email,
dni 
FROM users WHERE shop = true
"""

SEARCH_USER = """
SELECT username, 
    password,
    uuid,
    shop, 
    first_name, 
    last_name, 
    email,
    dni 
FROM users WHERE shop = :shop"""

CREATE_USER ="""
INSERT INTO users (
    username, 
    password,
    uuid,
    shop, 
    first_name, 
    last_name, 
    email,
    dni 
)
VALUES (
    :username, 
    :password,
    :uuid,
    :shop, 
    :first_name, 
    :last_name, 
    :email,
    :dni 
)
"""
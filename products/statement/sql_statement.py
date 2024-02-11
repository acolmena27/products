# Aqui las sentencias SQL para realizar operaciones referente a los casos de uso

ALL_PRODUCTS = """
SELECT 
    product_name,
    price,
    shop,
    uuid
FROM products
"""

SEARCH_PRODUCTS = """
SELECT u.username, 
       u.uuid, 
       u.first_name, 
       u.last_name, 
       u.email,
       u.dni,
       p.purchased_products
FROM users AS u
INNER JOIN purchased_products AS p ON u.uuid = p.uuid
WHERE u.uuid = :uuid """

CREATE_PRODUCTS ="""
INSERT INTO products (
    product_name,
    price,
    shop,
    uuid 
)
VALUES (
    :product_name,
    :price,
    :shop,
    :uuid 
)
"""

CREATE_PURCHASED ="""
INSERT INTO purchased_products (
    purchased_products,
    uuid
)
VALUES (
    :purchased_products,
    :uuid
)
"""

CREATED_ORDER = """
INSERT INTO orders(
    product_name,
    order_uuid,
    paid,
    user_uuid
)
VALUES(
    :product_name,
    :order_uuid,
    :paid,
    :user_uuid
)
"""

SEARCH_ORDER = """
SELECT u.username, 
       u.uuid,
       u.first_name, 
       u.last_name, 
       u.email,
       u.dni,
       o.product_name,
       o.order_uuid,
       o.paid
FROM users AS u
LEFT JOIN (
    SELECT product_name,
           order_uuid,
           paid,
           user_uuid
    FROM orders
) AS o ON u.uuid = o.user_uuid
WHERE u.uuid = :uuid
"""

SEARCH_UPDATE = """
SELECT product_name, price, shop, uuid FROM products WHERE uuid = :uuid
"""

DELETE_ITEM = """ DELETE FROM products WHERE product_name = :product_name """


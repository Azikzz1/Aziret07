import sqlite3
from db import queries

db_registered = sqlite3.connect('db/registered.sqlite3')
db_store = sqlite3.connect('db/STORE.sqlite3')
cursor_registered = db_registered.cursor()
cursor_store = db_store.cursor()


async def DataBase_create():
    if db_registered:
        print('База данных registered подключена!')
    if db_store:
        print('База данных STORE подключена!')

    cursor_registered.execute(queries.CREATE_TABLE_registered)
    cursor_store.execute(queries.CREATE_TABLE_STORE)
    cursor_store.execute(queries.CREATE_TABLE_products_details)
    cursor_store.execute(queries.CREATE_TABLE_collection_products)
    db_store.commit()


async def sql_insert_registered(fullname, age, gender, email, photo):
    cursor_registered.execute(queries.INSERT_registered_QUERY, (
        fullname, age, gender, email, photo
    ))
    db_registered.commit()


async def sql_insert_store(model_name, size_1, price, photo, productid):
    cursor_store.execute(queries.INSERT_STORE_QUERY, (
        model_name, size_1, price, photo, productid
    ))
    db_store.commit()


async def sql_insert_products_details(productid, category, infoproduct):
    cursor_store.execute(queries.INSERT_products_details_QUERY, (
        productid, category, infoproduct
    ))
    db_store.commit()


async def sql_insert_collection_products(productid, collection):
    cursor_store.execute(queries.INSERT_collection_products_QUERY, (
        productid, collection
    ))
    db_store.commit()


# CRUD - Read
# =====================================================
# Основное подключение к базе (Для CRUD)
def get_db_connection():
    conn = sqlite3.connect('db/STORE.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * from STORE S
    INNER JOIN products_details  PD 
    INNER JOIN collection_products  CP
    ON S.productid = PD.productid = CP.productid
    """).fetchall()
    conn.close()
    return products


# CRUD - Delete
# =====================================================
def delete_product(productid):
    conn = get_db_connection()
    conn.execute('DELETE FROM STORE WHERE productid = ?', (productid,))
    conn.execute('DELETE FROM products_details WHERE productid = ?', (productid,))
    conn.execute('DELETE FROM collection_products WHERE productid = ?', (productid,))
    conn.commit()
    conn.close()


# CRUD - Update
# =====================================================
def update_product_field(productid, field_name, new_value):
    STORE_table = ["model_name", "size_1", "price", "photo"]
    products_details_table = ["infoproduct", "category"]
    collection_products_table = ["collection"]
    conn = get_db_connection()
    try:
        if field_name in STORE_table:
            query = f'UPDATE STORE SET {field_name} = ? WHERE productid = ?'
        elif field_name in products_details_table:
            query = f'UPDATE products_details SET {field_name} = ? WHERE productid = ?'
        elif field_name in collection_products_table:
            query = f'UPDATE collection_products SET {field_name} = ? WHERE productid = ?'
        else:
            raise ValueError(f'Нет такого поля {field_name}')
        conn.execute(query, (new_value, productid))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'Ошибка - {e}')
    finally:
        conn.close()

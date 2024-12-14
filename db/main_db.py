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

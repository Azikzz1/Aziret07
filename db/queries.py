CREATE_TABLE_registered = """
    CREATE TABLE IF NOT EXISTS registered(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    age TEXT,
    gender TEXT,
    email TEXT,
    photo TEXT
    )
"""

CREATE_TABLE_STORE = """
    CREATE TABLE IF NOT EXISTS STORE(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT,
    size_1 TEXT,
    price REAL,
    photo TEXT,
    productid INTEGER
    )
"""

CREATE_TABLE_products_details = """
    CREATE TABLE IF NOT EXISTS products_details(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    productid INTEGER,
    category TEXT,
    infoproduct TEXT
    )
"""

CREATE_TABLE_collection_products = """
    CREATE TABLE IF NOT EXISTS collection_products(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    productid INTEGER,
    collection TEXT
    )
"""

INSERT_registered_QUERY = """
    INSERT INTO registered (fullname, age, gender, email, photo)
    VALUES (?, ?, ?, ?, ?)
"""

INSERT_STORE_QUERY = """
    INSERT INTO STORE (model_name, size_1, price, photo, productid)
    VALUES (?, ?, ?, ?, ?)
"""

INSERT_products_details_QUERY = """
    INSERT INTO products_details (productid, category, infoproduct)
    VALUES (?, ?, ?)
"""

INSERT_collection_products_QUERY = """
    INSERT INTO collection_products (productid, collection)
    VALUES (?, ?)
"""

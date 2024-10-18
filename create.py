import sqlite3


#Connecting to sqlite
conn = sqlite3.connect('products.db')


#Creating a cursor object using the cursor() method
cursor = conn.cursor()


#Droping STUDENT table if already exists.
cursor.execute("DROP TABLE IF EXISTS products")

#Creating table as per requirement
sql ='''CREATE TABLE products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image TEXT,
        code TEXT NOT NULL,
        brand TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 0,
        price INTEGER NOT NULL DEFAULT 0
    )'''
cursor.execute(sql)
print(" Product Table created successfully........")


cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute('''
    CREATE TABLE sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        reference TEXT NOT NULL
    )
''')

print("sales Table created successfully........")
cursor.execute("DROP TABLE IF EXISTS sales_items")
cursor.execute('''
    CREATE TABLE sales_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        products TEXT NOT NULL,
        time_bought TEXT NOT NULL,
        FOREIGN KEY (sale_id) REFERENCES sales (id)
    )
''')

print("sales items Table created successfully........")

cursor.execute("DROP TABLE IF EXISTS purchase")
cursor.execute('''
    CREATE TABLE purchase (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        supplier TEXT,
        quantity INTEGER,
        total_price REAL,
        reference TEXT NOT NULL,
        payment_status TEXT NOT NULL
    )
''')
print("purchase Table created successfully........")


cursor.execute("DROP TABLE IF EXISTS purchase_items")
cursor.execute('''
    CREATE TABLE purchase_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (purchase_id) REFERENCES purchase (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
''')
print("purchse items Table created successfully........")




# Commit your changes in the database
conn.commit()

#Closing the connection
conn.close()

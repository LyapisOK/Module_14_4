import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


def initiate_db():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    ''')
#cursor.execute("CREATE INDEX IF NOT EXISTS idx_title ON Products (title)")
    for i in range(1, 5):
        cursor.execute(" INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                        (f'Продукт {i}', f'Описание {i}', i * 100))

def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    result = cursor.execute("SELECT * FROM Products")
    products = result.fetchall()
    connection.close()
    for product in products:
        print(product)
    return products

connection.commit()
connection.close()
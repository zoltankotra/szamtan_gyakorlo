from app import get_db_connection


def modify_orders_table():
    conn = get_db_connection()
    c = conn.cursor()

    # Ideiglenes tábla létrehozása az új szerkezettel
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders_new (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            cikkszam TEXT,
            mennyiseg INTEGER,
            lezarva INTEGER DEFAULT 0,
            teljesitve INTEGER DEFAULT 0,
            FOREIGN KEY(customer_id) REFERENCES customers(id),
            FOREIGN KEY(cikkszam) REFERENCES products(cikkszam)
        )
    ''')

    # Adatok másolása a régi táblából
    c.execute('''
        INSERT INTO orders_new (id, customer_id, cikkszam, mennyiseg)
        SELECT id, customer_id, cikkszam, mennyiseg
        FROM orders
    ''')

    # Régi tábla törlése és új átnevezése
    c.execute('DROP TABLE orders')
    c.execute('ALTER TABLE orders_new RENAME TO orders')

    conn.commit()
    conn.close()

# Meghívás
modify_orders_table()

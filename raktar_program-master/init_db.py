import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Termékek tábla létrehozása
c.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                cikkszam TEXT,
                nev TEXT,
                mennyiseg INTEGER,
                ar REAL,
                suly REAL,
                lokacio TEXT,
                kategoria TEXT)''')

# Ügyfelek tábla létrehozása
c.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                nev TEXT,
                iranyitoszam TEXT,
                varos TEXT,
                utca TEXT,
                hazszam TEXT,
                email TEXT)''')

# Megrendelések tábla létrehozása
c.execute('''CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                mennyiseg INTEGER,
                cikkszam TEXT,
                leellenorozve BOOLEAN,
                lezarva BOOLEAN)''')

conn.commit()
conn.close()



import sqlite3

# Ügyfelek, Megrendelések és egyéb táblák létrehozása
def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Termékek tábla
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    cikkszam TEXT UNIQUE,
                    nev TEXT,
                    ar REAL,
                    suly REAL,
                    kategoria TEXT)''')

    # Raktáron lévő termékek tábla
    c.execute('''CREATE TABLE IF NOT EXISTS stock (
                    id INTEGER PRIMARY KEY,
                    cikkszam TEXT,
                    lokacio TEXT,
                    mennyiseg INTEGER,
                    FOREIGN KEY(cikkszam) REFERENCES products(cikkszam))''')

    # Ügyfelek tábla
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    nev TEXT NOT NULL,
                    iranyitoszam TEXT NOT NULL,
                    varos TEXT NOT NULL,
                    utca TEXT NOT NULL,
                    hazszam TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE)''')

    # Megrendelések tábla
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    cikkszam TEXT,
                    mennyiseg INTEGER,
                    status TEXT,
                    FOREIGN KEY(customer_id) REFERENCES customers(id),
                    FOREIGN KEY(cikkszam) REFERENCES products(cikkszam))''')

    conn.commit()
    conn.close()

# A database létrehozása, ha még nem létezik
create_database()

# Figyelem: Ez törli a 'products' táblát, és minden adatot!
def drop_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS orders')
    conn.commit()
    conn.close()

# Csak akkor használd, ha a tábla törlésére van szükséged.
#drop_table()
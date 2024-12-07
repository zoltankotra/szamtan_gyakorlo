

import sqlite3

# Ügyfelek, Megrendelések és egyéb táblák létrehozása
def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Termékek tábla
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    cikkszam TEXT UNIQUE,
                    egyseg_vonalkod INTEGER UNIQUE,
                    gyujto_vonalkod INTEGER UNIQUE,
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
                    order_id INTEGER,
                    FOREIGN KEY(cikkszam) REFERENCES products(cikkszam),
                    FOREIGN KEY(order_id) REFERENCES orders(id))''')

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
                    id INTEGER,
                    customer_id INTEGER,
                    cikkszam TEXT,
                    mennyiseg INTEGER,
                    lezarva INTEGER DEFAULT 0,
                    teljesitve INTEGER DEFAULT 0,
                    PRIMARY KEY(id, cikkszam),
                    FOREIGN KEY(customer_id) REFERENCES customers(id),
                    FOREIGN KEY(cikkszam) REFERENCES products(cikkszam))''')

    conn.commit()
    conn.close()

# A database létrehozása, ha még nem létezik
create_database()

# Figyelem: Ez törli a megadott táblát, és minden adatot!
def drop_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS stock')
    conn.commit()
    conn.close()

# Csak akkor használd, ha a tábla törlésére van szükséged.
#drop_table()

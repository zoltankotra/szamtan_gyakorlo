import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Termékek tábla létrehozása
    c.execute('''
        CREATE TABLE IF NOT EXISTS termekek (
            cikkszam INTEGER PRIMARY KEY,
            nev TEXT,
            mennyiseg INTEGER,
            ar REAL,
            suly REAL,
            lokacio TEXT
        )
    ''')

    # Ügyfelek tábla létrehozása
    c.execute('''
        CREATE TABLE IF NOT EXISTS ugyfelek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nev TEXT,
            iranyitoszam TEXT,
            varos TEXT,
            utca TEXT,
            hazszam TEXT,
            email TEXT
        )
    ''')

    # Megrendelések tábla létrehozása
    c.execute('''
        CREATE TABLE IF NOT EXISTS megrendelesek (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ugyfel_neve TEXT,
            leellenorizve BOOLEAN,
            lezarva BOOLEAN
        )
    ''')

    conn.commit()
    conn.close()

# Futtatás
if __name__ == "__main__":
    init_db()

import sqlite3
import random

# Csatlakozás az adatbázishoz
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Tábla létrehozása, ha nem létezik
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        cikkszam TEXT UNIQUE,
        nev TEXT,
        ar REAL,
        suly REAL,
        kategoria TEXT
    )
''')

# Termékek generálása
product_names = [
    "Laptop", "Egér", "Billentyűzet", "Monitor", "Telefon",
    "Táblagép", "Füles", "Hangszóró", "Kamera", "Router",
    "Kábel", "Töltő", "Okosóra", "Egérpad", "Pendrive",
    "Projektor", "Hűtő", "Nyomtató", "Szkenner", "Tablet",
    "Ventilátor", "Televízió", "Kávéfőző", "Robotporszívó",
    "Drón", "Játékvezérlő", "Fülhallgató", "Hangrendszer",
    "Hálózati kapcsoló", "Okosotthon eszköz"
]
categories = ["Elektronika", "Irodai eszközök", "Szórakozás", "Otthon", "Egyéb"]

# Beszúrási ciklus
for _ in range(30):
    cikkszam = str(random.randint(1000, 9999))
    nev = random.choice(product_names)
    ar = round(random.uniform(1000, 100000), 2)
    suly = round(random.uniform(0.1, 10), 2)
    kategoria = random.choice(categories)

    try:
        c.execute('''
            INSERT INTO products (cikkszam, nev, ar, suly, kategoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (cikkszam, nev, ar, suly, kategoria))
    except sqlite3.IntegrityError:
        # Ha a cikkszám ütközik, kihagyjuk a beszúrást
        print(f"Ütköző cikkszám: {cikkszam}, kihagyva.")

# Változások mentése és kapcsolat lezárása
conn.commit()
conn.close()

print("30 termék sikeresen generálva és hozzáadva az adatbázishoz!")

import sqlite3
from faker import Faker
import random


def generate_products(num_products):
    # Adatbázis kapcsolat
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Faker példány létrehozása
    fake = Faker('hu_HU')

    # Egyedi cikkszámok nyilvántartása
    cikkszamok = set()

    for _ in range(num_products):
        while True:
            cikkszam = str(fake.random_int(min=1000, max=9999))
            if cikkszam not in cikkszamok:
                cikkszamok.add(cikkszam)
                break

        name = fake.word().capitalize()
        price = round(random.uniform(100, 10000), 2)  # Ár: 100 és 10,000 között
        weight = round(random.uniform(0.5, 50), 2)  # Súly: 0.5 és 50 kg között
        category = random.choice(['Elektronika', 'Ruházat', 'Élelmiszer', 'Játék', 'Könyv'])

        try:
            # Adatok beszúrása az adatbázisba
            c.execute('''
                INSERT INTO products (cikkszam, nev, ar, suly, kategoria)
                VALUES (?, ?, ?, ?, ?)''', (cikkszam, name, price, weight, category))
        except sqlite3.IntegrityError:
            # Ha a cikkszám már létezik (bár ezt az előzetes szűrés elvileg kizárja)
            print(f"Hiba: A cikkszám már létezik: {cikkszam}")

    # Változások mentése és kapcsolat lezárása
    conn.commit()
    conn.close()
    print(f"{num_products} termék sikeresen generálva.")


# Termékek generálása
generate_products(30)  # 30 termék generálása

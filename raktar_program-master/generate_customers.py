import sqlite3
from faker import Faker


def generate_customers(num_customers):
    # Adatbázis kapcsolat
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Faker példány létrehozása
    fake = Faker('hu_HU')

    # Egyedi e-mailek nyilvántartása
    emails = set()

    for _ in range(num_customers):
        while True:
            email = fake.email()
            if email not in emails:
                emails.add(email)
                break

        name = fake.name()
        postal_code = fake.postcode()
        city = fake.city()
        street = fake.street_name()
        house_number = str(fake.random_int(min=1, max=200))

        try:
            # Adatok beszúrása az adatbázisba
            c.execute('''
                INSERT INTO customers (nev, iranyitoszam, varos, utca, hazszam, email)
                VALUES (?, ?, ?, ?, ?, ?)''', (name, postal_code, city, street, house_number, email))
        except sqlite3.IntegrityError:
            # Ha az email már létezik (bár ezt az előzetes szűrés elvileg kizárja)
            print(f"Hiba: Az email már létezik: {email}")

    # Változások mentése és kapcsolat lezárása
    conn.commit()
    conn.close()
    print(f"{num_customers} ügyfél sikeresen generálva.")


# Ügyfelek generálása
generate_customers(30)  # 30 ügyfél generálása

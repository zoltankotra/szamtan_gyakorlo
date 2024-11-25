import sqlite3
from faker import Faker


# Adatbázis csatlakozás
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Ügyfelek generálása
def generate_customers():
    fake = Faker('hu_HU')  # Magyar nyelvű adatokat generál
    customers = []

    for _ in range(30):  # 30 ügyfél generálása
        name = fake.name()
        postal_code = fake.postcode()  # Itt a 'postalcode()' a helyes metódus
        city = fake.city()
        street = fake.street_name()
        house_number = fake.building_number()
        email = fake.email()

        customers.append((name, postal_code, city, street, house_number, email))

    return customers


# Ügyfelek hozzáadása az adatbázishoz
def add_customers_to_db(customers):
    conn = get_db_connection()
    cursor = conn.cursor()

    for customer in customers:
        cursor.execute('''
            INSERT INTO customers (nev, iranyitoszam, varos, utca, hazszam, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', customer)

    conn.commit()
    conn.close()


# Fő futtató kód
if __name__ == '__main__':
    # Ügyfelek generálása
    customers = generate_customers()

    # Ügyfelek hozzáadása az adatbázishoz
    add_customers_to_db(customers)

    print("30 ügyfél sikeresen hozzáadva az adatbázishoz!")

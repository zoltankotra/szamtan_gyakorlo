import sqlite3


# Adatbázis csatlakozás
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Adatok törlése a termékek és ügyfelek táblákból
def delete_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Törlés a termékek táblából
    cursor.execute('DELETE FROM products')

    # Törlés az ügyfelek táblából
    cursor.execute('DELETE FROM customers')

    conn.commit()
    conn.close()


# Fő futtató kód
if __name__ == '__main__':
    # Az összes adat törlése
    delete_all_data()

    print("A termékek és ügyfelek adatbázisok teljes tartalma törölve!")

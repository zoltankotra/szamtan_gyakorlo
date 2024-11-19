from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 's3cr3t'

# Adatbázis kapcsolat
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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
                    nev TEXT,
                    iranyitoszam TEXT,
                    varos TEXT,
                    utca TEXT,
                    hazszam TEXT,
                    email TEXT)''')

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
#create_database()

# Figyelem: Ez törli a 'products' táblát, és minden adatot!
def drop_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS products')
    conn.commit()
    conn.close()

# Csak akkor használd, ha a tábla törlésére van szükséged.
#drop_table()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        nev = request.form['nev']
        ar = request.form['ar']
        suly = request.form['suly']
        kategoria = request.form['kategoria']

        # Ellenőrizzük, hogy a cikkszám már létezik-e
        conn = get_db_connection()
        existing_product = conn.execute('SELECT * FROM products WHERE cikkszam = ?', (cikkszam,)).fetchone()

        if existing_product:
            # Ha létezik, hibaüzenetet adunk
            flash("A cikkszám már létezik. Nem lehet új terméket hozzáadni!", "error")
            return redirect(url_for('products'))

        # Ha nem létezik, hozzáadjuk az új terméket
        conn.execute('INSERT INTO products (cikkszam, nev, ar, suly, kategoria) VALUES (?, ?, ?, ?, ?)',
                     (cikkszam, nev, ar, suly, kategoria))
        conn.commit()
        conn.close()

        flash("Termék hozzáadva!", "success")
        return redirect(url_for('products'))

    return render_template('add_product.html')


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()

    # Töröljük a terméket a products táblából az adott id alapján
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))

    # Eltávolítjuk a terméket a stock táblából is, ha létezik
    conn.execute('DELETE FROM stock WHERE cikkszam = (SELECT cikkszam FROM products WHERE id = ?)', (product_id,))

    conn.commit()
    conn.close()

    flash("A termék sikeresen törölve lett!", "success")
    return redirect(url_for('products'))


@app.route('/customers')
def customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

@app.route('/orders')
def orders():
    conn = get_db_connection()
    orders = conn.execute('''SELECT orders.id, customers.nev, orders.cikkszam, orders.mennyiseg, orders.status 
                            FROM orders
                            JOIN customers ON orders.customer_id = customers.id''').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        nev = request.form['nev']
        iranyitoszam = request.form['iranyitoszam']
        varos = request.form['varos']
        utca = request.form['utca']
        hazszam = request.form['hazszam']
        email = request.form['email']

        conn = get_db_connection()
        conn.execute('INSERT INTO customers (nev, iranyitoszam, varos, utca, hazszam, email) VALUES (?, ?, ?, ?, ?, ?)',
                     (nev, iranyitoszam, varos, utca, hazszam, email))
        conn.commit()
        conn.close()

        flash("Ügyfél hozzáadva!", "success")
        return redirect(url_for('customers'))

    return render_template('add_customer.html')

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        cikkszam = request.form['cikkszam']
        mennyiseg = request.form['mennyiseg']
        status = request.form['status']

        conn = get_db_connection()
        conn.execute('INSERT INTO orders (customer_id, cikkszam, mennyiseg, status) VALUES (?, ?, ?, ?)',
                     (customer_id, cikkszam, mennyiseg, status))
        conn.commit()
        conn.close()

        flash("Megrendelés hozzáadva!", "success")
        return redirect(url_for('orders'))

    return render_template('add_order.html')

@app.route('/stock')
def stock():
    conn = get_db_connection()
    stock = conn.execute('''SELECT stock.id, products.cikkszam, stock.lokacio, stock.mennyiseg 
                            FROM stock
                            JOIN products ON stock.cikkszam = products.cikkszam''').fetchall()
    conn.close()
    return render_template('stock.html', stock=stock)


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        lokacio = request.form['lokacio']
        mennyiseg = int(request.form['mennyiseg'])

        conn = get_db_connection()

        # Ellenőrizzük, hogy létezik-e már a cikkszám és lokáció kombináció a stock táblában
        existing_stock = conn.execute('SELECT * FROM stock WHERE cikkszam = ? AND lokacio = ?',
                                      (cikkszam, lokacio)).fetchone()

        if existing_stock:
            # Ha létezik, növeljük a mennyiséget
            new_mennyiseg = existing_stock['mennyiseg'] + mennyiseg
            conn.execute('UPDATE stock SET mennyiseg = ? WHERE cikkszam = ? AND lokacio = ?',
                         (new_mennyiseg, cikkszam, lokacio))
            flash("A mennyiség frissítve lett!", "success")
        else:
            # Ha nem létezik, új rekordot adunk hozzá
            conn.execute('INSERT INTO stock (cikkszam, lokacio, mennyiseg) VALUES (?, ?, ?)',
                         (cikkszam, lokacio, mennyiseg))
            flash("Új termék hozzáadva a raktárhoz!", "success")

        conn.commit()
        conn.close()
        return redirect(url_for('stock'))

    return render_template('add_stock.html')


@app.route('/delete_stock/<int:stock_id>', methods=['POST'])
def delete_stock(stock_id):
    conn = get_db_connection()

    # Töröljük a rekordot a stock táblából az adott id alapján
    conn.execute('DELETE FROM stock WHERE id = ?', (stock_id,))
    conn.commit()
    conn.close()

    flash("A rekord sikeresen törölve lett!", "success")
    return redirect(url_for('stock'))


if __name__ == '__main__':
    app.run(debug=True)

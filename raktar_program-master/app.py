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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cikkszam TEXT NOT NULL,
    mennyiseg INTEGER NOT NULL,
    lokacio TEXT NOT NULL,
    FOREIGN KEY (cikkszam) REFERENCES products(cikkszam));''')

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
create_database()

# Figyelem: Ez törli a 'products' táblát, és minden adatot!
def drop_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS products,orders,customers,stock')
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


@app.route('/add_to_stock', methods=['GET', 'POST'])
def add_to_stock():
    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        mennyiseg = request.form['mennyiseg']
        lokacio = request.form['lokacio']

        # Ellenőrizzük, hogy a cikkszám létezik a termékek táblájában
        product = db.execute('SELECT * FROM products WHERE cikkszam = ?', (cikkszam,)).fetchone()
        if product:
            db.execute('INSERT INTO stock (cikkszam, mennyiseg, lokacio) VALUES (?, ?, ?)',
                       (cikkszam, mennyiseg, lokacio))
            db.commit()
            flash('A termék hozzáadva a raktárhoz!', 'success')
        else:
            flash('A megadott cikkszám nem található a termékek között!', 'error')
        return redirect(url_for('stock'))

    return render_template('add_to_stock.html')

@app.route('/delete_from_stock/<int:id>', methods=['POST'])
def delete_from_stock(id):
    db.execute('DELETE FROM stock WHERE id = ?', (id,))
    db.commit()
    flash('A termék sikeresen törölve lett a raktárról.', 'success')
    return redirect(url_for('stock'))


if __name__ == '__main__':
    app.run(debug=True)

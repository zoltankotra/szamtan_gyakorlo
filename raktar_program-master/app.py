from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 's3cr3t'

# Adatbázis kapcsolat
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

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


@app.route('/customers', methods=['GET'])
def customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)


@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        # Új ügyfél hozzáadása
        nev = request.form['nev']
        iranyitoszam = request.form['iranyitoszam']
        varos = request.form['varos']
        utca = request.form['utca']
        hazszam = request.form['hazszam']
        email = request.form['email']

        conn = get_db_connection()
        # Ellenőrizzük, hogy az email cím már létezik-e
        existing_customer = conn.execute('SELECT * FROM customers WHERE email = ?', (email,)).fetchone()
        if existing_customer:
            flash('Ez az email cím már létezik!', 'error')
        else:
            conn.execute(
                'INSERT INTO customers (nev, iranyitoszam, varos, utca, hazszam, email) VALUES (?, ?, ?, ?, ?, ?)',
                (nev, iranyitoszam, varos, utca, hazszam, email))
            conn.commit()
            flash('Ügyfél sikeresen hozzáadva!', 'success')

        conn.close()
        return redirect(url_for('customers'))  # Visszairányítjuk a fő ügyféloldalra

    return render_template('add_customer.html')  # Ha GET kérés, akkor a formot mutatjuk

@app.route('/delete_customer/<email>', methods=['POST'])
def delete_customer(email):
    conn = get_db_connection()
    customer = conn.execute('SELECT * FROM customers WHERE email = ?', (email,)).fetchone()
    if customer:
        conn.execute('DELETE FROM customers WHERE email = ?', (email,))
        conn.commit()
        flash('Ügyfél sikeresen törölve!', 'success')
    else:
        flash('A törlés nem sikerült, ügyfél nem található!', 'error')

    conn.close()
    return redirect(url_for('customers'))


@app.route('/orders')
def orders():
    conn = get_db_connection()
    orders = conn.execute('''
        SELECT 
            orders.id, 
            customers.nev, 
            orders.cikkszam, 
            orders.mennyiseg, 
            orders.lezarva, 
            orders.teljesitve
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
    ''').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        email = request.form['email']
        cikkszam = request.form['cikkszam']
        mennyiseg = request.form['mennyiseg']
        lezarva = 1 if 'lezarva' in request.form else 0
        teljesitve = 1 if 'teljesitve' in request.form else 0

        conn = get_db_connection()
        # Ellenőrizzük, hogy az ügyfél email alapján létezik-e
        customer = conn.execute('SELECT id FROM customers WHERE email = ?', (email,)).fetchone()
        product_exists = conn.execute('SELECT cikkszam FROM products WHERE cikkszam = ?', (cikkszam,)).fetchone()

        if not customer:
            flash('Hiba: Az ügyfél email nem létezik!', 'error')
        elif not product_exists:
            flash('Hiba: A megadott cikkszám nem létezik!', 'error')
        else:
            customer_id = customer['id']
            conn.execute('''
                INSERT INTO orders (customer_id, cikkszam, mennyiseg, lezarva, teljesitve)
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, cikkszam, mennyiseg, lezarva, teljesitve))
            conn.commit()
            flash('Megrendelés sikeresen hozzáadva!', 'success')

        conn.close()
        return redirect(url_for('orders'))
    return render_template('add_order.html')

@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    flash('Megrendelés sikeresen törölve!', 'success')
    return redirect(url_for('orders'))


@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    lezarva = 'lezarva' in request.form
    teljesitve = 'teljesitve' in request.form

    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()

    if teljesitve:
        # Ha teljesítve van, levonjuk a mennyiséget a megfelelő raktári lokációról
        cikkszam = order['cikkszam']
        mennyiseg = order['mennyiseg']

        # Keresünk egy lokációt, ahol van elég készlet
        stock = conn.execute('''
            SELECT id, cikkszam, lokacio, mennyiseg 
            FROM stock 
            WHERE cikkszam = ? AND mennyiseg >= ? 
            LIMIT 1
        ''', (cikkszam, mennyiseg)).fetchone()

        if stock:
            # Levonjuk a szükséges mennyiséget a megtalált lokációról
            conn.execute('''
                UPDATE stock 
                SET mennyiseg = mennyiseg - ? 
                WHERE id = ?
            ''', (mennyiseg, stock['id']))
            conn.commit()
            flash('Megrendelés sikeresen teljesítve és a raktárkészlet frissítve!', 'success')
        else:
            flash('Nincs elegendő készlet a raktárban!', 'error')
            conn.close()
            return redirect(url_for('orders'))

    # Státusz frissítése
    conn.execute('''
        UPDATE orders
        SET lezarva = ?, teljesitve = ?
        WHERE id = ?
    ''', (1 if lezarva else 0, 1 if teljesitve else 0, order_id))
    conn.commit()
    conn.close()

    flash('Megrendelés státusza frissítve!', 'success')
    return redirect(url_for('orders'))



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

        # Ellenőrizzük, hogy létezik-e a cikkszám a products táblában
        product_exists = conn.execute('SELECT * FROM products WHERE cikkszam = ?', (cikkszam,)).fetchone()

        if not product_exists:
            # Ha a cikkszám nem létezik a termékek táblában
            flash("Hibás cikkszám! Ez a termék nem létezik.", "error")
            conn.close()
            return redirect(url_for('stock'))

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

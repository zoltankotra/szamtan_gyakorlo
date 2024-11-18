from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os


app = Flask(__name__)

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

@app.route('/customers')
def customers():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('customers.html', customers=customers)

# Megrendelések route hozzáadása
@app.route('/orders')
def orders():
    conn = get_db_connection()
    orders = conn.execute('''SELECT o.id, c.nev, p.nev AS product_name, o.mennyiseg, o.cikkszam, o.leellenorozve, o.lezarva
                             FROM orders o
                             JOIN customers c ON o.customer_id = c.id
                             JOIN products p ON o.product_id = p.id''').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/add_product', methods=('GET', 'POST'))
def add_product():
    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        nev = request.form['nev']
        mennyiseg = request.form['mennyiseg']
        ar = request.form['ar']
        suly = request.form['suly']
        lokacio = request.form['lokacio']
        kategoria = request.form['kategoria']

        conn = get_db_connection()
        conn.execute('INSERT INTO products (cikkszam, nev, mennyiseg, ar, suly, lokacio, kategoria) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (cikkszam, nev, mennyiseg, ar, suly, lokacio, kategoria))
        conn.commit()
        conn.close()

        return redirect(url_for('products'))

    return render_template('add_product.html')

# Termék szerkesztése route
@app.route('/edit_product/<int:id>', methods=('GET', 'POST'))
def edit_product(id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        nev = request.form['nev']
        mennyiseg = request.form['mennyiseg']
        ar = request.form['ar']
        suly = request.form['suly']
        lokacio = request.form['lokacio']
        kategoria = request.form['kategoria']

        conn.execute('''UPDATE products SET cikkszam = ?, nev = ?, mennyiseg = ?, ar = ?, suly = ?, lokacio = ?, kategoria = ? 
                        WHERE id = ?''', (cikkszam, nev, mennyiseg, ar, suly, lokacio, kategoria, id))
        conn.commit()
        conn.close()

        return redirect(url_for('products'))

    return render_template('edit_product.html', product=product)

# Termék törlésének route-ja
@app.route('/delete_product/<int:id>', methods=('POST',))
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('products'))

if __name__ == '__main__':
    app.run(debug=True)

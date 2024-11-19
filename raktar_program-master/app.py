from flask import Flask, render_template, request, redirect, url_for,flash
import sqlite3
import os


app = Flask(__name__)

# Adatbázis kapcsolat
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')


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

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        nev = request.form['nev']
        mennyiseg = request.form['mennyiseg']
        ar = request.form['ar']
        suly = request.form['suly']
        lokacio = request.form['lokacio']
        kategoria = request.form['kategoria']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Ellenőrizzük, hogy létezik-e már termék azonos cikkszámmal és lokációval
        c.execute('''SELECT * FROM products WHERE cikkszam = ? AND lokacio = ?''', (cikkszam, lokacio))
        product = c.fetchone()

        if product:
            # Ha létezik ilyen termék, akkor növeljük a mennyiséget
            new_quantity = product[2] + int(mennyiseg)
            c.execute('''UPDATE products SET mennyiseg = ? WHERE cikkszam = ? AND lokacio = ?''', (new_quantity, cikkszam, lokacio))
        else:
            # Ha nem létezik ilyen termék, új rekordot veszünk fel
            c.execute('''INSERT INTO products (cikkszam, nev, mennyiseg, ar, suly, lokacio, kategoria) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', (cikkszam, nev, mennyiseg, ar, suly, lokacio, kategoria))

        conn.commit()
        conn.close()

        # Sikeres hozzáadás után irányítjuk a megfelelő oldalra
        return render_template('success.html', message="Termék sikeresen hozzáadva!")

    return render_template('add_product.html')

# Termék szerkesztése route
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Termék lekérése az id alapján
    c.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = c.fetchone()

    if request.method == 'POST':
        # Csak a termék neve változhat
        nev = request.form['nev']

        # Ellenőrizzük, hogy létezik-e már olyan termék ugyanazzal a cikkszámmal és lokációval, de más névvel
        cikkszam = product[1]
        lokacio = product[6]

        c.execute('SELECT * FROM products WHERE cikkszam = ? AND lokacio = ?', (cikkszam, lokacio))
        existing_product = c.fetchone()

        if existing_product:
            # Ha létezik termék ugyanazzal a cikkszámmal és lokációval, csak a nevet módosítjuk
            c.execute('UPDATE products SET nev = ? WHERE id = ?', (nev, id))
            conn.commit()
            conn.close()
            return render_template('success.html', message="Termék sikeresen módosítva!")
        else:
            # Ha nem található ilyen termék, akkor visszairányítjuk a failure oldalra
            conn.close()
            return render_template('failure.html', message="Hiba történt a módosítás közben!")

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


#Megvan a termék hozzáadása adatokkal.Módositásnál is odakell figyelni a megeggyező adatokra...Törlés gomb mukodik
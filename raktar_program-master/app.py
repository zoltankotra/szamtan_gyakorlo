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
    per_page = int(request.args.get('per_page', 10))  # Egy oldalon megjelenő elemek száma
    page = int(request.args.get('page', 1))  # Az aktuális oldal lekérése (alapértelmezett: 1)
    offset = (page - 1) * per_page  # Az eltolás számítása
    order_by = str(request.args.get('order_by', 'cikkszam'))
    desc = request.args.get('desc', 'false').lower() in ('true', '1')

    valid_columns = {'cikkszam', 'nev', 'ar', 'suly', 'kategoria'}
    if order_by not in valid_columns:
        raise ValueError("Invalid column name for ordering.") #Elkerüljük az SQL injection-t
    if desc:
        descending = 'DESC'
    if not desc:
        descending = ''

    conn = get_db_connection()
    products = conn.execute(
        f'SELECT * FROM products ORDER BY {order_by} {descending} LIMIT ? OFFSET ?', (per_page, offset)
    ).fetchall()
    total_products = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    conn.close()

    total_pages = (total_products + per_page - 1) // per_page  # Összes oldal száma

    # Számítsuk ki az oldalszámok tartományát
    start_page = max(1, page - 2)  # Az aktuális oldalhoz képest 2-vel hátrébb
    end_page = min(total_pages, page + 2)  # Az aktuális oldalhoz képest 2-vel előrébb

    query_params = {
        'page': page,
        'per_page': per_page,
        'order_by': order_by,
        'desc': desc
    }

    columns = [
        {"name": "cikkszam", "label": "Cikkszám"},
        {"name": "nev", "label": "Termék neve"},
        {"name": "ar", "label": "Ár"},
        {"name": "suly", "label": "Súly"},
        {"name": "kategoria", "label": "Kategória"}
    ]

    return render_template(
        'products.html',
        products=products,
        page=page,
        order_by=order_by,
        desc=desc,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        query_params=query_params,
        columns=columns
    )



@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        egyseg_vonalkod = request.form['egyseg_vonalkod']
        gyujto_vonalkod = request.form['gyujto_vonalkod']
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
        conn.execute('INSERT INTO products (cikkszam, egyseg_vonalkod, gyujto_vonalkod, nev, ar, suly, kategoria) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (cikkszam, egyseg_vonalkod, gyujto_vonalkod, nev, ar, suly, kategoria))
        conn.commit()
        conn.close()

        flash("Termék hozzáadva!", "success")
        return redirect(url_for('products'))

    return render_template('add_product.html')


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = get_db_connection()

    # Check if the product exists in the stock table with non-zero quantity
    stock_check = conn.execute('''
        SELECT COUNT(*) as count
        FROM stock
        WHERE cikkszam = (SELECT cikkszam FROM products WHERE id = ?) AND mennyiseg > 0
    ''', (product_id,)).fetchone()

    if stock_check['count'] > 0:
        # If the product is in stock, prevent deletion
        conn.close()
        flash("A termék nem törölhető, mert még van készleten!", "error")
        return redirect(url_for('products'))

    # If the product is not in stock, proceed with deletion
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))

    # Also remove the product from the stock table, if it exists
    conn.execute('DELETE FROM stock WHERE cikkszam = (SELECT cikkszam FROM products WHERE id = ?)', (product_id,))

    conn.commit()
    conn.close()

    flash("A termék sikeresen törölve lett!", "success")
    return redirect(url_for('products'))



@app.route('/customers', methods=['GET'])
def customers():
    per_page = int(request.args.get('per_page', 10))  # Egy oldalon megjelenő elemek száma
    page = int(request.args.get('page', 1))  # Az aktuális oldal lekérése (alapértelmezett: 1)
    offset = (page - 1) * per_page  # Az eltolás számítása
    order_by = str(request.args.get('order_by', 'nev'))
    desc = request.args.get('desc', 'false').lower() in ('true', '1')

    valid_columns = {'nev', 'iranyitoszam', 'varos', 'utca', 'hazszam', 'email'}
    if order_by not in valid_columns:
        raise ValueError("Invalid column name for ordering.") #Elkerüljük az SQL injection-t
    if desc:
        descending = 'DESC'
    if not desc:
        descending = ''

    conn = get_db_connection()
    customers = conn.execute(
        f'SELECT * FROM customers ORDER BY {order_by} {descending} LIMIT ? OFFSET ?', (per_page, offset)
    ).fetchall()
    total_customers = conn.execute('SELECT COUNT(*) FROM customers').fetchone()[0]
    conn.close()

    total_pages = (total_customers + per_page - 1) // per_page  # Összes oldal száma

    # Számítsuk ki az oldalszámok tartományát
    start_page = max(1, page - 2)  # Az aktuális oldalhoz képest 2-vel hátrébb
    end_page = min(total_pages, page + 2)  # Az aktuális oldalhoz képest 2-vel előrébb

    query_params = {
        'page': page,
        'per_page': per_page,
        'order_by': order_by,
        'desc': desc
    }

    columns = [
        {"name": "nev", "label": "Név"},
        {"name": "iranyitoszam", "label": "Irányítószám"},
        {"name": "varos", "label": "Város"},
        {"name": "utca", "label": "Utca"},
        {"name": "hazszam", "label": "Házszám"},
        {"name": "email", "label": "E-mail"}
    ]

    return render_template(
        'customers.html',
        customers=customers,
        page=page,
        order_by=order_by,
        desc=desc,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        query_params=query_params,
        columns=columns
    )



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
    
    # Fetch customer details
    customer = conn.execute('SELECT * FROM customers WHERE email = ?', (email,)).fetchone()
    if not customer:
        flash('A törlés nem sikerült, ügyfél nem található!', 'error')
        conn.close()
        return redirect(url_for('customers'))

    # Check for active orders
    active_orders = conn.execute('''
        SELECT id 
        FROM orders 
        WHERE customer_id = ? AND teljesitve = 0
    ''', (customer['id'],)).fetchall()

    if active_orders:
        flash('Nem lehet törölni az ügyfelet, mert van befejezetlen rendelése!', 'error')
        conn.close()
        return redirect(url_for('customers'))

    # Proceed to delete the customer
    conn.execute('DELETE FROM customers WHERE email = ?', (email,))
    conn.commit()
    conn.close()
    flash('Ügyfél sikeresen törölve!', 'success')
    return redirect(url_for('customers'))


@app.route('/orders')
def orders():
    per_page = int(request.args.get('per_page', 10))  # Egy oldalon megjelenő elemek száma
    page = int(request.args.get('page', 1))  # Az aktuális oldal lekérése (alapértelmezett: 1)
    offset = (page - 1) * per_page  # Az eltolás számítása
    order_by = str(request.args.get('order_by', 'order_id'))
    desc = request.args.get('desc', 'false').lower() in ('true', '1')

    valid_columns = {'order_id', 
                     'customer_name', 
                     'total_quantity', 
                     'total_weight', 
                     'orders.lezarva', 
                     'orders.teljesitve'}
    if order_by not in valid_columns:
        raise ValueError("Invalid column name for ordering.")  # Elkerüljük az SQL injection-t
    if desc:
        descending = 'DESC'
    else:
        descending = ''

    conn = get_db_connection()
    # Query to aggregate order details
    orders = conn.execute(f'''
        SELECT 
            orders.id AS order_id, 
            customers.nev AS customer_name, 
            SUM(orders.mennyiseg) AS total_quantity, 
            SUM(orders.mennyiseg * products.suly) AS total_weight,
            orders.lezarva, 
            orders.teljesitve
        FROM orders
        JOIN customers ON orders.customer_id = customers.id
        JOIN products ON orders.cikkszam = products.cikkszam
        GROUP BY orders.id, customers.nev, orders.lezarva, orders.teljesitve
        ORDER BY {order_by} {descending}
        LIMIT ? OFFSET ?
    ''', (per_page, offset)).fetchall()

    total_orders = conn.execute('SELECT COUNT(DISTINCT orders.id) FROM orders').fetchone()[0]
    conn.close()

    total_pages = (total_orders + per_page - 1) // per_page  # Összes oldal száma

    # Számítsuk ki az oldalszámok tartományát
    start_page = max(1, page - 2)  # Az aktuális oldalhoz képest 2-vel hátrébb
    end_page = min(total_pages, page + 2)  # Az aktuális oldalhoz képest 2-vel előrébb

    query_params = {
        'page': page,
        'per_page': per_page,
        'order_by': order_by,
        'desc': desc
    }

    columns = [
        {"name": "order_id", "label": "Order ID"},
        {"name": "customer_name", "label": "Megrendelő"},
        {"name": "total_quantity", "label": "Mennyiség"},
        {"name": "total_weight", "label": "Összsúly"},
        {"name": "orders.lezarva", "label": "Lezárva"},
        {"name": "orders.teljesitve", "label": "Teljesítve"}
    ]

    return render_template(
        'orders.html',
        orders=orders,
        page=page,
        order_by=order_by,
        desc=desc,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        query_params=query_params,
        columns=columns
    )


@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        email = request.form['email']
        cikkszam = request.form['cikkszam']
        mennyiseg = int(request.form['mennyiseg'])
        order_id = request.form.get('order_id')  # New field for order number
        lezarva = 1 if 'lezarva' in request.form else 0
        teljesitve = 1 if 'teljesitve' in request.form else 0

        conn = get_db_connection()
        # Check if the customer exists
        customer = conn.execute('SELECT id FROM customers WHERE email = ?', (email,)).fetchone()
        product_exists = conn.execute('SELECT cikkszam FROM products WHERE cikkszam = ?', (cikkszam,)).fetchone()

        if not customer:
            flash('Hiba: Az ügyfél email nem létezik!', 'error')
        elif not product_exists:
            flash('Hiba: A megadott cikkszám nem létezik!', 'error')
        else:
            customer_id = customer['id']

            if order_id:
                # Check if the order ID exists and belongs to the customer
                existing_order = conn.execute('SELECT id FROM orders WHERE id = ? AND customer_id = ? AND (teljesitve = 0 OR teljesitve IS NULL)', (order_id, customer_id)).fetchone()
                if not existing_order:
                    flash('Hiba: A megadott rendelési szám nem aktív vagy nem tartozik ehhez az ügyfélhez!', 'error')
                    conn.close()
                    return redirect(url_for('add_order'))
            else:
                # Generate a new unique order_id
                order_id = conn.execute('SELECT IFNULL(MAX(id), 0) + 1 AS new_order_id FROM orders').fetchone()['new_order_id']
                conn.execute('''
                    INSERT INTO orders (id, customer_id, cikkszam, mennyiseg, lezarva, teljesitve)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (order_id, customer_id, cikkszam, mennyiseg, lezarva, teljesitve))

            # Get total available stock with order_id IS NULL
            available_stock = conn.execute('''
                SELECT id, cikkszam, mennyiseg, lokacio
                FROM stock
                WHERE cikkszam = ? AND order_id IS NULL
                ORDER BY mennyiseg DESC
            ''', (cikkszam,)).fetchall()

            total_available = sum(item['mennyiseg'] for item in available_stock)

            if total_available < mennyiseg:
                flash(f'Hiba: Nincs elegendő szabad készlet! Jelenlegi szabad készlet: {total_available}', 'error')
            else:
                # Update stock table
                remaining_quantity = mennyiseg
                for stock_item in available_stock:
                    if remaining_quantity == 0:
                        break
                    if stock_item['mennyiseg'] <= remaining_quantity:
                        # Reserve the original stock by setting mennyiseg to 0
                        conn.execute('''
                            UPDATE stock
                            SET mennyiseg = 0
                            WHERE id = ?
                        ''', (stock_item['id'],))

                        # Check if the cikkszam, lokacio, and order_id combination already exists
                        existing_stock = conn.execute('''
                            SELECT mennyiseg
                            FROM stock
                            WHERE cikkszam = ? AND lokacio = ? AND order_id = ?
                        ''', (stock_item['cikkszam'], stock_item['lokacio'], order_id)).fetchone()

                        if existing_stock:
                            # Update the quantity if the combination exists
                            new_quantity = existing_stock['mennyiseg'] + stock_item['mennyiseg']
                            conn.execute('''
                                UPDATE stock
                                SET mennyiseg = ?
                                WHERE cikkszam = ? AND lokacio = ? AND order_id = ?
                            ''', (new_quantity, stock_item['cikkszam'], stock_item['lokacio'], order_id))
                        else:
                            # Add a new row if the combination does not exist
                            conn.execute('''
                                INSERT INTO stock (cikkszam, lokacio, mennyiseg, order_id)
                                VALUES (?, ?, ?, ?)
                            ''', (stock_item['cikkszam'], stock_item['lokacio'], stock_item['mennyiseg'], order_id))

                        # Deduct the stock item quantity from the remaining quantity
                        remaining_quantity -= stock_item['mennyiseg']

                    else:
                        # Deduct partial stock and update remaining stock
                        conn.execute('''
                            UPDATE stock
                            SET mennyiseg = mennyiseg - ?
                            WHERE id = ?
                        ''', (remaining_quantity, stock_item['id']))
                        # Check if the cikkszam, lokacio, and order_id combination already exists
                        existing_stock = conn.execute('''
                            SELECT mennyiseg
                            FROM stock
                            WHERE cikkszam = (SELECT cikkszam FROM stock WHERE id = ?)
                            AND lokacio = (SELECT lokacio FROM stock WHERE id = ?)
                            AND order_id = ?
                        ''', (stock_item['id'], stock_item['id'], order_id)).fetchone()

                        if existing_stock:
                            # Update the quantity if the combination exists
                            new_quantity = existing_stock['mennyiseg'] + remaining_quantity
                            conn.execute('''
                                UPDATE stock
                                SET mennyiseg = ?
                                WHERE cikkszam = (SELECT cikkszam FROM stock WHERE id = ?)
                                AND lokacio = (SELECT lokacio FROM stock WHERE id = ?)
                                AND order_id = ?
                            ''', (new_quantity, stock_item['id'], stock_item['id'], order_id))
                        else:
                            # Add a new row if the combination does not exist
                            conn.execute('''
                                INSERT INTO stock (cikkszam, lokacio, mennyiseg, order_id)
                                SELECT cikkszam, lokacio, ?, ?
                                FROM stock
                                WHERE id = ?
                            ''', (remaining_quantity, order_id, stock_item['id']))

                        # Deduct remaining quantity as it has been fully assigned
                        remaining_quantity = 0


                conn.commit()
                if request.form.get('order_id'):
                    flash('Megrendelés sikeresen frissítve és készlet frissítve!', 'success')
                else:
                    flash('Új megrendelés sikeresen hozzáadva és készlet frissítve!', 'success')

        conn.close()
        return redirect(url_for('orders'))

    return render_template('add_order.html')






@app.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    conn = get_db_connection()

    try:
        # Fetch the stock items associated with the order
        allocated_stock = conn.execute('''
            SELECT id, mennyiseg, cikkszam, lokacio
            FROM stock
            WHERE order_id = ?
        ''', (order_id,)).fetchall()

        # Restore the stock by setting order_id to NULL
        for stock_item in allocated_stock:
            conn.execute('''
                UPDATE stock
                SET order_id = NULL
                WHERE id = ?
            ''', (stock_item['id'],))

        # Delete the order
        conn.execute('DELETE FROM orders WHERE id = ?', (order_id,))
        conn.commit()
        flash('Megrendelés sikeresen törölve és a készlet visszaállítva!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Hiba történt a törlés során: {str(e)}', 'error')
    finally:
        conn.close()

    return redirect(url_for('orders'))



@app.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    lezarva = 'lezarva' in request.form
    teljesitve = 'teljesitve' in request.form

    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()

    if teljesitve and not order['lezarva']:
        # If the order is not closed, it cannot be marked as complete
        flash('A rendelést először le kell zárni, mielőtt teljesíteni lehet!', 'error')
        conn.close()
        return redirect(url_for('orders'))

    # Update the order status
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
    per_page = int(request.args.get('per_page', 10))  # Egy oldalon megjelenő elemek száma
    page = int(request.args.get('page', 1))  # Az aktuális oldal lekérése (alapértelmezett: 1)
    offset = (page - 1) * per_page  # Az eltolás számítása
    order_by = str(request.args.get('order_by', 'products.cikkszam'))
    desc = request.args.get('desc', 'false').lower() in ('true', '1')

    valid_columns = {'stock.id', 'products.cikkszam', 'products.nev', 'stock.lokacio', 'total_mennyiseg', 'mennyiseg_null'}
    if order_by not in valid_columns:
        raise ValueError("Invalid column name for ordering.") #Elkerüljük az SQL injection-t
    if desc:
        descending = 'DESC'
    if not desc:
        descending = ''

    conn = get_db_connection()
    stock = conn.execute(f'''SELECT 
                                stock.id, 
                                products.cikkszam, 
                                products.nev, 
                                stock.lokacio, 
                                (
                                    SELECT SUM(s.mennyiseg) 
                                    FROM stock s 
                                    LEFT JOIN orders o ON s.order_id = o.id
                                    WHERE s.cikkszam = stock.cikkszam 
                                    AND s.lokacio = stock.lokacio 
                                    AND (o.teljesitve IS NULL OR o.teljesitve = 0)
                                ) AS total_mennyiseg,
                                (
                                    SELECT SUM(s.mennyiseg) 
                                    FROM stock s 
                                    LEFT JOIN orders o ON s.order_id = o.id
                                    WHERE s.cikkszam = stock.cikkszam 
                                    AND s.lokacio = stock.lokacio 
                                    AND s.order_id IS NULL
                                ) AS mennyiseg_null
                            FROM stock
                            JOIN products ON stock.cikkszam = products.cikkszam
                            WHERE stock.order_id IS NULL
                            ORDER BY {order_by} {descending} 
                            LIMIT ? OFFSET ?''', (per_page, offset) ).fetchall()
    total_products = conn.execute('SELECT COUNT(*) FROM stock').fetchone()[0]
    conn.close()

    total_pages = (total_products + per_page - 1) // per_page  # Összes oldal száma

    # Számítsuk ki az oldalszámok tartományát
    start_page = max(1, page - 2)  # Az aktuális oldalhoz képest 2-vel hátrébb
    end_page = min(total_pages, page + 2)  # Az aktuális oldalhoz képest 2-vel előrébb

    query_params = {
        'page': page,
        'per_page': per_page,
        'order_by': order_by,
        'desc': desc
    }

    columns = [
        {"name": "products.cikkszam", "label": "Cikkszám"},
        {"name": "products.nev", "label": "Termék"},
        {"name": "stock.lokacio", "label": "Lokáció"},
        {"name": "total_mennyiseg", "label": "Mennyiség"},
        {"name": "mennyiseg_null", "label": "Szabad M."}
    ]

    return render_template(
        'stock.html',
        stock=stock,
        page=page,
        order_by=order_by,
        desc=desc,
        total_pages=total_pages,
        start_page=start_page,
        end_page=end_page,
        query_params=query_params,
        columns=columns
    )


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        cikkszam = request.form['cikkszam']
        lokacio = request.form['lokacio']
        mennyiseg = int(request.form['mennyiseg'])

        conn = get_db_connection()

        # Check if the product exists in the products table
        product_exists = conn.execute('SELECT * FROM products WHERE cikkszam = ?', (cikkszam,)).fetchone()

        if not product_exists:
            # If the cikkszam doesn't exist in the products table
            flash("Hibás cikkszám! Ez a termék nem létezik.", "error")
            conn.close()
            return redirect(url_for('stock'))


        # If order_id is NULL, check only cikkszam and lokacio
        existing_stock = conn.execute('SELECT * FROM stock WHERE cikkszam = ? AND lokacio = ? AND order_id IS NULL',
                                    (cikkszam, lokacio)).fetchone()


        if existing_stock:
            # If it exists, increase the quantity
            new_mennyiseg = existing_stock['mennyiseg'] + mennyiseg
            conn.execute('UPDATE stock SET mennyiseg = ? WHERE cikkszam = ? AND lokacio = ? AND order_id IS NULL',
                         (new_mennyiseg, cikkszam, lokacio))
            flash("A mennyiség frissítve lett!", "success")
        else:
            # If not, add a new record
            conn.execute('INSERT INTO stock (cikkszam, lokacio, mennyiseg, order_id) VALUES (?, ?, ?, NULL)',
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


@app.route('/product/<cikkszam>')
def product_details(cikkszam):
    conn = get_db_connection()
    product = conn.execute(
        'SELECT * FROM products WHERE cikkszam = ?',
        (cikkszam,)
    ).fetchone()
    stock = conn.execute(
        '''SELECT stock.id, stock.lokacio, 
                            (SELECT SUM(mennyiseg) 
                            FROM stock s
                            WHERE s.cikkszam = ? AND s.lokacio = stock.lokacio) AS total_mennyiseg,
                            (SELECT SUM(mennyiseg) 
                            FROM stock s
                            WHERE s.cikkszam = ? AND s.lokacio = stock.lokacio  AND s.order_id IS NULL) AS mennyiseg_null
                            FROM products JOIN stock ON stock.cikkszam = products.cikkszam
                            WHERE stock.order_id IS NULL''',
        (cikkszam, cikkszam)
    ).fetchall()
    conn.close()

    #if product is None:
    #    abort(404, description="Product not found")

    return render_template(
        'product_details.html',
        product=product,
        stock=stock
    )

@app.route('/order_details/<int:order_id>', methods=['GET'])
def order_details(order_id):
    conn = get_db_connection()

    # Get order and customer information
    order_info = conn.execute('''
        SELECT SUM(stock.mennyiseg) AS total_quant,
                              SUM(products.ar * stock.mennyiseg) AS total_price,
                              SUM(products.suly * stock.mennyiseg) AS total_weight
        FROM stock LEFT JOIN products ON stock.cikkszam = products.cikkszam
                              LEFT JOIN orders ON stock.cikkszam = orders.cikkszam
                              LEFT JOIN customers ON customers.id = orders.customer_id
        WHERE order_id = ?
        


    ''', (order_id,)).fetchone()

    # Get product details for the order
    product_details = conn.execute('''
        SELECT 
            products.nev AS product_name,
            products.cikkszam,
            products.ar AS price,
            products.suly AS weight,
            stock.mennyiseg AS quantity,
            stock.lokacio AS lokacio
        FROM stock
        JOIN products ON stock.cikkszam = products.cikkszam
        WHERE stock.order_id = ?
        ORDER BY lokacio
    ''', (order_id,)).fetchall()


    conn.close()

    if not order_info:
        flash('Hiba: A rendelési szám nem létezik!', 'error')
        return redirect(url_for('orders'))

    return render_template(
        'order_details.html',
        order_info=order_info,
        product_details=product_details
    )




if __name__ == '__main__':
    app.run(debug=True)

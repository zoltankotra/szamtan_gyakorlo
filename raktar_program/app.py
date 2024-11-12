from flask import Flask, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite adatbázis kapcsolat
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/termekek')
def termekek():
    conn = get_db_connection()
    termekek = conn.execute('SELECT * FROM termekek').fetchall()
    conn.close()
    return render_template('termekek.html', termekek=termekek)

@app.route('/ugyfelek')
def ugyfelek():
    conn = get_db_connection()
    ugyfelek = conn.execute('SELECT * FROM ugyfelek').fetchall()
    conn.close()
    return render_template('ugyfelek.html', ugyfelek=ugyfelek)

@app.route('/megrendelesek')
def megrendelesek():
    conn = get_db_connection()
    megrendelesek = conn.execute('SELECT * FROM megrendelesek').fetchall()
    conn.close()
    return render_template('megrendelesek.html', megrendelesek=megrendelesek)

if __name__ == '__main__':
    app.run(debug=True)

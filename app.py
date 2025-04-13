from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random
import string

app = Flask(__name__)

DATABASE = 'urls.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def close_db(conn):
    if conn:
        conn.close()

def init_db():
    conn = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    close_db(conn)

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def generate_short_code(length=6):
    # Generate a random string of alphanumeric characters
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def insert_url(long_url, short_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (long_url, short_code))
    conn.commit()
    close_db(conn)

def fetch_long_url(short_code):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    close_db(conn)
    return result['long_url'] if result else None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_code = generate_short_code()
    insert_url(long_url, short_code)
    short_url = url_for('redirect_short_code', short_code=short_code, _external=True)
    return render_template('result.html', short_url=short_url, long_url=long_url)

@app.route('/<short_code>')
def redirect_short_code(short_code):
    long_url = fetch_long_url(short_code)
    if long_url:
        return redirect(long_url, code=302)
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
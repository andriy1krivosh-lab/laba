import sqlite3
DB_NAME = 'db.sqlite'

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # feedback
    c.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # products
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT
    )
    ''')

    # clients (level2)
    c.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT
    )
    ''')

    # orders & items
    c.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        customer_name TEXT,
        status TEXT DEFAULT 'new',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(order_id) REFERENCES orders(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    ''')

    # users for simple role system (level3)
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'client' -- 'admin' or 'client'
    )
    ''')

    conn.commit()

    # seed sample data if empty
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        products = [
            ('Yamaha R1', 18999, 'Sport'),
            ('Yamaha MT-07', 7599, 'Naked'),
            ('Yamaha Tenere 700', 9999, 'Adventure'),
            ('Yamaha XSR900', 8999, 'Retro'),
            ('Yamaha Tracer 9', 11499, 'Touring')
        ]
        c.executemany('INSERT INTO products (title, price, category) VALUES (?, ?, ?)', products)
        conn.commit()

    # create default admin if not exists
    c.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", ('admin', 'admin', 'admin'))
        conn.commit()

    conn.close()

# ----------------------- feedback CRUD -----------------------
def add_feedback(name, message):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO feedback (name, message) VALUES (?, ?)', (name, message))
    conn.commit()
    conn.close()

def get_feedbacks():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM feedback ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_feedback(feedback_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM feedback WHERE id=?', (feedback_id,))
    conn.commit()
    conn.close()

# ----------------------- products -----------------------
def get_products():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    rows = c.fetchall()
    conn.close()
    return rows

def get_product(product_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id=?', (product_id,))
    row = c.fetchone()
    conn.close()
    return row

def add_product(title, price, category=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO products (title, price, category) VALUES (?, ?, ?)', (title, price, category))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    conn.close()

# ----------------------- clients -----------------------
def get_clients():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM clients')
    rows = c.fetchall()
    conn.close()
    return rows

def add_client(name, email, phone):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
    conn.commit()
    conn.close()

# ----------------------- orders -----------------------
def add_order(client_id, customer_name, items):  # items = [(product_id, qty), ...]
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO orders (client_id, customer_name) VALUES (?, ?)', (client_id, customer_name))
    order_id = c.lastrowid
    for pid, qty in items:
        c.execute('INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)', (order_id, pid, qty))
    conn.commit()
    conn.close()
    return order_id

def get_orders():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM orders ORDER BY created_at DESC')
    orders = c.fetchall()
    all_orders = []
    for o in orders:
        c.execute('SELECT oi.quantity, p.title, p.price FROM order_items oi JOIN products p ON oi.product_id=p.id WHERE oi.order_id=?', (o['id'],))
        items = c.fetchall()
        all_orders.append({'order': o, 'items': items})
    conn.close()
    return all_orders

def update_order_status(order_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE orders SET status=? WHERE id=?', (status, order_id))
    conn.commit()
    conn.close()

# ----------------------- users (simple auth) -----------------------
def get_user_by_username(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()
    return user

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import get_feedbacks, delete_feedback, get_products, add_product, delete_product, get_orders, update_order_status, get_clients, add_client, get_user_by_username

admin_bp = Blueprint('admin', __name__)

def admin_required():
    return session.get('user_role') == 'admin'

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username)
        if user and user['password'] == password and user['role'] == 'admin':
            session['user'] = username
            session['user_role'] = 'admin'
            return redirect(url_for('admin.dashboard'))
        flash('Невірні облікові дані', 'error')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
def dashboard():
    if not admin_required():
        return redirect(url_for('admin.login'))
    return render_template('admin/index.html')

@admin_bp.route('/feedbacks')
def admin_feedbacks():
    if not admin_required():
        return redirect(url_for('admin.login'))
    items = get_feedbacks()
    return render_template('admin/feedbacks.html', items=items)

@admin_bp.route('/feedbacks/delete/<int:fid>', methods=['POST'])
def admin_delete_feedback(fid):
    if not admin_required():
        return redirect(url_for('admin.login'))
    delete_feedback(fid)
    flash('Відгук видалено', 'success')
    return redirect(url_for('admin.admin_feedbacks'))

@admin_bp.route('/products', methods=['GET', 'POST'])
def admin_products():
    if not admin_required():
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        title = request.form.get('title')
        price = float(request.form.get('price', 0))
        category = request.form.get('category')
        add_product(title, price, category)
        flash('Товар додано', 'success')
        return redirect(url_for('admin.admin_products'))
    products = get_products()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/delete/<int:pid>', methods=['POST'])
def admin_delete_product(pid):
    if not admin_required():
        return redirect(url_for('admin.login'))
    delete_product(pid)
    flash('Товар видалено', 'success')
    return redirect(url_for('admin.admin_products'))

@admin_bp.route('/orders', methods=['GET', 'POST'])
def admin_orders():
    if not admin_required():
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        oid = int(request.form.get('order_id'))
        status = request.form.get('status')
        update_order_status(oid, status)
        flash('Статус оновлено', 'success')
        return redirect(url_for('admin.admin_orders'))
    orders = get_orders()
    return render_template('admin/orders.html', orders=orders)

@admin_bp.route('/clients', methods=['GET', 'POST'])
def admin_clients():
    if not admin_required():
        return redirect(url_for('admin.login'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        add_client(name, email, phone)
        flash('Клієнта додано', 'success')
        return redirect(url_for('admin.admin_clients'))
    clients = get_clients()
    return render_template('admin/clients.html', clients=clients)

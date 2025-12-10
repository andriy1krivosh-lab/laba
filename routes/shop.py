from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import get_products, add_order, get_product

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/shop')
def shop_home():
    products = get_products()
    return render_template('shop.html', products=products)

@shop_bp.route('/order', methods=['POST'])
def place_order():
    name = request.form.get('name', 'Гість')
    client_id = request.form.get('client_id') or None
    product_id = int(request.form.get('product_id'))
    qty = int(request.form.get('quantity', 1))
    add_order(client_id, name, [(product_id, qty)])
    flash('Замовлення прийнято!', 'success')
    return redirect(url_for('shop.shop_home'))

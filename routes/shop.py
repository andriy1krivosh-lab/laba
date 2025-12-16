from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import get_products, add_order, get_product

shop_bp = Blueprint('shop', __name__)

# ------------------------------
# Ініціалізація корзини
# ------------------------------
def init_cart():
    if "cart" not in session:
        session["cart"] = []

# ------------------------------
# Головна сторінка магазину
# ------------------------------
@shop_bp.route('/')
def shop_home():
    rows = get_products()

    products = []
    for p in rows:
        products.append({
            "id": p["id"],
            "title": p["title"],
            "price": p["price"],
            "category": p["category"],
            # автоматично підставляє moto1.jpg, moto2.jpg ...
            "image": f"images/products/moto{p['id']}.jpg"
        })

    return render_template('shop.html', products=products)

# ------------------------------
# Перегляд корзини
# ------------------------------
@shop_bp.route('/cart')
def cart():
    init_cart()
    cart_items = session["cart"]
    total = sum(item["price"] * item["quantity"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

# ------------------------------
# Додати товар у корзину
# ------------------------------
@shop_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    init_cart()
    product_id = int(request.form.get("product_id"))
    quantity = int(request.form.get("quantity", 1))
    product = get_product(product_id)
    if not product:
        flash("Товар не знайдено!", "error")
        return redirect(url_for('shop.shop_home'))

    # Якщо товар вже є у корзині — додаємо кількість
    for item in session["cart"]:
        if item["id"] == product_id:
            item["quantity"] += quantity
            session.modified = True
            break
    else:
        session["cart"].append({
            "id": product["id"],
            "title": product["title"],
            "price": product["price"],
            "quantity": quantity
        })
        session.modified = True

    flash("Товар додано в корзину!", "success")
    return redirect(url_for('shop.shop_home'))

# ------------------------------
# Оновити кількість у корзині
# ------------------------------
@shop_bp.route('/update-cart', methods=['POST'])
def update_cart():
    init_cart()
    product_id = int(request.form.get("product_id"))
    quantity = int(request.form.get("quantity"))
    for item in session["cart"]:
        if item["id"] == product_id:
            item["quantity"] = max(1, quantity)
            session.modified = True
            break
    flash("Кількість оновлено!", "success")
    return redirect(url_for('shop.cart'))

# ------------------------------
# Видалити товар з корзини
# ------------------------------
@shop_bp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    init_cart()
    product_id = int(request.form.get("product_id"))
    session["cart"] = [i for i in session["cart"] if i["id"] != product_id]
    session.modified = True
    flash("Товар видалено!", "success")
    return redirect(url_for('shop.cart'))

# ------------------------------
# Оформлення замовлення
# ------------------------------
@shop_bp.route('/checkout', methods=['POST'])
def checkout():
    init_cart()
    cart_items = session["cart"]

    if not cart_items:
        flash("Корзина порожня!", "error")
        return redirect(url_for('shop.shop_home'))

    # Використовуємо "Гість" як замовника
    customer_name = "Гість"
    client_id = None

    # Підготуємо список товарів для add_order
    items = [(item["id"], item["quantity"]) for item in cart_items]

    # Додаємо замовлення в базу
    add_order(client_id, customer_name, items)

    # Очищаємо корзину
    session["cart"] = []
    session.modified = True

    flash("Замовлення прийнято! Дякуємо.", "success")
    return redirect(url_for('shop.shop_home'))

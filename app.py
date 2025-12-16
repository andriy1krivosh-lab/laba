from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from models import init_db, get_product
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp
from routes.api_feedback import api_feedback_bp  # новий Blueprint для API

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_strong_secret_in_prod'

# ------------------------------
# Register blueprints
# ------------------------------
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(shop_bp, url_prefix='/shop')
app.register_blueprint(api_feedback_bp, url_prefix='/api/v1/feedback')  # API


# ------------------------------
# Головні сторінки
# ------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

# ------------------------------
# КОРЗИНА
# ------------------------------
def init_cart():
    if "cart" not in session:
        session["cart"] = []

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    init_cart()
    product_id = int(request.form.get("product_id"))
    quantity = int(request.form.get("quantity", 1))
    product = get_product(product_id)
    if not product:
        flash("Товар не знайдено!", "error")
        return redirect(url_for('shop.shop_home'))
    for item in session["cart"]:
        if item["id"] == product_id:
            item["quantity"] += quantity
            session.modified = True
            break
    else:
        session["cart"].append({
            "id": product_id,
            "title": product["title"],
            "price": product["price"],
            "quantity": quantity
        })
        session.modified = True
    flash("Товар додано в корзину!", "success")
    return redirect(url_for('shop.shop_home'))

@app.route('/cart')
def cart():
    init_cart()
    cart_items = session["cart"]
    total = sum(item["price"] * item["quantity"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

@app.route('/update-cart', methods=['POST'])
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
    return redirect(url_for('cart'))

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    init_cart()
    product_id = int(request.form.get("product_id"))
    session["cart"] = [i for i in session["cart"] if i["id"] != product_id]
    session.modified = True
    flash("Товар видалено!", "success")
    return redirect(url_for('cart'))

# ------------------------------
# Друк доступних маршрутів (для перевірки)
# ------------------------------
print("Доступні маршрути:")
print(app.url_map)

# ------------------------------
# Запуск
# ------------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

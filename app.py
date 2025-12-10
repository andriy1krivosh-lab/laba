from flask import Flask, render_template, redirect, url_for, session
from models import init_db
from routes.feedback import feedback_bp
from routes.admin import admin_bp
from routes.shop import shop_bp

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_strong_secret_in_prod'

# register blueprints
app.register_blueprint(feedback_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(shop_bp)

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

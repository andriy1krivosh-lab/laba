from flask import Flask, render_template

app = Flask(__name__)

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Сторінка "Про нас"
@app.route('/about')
def about():
    return render_template('about.html')

# Сторінка каталогу
@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

# Сторінка контактів
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)

# Звіт з лабораторної роботи 4

## Реалізація бази даних для вебпроєкту

### Інформація про команду
- Назва команди:

- Учасники:
 Кривош Андрій 

Прошек Тимофій
## Завдання

### Обрана предметна область

Предметна область — інтернет-магазин мотоциклів .

### Реалізовані вимоги

Вкажіть, які рівні завдань було виконано:

- [ ] Рівень 1: Створено базу даних SQLite з таблицею для відгуків, реалізовано базові CRUD операції, створено адмін-панель для перегляду та видалення відгуків, додано функціональність магазину з таблицями для товарів та замовлень
- [ ] Рівень 2: Створено додаткову таблицю, релевантну предметній області, реалізовано роботу з новою таблицею через адмін-панель, інтегровано функціональність у застосунок
У вебзастосунку реалізовано:

каталог мотоциклів

каталог товарів (екіпірування, шоломи, запчастини)

можливість оформлення замовлення

система збору відгуків

адмін-панель для керування товарами, замовленнями та відгуками

## Хід виконання роботи

### Підготовка середовища розробки

Опишіть процес налаштування:
Підготовка середовища розробки

Python 3.12

Встановлені бібліотеки:

Flask

SQLite

Інструменти:

VS Code

SQLite Viewer розширення

GitHub 

 ChatGpt як джерело інформації

### Структура проєкту

Наведіть структуру файлів та директорій вашого проєкту:

LABA/
├── lab-reports/
│   └── lab04-report-student-id.md
├── routes/
│   ├── __init__.py
│   ├── admin.py
│   ├── feedback.py
│   └── shop.py
├── templates/
│   ├── admin/
│   │   ├── feedbacks.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── orders.html
│   ├── about.html
│   ├── base.html
│   ├── catalog.html
│   ├── contacts.html
│   ├── feedback.html
│   ├── index.html
│   ├── shop.html
├── app.py
├── models.py
├── db.sqlite
├── README.md
└── venv/


### Проектування бази даних

#### Схема бази даних

Опишіть структуру вашої бази даних:
Таблиця "feedback":
- id (INTEGER, PRIMARY KEY AUTOINCREMENT)
- name (TEXT NOT NULL)
- message (TEXT NOT NULL)
- created_at (DATETIME DEFAULT CURRENT_TIMESTAMP)

Таблиця "products":
- id (INTEGER, PRIMARY KEY AUTOINCREMENT)
- title (TEXT NOT NULL)
- price (REAL NOT NULL)
- category (TEXT)

Таблиця "clients":       [Рівень 2]
- id (INTEGER, PRIMARY KEY AUTOINCREMENT)
- name (TEXT)
- email (TEXT)
- phone (TEXT)

Таблиця "orders":
- id (INTEGER, PRIMARY KEY AUTOINCREMENT)
- client_id (INTEGER, FOREIGN KEY → clients.id)
- customer_name (TEXT)
- status (TEXT DEFAULT 'new')
- created_at (DATETIME DEFAULT CURRENT_TIMESTAMP)

Таблиця "order_items":
- id (INTEGER, PRIMARY KEY AUTOINCREMENT)
- order_id (INTEGER, FOREIGN KEY → orders.id)
- product_id (INTEGER, FOREIGN KEY → products.id)
- quantity (INTEGER)





### Опис реалізованої функціональності

#### Система відгуків

Система відгуків

Користувач може залишити відгук через сторінку feedback.html

Відгук одразу записується в таблицю feedback

В адмін-панелі адміністратор може:

переглядати всі відгуки

видаляти небажані

Відображення здійснюється у admin/feedbacks.html

#### Магазин

Реалізовано основний функціонал магазину мотоциклів:

каталог товарів на catalog.html

фільтрація за категоріями (Рівень 2)

сторінка перегляду товарів

кошик (збереження через сесію)

оформлення замовлення

збереження замовлень у таблицю orders

збереження товарів замовлення у таблицю order_items

#### Адміністративна панель

Адмін-панель реалізовано у папці templates/admin.

Можливості:

перегляд усіх відгуків

перегляд замовлень

зміна статусу замовлення

додавання та редагування товарів

видалення товарів

керування категоріями 

#### Додаткова функціональність (якщо реалізовано)

Опишіть додаткові таблиці та функції, які було реалізовано для рівнів 2 та 3.

## Ключові фрагменти коду

### Ініціалізація бази даних

Наведіть код створення таблиць у файлі `models.py`:

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from models import Product, Order, Feedback
        db.create_all()

    from routes.admin import admin_bp
    from routes.shop import shop_bp
    from routes.feedback import feedback_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(feedback_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


### CRUD операції

Наведіть приклади реалізації CRUD операцій:

#### Створення (Create)

new_product = Product(title="Yamaha R1", price=500000, description="Легендарний спортбайк")
db.session.add(new_product)
db.session.commit()


#### Читання (Read)

products = Product.query.all()


#### Оновлення (Update)

product = Product.query.get(id)
product.title = "Honda CBR600RR"
product.price = 270000
db.session.commit()


#### Видалення (Delete)

product = Product.query.get(id)
db.session.delete(product)
db.session.commit()


### Маршрутизація

Наведіть приклади маршрутів для роботи з базою даних:

```python
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        add_feedback(name, email, message)
        flash('Дякуємо за ваш відгук!', 'success')
        return redirect(url_for('feedback'))
    return render_template('feedback.html')
```

### Робота зі зв'язками між таблицями

Наведіть приклад запиту з використанням JOIN для отримання пов'язаних даних:

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


## Розподіл обов'язків у команді

Опишіть внесок кожного учасника команди:

Кривош Андрій   

адмін-панель

маршрути замовлень і відгуків

верстка шаблонів

Прошек Тимофій

створення структури БД

модулі моделей

реалізація магазину та категорій

## Скріншоти

Додайте скріншоти основних функцій вашого вебзастосунку:

### Форма зворотного зв'язку

![Форма зворотного зв'язку]lab-reports\Скіншоти\форма зворотнього зв'язку.png

### Каталог товарів

![Каталог товарів]lab-reports\Скіншоти\каталог.png

### Адміністративна панель

![Адмін-панель]lab-reports\Скіншоти\admin.png

### Управління замовленнями

![Управління замовленнями]lab-reports\Скіншоти\управління замовленнями.png



## Тестування

### Сценарії тестування

Тестування

Тестували:

створення відгуків

додавання товару → відображення → замовлення

зміна статусу замовлення

видалення записів у всіх таблицях

валідацію форм

## Висновки

Опишіть:

У ході роботи:

створено повноцінну базу даних для магазину мотоциклів отримано практичні навички роботи з SQLite
реалізовано CRUD-операції для кількох сутностей створена адмін-панель
виникали труднощі з налаштуванням зв’язків між таблицями
робота виконувалась командно: один учасник працював з БД, інший — з шаблонами та маршрутизацією

Очікувана оцінка: 9-10 балів
Обґрунтування: виконано обидва рівні, реалізовано зв’язки, магазин, адмін-панель, структуру БД.
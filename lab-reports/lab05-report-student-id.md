# Лабораторна робота №5: Розробка RESTful API


### Інформація про команду
- Назва команди:

- Учасники:
Кривош Андрій 
Прошек Тимофій

### Обрана предметна область

Предметна область — інтернет-магазин мотоциклів .

## Опис проєкту
Вебзастосунок на Flask для невеликого магазину: відображення сторінок сайту, перегляд каталогу товарів, робота з корзиною (додавання/оновлення/видалення), оформлення замовлення, сторінка відгуків. Є адмін-панель для керування товарами, клієнтами, замовленнями та відгуками. Дані зберігаються у SQLite.

## Технології
- Python 3.x
- Flask
- SQLite

## Endpoints API

Endpoints (Routes) вебзастосунку
1) Головна сторінка
URL: /
Метод: GET
Опис: Відображає головну сторінку сайту.
Відповідь: HTML (index.html)
Очікуваний статус: 200 OK

2) Про нас
URL: /about
Метод: GET
Опис: Сторінка “Про нас”.
Відповідь: HTML (about.html)
Статус: 200 OK

3) Каталог
URL: /catalog
Метод: GET
Опис: Сторінка каталогу.
Відповідь: HTML (catalog.html)
Статус: 200 OK

4) Контакти
URL: /contacts
Метод: GET
Опис: Сторінка контактів.
Відповідь: HTML (contacts.html)
Статус: 200 OK
Відгуки (feedback)

5) Перегляд відгуків
URL: /feedback
Метод: GET
Опис: Виводить список відгуків з БД.
Відповідь: HTML (feedback.html)
Статус: 200 OK

6) Додати відгук
URL: /feedback/add
Метод: POST
Опис: Додає відгук (name, message) у таблицю feedback.
Тип запиту: application/x-www-form-urlencoded
Приклад запиту (form-data):
name=Анонім
message=Все супер!
Результат: Redirect на /feedback
Статус: 302 Found
Помилка: якщо message пусте → flash error і redirect на /feedback (також 302)

Магазин (Blueprint /shop)
7) Головна сторінка магазину
URL: /shop/
Метод: GET
Опис: Відображає список товарів з таблиці products.
Відповідь: HTML (shop.html)
Статус: 200 OK

8) Корзина (в shop)
URL: /shop/cart
Метод: GET
Опис: Показує товари у корзині (зберігається в session["cart"]).
Відповідь: HTML (cart.html)
Статус: 200 OK

9) Додати товар у корзину
URL: /shop/add-to-cart
Метод: POST
Опис: Додає товар у корзину в сесії.
Тип запиту: application/x-www-form-urlencoded
Поля:
product_id (int)
quantity (int, за замовчуванням 1)
Результат: Redirect на /shop/
Статус: 302 Found
Помилки:
якщо product_id не існує → flash “Товар не знайдено!” і redirect на /shop/

10) Оновити кількість у корзині
URL: /shop/update-cart
Метод: POST
Опис: Оновлює кількість товару в сесії (мінімум 1).
Поля: product_id, quantity
Результат: Redirect на /shop/cart
Статус: 302 Found

11) Видалити товар з корзини
URL: /shop/remove-from-cart
Метод: POST
Опис: Видаляє позицію з корзини в сесії.
Поля: product_id
Результат: Redirect на /shop/cart
Статус: 302 Found

12) Оформлення замовлення
URL: /shop/checkout
Метод: POST
Опис: Створює замовлення у БД: запис у orders + позиції у order_items. Після цього очищує корзину.
Результат: Redirect на /shop/
Статус: 302 Found
Помилка: якщо корзина пуста → flash “Корзина порожня!” і redirect на /shop/

Адмін-панель (Blueprint /admin)
13) Логін адміна
URL: /admin/login
Методи: GET, POST
Опис:
GET — форма логіну
POST — перевірка username/password з таблиці users (роль admin)
Поля POST: username, password
Успіх: redirect на /admin/ (302)
Невдача: flash “Невірні облікові дані” (200 з формою або redirect залежно від шаблону)

14) Вихід
URL: /admin/logout
Метод: GET
Опис: Очищає сесію та повертає на сторінку логіну.
Статус: 302 Found

15) Адмін-головна
URL: /admin/
Метод: GET
Опис: Адмін-дашборд. Якщо не адмін → redirect на /admin/login.
Статуси: 200 або 302

16) Відгуки (перегляд)
URL: /admin/feedbacks
Метод: GET
Опис: Список відгуків для адміна.
Статус: 200 або 302 якщо не адмін

17) Відгуки (видалення)
URL: /admin/feedbacks/delete/<fid>
Метод: POST
Опис: Видаляє відгук за id.
Статус: 302 Found

18) Товари (перегляд/додавання)
URL: /admin/products
Методи: GET, POST
Опис:
GET — список товарів
POST — додає товар у products
Поля POST: title, price, category
Статус: 200 або 302

19) Товари (видалення)
URL: /admin/products/delete/<pid>
Метод: POST
Опис: Видаляє товар.
Статус: 302 Found

20) Замовлення (перегляд/оновлення статусу)
URL: /admin/orders
Методи: GET, POST
Опис:
GET — перегляд замовлень
POST — оновлення статусу (new/…)
Поля POST: order_id, status
Статус: 200 або 302

21) Клієнти (перегляд/додавання)
URL: /admin/clients
Методи: GET, POST
Опис:
GET — список клієнтів
POST — додає клієнта у clients
Поля POST: name, email, phone
Статус: 200 або 302


### Результати тестування (Postman або браузер)
Сценарій 1: Перевірка публічних сторінок
Мета: Переконатися, що сторінки відкриваються.
Кроки: GET /, GET /about, GET /catalog, GET /contacts
Очікування: 200 OK

Сценарій 2: Додати відгук
Мета: Перевірити додавання в БД.
Кроки: POST /feedback/add з name, message
Очікування: 302 redirect → потім GET /feedback показує новий відгук

Сценарій 3: Додати товар у корзину
Мета: Перевірити роботу session cart.
Кроки: POST /shop/add-to-cart (product_id=1, quantity=2) → GET /shop/cart
Очікування: 302, а потім у корзині є товар

Сценарій 4: Checkout
Мета: Перевірити створення замовлення.
Кроки: Додати товар у корзину → POST /shop/checkout
Очікування: 302 + корзина очищена, в адмінці з’явився order

Сценарій 5: Адмін-логін
Мета: Доступ до адмінки тільки після логіну.
Кроки: GET /admin/ без логіну → redirect на login; потім POST /admin/login (admin/admin)
Очікування: redirect на /admin/, доступ до сторінок

## Обробка помилок
200 OK — сторінки успішно відкриваються (HTML).
302 Found — після POST-запитів виконується redirect (після додавання/видалення/оновлення).
Доступ до адмінки без прав: redirect на /admin/login (фактично контроль доступу через session['user_role']).
Валідація:
порожнє повідомлення у відгуках → flash error + redirect
неіснуючий товар → flash error + redirect
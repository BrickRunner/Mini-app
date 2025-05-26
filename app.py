from flask import Flask, flash, render_template, request, redirect, url_for, render_template, send_from_directory, session, jsonify, render_template_string
from datetime import datetime
from flask_cors import CORS
from functools import wraps
import uuid
import random
from models import db, Order, OrderItem, Product, Cart, User, Favorite, BasketItem


app = Flask(__name__, template_folder='.')
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ ВЫНЕСЕНА ВНЕ ПАРАМЕТРОВ Flask
app.config.from_pyfile('config.py')
app.secret_key = 'секретный_ключ_сюда'  # используй os.urandom(24) или UUID

# Подключаем базу данных
db.init_app(app)
with app.app_context():
    db.create_all()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Пожалуйста, войдите в систему')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if not phone or not password or not password_confirm:
            flash('Пожалуйста, заполните все поля')
            return redirect(url_for('register'))

        if password != password_confirm:
            flash('Пароли не совпадают')
            return redirect(url_for('register'))

        if User.query.filter_by(phone_number=phone).first():
            flash('Пользователь с таким номером уже зарегистрирован')
            return redirect(url_for('register'))

        user = User(phone_number=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        flash('Регистрация прошла успешно')
        return redirect(url_for('account'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone')
        password = request.form.get('password')

        user = User.query.filter_by(phone_number=phone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Вы успешно вошли в систему')
            return redirect(url_for('account'))
        else:
            flash('Неверный номер телефона или пароль')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/account')
@login_required
def account():
    user = User.query.get(session['user_id'])
    return render_template('account.html', user=user)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Вы вышли из системы')
    return redirect(url_for('login'))

@app.route("/main")
def main():
    return render_template("main.html")

@app.route("/offer")
def offer():
    return render_template("offer.html")

@app.route('/admin')
def admin_panel():
    products = Product.query.all()
    return render_template('admin_panel.html', products=products)

@app.route('/all_products')
def all_products():
    # Проверим, какие товары есть в базе данных
    products = Product.query.all()
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('all_products.html', products=products)

@app.route('/clothes')
def clothes():
    # Проверим, какие товары есть в базе данных
    products = Product.query.filter_by(tupe='clothes').all()
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('clothes.html', products=products)

@app.route('/acessories')
def acessories():
    # Проверим, какие товары есть в базе данных
    products = Product.query.filter_by(tupe='acessories').all()
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('acessories.html', products=products)

@app.route('/shoes')
def shoes():
    # Проверим, какие товары есть в базе данных
    products = Product.query.filter_by(tupe='shoes').all()
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('shoes.html', products=products)

@app.route('/admin_panel-deleteProduct')
def admin_panel_deleteProduct():
    products = Product.query.all()
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('admin_panel-deleteProduct.html', products=products)

@app.route('/admin_panel-stock')
def admin_panel_stock():
    products = Product.query.all()
    user_id = session.get('user_id')
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('admin_panel-stock.html', products=products)

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('admin_panel'))  # Перенаправление на панель администратора


@app.route('/admin_panel_addProduct')
def admin_panel_addProduct():
    return render_template('admin_panel-addProduct.html')


@app.route('/admin/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Получаем данные из формы
        new_product = Product(
            title=request.form['title'],
            description=request.form['description'],
            price_1=float(request.form['price_1']),
            price_2=float(request.form['price_2']),
            size=request.form['size'],
            tupe=request.form['tupe'],
            for_what=request.form['for_what'],
            special=request.form['special'],
            stock=int(request.form['stock']),
            image_url=request.form['image_url']
        )
        db.session.add(new_product)
        db.session.commit()
        print('Товар добавлен')
        return redirect(url_for('admin_panel'))  # перенаправляем после добавления

    return render_template('admin_panel-addProduct.html')

@app.context_processor
def inject_user_favorites():
    user_id = session.get('user_id')
    if not user_id:
        return dict(user_fav_ids=set())
    user_fav_ids = {fav.product_id for fav in Favorite.query.filter_by(user_id=user_id).all()}
    return dict(user_fav_ids=user_fav_ids)


@app.route('/toggle_favorite', methods=['POST'])
def toggle_favorite():
    user_id = session.get('user_id')  # или получить из токена
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    product_id = data.get('product_id')

    favorite = Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_fav = Favorite(user_id=user_id, product_id=product_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({'status': 'added'})

@app.route('/my-orders')
def my_orders():
    telegram_id = session.get('telegram_id')
    if not telegram_id:
        return redirect('/')

    orders = Order.query.filter_by(telegram_id=telegram_id).all()
    return render_template('my_orders.html', orders=orders)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        try:
            order = Order(
                session_id=request.cookies.get('session_id'),
                surname=request.form['surname'],
                name=request.form['name'],
                name_1=request.form['name_1'],
                payment=request.form['payment'],
                delivery=request.form['delivery'],
                phone=request.form['phone'],
                email=request.form['email'],
                address=request.form['address'],
                created_at=datetime.utcnow()
            )

            # Здесь должен быть список товаров из корзины
            # Пример временного списка:
            cart_items = [
                {'product_id': 1, 'quantity': 2},
                {'product_id': 3, 'quantity': 1},
            ]

            for item in cart_items:
                product = Product.query.get(item['product_id'])
                if product:
                    order_item = OrderItem(
                        product_id=product.id,
                        quantity=item['quantity'],
                        product=product
                    )
                    order.items.append(order_item)

            db.session.add(order)
            db.session.commit()
            flash('Заказ успешно оформлен!')
            return redirect('/checkout')

        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при оформлении заказа: {e}')
            return redirect('/checkout')

    return render_template('checkout.html')


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    session_id = session.get('session_id')

    if not session_id:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id

    cart_item = Cart.query.filter_by(session_id=session_id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(session_id=session_id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()

    return redirect(request.referrer or url_for('catalog'))



@app.route('/update_quantity/<int:cart_id>', methods=['POST'])
def update_quantity(cart_id):
    action = request.form.get('action')
    cart_item = Cart.query.get_or_404(cart_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            db.session.delete(cart_item)
            db.session.commit()
            return redirect(url_for('view_cart'))

    db.session.commit()
    return redirect(url_for('view_cart'))


@app.context_processor
def inject_cart_item_count():
    session_id = session.get('session_id')
    if not session_id:
        return dict(cart_item_count=0)

    total_quantity = db.session.query(db.func.sum(Cart.quantity)).filter_by(session_id=session_id).scalar() or 0
    return dict(cart_item_count=total_quantity)





@app.route('/remove-from-cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    item = BasketItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('cart'))



@app.route('/cart')
def view_cart():
    session_id = session.get('session_id')
    if not session_id:
        return render_template('cart.html', cart_items=[], total=0, favorites=[])

    cart_items = Cart.query.filter_by(session_id=session_id).all()
    favorites = Favorite.query.filter_by(session_id=session_id).all()

    # Получаем список товаров
    favorite_products = [fav.product for fav in favorites]

    total = sum(item.product.price_2 * item.quantity for item in cart_items)

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=total,
        favorite_products=favorite_products
    )


@app.route('/favorites')
def favorites():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')  # или страница авторизации

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return render_template('favorites.html', favorites=favorites)


@app.route('/')
def index():
    products = Product.query.all()
    
    # Путь к шаблону
    with open('admin_panel.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    return render_template_string(template_content, products=products)

@app.route('/styles/<path:filename>')
def styles(filename):
    return send_from_directory('styles', filename)

@app.route('/scripts/<path:filename>')
def scripts(filename):
    return send_from_directory('scripts', filename)

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)


with app.app_context():
    db.create_all()
    if not Product.query.first():
        db.session.add_all([
            Product(
                title="Футболка",
                description="Хлопковая футболка",
                price_1=1000,
                price_2=900,
                size="M",
                special="casual",
                for_what="daily",
                stock=10,
                tupe="clothes",
                image_url="images/shirt.svg"
                ),
                Product(
                    title="Кроссовки",
                    description="Для бега",
                    price_1=3000,
                    price_2=2000,
                    size="42",
                    special="carbon",
                    for_what="marathon",
                    stock=5,
                    tupe="shoes",
                    image_url="images/shoe.svg"
                )
            ])
    db.session.commit()




if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # создаем таблицы если их нет
    app.run(debug=True)



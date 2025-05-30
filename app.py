from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

app = Flask(__name__, template_folder='.')
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'секретный_ключ_сюда'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# ========== МОДЕЛИ ==========
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price_1 = db.Column(db.Float)
    price_2 = db.Column(db.Float)
    size = db.Column(db.String(10))
    special = db.Column(db.String(50))
    for_what = db.Column(db.String(50))
    stock = db.Column(db.Integer)
    tupe = db.Column(db.String(50))
    image_url = db.Column(db.String(200))


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    product = db.relationship('Product')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    surname = db.Column(db.String(100))
    name = db.Column(db.String(100))
    name_1 = db.Column(db.String(100))
    payment = db.Column(db.String(50))
    delivery = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # <-- ВАЖНО!
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    product = db.relationship('Product')

# ========== LOGIN ==========
@app.before_request
def check_user_authentication():
    if current_user.is_authenticated:
        print(f"[INFO] Пользователь авторизован: {current_user.username}")
    else:
        print("[INFO] Пользователь НЕ авторизован")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.context_processor
def inject_common_data():
    cart_count = Cart.query.filter_by(user_id=current_user.id).count() if current_user.is_authenticated else 0
    token = current_user.token if current_user.is_authenticated else None
    return {
        'cart_item_count': cart_count,
        'user_token': token
    }


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        phone = request.form['phone'].strip()
        if not phone.startswith('+') or not phone[1:].isdigit():
            flash('Введите корректный номер в формате +71234567890')
            return redirect(url_for('auth'))

        user = User.query.filter_by(username=phone).first()
        if user is None:
            # Регистрация
            user = User(username=phone)
            db.session.add(user)
            db.session.commit()
            flash('Вы зарегистрированы')

        # Авторизация
        login_user(user)
        flash('Вы вошли как ' + user.username)
        return redirect(url_for('main'))

    return render_template('auth.html')



# ========== СТРАНИЦЫ ==========
@app.route('/')
def start():
    products = Product.query.all()
    return render_template('admin_panel.html', products=products)

@app.route('/main')
def main():
    products = Product.query.all()
    user_token = current_user.token if current_user.is_authenticated else None
    return render_template('main.html', products=products, user_token=user_token)


@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/clothes')
def clothes():
    products = Product.query.filter_by(tupe='clothes').all()
    return render_template('clothes.html', products=products)


@app.route('/shoes')
def shoes():
    products = Product.query.filter_by(tupe='shoes').all()
    return render_template('shoes.html', products=products)


@app.route('/acessories')
def acessories():
    products = Product.query.filter_by(tupe='acessories').all()
    return render_template('acessories.html', products=products)


@app.route('/all_products')
def all_products():
    products = Product.query.all()
    return render_template('all_products.html', products=products)


@app.route('/admin_panel_addProduct', methods=['GET', 'POST'])
def admin_panel_addProduct():
    if request.method == 'POST':
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
        return redirect(url_for('admin_panel'))
    return render_template('admin_panel-addProduct.html')


@app.route('/admin_panel-deleteProduct')
def admin_panel_deleteProduct():
    products = Product.query.all()
    return render_template('admin_panel-deleteProduct.html', products=products)


@app.route('/admin_panel-stock')
def admin_panel_stock():
    products = Product.query.all()
    return render_template('admin_panel-stock.html', products=products)

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)


@app.route('/favorites')
@login_required
def favorites():
    favs = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favs)


@app.route('/cart')
@login_required
def view_cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price_2 * item.quantity for item in items)
    return render_template('cart.html', cart_items=items, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    return redirect(request.referrer or url_for('main'))

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

@app.route('/toggle_favorite', methods=['POST'])
@login_required
def toggle_favorite():
    data = request.get_json()
    product_id = data.get('product_id')
    fav = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_fav = Favorite(user_id=current_user.id, product_id=product_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({'status': 'added'})


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    print("📥 Заход в /checkout")

    if request.method == 'POST':
        print("📨 POST-запрос на оформление заказа")

        try:
            order = Order(
                user_id=current_user.id,
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
            print(f"✅ Создан объект заказа: {order}")

            cart_items = Cart.query.filter_by(user_id=current_user.id).all()
            if not cart_items:
                print("⚠️ Корзина пуста, заказ не может быть оформлен")
                flash("Корзина пуста")
                return redirect(url_for('checkout'))

            for item in cart_items:
                order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
                order.items.append(order_item)
                print(f"➕ Добавлен товар: {order_item.product_id} x{order_item.quantity}")

            db.session.add(order)
            db.session.commit()
            print(f"🎉 Заказ сохранен в базе данных: {order.id}")

            db.session.query(Cart).filter_by(user_id=current_user.id).delete()
            db.session.commit()

            flash('Заказ оформлен!')

        except Exception as e:
            db.session.rollback()
            print(f"❌ Ошибка при сохранении заказа: {e}")
            flash(f'Ошибка: {e}')

    return render_template('checkout.html')


# ========== ФАЙЛЫ ==========
@app.route('/styles/<path:filename>')
def styles(filename):
    return send_from_directory('styles', filename)


@app.route('/scripts/<path:filename>')
def scripts(filename):
    return send_from_directory('scripts', filename)


@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)


# ========== ЗАПУСК ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

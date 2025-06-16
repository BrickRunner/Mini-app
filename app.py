from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
import requests
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

# Инициализация Flask-приложения
app = Flask(__name__, template_folder='.')
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'секретный_ключ_сюда'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# ========== МОДЕЛИ БД ==========
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    is_admin = db.Column(db.Boolean, default=False)

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
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50), default='Ожидает подтверждения') 
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # <-- ВАЖНО!
    quantity = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    product = db.relationship('Product')

# ========== ВХОД И РЕГИСТРАЦИЯ ==========
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
    if current_user.is_authenticated:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
        token = current_user.token
    else:
        cart_count = 0
        token = None

    return {
        'cart_item_count': cart_count,
        'user_token': token
    }


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        phone = request.form.get('phone')
        if not phone:
            flash('Номер не передан')
            return redirect(url_for('auth'))

        phone = phone.strip()

        if not phone.startswith('+') or not phone[1:].isdigit():
            flash('Введите корректный номер в формате +71234567890')
            return redirect(url_for('auth'))

        ADMIN_SECRET_CODE = '+71512201107'
        is_admin = phone == ADMIN_SECRET_CODE

        user = User.query.filter_by(username=phone).first()

        if user is None:
            user = User(username=phone, is_admin=is_admin)
            db.session.add(user)
            db.session.commit()
            flash('Вы зарегистрированы')
        else:
            if is_admin and not user.is_admin:
                user.is_admin = True
                db.session.commit()

        db.session.refresh(user)
        login_user(user)
        flash('Вы вошли как ' + user.username)

        if user.is_admin:
            return redirect(url_for('admin_panel'))

        return redirect(url_for('main'))

    return render_template('auth.html')

# ========== СТРАНИЦЫ ==========
@app.route('/')
def main():
    products = Product.query.all()
    user_token = current_user.token if current_user.is_authenticated else None
    if current_user.is_authenticated:
        favorite_ids = {f.product_id for f in Favorite.query.filter_by(user_id=current_user.id).all()}
    else:
        favorite_ids = set()

    return render_template('main.html', products=products, favorite_ids=favorite_ids)

@app.route("/offer")
def offer():
    return render_template("offer.html")


@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html')


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/clothes')
def clothes():
    # Получаем все товары
    all_products = Product.query.all()

    # Группируем по имени (оставляя один товар для каждой группы)
    grouped_products = {}
    for product in all_products:
        if product.title not in grouped_products:
            grouped_products[product.title] = product  # Берем первый из группы

    return render_template("clothes.html", products=grouped_products.values())


@app.route('/shoes')
def shoes():
    all_products = Product.query.all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    favorite_ids = [fav.product_id for fav in favorites]
    grouped_products = {}
    for product in all_products:
        if product.title not in grouped_products:
            grouped_products[product.title] = product 
    return render_template('shoes.html', favorite_ids=favorite_ids, products=grouped_products.values())


@app.route('/acessories')
def acessories():
    all_products = Product.query.all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    favorite_ids = [fav.product_id for fav in favorites]
    grouped_products = {}
    for product in all_products:
        if product.title not in grouped_products:
            grouped_products[product.title] = product 
    return render_template('acessories.html', favorite_ids=favorite_ids, products=grouped_products.values())


@app.route('/all_products')
def all_products():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    favorite_ids = [f.product_id for f in favorites]
    all_products = Product.query.all()
    grouped_products = {}
    for product in all_products:
        if product.title not in grouped_products:
            grouped_products[product.title] = product 
    
    return render_template("all_products.html", favorite_ids=favorite_ids, products=grouped_products.values())

@app.route('/product/<int:product_id>')
  # если хотите, чтобы страница была доступна только авторизованным
def product_detail(product_id):
    product = Product.query.get(product_id)
    
    same_name_products = Product.query.filter_by(title=product.title).all()

    return render_template("productCard.html", product=product, size_variants=same_name_products)

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

@app.route('/admin_panel-changeStatus')
@login_required  # Только для админов
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_panel-changeStatus.html', orders=orders)

@app.route('/admin/update_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    new_status = request.form.get('status')
    order = Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()
    return redirect(url_for('admin_panel'))

@app.route('/my_orders')
@login_required
def my_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('my_orders.html', orders=orders)


@app.route('/favorites')
@login_required
def view_favorites():
    favorite_entries = Favorite.query.filter_by(user_id=current_user.id).all()
    favorite_ids = [entry.product_id for entry in favorite_entries]

    products = Product.query.filter(Product.id.in_(favorite_ids)).all()
    cart_item_count = Cart.query.filter_by(user_id=current_user.id).count()

    return render_template('favorites.html',
                           products=products,
                           cart_item_count=cart_item_count)

@app.route('/favorites/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_from_favorites(product_id):
    favorite = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
    return redirect(url_for('view_favorites'))



@app.route('/cart')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    # ВАЖНО: получаем список ID избранных товаров
    favorite_ids = [f.product_id for f in Favorite.query.filter_by(user_id=current_user.id).all()]

    total = sum(item.product.price_2 * item.quantity for item in cart_items)
    
    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=total,
        favorite_ids=favorite_ids  
    )


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    product = Product.query.get_or_404(product_id)

    existing_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    new_quantity = quantity
    if existing_item:
        new_quantity += existing_item.quantity

    if new_quantity > product.stock:
        flash(f'Нельзя добавить больше {product.stock} штук товара "{product.title}" в корзину.')
        return redirect(request.referrer or url_for('main'))

    if existing_item:
        existing_item.quantity = new_quantity
    else:
        item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(item)

    db.session.commit()
    flash('Товар добавлен в корзину.')
    return redirect(request.referrer or url_for('main'))

@app.route('/update_quantity/<int:cart_id>', methods=['POST'])
@login_required
def update_quantity(cart_id):
    action = request.form.get('action')
    cart_item = Cart.query.get_or_404(cart_id)

    if cart_item.user_id != current_user.id:
        abort(403)

    product = Product.query.get_or_404(cart_item.product_id)

    if action == 'increase':
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
        else:
            flash(f'Нельзя добавить больше {product.stock} шт. товара "{product.title}"')
    elif action == 'decrease':
        cart_item.quantity -= 1
        if cart_item.quantity <= 0:
            db.session.delete(cart_item)
            db.session.commit()
            return redirect(url_for('view_cart'))

    db.session.commit()
    return redirect(url_for('view_cart'))


@app.route('/toggle_favorite_ajax', methods=['POST'])
@login_required
def toggle_favorite_ajax():
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'status': 'error', 'message': 'Нет ID товара'}), 400

    favorite = Favorite.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        new_fav = Favorite(user_id=current_user.id, product_id=product_id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({'status': 'added'})
    
@app.route('/delete_product/<int:product_id>', methods=['POST', 'GET'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)  

    try:
        db.session.delete(product)
        db.session.commit()
        flash('Товар успешно удалён', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении товара', 'danger')

    return redirect(url_for('admin_panel')) 

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    total = 0

    if request.method == 'POST':

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
                flash("Корзина пуста")
                return redirect(url_for('checkout'))

            for item in cart_items:
                product = Product.query.get(item.product_id)
                if not product:
                    flash(f"❌ Товар с ID {item.product_id} не найден.")
                    return redirect(url_for('checkout'))

                if product.stock < item.quantity:
                    flash(f"⚠️ Недостаточно товара: {product.title}")
                    return redirect(url_for('checkout'))

                product.stock -= item.quantity

                order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
                order.items.append(order_item)
                total += product.price_1 * item.quantity 
            order.total_price = total 
            db.session.add(order)
            db.session.commit()
            print(f"🎉 Заказ сохранён: ID {order.id}")

            Cart.query.filter_by(user_id=current_user.id).delete()
            db.session.commit()

            flash('✅ Заказ оформлен!')
            return render_template('account.html', order_success=True)

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
    print(f"Запрошен скрипт: {filename}")
    return send_from_directory('scripts', filename)


@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)


# ========== ЗАПУСК ==========
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
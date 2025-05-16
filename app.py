from flask import Flask, render_template, request, redirect, url_for, render_template, send_from_directory, session
from config import Config
import uuid
from models import db, Product, Cart, User, Favorite, BasketItem

app = Flask(__name__,
            static_folder=None,
            template_folder='.')
app.config.from_object(Config)

# Подключаем базу данных
db.init_app(app)


@app.route("/account")
def account():
    return render_template("account.html")

@app.route("/main")
def main():
    return render_template("main.html")

@app.route('/admin')
def admin_panel():
    products = Product.query.all()
    return render_template('admin_panel.html', products=products)

@app.route('/all_products')
def all_products():
    # Проверим, какие товары есть в базе данных
    products = Product.query.all()
    return render_template('all_products.html', products=products)

@app.route('/clothes')
def clothes():
    # Проверим, какие товары есть в базе данных
    products = Product.query.filter_by(tupe='clothes').all()
    return render_template('clothes.html', products=products)

@app.route('/acessories')
def acessories():
    # Проверим, какие товары есть в базе данных
    products = Product.query.filter_by(tupe='acessories').all()
    return render_template('acessories.html', products=products)

@app.route('/shoes')
def shoes():
    # Проверим, какие товары есть в базе данных
    products = Product.query.filter_by(tupe='shoes').all()
    return render_template('shoes.html', products=products)

@app.route('/admin_panel-deleteProduct')
def admin_panel_deleteProduct():
    products = Product.query.all()
    return render_template('admin_panel-deleteProduct.html', products=products)

@app.route('/admin_panel-stock')
def admin_panel_stock():
    products = Product.query.all()
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

@app.route('/add_to_favorites/<int:product_id>', methods=['POST'])
def add_to_favorites(product_id):
    favorite = Favorite.query.filter_by(product_id=product_id).first()
    if not favorite:
        favorite = Favorite(product_id=product_id, user_id=1)  # замените 1 на нужного user_id
        db.session.add(favorite)
        db.session.commit()
    return '', 204  # чтобы не перезагружать страницу



@app.route('/favorites/delete/<int:product_id>', methods=['POST'])
def delete_from_favorites(product_id):
    favorite = Favorite.query.filter_by(product_id=product_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
    return redirect(url_for('favorites'))


@app.route('/toggle_favorite/<int:product_id>', methods=['POST'])
def toggle_favorite(product_id):
    session_id = session.get('session_id')
    if not session_id:
        session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']

    favorite = Favorite.query.filter_by(session_id=session_id, product_id=product_id).first()

    if favorite:
        db.session.delete(favorite)
    else:
        new_fav = Favorite(session_id=session_id, product_id=product_id)
        db.session.add(new_fav)

    db.session.commit()
    return redirect(request.referrer or url_for('view_cart'))


@app.before_request
def ensure_cart_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        cart[str(product_id)] = {'quantity': quantity}

    session.modified = True  # Обязательно!
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
    cart = session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())
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
    favorite_ids = [fav.product_id for fav in favorites]

    total = sum(item.product.price_2 * item.quantity for item in cart_items)

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=total,
        favorite_ids=favorite_ids
    )

@app.route('/favorites')
def favorites():
    favorites = Favorite.query.filter_by(user_id=1).all()
    products = [f.product for f in favorites]
    return render_template('favorites.html', products=products)


@app.route('/')
def index():
    products = Product.query.all()
    print(products)
    return render_template('admin_panel.html', products=products)

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

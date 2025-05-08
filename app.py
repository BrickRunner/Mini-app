from flask import Flask, render_template, request, redirect, url_for, render_template, send_from_directory
from config import Config
from models import db, Product

app = Flask(__name__,
            static_folder=None,
            template_folder='.')
app.config.from_object(Config)

# Подключаем базу данных
db.init_app(app)


@app.route("/account")
def account():
    return render_template("account.html")

@app.route('/admin')
def admin_panel():
    products = Product.query.all()
    return render_template('admin_panel.html', products=products)


@app.route('/clothes')
def clothes():
    # Проверим, какие товары есть в базе данных
    products = Product.query.filter_by(tupe='clothes').all()
    return render_template('clothes.html', products=products)

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

@app.route('/')
def index():
    products = Product.query.all()
    print(products)
    return render_template('main.html', products=products)

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

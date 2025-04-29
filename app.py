from flask import Flask, render_template, send_from_directory
from config import Config
from models import db, Product

app = Flask(__name__,
            static_folder=None,
            template_folder='.')
app.config.from_object(Config)

# Подключаем базу данных
db.init_app(app)

# Стандартные роуты и маршруты для статики...

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('clothes.html', products=products)

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
        sample_product = Product(
            title="Пример товара",
            description="Описание товара",
            price=1999.99,
            size="S",
            special="carbon",
            for_what="marathon",
            stock=100,
            image_url="/images/shirt.svg"  # путь до картинки
        )
        db.session.add(sample_product)
        db.session.commit()



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # создаем таблицы если их нет
    app.run(debug=True)

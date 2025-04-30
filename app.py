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

@app.route("/account")
def account():
    return render_template("account.html")


@app.route('/')
def index():
    products = Product.query.all()
    print(products)
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
        db.session.add_all([
            Product(
                title="Футболка",
                description="Хлопковая футболка",
                price=1000,
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
                    price=3000,
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

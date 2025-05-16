from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # ВАЖНО!
    image_url = db.Column(db.String(200), nullable=False)
    tupe = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(10), nullable=True)
    special = db.Column(db.String(50), nullable=True)
    for_what = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price_1 = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price_2 = db.Column(db.Float, nullable=False)
    

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # ForeignKey на user.id
    session_id = db.Column(db.String(100), nullable=True)  # если используешь сессии для гостей
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    product = db.relationship('Product', backref='favorites')


class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    session_id = db.Column(db.String(100), nullable=False)  # если без авторизации
    product = db.relationship('Product')
    
    def __repr__(self):
        return f'<Product {self.title}>'

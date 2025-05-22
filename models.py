from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



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
    favorited_by = db.relationship('Favorite', back_populates='product')
    

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    favorites = db.relationship('Favorite', back_populates='user')


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 👈 внешний ключ на User
    session_id = db.Column(db.String(100))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    user = db.relationship('User', back_populates='favorites')
    product = db.relationship('Product')


class BasketItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    session_id = db.Column(db.String(100), nullable=False)  # если без авторизации
    product = db.relationship('Product')
    


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    telegram_id = db.Column(db.BigInteger)
    surname = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_1 = db.Column(db.String(100), nullable=False)
    payment = db.Column(db.String(100), nullable=False)
    delivery = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    product = db.relationship('Product')

    def __repr__(self):
        return f'<Product {self.title}>'

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(200), nullable=False)
    tupe = db.Column(db.String(200), nullable=False)  # исправлено с 'tupe' на 'type'
    title = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(10), nullable=True)
    special = db.Column(db.String(50), nullable=True)
    for_what = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price_1 = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price_2 = db.Column(db.Float, nullable=False)

    favorites = db.relationship('Favorite', back_populates='product', cascade='all, delete-orphan')
    cart_items = db.relationship('Cart', backref='product', lazy=True)
    basket_items = db.relationship('BasketItem', backref='product', lazy=True)
    order_items = db.relationship('OrderItem', backref='product', lazy=True)


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # поле для хранения хэша пароля

    favorites = db.relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    user = db.relationship('User', back_populates='favorites')
    product = db.relationship('Product', back_populates='favorites')


class BasketItem(db.Model):
    __tablename__ = 'basket_item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    session_id = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
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
    user = db.relationship('User', back_populates='orders')


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
